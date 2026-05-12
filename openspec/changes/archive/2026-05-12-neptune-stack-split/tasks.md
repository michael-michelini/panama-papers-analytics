## 1. Create neptune-core CloudFormation template

- [x] 1.1 Create `pipeline/infra/neptune-core.yaml` — extract VPC, subnets, IGW, route table, security group, subnet group, parameter group, `NeptuneS3Role`, cluster, and instance from `NeptuneServerlessMigration.yaml`
- [x] 1.2 Add `DeletionPolicy: Retain` to `NeptuneCluster` and `NeptuneInstance` resources
- [x] 1.3 Add `Outputs` section exporting `NeptuneEndpoint` and `NeptuneLoadRoleArn` with export names consumable via `Fn::ImportValue`
- [x] 1.4 Run `cfn-lint` against `neptune-core.yaml` and resolve any errors

## 2. Create neptune-loader CloudFormation template

- [x] 2.1 Create `pipeline/infra/neptune-loader.yaml` — extract `LambdaExecutionRole`, `LambdaNeptuneLoaderPolicy`, `BulkLoadTriggerLambda`, `LambdaInvokePermission`, and `StagingBucket` from `NeptuneServerlessMigration.yaml`
- [x] 2.2 Replace hardcoded Neptune endpoint and role ARN with `Fn::ImportValue` referencing core stack exports
- [x] 2.3 Confirm Lambda `Code.ZipFile` references `pipeline/loaders/bulk_load_trigger.py` logic (iterates all records, not just `Records[0]`)
- [x] 2.4 Run `cfn-lint` against `neptune-loader.yaml` and resolve any errors

## 3. Create GitHub Actions workflows

- [x] 3.1 Create `.github/workflows/deploy-neptune-core.yml` — triggers on PR path `pipeline/infra/neptune-core.yaml` and `workflow_dispatch`; lints, validates, deploys, and confirms cluster availability
- [x] 3.2 Create `.github/workflows/deploy-neptune-loader.yml` — `workflow_dispatch` only; lints, validates, deploys, and prints stack outputs (bucket name, Neptune endpoint)
- [x] 3.3 Update path references in both workflows to point to the correct template files under `pipeline/infra/`

## 4. Remove superseded files

- [x] 4.1 Delete `pipeline/infra/NeptuneServerlessMigration.yaml`
- [x] 4.2 Delete `.github/workflows/deploy-neptune-migration.yml`

## 5. Update operator runbook

- [x] 5.1 Update `pipeline/MIGRATION_README.md` (or equivalent) to document the two-stack deploy sequence: deploy core → deploy loader → load vertices → wait → load edges → delete loader stack
- [x] 5.2 Document retained resource teardown: how to manually delete the Neptune cluster and instance if the core stack is intentionally destroyed
