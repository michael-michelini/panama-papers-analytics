## Why

The existing prototype uses a single CloudFormation stack for both the Neptune cluster and the S3/Lambda bulk-load infrastructure. This conflates a persistent data layer with ephemeral load tooling — a future stack update that touches a cluster property could silently reprovision Neptune and wipe loaded data. The load infrastructure is only needed once (or on demand), but the cluster must live indefinitely.

## What Changes

- Split `NeptuneServerlessMigration.yaml` into two CloudFormation templates:
  - `neptune-core.yaml` — VPC, Neptune cluster, subnet group, parameter group, IAM S3 role. Deployed once; `DeletionPolicy: Retain` on cluster and instance.
  - `neptune-loader.yaml` — S3 staging bucket, Lambda bulk-load trigger, IAM Lambda role. Ephemeral; deleted by operator after load completes.
- Add cross-stack references: loader stack imports `NeptuneEndpoint` and `NeptuneLoadRoleArn` from core stack via `Fn::ImportValue`.
- Split the single deploy workflow into two:
  - `deploy-neptune-core.yml` — triggers on core template changes or `workflow_dispatch`.
  - `deploy-neptune-loader.yml` — `workflow_dispatch` only; used when a (re)load is needed.
- Remove the original `NeptuneServerlessMigration.yaml` and `deploy-neptune-migration.yml`.

## Capabilities

### New Capabilities

- `neptune-core-stack`: Persistent Neptune cluster stack with retention policy — provisions VPC, Neptune Serverless cluster, and the IAM role Neptune needs to read from S3 during bulk load.
- `neptune-loader-stack`: Ephemeral bulk-load stack — provisions S3 staging bucket and Lambda trigger; deleted by the operator after data is loaded, redeployed on demand via GitHub Actions.

### Modified Capabilities

- `cicd-scaffold`: Two new deployment workflows replace the single Neptune migration workflow.

## Impact

- `pipeline/infra/NeptuneServerlessMigration.yaml` — replaced by two templates
- `.github/workflows/deploy-neptune-migration.yml` — replaced by two workflows
- No application code changes; Lambda handler (`bulk_load_trigger.py`) is unchanged
- Operator runbook (`MIGRATION_README.md`) needs updating to reflect the two-stack deploy/delete sequence
