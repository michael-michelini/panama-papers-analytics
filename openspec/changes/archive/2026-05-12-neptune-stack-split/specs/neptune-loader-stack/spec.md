## ADDED Requirements

### Requirement: Ephemeral bulk-load stack
A CloudFormation template (`pipeline/infra/neptune-loader.yaml`) SHALL provision only the infrastructure required to bulk-load data into Neptune: an S3 staging bucket with S3→Lambda notification and a Lambda function that submits Neptune bulk load jobs. The stack SHALL be deployed on demand and deleted by the operator after the load is complete.

#### Scenario: Loader stack deployed and functional
- **WHEN** the `neptune-loader` stack is deployed after `neptune-core`
- **THEN** uploading a CSV file to the staging bucket SHALL trigger the Lambda, which SHALL submit a Neptune bulk load job pointing at that S3 object

#### Scenario: Loader stack deleted after load completes
- **WHEN** the operator deletes the `neptune-loader` stack after data is fully loaded
- **THEN** all loader stack resources (bucket, Lambda, IAM roles) SHALL be removed and the Neptune cluster SHALL remain unaffected

### Requirement: Loader stack imports Neptune connection details
The loader stack SHALL obtain the Neptune endpoint and IAM load role ARN exclusively via `Fn::ImportValue` from the `neptune-core` stack outputs. These values SHALL NOT be hardcoded or provided as manual stack parameters.

#### Scenario: Loader stack resolves Neptune endpoint automatically
- **WHEN** the `neptune-loader` stack is deployed
- **THEN** the Lambda environment variable `NEPTUNE_ENDPOINT` SHALL be set from the imported core stack output without operator input

### Requirement: Lambda iterates all S3 event records
The Lambda handler SHALL process every record in the S3 event payload, not only the first. Each record SHALL result in a separate Neptune bulk load job submission.

#### Scenario: Batched S3 event processed fully
- **WHEN** an S3 event containing multiple object records triggers the Lambda
- **THEN** a separate bulk load job SHALL be submitted for each object in the event

### Requirement: Staging bucket is single-use per load cycle
The S3 staging bucket SHALL have a lifecycle rule that expires objects after 7 days. The operator SHALL delete the loader stack (and with it the bucket) after the load cycle is complete to prevent accidental re-triggering.

#### Scenario: Expired objects are cleaned up automatically
- **WHEN** an object in the staging bucket is older than 7 days
- **THEN** S3 SHALL automatically delete the object
