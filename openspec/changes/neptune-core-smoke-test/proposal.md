## Why

The `deploy-neptune-core` workflow confirms the Neptune cluster status is `available` via the AWS API, but never actually connects to the endpoint. This means a successful deployment could mask a cluster that is unreachable or not accepting queries — which would only surface when Linkurious or the loader tries to connect.

## What Changes

- A post-deploy smoke test step is added to `.github/workflows/deploy-neptune-core.yml` that runs a signed openCypher query (`MATCH (n) RETURN count(n) LIMIT 1`) against the Neptune endpoint using the boto3 `neptunedata` client
- A small Python helper script (`pipeline/scripts/smoke_test.py`) is introduced to hold the test logic, keeping the workflow YAML clean
- The `deploy-neptune-core` workflow gains a dependency on `boto3` and `botocore` (already present in the Lambda runtime; needed in the CI job runner)

## Capabilities

### New Capabilities
- `neptune-core-smoke-test`: Post-deploy step in the neptune-core workflow that verifies the cluster endpoint is reachable and accepts a signed openCypher query

### Modified Capabilities
- `cicd-scaffold`: The deploy-neptune-core workflow gains an additional post-deploy verification requirement — cluster status `available` is necessary but not sufficient; a live query must also succeed

## Impact

- `.github/workflows/deploy-neptune-core.yml` — new step added after "Confirm cluster is available"
- `pipeline/scripts/smoke_test.py` — new file (~30 lines)
- No changes to the CloudFormation templates
- No changes to the Lambda or loader stack
