## 1. Smoke Test Script

- [x] 1.1 Create `pipeline/scripts/smoke_test.py` — accepts Neptune endpoint as CLI arg or `NEPTUNE_ENDPOINT` env var, connects via boto3 `neptunedata` client, runs `MATCH (n) RETURN count(n) LIMIT 1`, prints result, exits 0 on success / non-zero on failure

## 2. Workflow Update

- [x] 2.1 Add `pip install boto3` step to `deploy-neptune-core.yml` (before smoke test step)
- [x] 2.2 Add smoke test step to `deploy-neptune-core.yml` — reads endpoint from CloudFormation stack outputs and passes it to `pipeline/scripts/smoke_test.py`

## 3. Verification

- [ ] 3.1 Trigger `deploy-neptune-core` workflow manually via `workflow_dispatch` and confirm smoke test step passes
- [ ] 3.2 Confirm workflow output shows the query result (node count)
