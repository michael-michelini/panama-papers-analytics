# Pipeline Audit — Issue #2 Spike

Reviewed: 2026-05-12  
Source: `neptune-analytics/current/` (prototype files moved to `pipeline/` as part of this spike)

---

## What the Pipeline Does

The prototype implements a Neo4j → Amazon Neptune Serverless migration in three phases:

```
scripts/neo4j_export.py          (runs locally by an operator)
  └─ Bolt → Neo4j (APOC or direct Cypher)
  └─ writes output/vertices/nodes.csv
  └─ writes output/edges/relationships.csv

Operator uploads CSVs to S3 staging bucket
  └─ S3 ObjectCreated event
  └─ Lambda (loaders/bulk_load_trigger.py)
       └─ SigV4-signed POST /loader → Neptune Serverless cluster

Neptune Serverless reads directly from S3 and bulk-loads the CSV data.
```

Infrastructure is a single CloudFormation stack (`pipeline/infra/NeptuneServerlessMigration.yaml`) provisioning:
- VPC with two public subnets and an internet gateway
- Neptune Serverless cluster (engine 1.4, 1–4 NCUs, IAM auth, encrypted storage)
- S3 staging bucket with 7-day object expiry and S3→Lambda notification
- Lambda function (Python 3.13) that submits Neptune bulk load jobs
- IAM roles for Neptune S3 access and Lambda execution

CI/CD is a GitHub Actions workflow (`.github/workflows/deploy-neptune-migration.yml`) that lints the template with cfn-lint, validates it, handles bad stack states, deploys, and confirms the cluster is available. Teardown is intentionally manual.

---

## Data Format

Neptune CSV bulk load format. Files must conform to the [Neptune bulk load format spec](https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load-tutorial-format-gremlin.html):

**Vertex file** (`output/vertices/nodes.csv`):
```
~id,~label,name:String,address:String,country_codes:String,status:String
12345,Officer,John Doe,"123 Main St",PAN;GBR,Active
```

**Edge file** (`output/edges/relationships.csv`):
```
~id,~label,~from,~to
99001,officer_of,12345,67890
```

Load order is strict: **vertices must reach `LOAD_COMPLETED` before edge files are uploaded.** Neptune rejects edges whose `~from` or `~to` IDs do not yet exist.

---

## Query Language Decision

**Decision: openCypher.**

Rationale:
- Linkurious uses Cypher natively — openCypher alignment reduces translation friction
- Neptune Analytics (graph algorithms pillar) uses openCypher as its primary query interface
- openCypher is more expressive for path queries relevant to the Panama Papers use case (e.g. `shortestPath`, `allShortestPaths`)
- Gremlin is TinkerPop-specific; openCypher is the direction Neptune is investing in

All future query examples, alert definitions, and investigation stories should use openCypher.

---

## Gap Analysis

| # | Gap | Severity | Status | Affects Issues |
|---|-----|----------|--------|----------------|
| 1 | IaC is raw CloudFormation; repo convention was CDK | Medium | ✅ Closed — CloudFormation is now the confirmed IaC approach | #3 |
| 2 | Export script had hardcoded credentials (now parameterized) | High | ✅ Fixed | #3 |
| 3 | Lambda only processed `Records[0]` — batched S3 events dropped all but first | High | ✅ Fixed — iterates all Records | #3 |
| 4 | Load ordering (vertices before edges) is a manual operator step, not automated | High | ✅ Closed — data is already loaded; manual sequencing is acceptable for this demo | #3 |
| 5 | No data validation before upload — bad CSVs trigger silent partial loads | High | ✅ Closed — not required for this use case | #4 |
| 6 | `failOnError: FALSE` — partial load failures are not surfaced | Medium | ✅ Closed — data is loaded and verified | #4 |
| 7 | No idempotency — re-uploading CSVs submits duplicate load jobs | Medium | ✅ Closed — CSVs are uploaded once; re-upload is not a scenario | #5 |
| 8 | CI deploys the stack but does not poll for load job completion | Medium | ✅ Closed — operator manually polls; this is a one-time load | #6 |
| 9 | No tests — `pipeline/tests/` is empty | High | Open — tests will be added alongside a future feature | #7 |
| 10 | Neptune placed in public subnets; SG opens 8182 to 0.0.0.0/0 | Low (demo), High (prod) | ✅ Closed — acceptable for demo; documented in code | #3 |
| 11 | Neptune Analytics not provisioned — CFn creates Neptune DB only | High | Open — Milestone 2 scope | Milestone 2 |
| 12 | No `.python-version` file — `pipeline-ci.yml` references it but it is absent | Low | ✅ Fixed — `pipeline/.python-version` added | #7 |
| 13 | `pipeline/infra/` is expected to be CDK but currently holds a CFn template | Medium | ✅ Closed — CloudFormation is now the confirmed IaC approach | #3 |

### Notes on Gap 3 (Lambda batching)
Fixed in `pipeline/loaders/bulk_load_trigger.py` — now iterates all `Records`. The original inline CFn ZipFile processed only `event["Records"][0]`.

### Notes on Gap 11 (Neptune Analytics)
Neptune Analytics is a separate AWS service from Neptune Database. The current stack provisions only Neptune Database (Serverless). Neptune Analytics graph provisioning, algorithm jobs (PageRank, community detection), and write-back to Neptune DB are entirely unimplemented and belong in `neptune-analytics/` — that work is scoped to Milestone 2.

---

## Refactor vs Rebuild Decision

**Decision: Refactor.**

The core architecture (S3 → Lambda → Neptune bulk loader) is correct and well-implemented. The IAM trust policies, SigV4 signing, and bulk loader API usage are all sound.

What needs changing is layered on top — not a reason to start over:
- Port CFn → CDK constructs (issue #3)
- Add pre-upload CSV validation step (issue #4)
- Add idempotency guard on Lambda (issue #5)
- Add load status polling to CI (issue #6)
- Add tests (issue #7)
- Move Neptune to private subnets if this moves toward production

---

## Files Placed in This Spike

| File | Description |
|------|-------------|
| `pipeline/infra/NeptuneServerlessMigration.yaml` | CloudFormation template — Neptune Serverless cluster, S3, Lambda |
| `pipeline/loaders/bulk_load_trigger.py` | Lambda handler (batching bug fixed) |
| `pipeline/scripts/neo4j_export.py` | Export script skeleton (parameterized via env vars) |
| `.github/workflows/deploy-neptune-migration.yml` | CI deploy workflow (paths corrected) |
