## ADDED Requirements

### Requirement: Mono-repo directory layout
The repository SHALL contain four top-level component directories (`pipeline/`, `neptune-analytics/`, `bedrock/`, `linkurious/`) plus a `docs/` directory, each with a component-level README.

#### Scenario: Directory structure is present
- **WHEN** the repository is cloned fresh
- **THEN** running `ls` at the root SHALL show `pipeline/`, `neptune-analytics/`, `bedrock/`, `linkurious/`, `docs/`, and `openspec/`

### Requirement: Root README
The repository SHALL have a root `README.md` that describes the project purpose, mono-repo structure, component summaries, and links to the architecture decision record and cost model.

#### Scenario: README exists and is informative
- **WHEN** a developer opens the repository on GitHub
- **THEN** the README SHALL render with at minimum: project title, one-paragraph description, directory map, and links to `docs/architecture.md` and `docs/cost-model.md`

### Requirement: Gitignore covers all components
The root `.gitignore` SHALL exclude common Python, Node.js, CDK, and AWS artefacts (`.env`, `__pycache__`, `cdk.out`, `node_modules`, `*.pyc`, `.aws-sam`).

#### Scenario: Sensitive and generated files are excluded
- **WHEN** a developer runs `git status` after installing dependencies
- **THEN** no `.env` files, `node_modules/`, `cdk.out/`, or `__pycache__/` directories SHALL appear as untracked

### Requirement: Conventions document
A `docs/conventions.md` file SHALL document agreed conventions: query language (openCypher), Python version, linting tool (ruff), test framework (pytest), and branch naming.

#### Scenario: New developer can onboard from conventions doc alone
- **WHEN** a developer reads `docs/conventions.md`
- **THEN** they SHALL know which Python version to use, how to run linting, how to run tests, and what the branch naming convention is
