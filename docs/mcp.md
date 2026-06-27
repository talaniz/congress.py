# MCP Server

`congress_py` includes an optional read-only MCP server for selected
Congress.gov bill workflows. The MCP layer calls `CongressClient`; it does not
duplicate Congress.gov HTTP logic.

## Install MCP Support

From PyPI:

```bash
python -m pip install "congress-py[mcp]"
```

For local development:

```bash
.venv/bin/python -m pip install -e ".[mcp]"
```

## Available Tools

- `get_bill`
- `get_bill_actions`
- `get_bill_summaries`
- `list_recent_bills`

Tool output uses the same snake_case JSON-compatible shape as the SDK and CLI.

## Start Locally

The easiest local entry point is:

```bash
congress mcp-start
```

The command resolves credentials in the same order as the rest of the CLI:

1. `--api-key`
2. `CONGRESS_API_KEY`
3. `~/.congress/config.toml`

You can also start the MCP module directly:

```bash
CONGRESS_API_KEY=your_api_key_here python -m congress_py.mcp_server
```

The server uses stdio transport for local MCP clients.

## Docker

Build the image locally:

```bash
docker build -t congress-py-mcp .
```

Run it with the API key supplied at runtime:

```bash
docker run --rm -i -e CONGRESS_API_KEY=your_api_key_here congress-py-mcp
```

Do not pass API keys as Docker build arguments. Runtime environment variables
avoid baking secrets into the image.

The container entry point runs the Python module directly:

```dockerfile
ENTRYPOINT ["python", "-m", "congress_py.mcp_server"]
```

## Example Client Configuration

For an MCP client that launches a local command, configure the command to run:

```bash
congress mcp-start
```

For Docker-based local testing, configure the client to run the `docker run`
command above with `CONGRESS_API_KEY` supplied by the environment.
