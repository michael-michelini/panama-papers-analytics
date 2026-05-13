## ADDED Requirements

### Requirement: GitHub Actions workflow skeleton per component
Each component directory (`pipeline/`, `neptune-analytics/`, `bedrock/`) SHALL contain a `.github/workflows/<component>-ci.yml` file (or the root `.github/workflows/` directory SHALL contain one file per component) that runs on pull requests targeting `main`.

#### Scenario: CI triggers on PR
- **WHEN** a pull request is opened targeting `main` with changes in `pipeline/`
- **THEN** the `pipeline-ci` GitHub Actions workflow SHALL trigger automatically

### Requirement: Lint step in every CI workflow
Every CI workflow SHALL include a lint step using `ruff` for Python files, configured to fail the workflow on any lint error.

#### Scenario: Lint failure blocks merge
- **WHEN** a pull request contains Python code with a lint error (e.g., unused import)
- **THEN** the CI workflow SHALL fail and the PR SHALL be blocked from merging

### Requirement: Test step in every CI workflow
Every CI workflow SHALL include a test step using `pytest`, configured to fail the workflow if any test fails or if no tests are found in the component directory.

#### Scenario: Test failure blocks merge
- **WHEN** a pull request introduces a failing test
- **THEN** the CI workflow SHALL fail and the PR SHALL be blocked from merging

### Requirement: Python version pinned
All Python components SHALL pin the Python version in a `.python-version` file or `pyproject.toml`, and the CI workflows SHALL use that same pinned version via `actions/setup-python`.

#### Scenario: Python version is consistent
- **WHEN** the CI workflow runs
- **THEN** it SHALL use the same Python version as specified in the component's version pin file

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
