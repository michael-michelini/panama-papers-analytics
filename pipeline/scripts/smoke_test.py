"""Neptune connectivity smoke test.

Usage:
    python smoke_test.py <neptune-endpoint>
    NEPTUNE_ENDPOINT=<endpoint> python smoke_test.py
"""

import os
import sys

import boto3


def main() -> None:
    endpoint = None
    if len(sys.argv) > 1:
        endpoint = sys.argv[1]
    else:
        endpoint = os.environ.get("NEPTUNE_ENDPOINT")

    if not endpoint:
        print(
            "Error: Neptune endpoint required as CLI arg or NEPTUNE_ENDPOINT env var",
            file=sys.stderr,
        )
        sys.exit(1)

    host = endpoint if endpoint.startswith("https://") else f"https://{endpoint}:8182"
    region = os.environ.get("AWS_REGION", "ap-southeast-2")

    client = boto3.client("neptunedata", endpoint_url=host, region_name=region)

    try:
        query = "MATCH (n) RETURN count(n) LIMIT 1"
        response = client.execute_open_cypher_query(openCypherQuery=query)
        results = response.get("results", [])
        print(f"Smoke test passed. Query result: {results}")
        sys.exit(0)
    except Exception as exc:
        print(f"Smoke test failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
