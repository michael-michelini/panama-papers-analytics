## Context

This is a greenfield mono-repo for a Panama Papers graph analytics platform. The audience is a single developer (+ Claude) building a sales demo for Linkurious. The project must show how AWS graph services (Neptune, Neptune Analytics, Bedrock) and Linkurious combine to surface meaningful insights from the ICIJ Panama Papers dataset (2M nodes, 3M relationships, CSV format).

The foundation change delivers the skeleton everything else plugs into: directory layout, GitHub tracking board, architecture documentation, cost model, and CI/CD conventions.

There are no existing systems to migrate. The only constraint is that an early pipeline prototype may already exist in another location and will be absorbed into `pipeline/` during Milestone 1.

## Goals / Non-Goals

**Goals:**
- Establish mono-repo directory structure with clear per-component boundaries
- Configure GitHub as a Jira-equivalent board (milestones = epics, issues = stories, labels = type/pillar)
- Document the full 4-pillar architecture with a data flow diagram
- Produce a costed AWS estimate for the POC environment with sizing options
- Define CI/CD conventions (GitHub Actions, linting, test frameworks) applied consistently across all components

**Non-Goals:**
- Implementing any pipeline, analytics, or AI functionality (that is Milestones 1–4)
- Provisioning any AWS infrastructure (CDK/Terraform comes in `pipeline/infra`)
- Finalising Linkurious story narratives (explored but not locked in Milestone 2)
- Integrating the existing pipeline prototype (done as the first story in Milestone 1)

## Decisions

### D1: Mono-repo over poly-repo
**Decision:** Single repository with top-level directories per component.  
**Rationale:** The four pillars are tightly coupled — Neptune Analytics writes back to Neptune Core, Bedrock queries Neptune, Linkurious reads from Neptune. Shared IaC, shared test utilities, and cross-component CI make a mono-repo the natural fit at this team size (1–2 people).  
**Alternative considered:** Separate repos per component. Rejected because the overhead of cross-repo dependency management outweighs the isolation benefit at this scale.

### D2: GitHub Issues as project board (Jira-equivalent)
**Decision:** Use GitHub Milestones as epics, Issues as stories, and Labels for type and pillar.  
**Rationale:** The project is already on GitHub, the team is just one developer + Claude, and GitHub Issues are free. Adding Jira would be unnecessary toolchain overhead.  
**Label scheme:**
```
Type:    story | spike | chore | bug
Pillar:  pipeline | linkurious | neptune-analytics | bedrock
Priority: p0-critical | p1-high | p2-medium
```

### D3: Neptune query language — openCypher preferred
**Decision:** Default to openCypher across Neptune, Lambda loaders, and Linkurious datasource config.  
**Rationale:** openCypher is more readable than Gremlin, maps better to Bedrock Text2Query prompting, and Linkurious has strong openCypher support. Gremlin remains available for bulk-load operations via the Neptune Bulk Loader API (which is transport-level, not query-language).  
**Alternative considered:** Gremlin throughout. Rejected due to verbosity and weaker LLM prompting patterns.

### D4: CI/CD via GitHub Actions
**Decision:** GitHub Actions for all lint, test, and (eventually) deploy workflows.  
**Rationale:** Already integrated with the repo, free for public repos, and familiar. Each component directory gets its own workflow file so they can be triggered independently.  
**Conventions:**
- Python: `ruff` for linting, `pytest` for tests
- IaC: `cfn-lint` or `cdk synth` for CloudFormation/CDK validation
- All PRs must pass lint + tests before merge

### D5: Cost model targets db.r6g.large for POC
**Decision:** Size Neptune Core at `db.r6g.large` (~$252/month) for the demo environment with a documented upgrade path to `db.r6g.xlarge` (~$503/month) if query performance is insufficient.  
**Rationale:** 2M nodes / 3M edges is within the comfortable range of a large instance. The demo will have low concurrent load (1–2 users). Stopping the instance outside demo hours reduces cost further to ~$75/month.  
**Cost summary (POC, always-on):**

| Service              | $/month     |
|----------------------|-------------|
| Neptune Core (large) | ~$270       |
| Neptune Analytics    | ~$40        |
| Lambda               | ~$5         |
| S3                   | ~$2         |
| NAT Gateway          | ~$40        |
| Bedrock              | ~$10        |
| **Total AWS**        | **~$370**   |
| Linkurious license   | TBD (POC trial or enterprise) |

## Risks / Trade-offs

- **NAT Gateway cost creep** → Mitigation: Use VPC endpoints for S3 and Neptune where possible to avoid NAT Gateway charges on data transfer
- **Linkurious licensing unknown** → Mitigation: Confirm POC trial availability before Milestone 2 begins; if no trial, Linkurious stories are blocked
- **Existing pipeline compatibility** → Mitigation: Milestone 1 spike issue (#2) reviews the existing code before any refactoring; don't absorb blindly
- **openCypher on Neptune has feature gaps vs. full Cypher** → Mitigation: Validate that the query patterns needed for Linkurious stories and Bedrock prompts work in Neptune's openCypher dialect during the Milestone 2 spike
- **Neptune Analytics GCU sizing for 5M elements is unvalidated** → Mitigation: Milestone 3 spike (#15) validates before committing to the ephemeral architecture

## Open Questions

1. Does the existing pipeline use Gremlin or openCypher? (Unblocks D3 fully)
2. Is a Linkurious POC license available, and what are the Neptune connection requirements?
3. Should the Neptune instance be in the same AWS account as the existing environment, or a dedicated demo account?
4. Are there specific persons-of-interest or jurisdictions the Linkurious stories must feature for the target customer?
