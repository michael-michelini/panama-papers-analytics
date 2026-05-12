# Panama Papers Analytics Platform

A graph analytics platform built on the [ICIJ Panama Papers dataset](https://offshoreleaks.icij.org/pages/database) — 2 million nodes and 3 million relationships — demonstrating how AWS graph services and [Linkurious](https://linkurious.com/) combine to surface meaningful insights from complex financial networks.

## What This Is

This platform is a sales demonstration for Linkurious, showing how graph technology, AI-powered querying, and interactive visualisation can be used to investigate offshore financial structures. It is built on four integrated pillars:

| Pillar | Directory | Purpose |
|--------|-----------|---------|
| Data Pipeline | `pipeline/` | Ingest Panama Papers CSVs into Amazon Neptune via S3 + Lambda |
| Linkurious Integration | `linkurious/` | Datasource config, investigation stories, alert definitions |
| Neptune Analytics | `neptune-analytics/` | Ephemeral graph algorithm runs → enrich Neptune → surface in Linkurious |
| Bedrock / GraphRAG | `bedrock/` | Natural language querying of the graph via Amazon Bedrock |

## Repository Structure

```
panama-papers-analytics/
│
├── pipeline/              # CSV → S3 → Lambda → Neptune Core
│   ├── infra/             # CDK for Neptune cluster, S3, Lambda
│   ├── loaders/           # Lambda bulk loader functions
│   └── tests/
│
├── neptune-analytics/     # Ephemeral algo runs → write back to Neptune
│   ├── jobs/              # PageRank, community detection, etc.
│   ├── infra/             # CDK for Neptune Analytics provisioning
│   └── tests/
│
├── bedrock/               # Natural language graph querying
│   ├── api/               # Lambda API endpoint
│   ├── graphrag/          # Subgraph chunking + embedding pipeline
│   └── tests/
│
├── linkurious/            # Visualisation, stories, alerts
│   ├── config/            # Datasource configuration
│   └── stories/           # Investigation narrative documentation
│
├── docs/                  # Architecture, cost model, conventions
│   ├── architecture.md    # System design and data flow diagrams
│   ├── cost-model.md      # AWS monthly cost estimates
│   └── conventions.md     # Development conventions and tooling
│
└── .github/workflows/     # CI/CD pipelines per component
```

## Documentation

- [Architecture & Data Flow](docs/architecture.md)
- [AWS Cost Model](docs/cost-model.md)
- [Development Conventions](docs/conventions.md)

## Quick Start

See each component's README for setup instructions:
- [Pipeline](pipeline/README.md)
- [Neptune Analytics](neptune-analytics/README.md)
- [Bedrock](bedrock/README.md)
- [Linkurious](linkurious/README.md)

## Project Tracking

This project is tracked as GitHub Issues organised into four milestones (epics). See the [Issues tab](../../issues) and [Milestones](../../milestones) for the full backlog.
