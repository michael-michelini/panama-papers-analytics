## 1. Remove duplicate loader directory

- [x] 1.1 Delete `pipeline/loaders/` directory and all contents

## 2. Fix Neptune core stack deletion policy

- [x] 2.1 Change `DeletionPolicy: Retain` to `DeletionPolicy: Delete` on `NeptuneCluster` in `pipeline/infra/neptune-core.yaml`
- [x] 2.2 Change `DeletionPolicy: Retain` to `DeletionPolicy: Delete` on `NeptuneInstance` in `pipeline/infra/neptune-core.yaml`
- [x] 2.3 Update the `Description` field in `neptune-core.yaml` to remove the reference to `DeletionPolicy: Retain`
- [x] 2.4 Run `cfn-lint pipeline/infra/neptune-core.yaml` and resolve any errors
