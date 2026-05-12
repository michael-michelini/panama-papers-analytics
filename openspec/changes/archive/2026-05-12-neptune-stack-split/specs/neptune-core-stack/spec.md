## ADDED Requirements

### Requirement: Persistent Neptune cluster stack
A CloudFormation template (`pipeline/infra/neptune-core.yaml`) SHALL provision the Neptune Serverless cluster and all supporting networking resources as a long-lived stack. The cluster and its instance SHALL have `DeletionPolicy: Retain` so that data is preserved if the stack is deleted or updated in a way that would otherwise reprovision the cluster.

#### Scenario: Stack deletion does not destroy Neptune cluster
- **WHEN** the `neptune-core` CloudFormation stack is deleted
- **THEN** the Neptune cluster and instance SHALL be retained and continue to exist with their loaded data intact

#### Scenario: Stack update to safe properties does not reprovision cluster
- **WHEN** the `neptune-core` stack is updated with a change that does not require cluster replacement (e.g., scaling configuration)
- **THEN** the Neptune cluster SHALL be updated in-place and no data SHALL be lost

### Requirement: Core stack exports consumed by loader stack
The `neptune-core` stack SHALL export the Neptune cluster endpoint and the Neptune S3 IAM role ARN as CloudFormation outputs using names that the loader stack can import via `Fn::ImportValue`.

#### Scenario: Loader stack imports core stack outputs
- **WHEN** the `neptune-loader` stack is deployed after `neptune-core`
- **THEN** the loader stack SHALL successfully resolve the Neptune endpoint and load role ARN from core stack exports without requiring manual parameter input

### Requirement: Neptune S3 role lives in core stack
The IAM role that Neptune uses to read from S3 during bulk load (`NeptuneS3Role`) SHALL be defined in and associated with the cluster in `neptune-core.yaml`. It SHALL NOT be moved to the loader stack.

#### Scenario: Bulk load succeeds without loader stack modifying cluster
- **WHEN** the `neptune-loader` stack triggers a bulk load job
- **THEN** Neptune SHALL use the IAM role already associated at the cluster level, with no modification to the core stack required

### Requirement: Core stack blocks deletion while loader stack exists
Because the loader stack imports outputs from the core stack via `Fn::ImportValue`, CloudFormation SHALL prevent deletion of the core stack while the loader stack is deployed.

#### Scenario: Core stack deletion blocked by active import
- **WHEN** an operator attempts to delete the `neptune-core` stack while `neptune-loader` is deployed and importing its outputs
- **THEN** CloudFormation SHALL reject the deletion with an error indicating the export is in use
