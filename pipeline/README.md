# Pipeline

Ingests the Panama Papers CSV dataset into Amazon Neptune via S3 and Lambda.

## Responsibilities

- S3 bucket provisioning and CSV upload tooling
- Lambda function triggered by S3 events to invoke the Neptune Bulk Loader API
- CloudFormation infrastructure for Neptune cluster, S3 bucket, Lambda, and IAM roles

## NOT Responsible For

- Graph algorithm runs (see `neptune-analytics/`)
- Natural language querying (see `bedrock/`)
- Linkurious configuration (see `linkurious/`)

## Structure

```
pipeline/
├── infra/          # CloudFormation templates (neptune-core.yaml, neptune-loader.yaml)
├── tests/          # Tests (scaffolded, not yet implemented)
└── pyproject.toml
```

> The Lambda handler is defined inline in `infra/neptune-loader.yaml` as a CloudFormation `ZipFile` resource.

## Setup

```bash
cd pipeline
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Related Issues

See [Milestone 1: 🗄️ Data Pipeline & Neptune Core](../../milestones) on GitHub.
