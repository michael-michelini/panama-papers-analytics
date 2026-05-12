## ADDED Requirements

### Requirement: Separate CI workflow for Neptune core stack deployment
A GitHub Actions workflow (`.github/workflows/deploy-neptune-core.yml`) SHALL deploy the `neptune-core` CloudFormation stack. It SHALL trigger on pull requests to `main` that modify `pipeline/infra/neptune-core.yaml`, and SHALL be manually triggerable via `workflow_dispatch`.

#### Scenario: Core workflow triggers on template change
- **WHEN** a pull request modifying `pipeline/infra/neptune-core.yaml` is opened against `main`
- **THEN** the `deploy-neptune-core` workflow SHALL run automatically

#### Scenario: Core workflow confirms cluster availability
- **WHEN** the `deploy-neptune-core` workflow completes stack deployment
- **THEN** it SHALL verify the Neptune cluster status is `available` before the job succeeds

### Requirement: Separate manual-only workflow for Neptune loader stack
A GitHub Actions workflow (`.github/workflows/deploy-neptune-loader.yml`) SHALL deploy the `neptune-loader` CloudFormation stack. It SHALL be triggered exclusively via `workflow_dispatch` and SHALL NOT trigger automatically on any push or pull request event.

#### Scenario: Loader workflow is not triggered by code changes
- **WHEN** a pull request modifying any file is opened against `main`
- **THEN** the `deploy-neptune-loader` workflow SHALL NOT trigger automatically

#### Scenario: Loader workflow deployable on demand
- **WHEN** an operator manually triggers the `deploy-neptune-loader` workflow via `workflow_dispatch`
- **THEN** the workflow SHALL deploy the loader stack and print its outputs (staging bucket name, Neptune endpoint)

## REMOVED Requirements

### Requirement: Single Neptune migration deployment workflow
**Reason**: Replaced by two separate workflows — `deploy-neptune-core.yml` for the persistent cluster stack and `deploy-neptune-loader.yml` for the ephemeral loader stack. A single workflow cannot safely express the different trigger semantics (auto vs. manual-only) required by each stack.
**Migration**: Use `deploy-neptune-core.yml` for cluster infrastructure changes and `deploy-neptune-loader.yml` when a data load is needed.
