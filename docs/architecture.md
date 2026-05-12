# Architecture

## Overview

The Panama Papers Analytics Platform is a four-pillar system that ingests the ICIJ Panama Papers dataset into Amazon Neptune and exposes it through complementary analytics and visualisation layers. The primary customer-facing product is Linkurious; Neptune Analytics and Bedrock are enrichment and querying layers that feed into it.

### Four Pillars

| Pillar | AWS Services | Purpose |
|--------|-------------|---------|
| Data Pipeline | S3, Lambda, Neptune | Ingest 2M nodes / 3M relationships from CSV |
| Linkurious Integration | Neptune, Linkurious | Graph visualisation, investigation stories, alerts |
| Neptune Analytics | Neptune Analytics, Lambda | Ephemeral graph algorithm runs → enrich Neptune |
| Bedrock / GraphRAG | Bedrock, Lambda, OpenSearch/S3 | Natural language querying of the graph |

---

## Data Flow Diagrams

### Pipeline & Enrichment Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│  Source Data                                                         │
│  CSV files (2M nodes, 3M relationships — ICIJ Panama Papers)        │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ upload
                               ▼
                        ┌─────────────┐
                        │  Amazon S3  │
                        │  (raw CSVs) │
                        └──────┬──────┘
                               │ S3 event trigger
                               ▼
                        ┌─────────────┐
                        │   Lambda    │
                        │ Bulk Loader │
                        └──────┬──────┘
                               │ Neptune Bulk Loader API
                               ▼
                ┌──────────────────────────────┐
                │       Amazon Neptune         │
                │       (Core Graph DB)        │
                │  openCypher query language   │
                └──────┬───────────────────────┘
                       │
          ┌────────────┴─────────────┐
          │ Lambda trigger           │
          ▼                          │
┌──────────────────────┐             │ enriched properties
│  Neptune Analytics   │             │ written back
│   (ephemeral)        │─────────────┘
│                      │
│  • PageRank          │
│  • Betweenness       │
│  • Community detect. │
└──────────────────────┘
                               │
                               │ (Neptune Core now enriched)
                               ▼
                ┌──────────────────────────────┐
                │          Linkurious          │
                │  • Investigation stories     │
                │  • Alerts (enriched props)   │
                │  • Graph visualisation       │
                └──────────────────────────────┘
```

### Natural Language Query Flow (Bedrock)

```
┌─────────────────────────────────────────────────────┐
│  User types natural language question               │
│  (via Linkurious panel or direct API)               │
└───────────────────────────┬─────────────────────────┘
                            │
                            ▼
                   ┌────────────────┐
                   │ Query Router   │
                   │ (Lambda)       │
                   └───┬────────┬───┘
                       │        │
            structured │        │ fuzzy / contextual
                       │        │
                       ▼        ▼
          ┌──────────────┐  ┌───────────────────────┐
          │ Text2Cypher  │  │     GraphRAG           │
          │              │  │                        │
          │ NL → openCypher│ │ Subgraph → chunks     │
          │ query →      │  │ → Titan embeddings     │
          │ Neptune →    │  │ → vector retrieval     │
          │ NL answer    │  │ → Bedrock generation   │
          └──────┬───────┘  └────────────┬───────────┘
                 │                        │
                 └───────────┬────────────┘
                             ▼
                    Natural language answer
                    returned to user
```

---

## Technology Decisions

### TD1: openCypher as the graph query language

**Decision:** All application-layer graph queries use openCypher.

**Rationale:**
- More readable than Gremlin for developers and reviewers
- Maps cleanly to Bedrock Text2Query prompting (Cypher syntax is well-represented in LLM training data)
- Linkurious has strong openCypher support
- Neptune supports openCypher natively since 2022

**Exception:** Neptune Bulk Loader API is used for initial CSV ingestion — this is a transport-level API, not a query language, and has no openCypher equivalent for bulk loading.

**Trade-off:** Neptune's openCypher implementation has some gaps vs. full Cypher (e.g., some APOC procedures unavailable). Validate query patterns during the Milestone 2 Linkurious spike.

---

### TD2: Neptune Bulk Loader API for initial ingestion

**Decision:** Use the [Neptune Bulk Loader API](https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load.html) rather than Gremlin/openCypher `MERGE` statements for the initial 2M node / 3M relationship load.

**Rationale:**
- Orders of magnitude faster than row-by-row Gremlin inserts for large datasets
- Native support for ICIJ-format CSVs (node files + edge files)
- Idempotent with the `updateSingleCardinalityProperties` flag
- Lambda invokes the loader via REST API; Neptune pulls directly from S3

**Trade-off:** Bulk Loader runs asynchronously — Lambda must poll for completion status. Error handling is more complex than synchronous inserts.

---

### TD3: Ephemeral Neptune Analytics for algorithm runs

**Decision:** Spin up a Neptune Analytics graph instance on-demand, run algorithms, push results back to Neptune Core, then tear down.

**Rationale:**
- Neptune Analytics is billed per GCU-hour — ephemeral usage costs ~$40/month vs. always-on ~$200+/month
- Algorithms (PageRank, community detection) are batch jobs, not real-time — no need for a persistent analytics instance
- Enriched properties stored in Neptune Core are available immediately to Linkurious

**Trade-off:** Cold start time for Neptune Analytics (minutes). Acceptable for scheduled enrichment runs; not suitable for interactive real-time analysis.

---

### TD4: Amazon Bedrock (Claude) for natural language querying

**Decision:** Use Amazon Bedrock with the Claude model family for both Text2openCypher generation and GraphRAG generation.

**Rationale:**
- Claude has strong structured output and code generation capabilities (good for Text2Cypher)
- Native AWS integration — no external API keys, IAM-controlled access
- Bedrock Titan Embeddings for cost-effective vector embeddings in the GraphRAG pipeline
- Claude Haiku is extremely cheap for high-volume query handling ($0.25/1M input tokens)

**Trade-off:** Bedrock Text2Cypher quality depends on few-shot examples provided. Plan to invest in a prompt engineering spike (Milestone 4, issue #20) before building the full pipeline.

---

## Component Boundaries

| Directory | Owns | Does NOT Own |
|-----------|------|-------------|
| `pipeline/` | S3 bucket, Neptune cluster IaC, Lambda bulk loader, data validation, idempotency logic | Graph algorithm runs, NL querying, Linkurious config |
| `neptune-analytics/` | Neptune Analytics IaC, algorithm job scripts, result write-back to Neptune Core | Initial data ingestion, NL interface, Linkurious config |
| `bedrock/` | Bedrock API integration, Text2Cypher pipeline, GraphRAG pipeline, Lambda API endpoint | Graph data storage, algorithm runs, Linkurious config |
| `linkurious/` | Datasource config, investigation story documentation, alert definitions | Graph infrastructure, algorithm runs, NL querying |
| `docs/` | Architecture decisions, cost model, conventions | Any runnable code |
| `.github/workflows/` | CI/CD pipeline definitions | Application logic |
