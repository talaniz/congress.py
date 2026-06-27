# MCP Build Context

## Current Session

- Branch: `feature/build-mcp`
- Build lane: MCP Session 04
- Plan file: `build/mcp/04_add_mcp_server.md`
- Goal: add a small read-only MCP server backed by `CongressClient`.

## Project Context

`congress_py` is an unofficial Python SDK and CLI for the Congress.gov API. The
SDK and CLI are stable enough for the first MCP layer. The MCP layer should be
thin, read-only, and should call `CongressClient` rather than duplicating API
logic.

The SDK now includes:

- `get_bill(congress, bill_type, number)`
- `get_bill_actions(congress, bill_type, number)`
- `get_bill_summaries(congress, bill_type, number)`
- `list_recent_bills(limit=10)`

## Locked Decisions

- Use the simplest local MCP transport: stdio.
- Keep MCP dependencies optional.
- Add an optional install extra:

  ```toml
  mcp = ["mcp[cli]>=1.27,<2"]
  ```

- Local MCP install command:

  ```bash
  .venv/bin/python -m pip install -e ".[mcp]"
  ```

- Published MCP install command:

  ```bash
  pip install "congress-py[mcp]"
  ```

- Add local CLI command:

  ```bash
  congress mcp-start
  ```

- `congress mcp-start` should resolve credentials like the rest of the CLI:
  1. explicit `--api-key`
  2. `CONGRESS_API_KEY`
  3. `~/.congress/config.toml`

- Keep the existing friendly missing-key behavior:

  ```text
  No Congress.gov API key found. Run congress configure or set CONGRESS_API_KEY.
  ```

- Docker should not use the `congress mcp-start` CLI command as its entrypoint.
- Docker should run the Python module directly:

  ```dockerfile
  ENTRYPOINT ["python", "-m", "congress_py.mcp_server"]
  ```

- Docker API keys must be provided at container runtime, not build time:

  ```bash
  docker run --rm -i -e CONGRESS_API_KEY=... congress-py-mcp
  ```

- Do not use Docker build args for API keys.
- MCP tool outputs should use the existing SDK/CLI snake_case JSON-compatible
  shape.

## Implementation Plan

1. Add optional MCP dependency support in `pyproject.toml`.
2. Create `src/congress_py/mcp_server.py`.
3. Expose read-only MCP tools:
   - `get_bill`
   - `get_bill_actions`
   - `get_bill_summaries`
   - `list_recent_bills`
4. Add a testable server factory/helper layer so tool behavior can be tested
   without launching a blocking MCP process.
5. Add `congress mcp-start` in `src/congress_py/cli.py`.
6. Add `Dockerfile` and `.dockerignore`.
7. Add tests for MCP tool delegation, output shape, invalid recent-bills limits,
   and CLI start wiring.
8. Add `docs/mcp.md`, add it to `mkdocs.yml`, and update `docs/changelog.md`.
9. Append a factual session entry to `build/build_log.md`.

## Validation

Run:

```bash
.venv/bin/python -m pip install -e ".[mcp]"
.venv/bin/python -m pytest
```

If docs dependencies are available:

```bash
.venv/bin/python -m mkdocs build --strict
```

If Docker is available:

```bash
docker build -t congress-py-mcp .
```

## Follow-Up

After Session 04, the MCP execution plan recommends verifying the PyPI MCP
extras/install path before adding the optional LLM summarization layer.

## Post-Docker Validation Context

After the MCP implementation and initial validation, Docker validation was
blocked because the Docker daemon was not running. The user started Docker
Desktop and asked to finish the Docker portion.

The Docker build then completed successfully:

```bash
docker build -t congress-py-mcp .
```

A no-secret container smoke test also ran:

```bash
docker run --rm congress-py-mcp
```

The container started the module entrypoint and failed cleanly without
credentials:

```text
No Congress.gov API key found. Run congress configure or set CONGRESS_API_KEY.
```

This confirms the image entrypoint runs and does not require secrets at build
time. The intended real runtime command remains:

```bash
docker run --rm -i -e CONGRESS_API_KEY=... congress-py-mcp
```

After updating the build log with the successful Docker validation, the final
test run passed:

```text
61 passed in 0.20s
```
