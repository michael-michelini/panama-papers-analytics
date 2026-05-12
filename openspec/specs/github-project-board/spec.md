## ADDED Requirements

### Requirement: GitHub Milestones as epics
The repository SHALL have four GitHub Milestones corresponding to the four project pillars, each with a title, description, and no due date set at this stage.

#### Scenario: Milestones visible on GitHub
- **WHEN** a user navigates to the repository's Milestones page
- **THEN** four milestones SHALL exist: "🗄️ Data Pipeline & Neptune Core", "🔍 Linkurious Integration & Storytelling", "📊 Neptune Analytics Enrichment", "🤖 Bedrock / GraphRAG NL Interface"

### Requirement: GitHub Labels for type and pillar
The repository SHALL have a defined label set covering issue type and component pillar, applied consistently across all issues.

#### Scenario: Label set is complete
- **WHEN** a user opens the Labels page on GitHub
- **THEN** the following labels SHALL exist:
  - Type: `story`, `spike`, `chore`, `bug`
  - Pillar: `pipeline`, `linkurious`, `neptune-analytics`, `bedrock`
  - Priority: `p0-critical`, `p1-high`, `p2-medium`

### Requirement: GitHub Issues as stories covering all 4 milestones
The repository SHALL have at least 25 GitHub Issues, each assigned to the correct milestone, labelled with type and pillar, and written with a one-line title and acceptance criteria in the body.

#### Scenario: All milestone 1 issues exist
- **WHEN** filtering issues by milestone "🗄️ Data Pipeline & Neptune Core"
- **THEN** at least 7 issues SHALL be present covering: mono-repo scaffold, pipeline audit spike, Neptune IaC, S3 IaC, Lambda bulk loader, data validation, idempotent load strategy, and GitHub Actions CI/CD

#### Scenario: All milestone 2 issues exist
- **WHEN** filtering issues by milestone "🔍 Linkurious Integration & Storytelling"
- **THEN** at least 6 issues SHALL be present covering: Linkurious datasource spike, data model documentation, and three investigation stories (shell companies, intermediary networks, jurisdiction clustering) plus alert configuration

#### Scenario: All milestone 3 issues exist
- **WHEN** filtering issues by milestone "📊 Neptune Analytics Enrichment"
- **THEN** at least 5 issues SHALL be present covering: Neptune Analytics sizing spike, ephemeral provisioning, centrality analysis job, community detection job, and Linkurious enrichment visualisations

#### Scenario: All milestone 4 issues exist
- **WHEN** filtering issues by milestone "🤖 Bedrock / GraphRAG NL Interface"
- **THEN** at least 6 issues SHALL be present covering: Bedrock model eval spike, Text2Gremlin pipeline, GraphRAG pipeline, hybrid query router, Lambda API endpoint, and Linkurious panel integration

### Requirement: Issue body template
Every issue SHALL follow a consistent body format: one-line summary, "Acceptance Criteria" checklist, and "Notes" section for context or links.

#### Scenario: Issue body is structured
- **WHEN** any issue is opened
- **THEN** the body SHALL contain an "Acceptance Criteria" heading with at least one checkbox item
