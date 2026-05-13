## MODIFIED Requirements

### Requirement: Separate CI workflow for Neptune core stack deployment
A GitHub Actions workflow (`.github/workflows/deploy-neptune-core.yml`) SHALL deploy the `neptune-core` CloudFormation stack. It SHALL trigger on pull requests to `main` that modify `pipeline/infra/neptune-core.yaml`, and SHALL be manually triggerable via `workflow_dispatch`.

#### Scenario: Core workflow triggers on template change
- **WHEN** a pull request modifying `pipeline/infra/neptune-core.yaml` is opened against `main`
- **THEN** the `deploy-neptune-core` workflow SHALL run automatically

#### Scenario: Core workflow confirms cluster availability
- **WHEN** the `deploy-neptune-core` workflow completes stack deployment
- **THEN** it SHALL verify the Neptune cluster status is `available` via the AWS API before proceeding to the smoke test

#### Scenario: Core workflow runs smoke test after deployment
- **WHEN** the `deploy-neptune-core` workflow confirms the cluster is `available`
- **THEN** it SHALL run `pipeline/scripts/smoke_test.py` against the deployed endpoint and fail the workflow if the query does not succeed
