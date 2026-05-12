# Development Conventions

## Python

- **Version:** Python 3.12 (pinned via `.python-version` in each component directory)
- **Package manager:** `pip` with `pyproject.toml` for dependency declaration
- **Virtual environments:** Use `.venv/` (excluded from git)

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
pip install -e ".[dev]"
```

## Linting

- **Tool:** [`ruff`](https://docs.astral.sh/ruff/) — fast Python linter and formatter
- **Configuration:** `pyproject.toml` in each component directory
- **Run locally:**

```bash
ruff check .         # lint
ruff check . --fix   # auto-fix
ruff format .        # format
```

- **CI:** All PRs must pass `ruff check` with zero errors before merge.

## Testing

- **Framework:** `pytest`
- **Location:** `tests/` directory within each component
- **Run locally:**

```bash
pytest tests/ -v
```

- **CI:** All PRs must pass `pytest` with zero failures. Workflows fail if no tests are found.

## Graph Query Language

- **Preferred:** openCypher — more readable, better LLM prompting patterns, strong Linkurious support
- **Acceptable for bulk ops:** Neptune Bulk Loader API (transport-level, not query-language)
- **Avoid:** Gremlin unless the specific operation is not supported in openCypher on Neptune

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature / story | `feat/<issue-number>-short-description` | `feat/3-neptune-iac` |
| Bug fix | `fix/<issue-number>-short-description` | `fix/12-loader-timeout` |
| Spike / research | `spike/<issue-number>-short-description` | `spike/2-pipeline-audit` |
| Chore | `chore/<issue-number>-short-description` | `chore/1-monorepo-scaffold` |

## Commit Messages

Use the imperative mood, present tense. Reference the issue number.

```
feat(pipeline): add S3 trigger for Lambda bulk loader (#5)
fix(bedrock): handle empty graph query results (#23)
chore: initialise mono-repo structure (#1)
```

## Pull Requests

- All PRs target `main`
- CI must be green (lint + tests) before merge
- PRs should reference the GitHub issue number in the title or body
- Keep PRs small and focused on a single story/task

## AWS & Infrastructure

- **IaC tool:** AWS CDK (Python) — CDK code lives in `infra/` within each component
- **Naming convention:** Resources prefixed with `panama-papers-` (e.g., `panama-papers-neptune-cluster`)
- **Environment:** Single POC/demo environment; no prod/staging split at this stage
- **Secrets:** Never commit credentials. Use AWS Secrets Manager or environment variables via `.env` (gitignored).
