## 1. Mono-repo Scaffold

- [x] 1.1 Create top-level directories: `pipeline/`, `neptune-analytics/`, `bedrock/`, `linkurious/`, `docs/`
- [x] 1.2 Add root `.gitignore` covering Python, Node.js, CDK, AWS, and `.env` artefacts
- [x] 1.3 Write root `README.md` with project title, description, directory map, and links to architecture and cost model docs
- [x] 1.4 Write `docs/conventions.md` documenting Python version, ruff linting, pytest, openCypher preference, and branch naming
- [x] 1.5 Add a `README.md` stub to each component directory (`pipeline/`, `neptune-analytics/`, `bedrock/`, `linkurious/`)

## 2. Architecture Documentation

- [x] 2.1 Write `docs/architecture.md` with a project overview and four-pillar summary
- [x] 2.2 Add ASCII data flow diagram: CSV → S3 → Lambda → Neptune Core → Neptune Analytics → Neptune Core (enriched) → Linkurious
- [x] 2.3 Add ASCII data flow diagram: Neptune Core → Bedrock → NL response
- [x] 2.4 Document technology decisions: openCypher choice, Neptune Bulk Loader for ingestion, ephemeral analytics pattern, Bedrock model selection rationale
- [x] 2.5 Define component boundary table: what each directory owns and explicitly does NOT own

## 3. Cost Model Documentation

- [x] 3.1 Write `docs/cost-model.md` with monthly estimates for all AWS services (Neptune, Neptune Analytics, Lambda, S3, NAT Gateway, Bedrock)
- [x] 3.2 Add two Neptune Core sizing options (`db.r6g.large` vs `db.r6g.xlarge`) with cost comparison and recommended starting point
- [x] 3.3 Document cost optimisation levers: stopping Neptune outside demo hours, VPC endpoints for S3/Neptune to reduce NAT Gateway charges
- [x] 3.4 Add Linkurious licensing as a TBD line item with enterprise pricing range and a note to confirm POC trial availability

## 4. GitHub Project Board

- [x] 4.1 Create GitHub labels: type (`story`, `spike`, `chore`, `bug`), pillar (`pipeline`, `linkurious`, `neptune-analytics`, `bedrock`), priority (`p0-critical`, `p1-high`, `p2-medium`)
- [x] 4.2 Create four GitHub Milestones: "🗄️ Data Pipeline & Neptune Core", "🔍 Linkurious Integration & Storytelling", "📊 Neptune Analytics Enrichment", "🤖 Bedrock / GraphRAG NL Interface"
- [x] 4.3 Create Milestone 1 issues (8 issues): mono-repo scaffold, pipeline audit spike, Neptune IaC, S3 IaC + upload tooling, Lambda bulk loader, data validation, idempotent load strategy, GitHub Actions CI/CD
- [x] 4.4 Create Milestone 2 issues (6 issues): Linkurious datasource spike, graph data model documentation, investigation story (shell company chains), investigation story (intermediary networks), investigation story (jurisdiction clustering), alert configuration
- [x] 4.5 Create Milestone 3 issues (5 issues): Neptune Analytics sizing spike, ephemeral provisioning Lambda, centrality analysis job, community detection job, Linkurious enrichment visualisations
- [x] 4.6 Create Milestone 4 issues (6 issues): Bedrock model eval spike, Text2Gremlin pipeline, GraphRAG pipeline, hybrid query router, Lambda API endpoint, Linkurious panel integration
- [x] 4.7 Verify every issue has correct milestone, labels (type + pillar), and an "Acceptance Criteria" checklist in the body

## 5. CI/CD Scaffold

- [x] 5.1 Create `.github/workflows/pipeline-ci.yml` with lint (ruff) and test (pytest) steps, triggered on PRs to `main` for changes in `pipeline/`
- [x] 5.2 Create `.github/workflows/neptune-analytics-ci.yml` with lint and test steps for `neptune-analytics/`
- [x] 5.3 Create `.github/workflows/bedrock-ci.yml` with lint and test steps for `bedrock/`
- [x] 5.4 Add a `pyproject.toml` (or `.python-version`) to each Python component directory pinning the Python version
- [x] 5.5 Verify CI workflows trigger correctly on a test PR and both lint and test steps pass (or fail predictably with no source files yet)
