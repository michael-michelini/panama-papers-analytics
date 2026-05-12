## ADDED Requirements

### Requirement: AWS cost estimate document
A `docs/cost-model.md` file SHALL exist providing a monthly AWS cost estimate for the POC/demo environment, broken down by service with assumptions stated.

#### Scenario: Cost document covers all services
- **WHEN** a stakeholder reads `docs/cost-model.md`
- **THEN** it SHALL include line-item estimates for: Neptune Core (instance + storage + I/O), Neptune Analytics (ephemeral GCU-hours), Lambda, S3, NAT Gateway, and Bedrock

### Requirement: Instance sizing options documented
The cost model SHALL present at least two Neptune Core sizing options (e.g., `db.r6g.large` and `db.r6g.xlarge`) with the cost implication of each and a recommended starting point for the POC.

#### Scenario: Sizing decision is self-service
- **WHEN** a developer needs to choose an instance size
- **THEN** the cost model SHALL provide enough information to make the decision without external research

### Requirement: Cost optimisation levers documented
The cost model SHALL document at least two cost reduction strategies applicable to a demo environment (e.g., stopping the Neptune instance outside demo hours, using VPC endpoints to reduce NAT Gateway charges).

#### Scenario: Demo-mode cost is quantified
- **WHEN** a developer wants to minimise cost between demo sessions
- **THEN** the cost model SHALL show the estimated monthly cost when the Neptune instance is stopped outside business hours (~8hrs/day, 5 days/week)

### Requirement: Linkurious licensing flagged as unknown
The cost model SHALL explicitly flag Linkurious licensing cost as a TBD item with a note on typical enterprise pricing range and the need to confirm POC trial availability.

#### Scenario: Licensing gap is visible
- **WHEN** a stakeholder reviews the cost model
- **THEN** Linkurious licensing SHALL appear as a line item marked "TBD — confirm POC trial" rather than being omitted
