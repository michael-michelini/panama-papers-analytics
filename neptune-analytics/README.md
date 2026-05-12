# Neptune Analytics

Runs graph algorithms ephemerally on Amazon Neptune Analytics and writes enriched properties back to Neptune Core for surfacing in Linkurious.

## Responsibilities

- Lambda-triggered spin-up and tear-down of ephemeral Neptune Analytics instances
- Graph algorithm jobs: PageRank, betweenness centrality, community detection
- Writing algorithm results back to Neptune Core as node properties
- CDK infrastructure for Neptune Analytics provisioning

## NOT Responsible For

- Initial data ingestion (see `pipeline/`)
- Natural language querying (see `bedrock/`)
- Linkurious visualisation configuration (see `linkurious/`)

## Core Flow

```
Lambda trigger
    → Spin up Neptune Analytics (ephemeral)
    → Load graph snapshot from Neptune Core
    → Run algorithms (PageRank, community detection)
    → Write results back to Neptune Core as node properties
    → Tear down Neptune Analytics
```

## Structure

```
neptune-analytics/
├── infra/          # AWS CDK stack for Neptune Analytics
├── jobs/           # Algorithm job scripts
├── tests/
└── pyproject.toml
```

## Related Issues

See [Milestone 3: 📊 Neptune Analytics Enrichment](../../milestones) on GitHub.
