# Bedrock

Natural language querying of the Panama Papers graph via Amazon Bedrock, supporting both Text2openCypher (structured queries) and GraphRAG (contextual retrieval).

## Responsibilities

- Text2openCypher pipeline: translate natural language → openCypher query → Neptune → natural language response
- GraphRAG pipeline: subgraph chunking, Titan embedding, vector retrieval, Bedrock generation
- Hybrid query router: classify query type and route to the appropriate pattern
- Lambda API endpoint exposing the NL query interface
- Linkurious panel integration

## NOT Responsible For

- Initial data ingestion (see `pipeline/`)
- Graph algorithm runs (see `neptune-analytics/`)
- Linkurious datasource configuration (see `linkurious/`)

## Query Patterns

```
Pattern A — Text2openCypher (precise, structured questions)
  NL question → Bedrock → openCypher query → Neptune → NL answer

Pattern B — GraphRAG (fuzzy, contextual questions)
  NL question → subgraph retrieval → embedding → Bedrock → NL answer

Pattern C — Hybrid Router
  Query classifier → routes to A or B
```

## Structure

```
bedrock/
├── api/            # Lambda API endpoint
├── graphrag/       # Chunking and embedding pipeline
├── tests/
└── pyproject.toml
```

## Related Issues

See [Milestone 4: 🤖 Bedrock / GraphRAG NL Interface](../../milestones) on GitHub.
