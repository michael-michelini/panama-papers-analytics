## Why

The Panama Papers dataset (2M nodes, 3M relationships) needs a production-grade analytics platform to demonstrate the value of graph technology to prospective Linkurious customers. This project establishes the foundational mono-repo structure, GitHub project board, and full architecture — spanning data ingestion, graph enrichment, AI-powered querying, and interactive visualisation — so that all subsequent development has a clear home, tracked backlog, and agreed cost model.

## What Changes

- Mono-repo created with four top-level directories (`pipeline/`, `neptune-analytics/`, `bedrock/`, `linkurious/`)
- GitHub repository initialised with milestones (epics), issues (stories), and labels mirroring a Jira-style board
- Architecture decision record (ADR) established covering Neptune Core, Neptune Analytics, Bedrock, and Linkurious integration
- AWS cost model documented for the POC/demo environment (~$340–$690/month excluding Linkurious licensing)
- CI/CD scaffold in place (GitHub Actions) with linting and test conventions defined for all components

## Capabilities

### New Capabilities

- `repo-structure`: Mono-repo directory layout, root README, .gitignore, and conventions document
- `github-project-board`: GitHub milestones, issues, and labels configured as the project's Jira-equivalent backlog
- `architecture-decision-record`: High-level architecture documented — Neptune Core as graph store, Neptune Analytics for ephemeral enrichment, Bedrock for NL querying, Linkurious as the sales-facing front-end
- `cost-model`: AWS monthly cost estimates per service, with instance sizing options and optimisation levers documented
- `cicd-scaffold`: GitHub Actions workflow skeleton with lint and test jobs, ready to be extended per component

### Modified Capabilities

- None (greenfield project)

## Impact

- All subsequent milestones (Data Pipeline, Linkurious Integration, Neptune Analytics, Bedrock) depend on this foundation being in place
- GitHub board becomes the single source of truth for project tracking
- Cost model informs infrastructure decisions throughout the project
- No existing systems are modified; this is net-new
