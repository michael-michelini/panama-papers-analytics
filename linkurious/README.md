# Linkurious

Datasource configuration, investigation stories, and alert definitions for the Linkurious graph visualisation platform — the customer-facing front-end of the Panama Papers demo.

## Responsibilities

- Neptune datasource configuration (connection, auth, query dialect)
- Documentation of investigation stories (shell company chains, intermediary networks, jurisdiction clustering)
- Alert definitions for high-risk entities (based on Neptune-enriched properties from Neptune Analytics)
- Saved search and visualisation template documentation

## NOT Responsible For

- Graph data ingestion (see `pipeline/`)
- Graph enrichment algorithms (see `neptune-analytics/`)
- Natural language querying (see `bedrock/`)

## Investigation Stories

| Story | Description |
|-------|-------------|
| Shell company ownership chains | N-hop ownership traversal, visualise layering |
| Key intermediary / broker networks | Who facilitated the most? Centrality-driven |
| Jurisdiction clustering | Which offshore centres cluster together? |

## Structure

```
linkurious/
├── config/         # Datasource configuration files
└── stories/        # Documented investigation narratives
```

## Related Issues

See [Milestone 2: 🔍 Linkurious Integration & Storytelling](../../milestones) on GitHub.
