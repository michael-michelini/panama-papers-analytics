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
