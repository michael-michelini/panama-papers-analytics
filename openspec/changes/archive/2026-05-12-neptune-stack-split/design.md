## Context

The prototype delivers a single CloudFormation template (`NeptuneServerlessMigration.yaml`) that provisions the Neptune cluster, VPC networking, and the S3/Lambda bulk-load infrastructure in one stack. The data load is a one-time operation — once Panama Papers data is in Neptune, the load infrastructure serves no purpose until a reload is explicitly needed. Keeping it in one stack means the operator must leave load infrastructure running permanently, and risks inadvertently reprovisioning Neptune (wiping data) if a cluster property is changed during a routine stack update.

## Goals / Non-Goals

**Goals:**
- Isolate the Neptune cluster behind `DeletionPolicy: Retain` so a stack update or accidental delete cannot destroy loaded data
- Make the load infrastructure independently deployable and deletable
- Enforce load infrastructure lifecycle via GitHub Actions (`workflow_dispatch`) rather than manual CLI
- Preserve the existing bulk-load mechanism (S3 upload → Lambda → Neptune Bulk Loader API) unchanged

**Non-Goals:**
- Changing the Lambda handler logic (`bulk_load_trigger.py`)
- Automating the vertex-before-edge sequencing (operator sequences manually)
- Adding load status polling
- Moving Neptune to private subnets (out of scope for this change)

## Decisions

### 1. Cross-stack references via `Fn::ImportValue`

The loader stack needs the Neptune endpoint and IAM role ARN from the core stack. Options considered:

| Approach | Pros | Cons |
|---|---|---|
| `Fn::ImportValue` (CFn cross-stack) | Native CFn; blocks core deletion while loader exists | Tight coupling between stacks |
| SSM Parameter Store | Decoupled; works across accounts | Extra resources; extra IAM permissions |
| Hardcoded parameters | Simple | Manual sync; error-prone |

**Decision: `Fn::ImportValue`.** The tight coupling is a feature here — CFn will refuse to delete the core stack while the loader stack imports from it, preventing accidental data loss. No cross-account requirements exist.

### 2. `NeptuneS3Role` stays in the core stack

The IAM role that Neptune uses to read from S3 during bulk load must be in `AssociatedRoles` on the Neptune cluster. Moving it to the loader stack would require updating `AssociatedRoles` on the cluster at loader deploy/delete time, creating a circular dependency. The role is cheap to keep and harmless when the loader stack is absent.

### 3. Two separate GitHub Actions workflows

Options: one workflow with a parameter, or two separate files.

**Decision: two separate files.** The core deploy workflow triggers on template changes to `pipeline/infra/neptune-core.yaml` (PR path filter), making it part of normal CI. The loader workflow is `workflow_dispatch`-only — it should never run automatically. Separating them makes the trigger semantics explicit and avoids conditional logic inside a single file.

### 4. `DeletionPolicy: Retain` on cluster and instance only

Applying `Retain` to the VPC/subnets/security group would leave orphaned networking resources if the core stack is ever intentionally deleted. Only the Neptune cluster and instance carry data and are expensive to reprovision.

## Risks / Trade-offs

- **Retained resources after stack deletion** — If the core stack is deleted (e.g., to rebuild from scratch), the Neptune cluster and instance are retained but orphaned. They must be manually deleted via the Neptune console or AWS CLI, and will continue to incur cost. Mitigation: document the teardown procedure explicitly in the runbook.

- **Cross-stack import lock** — `Fn::ImportValue` references block the core stack from being updated in ways that change the exported values while the loader stack exists. Mitigation: delete the loader stack before making breaking changes to core stack outputs.

- **Accidental reload** — If the operator redeploys the loader stack and re-uploads CSVs, the Lambda will fire again and Neptune will create duplicate nodes/edges (bulk load is not idempotent). Mitigation: document that the staging bucket is for single-use per load cycle; delete the stack when done.

## Migration Plan

1. Deploy `neptune-core.yaml` as a new stack (`neptune-core`) — this provisions a fresh Neptune cluster.
2. Deploy `neptune-loader.yaml` as a new stack (`neptune-loader`) — imports outputs from core stack.
3. Run the data load (upload vertices, wait, upload edges).
4. Delete the `neptune-loader` stack.
5. Delete the old `neptune-migration` stack (if still present) — it is now superseded.
6. Remove `pipeline/infra/NeptuneServerlessMigration.yaml` and `.github/workflows/deploy-neptune-migration.yml`.

Rollback: if anything fails before step 3, delete both new stacks and the old stack remains untouched.

## Open Questions

- None. Design is fully resolved based on explore session decisions.
