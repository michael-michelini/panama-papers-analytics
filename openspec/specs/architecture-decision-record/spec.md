## ADDED Requirements

### Requirement: Architecture document with data flow diagram
A `docs/architecture.md` file SHALL exist describing the four-pillar architecture and containing an ASCII data flow diagram showing how data moves from CSV ingestion through to Linkurious.

#### Scenario: Data flow is unambiguous
- **WHEN** a developer reads `docs/architecture.md`
- **THEN** they SHALL be able to trace the complete path from raw CSV → S3 → Lambda → Neptune Core → Neptune Analytics → Neptune Core (enriched) → Linkurious, and separately CSV → Neptune Core → Bedrock → NL response

### Requirement: Technology decisions recorded
`docs/architecture.md` SHALL record key technology decisions with rationale: openCypher as the query language, Neptune Bulk Loader API for initial ingestion, ephemeral Neptune Analytics for algorithm runs, and Bedrock (Claude) for NL querying.

#### Scenario: Query language decision is explained
- **WHEN** a developer reads the architecture doc
- **THEN** it SHALL explain why openCypher was chosen over Gremlin and what the trade-offs are

### Requirement: Component responsibility boundaries defined
The architecture document SHALL define what each top-level directory is responsible for and what it is explicitly NOT responsible for, preventing scope creep between components.

#### Scenario: Boundary ambiguity is resolved
- **WHEN** a developer is unsure whether to place new code in `pipeline/` or `neptune-analytics/`
- **THEN** the architecture document SHALL provide enough boundary definition to make the decision without asking
