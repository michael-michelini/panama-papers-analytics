# Panama Papers Analytics — Project Constitution

## Project Overview

Graph analytics platform built on the ICIJ Panama Papers dataset (~2M nodes, ~3M relationships). Demonstrates how AWS graph services and Linkurious combine to surface insights from complex financial networks. Built as a Linkurious sales demonstration.

## Four Pillars

| Pillar | Directory | Purpose |
|---|---|---|
| Data Pipeline | `pipeline/` | Neo4j export → S3 → Lambda → Neptune Serverless bulk load |
| Linkurious | `linkurious/` | Datasource config, investigation stories, alert definitions |
| Neptune Analytics | `neptune-analytics/` | Graph algorithm runs (PageRank, community detection) → write back to Neptune |
| Bedrock / GraphRAG | `bedrock/` | Natural language querying via Amazon Bedrock |

## Key Decisions (Locked)

- **Query language**: openCypher (not Gremlin) — aligns with Linkurious and Neptune Analytics
- **Bulk load approach**: S3 upload → Lambda trigger → Neptune Bulk Loader API (not direct Lambda writes)
- **IaC target**: AWS CloudFormation — templates live in `infra/` within each component
- **Load sequencing**: Manual — operator uploads vertices, waits for LOAD_COMPLETED, then uploads edges

## AWS Configuration

- Region: `ap-southeast-2`
- Stack prefix: controlled by `AWS_GLOBAL_STACK_PREFIX` GitHub Actions variable

## GitHub Issues & opsx

This project tracks work as GitHub Issues organised into milestones. When using any opsx workflow:

- **On `/opsx:propose`**: Ask for a linked GitHub issue number and post a "change proposed" comment to that issue.
- **On `/opsx:apply` completion**: Post a progress/completion comment to the linked issue if one exists.
- **On `/opsx:archive`**: Post a "change complete" summary comment to the linked issue if one exists.

Issue number is stored in `openspec/changes/<name>/issue.txt` so all three commands can find it.

## Development Conventions

See [`docs/conventions.md`](docs/conventions.md) for full tooling conventions. Summary:
- Python: ruff (lint + format), pytest
- IaC: AWS CloudFormation
- CI: GitHub Actions — one workflow per component
- No hardcoded credentials anywhere; use env vars or AWS Secrets Manager
