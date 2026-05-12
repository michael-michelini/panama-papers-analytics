## Why

Two issues were identified during the pipeline spike that need resolving before the branch can be merged: the `pipeline/loaders/` directory duplicates Lambda handler code already embedded in the CloudFormation ZipFile, and the Neptune core stack's `DeletionPolicy: Retain` prevents intentional teardown via the stack while `UpdateReplacePolicy: Retain` (already correct) is sufficient to protect against accidental data loss during updates.

## What Changes

- **Remove** `pipeline/loaders/` directory — the Lambda handler lives in `neptune-loader.yaml`'s `Code.ZipFile`; the standalone `.py` file is an unreferenced duplicate
- **Change** `DeletionPolicy: Retain` → `DeletionPolicy: Delete` on `NeptuneCluster` and `NeptuneInstance` in `pipeline/infra/neptune-core.yaml` — allows deliberate teardown via `delete-stack`
- **Keep** `UpdateReplacePolicy: Retain` on both resources — protects data if an update would trigger resource replacement
- **Update** the `Description` field in `neptune-core.yaml` to remove the now-incorrect statement about `DeletionPolicy: Retain`

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `neptune-core-stack`: Deletion policy changes — stack deletion now removes Neptune resources; update-triggered replacement still retains the old cluster

## Impact

- `pipeline/infra/neptune-core.yaml` — two resource policy changes and description update
- `pipeline/loaders/` — directory removed
- No impact on CI workflows, IAM, or runtime behaviour
