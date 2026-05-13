## Requirements

### Requirement: Smoke test script verifies Neptune connectivity
A Python script (`pipeline/scripts/smoke_test.py`) SHALL connect to a Neptune endpoint using the boto3 `neptunedata` client and execute the openCypher query `MATCH (n) RETURN count(n) LIMIT 1`. The script SHALL exit with code 0 on success and a non-zero code on failure. It SHALL accept the Neptune endpoint as a command-line argument or environment variable.

#### Scenario: Successful smoke test against available cluster
- **WHEN** the script is run against a reachable Neptune endpoint with valid AWS credentials
- **THEN** the script SHALL execute the query, print the result, and exit with code 0

#### Scenario: Smoke test fails on unreachable endpoint
- **WHEN** the script is run against an endpoint that does not respond
- **THEN** the script SHALL print a descriptive error message and exit with a non-zero code

#### Scenario: Smoke test fails on auth error
- **WHEN** the script is run with AWS credentials that lack Neptune query permissions
- **THEN** the script SHALL print the auth error and exit with a non-zero code

### Requirement: Smoke test step in deploy-neptune-core workflow
The `deploy-neptune-core` GitHub Actions workflow SHALL include a post-deploy step that runs `pipeline/scripts/smoke_test.py` against the deployed cluster endpoint. This step SHALL run after "Confirm cluster is available" and SHALL fail the workflow if the query does not succeed.

#### Scenario: Workflow fails if smoke test fails
- **WHEN** the deploy-neptune-core workflow runs and the smoke test step exits non-zero
- **THEN** the overall workflow job SHALL fail and subsequent steps SHALL not run

#### Scenario: Smoke test uses endpoint from stack outputs
- **WHEN** the smoke test step runs
- **THEN** it SHALL read the Neptune endpoint from the CloudFormation stack outputs, not from a hardcoded value
