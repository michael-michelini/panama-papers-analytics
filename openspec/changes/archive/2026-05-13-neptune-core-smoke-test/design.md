## Context

The `deploy-neptune-core` workflow today verifies deployment success by polling `describe-db-clusters` until status is `available`. This is an AWS control-plane check only — it says the cluster resource exists, not that the data plane is reachable. An operator discovering connectivity issues would have to wait until Linkurious or a bulk load attempt tried to connect.

The Neptune endpoint is publicly accessible on port 8182 (IAM auth enabled). The boto3 `neptunedata` client — already used by the loader Lambda — handles SigV4 signing transparently and supports openCypher via `execute_open_cypher_query`. This makes a post-deploy query straightforward from a GitHub Actions runner with AWS credentials.

## Goals / Non-Goals

**Goals:**
- Verify the Neptune endpoint is reachable and accepting signed queries after every core stack deployment
- Reuse the boto3 `neptunedata` pattern already established in the project
- Keep the test logic out of the workflow YAML (in a Python script) for readability and local runnability

**Non-Goals:**
- Data correctness checks (whether loaded nodes/edges are present or valid)
- Performance or latency assertions
- Testing the loader stack or S3 trigger path
- Any changes to the CloudFormation templates

## Decisions

### Decision: boto3 `neptunedata` client over raw HTTP curl

`curl` with a SigV4 signature is doable but fragile — the signing logic is non-trivial shell. The `neptunedata` client handles auth, retries, and endpoint construction cleanly and is already the pattern used in the loader Lambda. Keeping both callers on the same client reduces divergence.

Alternative considered: `requests` + `requests-aws4auth`. Ruled out — adds a pip dependency and duplicates what boto3 already provides.

### Decision: standalone `pipeline/scripts/smoke_test.py` over inline workflow shell

Embedding a 20-line Python script in `run: |` makes it untestable locally. A standalone script can be run by an operator against any environment with `python pipeline/scripts/smoke_test.py <endpoint>` and is easier to read in code review.

### Decision: `MATCH (n) RETURN count(n) LIMIT 1` as the smoke query

This query is valid on an empty graph (returns 0) and on a loaded graph (returns node count). It exercises the query parser, execution engine, and IAM auth path without depending on any specific data being present.

## Risks / Trade-offs

- [Risk] Smoke test adds ~10–15 seconds of cold-start latency to the workflow → Acceptable; the cluster is already available by the time this step runs
- [Risk] If the Neptune endpoint changes between the "Print stack outputs" step and the smoke test step, the test uses a stale value → Mitigated by reading the endpoint from CloudFormation outputs within the same job
- [Risk] boto3 is not pre-installed on `ubuntu-latest` GitHub Actions runners → Mitigated by a `pip install boto3` step (fast, ~2s)

## Migration Plan

1. Add `pipeline/scripts/smoke_test.py`
2. Add a `pip install boto3` step to the workflow (before the smoke test step)
3. Add the smoke test step after "Confirm cluster is available"
4. No rollback needed — the step is additive; removing it restores the prior behaviour
