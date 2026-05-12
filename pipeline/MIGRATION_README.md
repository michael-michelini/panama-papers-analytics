# Neptune Data Migration Runbook

End-to-end operator guide for loading the Panama Papers dataset into Neptune using the two-stack deployment model.

## Architecture

The pipeline uses two CloudFormation stacks with separate lifecycles:

| Stack | Template | Lifecycle |
|---|---|---|
| `neptune-core` | `pipeline/infra/neptune-core.yaml` | **Persistent** — deploy once; never delete unless rebuilding from scratch |
| `neptune-loader` | `pipeline/infra/neptune-loader.yaml` | **Ephemeral** — deploy per load cycle; delete when done |

The loader stack imports the Neptune endpoint and S3 role ARN from the core stack via `Fn::ImportValue`. CloudFormation will refuse to delete the core stack while the loader stack is deployed, preventing accidental data loss.

## Prerequisites

- AWS credentials configured with permissions for CloudFormation, Neptune, S3, Lambda, and IAM
- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` set as GitHub Actions secrets
- `AWS_GLOBAL_STACK_PREFIX` set as a GitHub Actions variable (optional; defaults to no prefix)

## Deploy Sequence

### Step 1 — Deploy the core stack (one-time)

Trigger the **Deploy Neptune Core Stack** workflow from GitHub Actions → `deploy-neptune-core.yml`, or push a change to `pipeline/infra/neptune-core.yaml` on a PR to `main`.

The workflow:
1. Lints and validates `neptune-core.yaml`
2. Deploys (or updates) the `neptune-core` CloudFormation stack
3. Confirms the Neptune cluster status is `available`
4. Prints stack outputs (Neptune endpoint, S3 role ARN, cluster resource ID)

The core stack provisions: VPC, subnets, internet gateway, route table, security group, Neptune subnet group, Neptune parameter group, Neptune S3 IAM role, Neptune Serverless cluster, and Neptune instance.

**Only run this once.** Subsequent runs update the stack in-place. The cluster carries `DeletionPolicy: Retain` so updates that would trigger replacement are blocked.

### Step 2 — Deploy the loader stack

Trigger the **Deploy Neptune Loader Stack** workflow manually from GitHub Actions → `deploy-neptune-loader.yml` → **Run workflow**.

The workflow:
1. Lints and validates `neptune-loader.yaml`
2. Deploys the `neptune-loader` CloudFormation stack
3. Prints stack outputs including the staging bucket name

The loader stack provisions: S3 staging bucket (with 7-day object expiry), Lambda bulk-load trigger, and Lambda IAM role.

### Step 3 — Load vertices

Upload all vertex CSV files to the staging bucket. The Lambda fires for each object and submits a Neptune bulk load job.

```bash
aws s3 cp data/vertices/ s3://<staging-bucket-name>/ --recursive
```

Wait until all vertex load jobs reach `LOAD_COMPLETED` before proceeding:

```bash
# Check load job status via Neptune loader endpoint
curl -s "https://<neptune-endpoint>:8182/loader" \
  | python3 -m json.tool
```

### Step 4 — Load edges

Only after all vertex jobs are `LOAD_COMPLETED`, upload edge CSV files:

```bash
aws s3 cp data/edges/ s3://<staging-bucket-name>/ --recursive
```

Wait for all edge load jobs to reach `LOAD_COMPLETED`.

### Step 5 — Delete the loader stack

Once the load cycle is complete, delete the loader stack to remove the S3 bucket, Lambda, and IAM roles:

```bash
aws cloudformation delete-stack --stack-name <stack-prefix>neptune-loader
aws cloudformation wait stack-delete-complete --stack-name <stack-prefix>neptune-loader
```

Or trigger a stack deletion via the AWS Console → CloudFormation → `neptune-loader` → Delete.

**Important:** Empty the staging bucket before deleting the stack, or the bucket deletion will fail and the stack will roll back:

```bash
aws s3 rm s3://<staging-bucket-name>/ --recursive
```

## Retained Resource Teardown

> **Only follow these steps if you intend to permanently destroy the Neptune cluster and all loaded data.**

The Neptune cluster and instance carry `DeletionPolicy: Retain`. Deleting the `neptune-core` CloudFormation stack will **not** delete the cluster or instance — they are retained and continue to incur cost.

To permanently destroy the Neptune cluster after deleting the core stack:

### 1. Delete the loader stack first (if deployed)

The core stack cannot be deleted while the loader stack imports its outputs. Delete the loader stack first (see Step 5 above).

### 2. Delete the core stack

```bash
aws cloudformation delete-stack --stack-name <stack-prefix>neptune-core
aws cloudformation wait stack-delete-complete --stack-name <stack-prefix>neptune-core
```

The stack will delete all resources **except** the Neptune cluster and instance, which are retained.

### 3. Manually delete the Neptune instance

```bash
aws neptune delete-db-instance \
  --db-instance-identifier <stack-prefix>neptune-core-instance
```

Wait for the instance to be deleted before deleting the cluster.

### 4. Manually delete the Neptune cluster

```bash
aws neptune delete-db-cluster \
  --db-cluster-identifier <stack-prefix>neptune-core-cluster \
  --skip-final-snapshot
```

### 5. Verify deletion

```bash
aws neptune describe-db-clusters \
  --db-cluster-identifier <stack-prefix>neptune-core-cluster 2>&1
# Expected: "DBClusterNotFoundFault"
```

Any orphaned IAM roles or policies from the core stack can be found and deleted via the IAM console, filtered by the stack prefix.

## Stack Parameters

| Parameter | Core stack | Loader stack | Default |
|---|---|---|---|
| `StackPrefix` | Resource name prefix | Resource name prefix | `neptune-core` / `neptune-loader` |
| `CoreStackPrefix` | — | Export name prefix to import from core stack | `neptune-core` |

If you deployed the core stack with a custom `StackPrefix`, pass the same value as `CoreStackPrefix` when deploying the loader stack.
