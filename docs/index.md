# congress_py

`congress_py` is an unofficial Python SDK and CLI for the Congress.gov API.
It provides a small, testable interface for reading congressional sessions,
bills, bill actions, and bill summaries.

The project is intended to stay compact and readable while it grows toward a
read-only MCP server for selected Congress.gov workflows. The SDK remains the
source of truth; the CLI and future MCP tools call the SDK instead of
duplicating API logic.

!!! warning "Unofficial project"
    This project is not affiliated with Congress.gov, the Library of Congress,
    Congress, or the U.S. government.

!!! warning "No advice"
    This project does not provide legal, legislative, lobbying, financial,
    compliance, or policy advice. Verify important information against official
    Congress.gov records.

## What is included

- A `CongressClient` SDK for read-only API access.
- Typed models for bills, bill actions, and bill summaries.
- A JSON-first `congress` CLI.
- Mocked tests for SDK and CLI behavior.

## Start here

- [Installation](installation.md)
- [Quickstart](quickstart.md)
- [CLI usage](cli.md)
- [SDK guide](sdk.md)
- [API reference](api-reference.md)
