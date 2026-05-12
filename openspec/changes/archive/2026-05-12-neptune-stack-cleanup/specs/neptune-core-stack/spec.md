## MODIFIED Requirements

### Requirement: Persistent Neptune cluster stack
A CloudFormation template (`pipeline/infra/neptune-core.yaml`) SHALL provision the Neptune Serverless cluster and all supporting networking resources as a long-lived stack. The cluster and its instance SHALL have `DeletionPolicy: Delete` so that intentional teardown via `delete-stack` removes all resources. The cluster and its instance SHALL have `UpdateReplacePolicy: Retain` so that if a stack update would trigger resource replacement, the existing cluster is orphaned rather than destroyed, preventing silent data loss.

#### Scenario: Stack deletion removes Neptune cluster
- **WHEN** the `neptune-core` CloudFormation stack is deleted
- **THEN** the Neptune cluster and instance SHALL be deleted by CloudFormation

#### Scenario: Stack update that triggers replacement retains old cluster
- **WHEN** the `neptune-core` stack is updated with a change that requires cluster replacement
- **THEN** the existing Neptune cluster SHALL be retained (orphaned) rather than deleted, and the operator SHALL be able to recover data from it

#### Scenario: Stack update to safe properties does not reprovision cluster
- **WHEN** the `neptune-core` stack is updated with a change that does not require cluster replacement (e.g., scaling configuration)
- **THEN** the Neptune cluster SHALL be updated in-place and no data SHALL be lost
