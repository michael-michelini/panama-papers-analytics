# Pipeline

Ingests the Panama Papers CSV dataset into Amazon Neptune via S3 and Lambda.

## Responsibilities

- S3 bucket provisioning and CSV upload tooling
- Lambda function triggered by S3 events to invoke the Neptune Bulk Loader API
- Data validation before load (schema checks, required properties)
- Idempotent load strategy (safe to re-run without creating duplicates)
- CDK infrastructure for Neptune cluster, S3 bucket, Lambda, VPC, and IAM roles

## NOT Responsible For

- Graph algorithm runs (see `neptune-analytics/`)
- Natural language querying (see `bedrock/`)
- Linkurious configuration (see `linkurious/`)

## Structure

```
pipeline/
├── infra/          # AWS CDK stack
├── loaders/        # Lambda function code
├── tests/          # Unit and integration tests
└── pyproject.toml
```

## Setup

```bash
cd pipeline
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Related Issues

See [Milestone 1: 🗄️ Data Pipeline & Neptune Core](../../milestones) on GitHub.
