# AWS Cost Model

Monthly cost estimates for the Panama Papers Analytics Platform in a POC/demo environment. All prices are AWS ap-southeast-2 (Sydney) region pricing as of mid-2025. Actual costs will vary with usage.

---

## Summary

| Service | Always-On ($/month) | Demo-Mode ($/month) | Notes |
|---------|--------------------|--------------------|-------|
| Neptune Core (db.r6g.large) | ~$270 | ~$75 | See sizing options below |
| Neptune Analytics (ephemeral) | ~$40 | ~$40 | Already ephemeral |
| Lambda | ~$5 | ~$2 | Mostly ingestion + triggers |
| S3 | ~$2 | ~$2 | CSV storage + outputs |
| NAT Gateway | ~$40 | ~$15 | See optimisation levers |
| Bedrock | ~$10 | ~$5 | Claude Haiku + Titan embeddings |
| **Total AWS** | **~$370/month** | **~$140/month** | |
| Linkurious license | **TBD** | **TBD** | See note below |

> **Demo-mode** = Neptune instance stopped outside business hours (~8 hrs/day, 5 days/week ≈ 35% of hours running)

---

## Neptune Core — Sizing Options

Neptune is the largest cost driver. Two realistic options for the POC:

### Option A: db.r6g.large (Recommended starting point)

| Metric | Value |
|--------|-------|
| vCPUs | 2 |
| RAM | 16 GB |
| Price | $0.371/hr (Sydney) |
| Always-on monthly | ~$270 |
| Demo-mode monthly | ~$95 |

**Suitable for:** 2M nodes / 3M relationships with low concurrent load (1–2 demo users). Adequate for the POC.

**Upgrade trigger:** If query latency on multi-hop traversals exceeds 3–5 seconds during demos, upgrade to xlarge.

### Option B: db.r6g.xlarge (Upgrade path)

| Metric | Value |
|--------|-------|
| vCPUs | 4 |
| RAM | 32 GB |
| Price | $0.741/hr (Sydney) |
| Always-on monthly | ~$535 |
| Demo-mode monthly | ~$185 |

**Suitable for:** Higher query complexity, more concurrent users, or if the graph grows beyond 5M elements.

### Storage & I/O (both options)

| Item | Rate | Estimated monthly |
|------|------|------------------|
| Storage | $0.115/GB | ~$2–5 (20–40 GB) |
| I/O requests | $0.22/1M requests | ~$10–20 |

---

## Neptune Analytics — Ephemeral

Neptune Analytics is billed per Graph Compute Unit (GCU) hour. Because runs are ephemeral (spin up → run → tear down), costs are naturally contained.

| Assumption | Value |
|------------|-------|
| GCUs needed for 5M elements | ~16 GCUs |
| Runtime per analysis run | ~2 hours |
| Runs per month | ~4 (weekly) |
| Price per GCU-hour | $0.30 |
| **Estimated monthly** | **~$38** |

> **Note:** GCU sizing for the Panama Papers dataset is unvalidated. Milestone 3 spike (#15) must confirm requirements before committing to this estimate.

---

## Lambda

| Use case | Estimated monthly |
|----------|------------------|
| Bulk loader invocation (one-time initial load) | ~$0 (within free tier) |
| Ongoing S3 event triggers | ~$1 |
| Neptune Analytics orchestration | ~$2 |
| Bedrock API endpoint | ~$2 |
| **Total** | **~$5** |

Lambda free tier (1M requests + 400,000 GB-seconds/month) covers most demo-volume workloads.

---

## S3

| Item | Estimate |
|------|----------|
| CSV storage (~5 GB raw data) | ~$0.12 |
| Neptune Analytics export/import | ~$1 |
| Bedrock GraphRAG chunks/embeddings | ~$1 |
| **Total** | **~$2** |

---

## NAT Gateway

> ⚠️ NAT Gateway is often overlooked but consistently adds $33–50/month even at low traffic volumes.

| Item | Rate | Monthly |
|------|------|---------|
| NAT Gateway hourly | $0.059/hr | ~$43 |
| Data processing | $0.059/GB | ~$5–10 |

### Optimisation: VPC Endpoints

Replace NAT Gateway traffic with VPC Interface Endpoints for services used heavily:

| Endpoint | Saves | Cost to add |
|----------|-------|-------------|
| S3 Gateway Endpoint | NAT costs for all S3 traffic | Free |
| Neptune (Interface Endpoint) | NAT costs for Neptune API calls | ~$7/month |
| Bedrock (Interface Endpoint) | NAT costs for Bedrock calls | ~$7/month |

With S3 Gateway Endpoint in place, NAT Gateway costs drop to ~$15–20/month.

---

## Amazon Bedrock

| Use case | Model | Rate | Monthly estimate |
|----------|-------|------|-----------------|
| Text2Cypher + NL response | Claude Haiku | $0.25/1M input, $1.25/1M output | ~$5 |
| GraphRAG generation | Claude Haiku | $0.25/1M input, $1.25/1M output | ~$3 |
| Embeddings | Titan Embeddings V2 | $0.00002/1K tokens | ~$1 |
| **Total (demo usage)** | | | **~$9** |

Bedrock costs scale linearly with query volume. At demo-level traffic (dozens of queries/day), costs are minimal.

---

## Linkurious Licensing

> ⚠️ **TBD — confirm POC trial availability before Milestone 2 begins.**

Linkurious is commercial software with enterprise pricing:

| License type | Typical range |
|-------------|--------------|
| Enterprise annual license | ~$50,000–$150,000/year |
| POC / trial license | Free (negotiate with Linkurious sales) |
| Per-seat or consumption pricing | Varies by contract |

**Action required:** Contact Linkurious to confirm whether a POC trial license is available for this engagement. If no trial is available, Milestone 2 work is blocked on licensing.

---

## Cost Optimisation Levers

### 1. Stop Neptune between demo sessions (biggest lever)

Neptune can be stopped when not in use. Stopping the instance eliminates instance-hour charges but retains storage.

| Scenario | Monthly Neptune cost |
|---------|---------------------|
| Always-on (db.r6g.large) | ~$270 |
| Stopped outside 8hrs/day, 5 days/week | ~$95 |
| Stopped outside 4hrs/day, 3 days/week | ~$50 |

**Automation:** Use a Lambda + EventBridge schedule to auto-stop/start before and after demo windows.

### 2. S3 Gateway VPC Endpoint (free, immediate)

Add an S3 Gateway VPC Endpoint in the CDK stack. Zero cost, eliminates all S3 traffic from passing through the NAT Gateway.

### 3. Use Neptune Analytics only ephemerally (already planned)

Never leave Neptune Analytics running — always tear down after algorithm jobs complete. This is already the planned architecture.

### 4. Use Bedrock Haiku over Sonnet/Opus

Claude Haiku is ~20x cheaper than Sonnet for the same query volume. Use Haiku for all production Text2Cypher and GraphRAG queries. Only use Sonnet during development/prompting experimentation.
