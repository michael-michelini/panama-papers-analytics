## Context

During the pipeline spike (issue #2), two artifacts were created that now need correction before the branch is merged:

1. `pipeline/loaders/bulk_load_trigger.py` was written as a readable, lintable copy of the Lambda handler. The CloudFormation template (`neptune-loader.yaml`) uses `Code.ZipFile` with identical inline code. There is no build step that references the `.py` file — it is simply a duplicate.

2. `neptune-core.yaml` was given `DeletionPolicy: Retain` on `NeptuneCluster` and `NeptuneInstance` to prevent accidental data loss. However, this also prevents intentional teardown via `delete-stack`. The protection needed is against accidental **replacement during updates**, not against deletion — which is what `UpdateReplacePolicy: Retain` already provides.

## Goals / Non-Goals

**Goals:**
- Single source of truth for the Lambda handler (the CloudFormation ZipFile)
- Neptune cluster deletable via `aws cloudformation delete-stack` (teardown path must work)
- Neptune cluster protected against silent replacement during routine stack updates

**Non-Goals:**
- Unit-testing the Lambda handler (deferred to CDK migration, issue #3)
- Packaging the Lambda from an external file (deferred to CDK migration, issue #3)
- Any other changes to the loader or core stack

## Decisions

**Decision: Remove `pipeline/loaders/` entirely**

The directory exists solely for the `.py` file. With the ZipFile as the deployment mechanism, the directory has no purpose. Keeping it invites drift — any fix applied to one copy won't propagate to the other. Deleting it eliminates the ambiguity.

Considered: keeping the `.py` file and removing the ZipFile (making the standalone file authoritative and adding a packaging step). Rejected because it requires CI changes and a build artifact upload before deployment, which is throwaway work ahead of the CDK migration.

**Decision: `DeletionPolicy: Delete` + `UpdateReplacePolicy: Retain`**

`DeletionPolicy` controls what happens when CloudFormation removes the resource from a stack (via `delete-stack` or resource removal from template). `UpdateReplacePolicy` controls what happens when an update requires replacing the resource.

Setting both to `Retain` was overly conservative — it also blocks teardown. The correct pairing:
- `DeletionPolicy: Delete` — stack deletion removes Neptune (teardown works)
- `UpdateReplacePolicy: Retain` — update-triggered replacement orphans the old cluster rather than destroying it, preventing silent data loss

## Risks / Trade-offs

**Risk: Operator accidentally deletes the core stack** → The Neptune cluster will be deleted. Mitigation: the MIGRATION_README.md teardown section documents this; the ephemeral loader stack design means operators should only delete-stack the loader, not the core, during normal operations.

**Risk: ZipFile and future standalone .py diverge post-CDK migration** → Not a risk until CDK migration begins; tracked as part of issue #3 scope.

## Migration Plan

1. Delete `pipeline/loaders/` directory
2. Edit `pipeline/infra/neptune-core.yaml` — change `DeletionPolicy: Retain` to `DeletionPolicy: Delete` on `NeptuneCluster` and `NeptuneInstance`; update `Description` field
3. Run `cfn-lint pipeline/infra/neptune-core.yaml` to confirm no regressions
4. Commit, push, open PR

Rollback: revert the two-line change to `neptune-core.yaml` and restore `pipeline/loaders/` from git history if needed. No AWS resources are affected until the stack is redeployed.
