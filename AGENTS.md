# Repository Guidelines

## Project Purpose

This repository is an unofficial Python SDK, CLI, and future MCP server for the Congress.gov API. The project should remain small, readable, testable, and safe to publish as an open-source portfolio project.

The near-term goal is to stabilize the SDK, expose the same core functionality through a developer-friendly CLI, and then expose selected read-only Congress.gov workflows through an MCP server. The CLI and MCP layers should call the SDK rather than duplicating API logic.

## Project Structure & Module Organization

Use a `src`-based package layout.

- `src/congress_py/`: source package.
  - `client.py`: contains `CongressClient` and all HTTP/API access logic.
  - `models.py`: contains dataclasses or typed response models such as `Bill`, `BillAction`, `BillSummary`, `Member`, and `Committee` as they are added.
  - `exceptions.py`: contains project-specific exceptions.
  - `cli.py` or `cli/`: CLI implementation. Start with `cli.py`; split into `cli/` only if the CLI grows beyond one file.
  - `mcp_server.py` or `server.py`: future read-only MCP server layer.
- `tests/`: unit tests and mocked API response fixtures.
  - `tests/TESTS.md`: testing strategy and expectations.
- `scripts/`: ad hoc development scripts for raw API checks.
- `build/`: execution planning documents for Codex-assisted development sessions.
  - `build/build_log.md`: durable build history used to carry context between Codex sessions.
  - `build/api/`: SDK/API implementation plans.
  - `build/cli/`: CLI implementation plans.
  - `build/mcp/`: MCP implementation plans.
- `pyproject.toml`: package metadata, build configuration, and console script entry point.
- `requirements.txt`: pinned development/test dependencies when used.
- `README.md`: user-facing setup, usage, disclaimers, and examples.

Avoid keeping the old `congress/` package once imports, tests, and docs have been updated to `congress_py`. This is a pre-release portfolio project, so backward compatibility shims are not needed unless explicitly requested.

Do not create a top-level `cli/` directory for product code. Keep CLI code inside `src/congress_py/` so the package installs cleanly and can share the SDK client without import-path workarounds.

## Development Principles

- Prefer simple, typed Python.
- Keep API client methods thin, predictable, and testable.
- Keep models focused on representing data. Avoid putting network-fetching behavior in models.
- Keep CLI commands thin. They should resolve configuration, call `CongressClient`, and format output.
- Keep MCP tools thin. They should validate input, call `CongressClient`, and return structured, JSON-compatible output.
- Do not add broad architecture before it is needed.
- Add functionality incrementally and keep tests passing after each meaningful change.
- Favor small, reviewable commits over large refactor piles.
- Do not introduce database persistence, caching, auth systems beyond local CLI configuration, or AI-generated legal/policy analysis unless explicitly requested.

## API Client Expectations

`CongressClient` should own:

- Base URL and endpoint construction.
- API key handling.
- Query parameter construction.
- HTTP session management.
- Timeouts.
- `raise_for_status()` behavior.
- JSON decoding.
- Pagination helpers.
- Conversion from raw API responses into typed models where appropriate.

Use `requests.Session` when using `requests`. Prefer `params={...}` over manually concatenating query strings.

Use endpoint paths that match Congress.gov API conventions. Bill endpoints should use `/bill/...`; congress/session endpoints should use `/congress/...`.

The SDK should be explicit and environment-first:

- `CongressClient` must accept an explicit `api_key`.
- The SDK may support loading `CONGRESS_API_KEY` from the environment.
- The SDK must not automatically read `~/.congress/config.toml`.
- Local config files are a CLI convenience only.

## CLI Expectations

The CLI should expose the SDK through a developer-friendly command named `congress`.

Start with commands for existing SDK behavior only. Do not add new Congress.gov endpoints during CLI scaffolding unless explicitly requested.

Recommended command shape:

- `congress configure`
- `congress congress current`
- `congress congress list`
- `congress bills list --congress 118 --bill-type hr`
- `congress bills get 118 hr 7437`

CLI rules:

- Use Typer unless the project already uses another CLI framework.
- Add the CLI module under `src/congress_py/cli.py` at first.
- Add a console script entry point named `congress` in `pyproject.toml`.
- Default output should be JSON and stable enough to test.
- Do not add rich/table formatting unless explicitly requested.
- Do not duplicate HTTP request logic in the CLI.
- The CLI must call `CongressClient`; the client remains the source of truth.
- Every new SDK endpoint should receive CLI coverage unless intentionally excluded and documented.

### CLI Credential Resolution

The CLI may provide local developer convenience through `~/.congress/config.toml`, but the SDK must not read that file automatically.

Credential resolution order for the CLI:

1. Explicit `--api-key` option, if provided.
2. `CONGRESS_API_KEY` environment variable.
3. `~/.congress/config.toml`.
4. Otherwise raise `MissingAPIKeyError`.

Config file path:

- `~/.congress/config.toml`

Config file format:

```toml
[auth]
api_key = "your-api-key-here"
```

Configuration rules:

- Only `congress configure` should prompt for an API key.
- Normal API commands must not prompt for credentials.
- If no key is available, commands should fail clearly and exit non-zero.
- When creating the config file, create `~/.congress/` if needed.
- When writing the config file, try to use file permissions `0600` where supported.
- Do not print the full API key after configuration. At most, print that configuration was saved.
- Do not log, print, commit, or expose API keys.

## Exception Handling

Use project-specific exceptions rather than generic exceptions when the failure mode matters.

Recommended exception hierarchy:

```python
class CongressAPIError(Exception):
    """Base exception for congress_py errors."""


class CongressAuthError(CongressAPIError):
    """Base exception for authentication-related errors."""


class MissingAPIKeyError(CongressAuthError):
    """Raised when no Congress.gov API key is available."""


class InvalidAPIKeyError(CongressAuthError):
    """Raised when Congress.gov rejects the provided API key."""
```

Rules:

- Use `MissingAPIKeyError` when no API key is found in the expected sources.
- Reserve `InvalidAPIKeyError` for cases where an API key is provided but Congress.gov rejects it, such as HTTP 401 or 403.
- Do not use a generic name like `AuthenticationException` for the missing-key case because that can imply the API rejected a provided key.
- The CLI should catch `MissingAPIKeyError` and show a friendly message: `No Congress.gov API key found. Run congress configure or set CONGRESS_API_KEY.`
- The CLI should exit with a non-zero status code when authentication configuration is missing.
- Error messages must not include secret values.

## Recommended Feature Roadmap

Build toward a clean SDK, CLI, and read-only MCP server.

Recommended order:

1. Stabilize SDK after refactor. If the src-based `congress_py` refactor is complete and tests pass, mark this as completed in `build/build_log.md` before starting the next feature.
2. Add CLI scaffolding for existing SDK methods only.
3. Add `get_bill_actions(congress, bill_type, number)`.
4. Add `get_bill_summaries(congress, bill_type, number)`.
5. Add a pagination helper.
6. Add `list_recent_bills(...)` with safe defaults.
7. Add CLI commands for each new endpoint as it is implemented.
8. Add a read-only MCP server with a small set of tools.
9. Add README demo instructions, CLI examples, and MCP configuration examples.
10. Add tests for SDK behavior, CLI behavior, and MCP tool behavior.

Initial MCP tools should be small and read-only:

- `get_bill`
- `get_bill_actions`
- `get_bill_summaries`
- `list_recent_bills`
- `get_member` only after member client support exists
- `list_committees` only after committee client support exists

Do not start with large, agentic workflows. Do not let tools write files, mutate external systems, open PRs, trigger deployments, or make legal/compliance recommendations.

## Codex / Agent Instructions

When using Codex or another coding agent:

- Make one coherent change at a time.
- Before coding, summarize the intended files and behavior changes.
- Do not add unrelated features during refactors.
- Preserve public behavior unless the task explicitly changes it.
- Update tests and docs when behavior changes.
- Run tests after changes when possible.
- If tests fail, report the failure and propose the smallest fix.
- Never commit secrets, `.env` files, API keys, local machine paths, or private notes.
- Before committing, run `git status`, summarize the diff, and confirm staged files are intentional.
- Do not push unless explicitly instructed.

For multi-step work, follow the execution plans in `build/` and the relevant lane-specific plan files.

### Build Planning Structure

Use `build/` as planning and context for Codex sessions, not runtime product code.

Recommended structure:

```text
build/
  build_log.md
  api/
    execution_plan.md
    01_stabilize_sdk.md
    02_add_bill_workflows.md
    03_add_pagination_and_recent_bills.md
  cli/
    execution_plan.md
    01_add_cli_scaffold.md
    02_add_cli_commands.md
    03_add_cli_tests.md
  mcp/
    execution_plan.md
    01_add_mcp_server.md
```

If existing build files are still in the root of `build/`, move them into the appropriate lane before starting new implementation work.

### Build Session Logging

Use `build/build_log.md` as the durable project memory for Codex-assisted work.

At the start of each new Codex session:

- Read `AGENTS.md`.
- Read `build/build_log.md` if it exists.
- Read the relevant execution plan under `build/api/`, `build/cli/`, or `build/mcp/`.
- Read the relevant session plan under the same lane.
- Summarize the current project state before making changes.
- Confirm which session or task is being worked on.

At the end of each meaningful Codex session, update `build/build_log.md` with:

- Date of the session.
- Session name or build phase.
- Goal of the session.
- Files changed.
- Behavioral changes made.
- Tests run and results.
- Any known issues, skipped work, or follow-up tasks.
- The recommended next session or next action.

The build log should be factual and concise. Do not use it as a scratchpad. It should help the next agent session quickly recover context without rereading the entire conversation.

If `build/build_log.md` does not exist, create it with this structure:

```md
# Build Log

This file captures completed Codex-assisted development sessions for the congress_py project. Each entry should summarize what changed, what was tested, and what should happen next.

## Sessions

### YYYY-MM-DD - Session Name

**Goal:**

**Files changed:**

**Changes made:**

**Tests run:**

**Known issues / follow-ups:**

**Next recommended action:**
```

## Build, Test, and Development Commands

Common commands:

- `python3 -m venv .venv`: create a local virtual environment.
- `.venv/bin/python -m pip install -r requirements.txt`: install pinned development dependencies when `requirements.txt` is used.
- `.venv/bin/python -m pip install -e .`: install the package in editable mode.
- `.venv/bin/python -m pytest`: run the full test suite.
- `.venv/bin/python scripts/fetch_congress_raw.py`: run the raw API debugging script. This requires `CONGRESS_API_KEY` unless the script explicitly documents another variable.

If the environment variable name is changed, update README, tests, examples, and this file together.

## Coding Style & Naming Conventions

Use standard Python style with 4-space indentation.

- Public methods and functions should use `snake_case`.
- Test names should describe behavior, such as `test_get_bills_returns_bill_models`.
- Prefer dataclasses for simple response objects.
- Prefer explicit names over clever abbreviations.
- Keep imports tidy.
- Avoid undefined names.
- Keep lines reasonably short.

No formatter is currently required unless one is added to the project. If `ruff`, `black`, `mypy`, or `flake8` is configured, follow the project configuration and update this file with the relevant commands.

## Testing Guidelines

Tests should be meaningful, behavior-focused, and cleanly separated by project layer. Do not add random tests only to increase coverage.

Use mocked HTTP for default unit tests. Avoid live network calls in normal test runs.

Test categories should be separated by file or directory when the project grows:

- Client tests: endpoint construction, query params, JSON parsing, pagination, and HTTP errors.
- Model tests: parsing optional/missing fields and stable serialization behavior.
- CLI tests: credential resolution, command behavior, output shape, friendly errors, and secret safety.
- MCP tests: tool input validation, tool output shape, error behavior, and secret safety.
- Integration tests: optional live API smoke tests gated behind an environment variable.

CLI authentication tests should cover:

- `--api-key` takes precedence.
- `CONGRESS_API_KEY` is used when no explicit key is provided.
- `~/.congress/config.toml` is used when no explicit key or env var is available.
- Missing credentials raise `MissingAPIKeyError`.
- The CLI converts `MissingAPIKeyError` into a friendly non-zero failure.
- The missing-key error message does not include secret values.
- `congress configure` creates the config file without printing the API key.
- If HTTP 401/403 handling is implemented, a rejected key maps to `InvalidAPIKeyError`.

See `tests/TESTS.md` for testing strategy.

## Commit & Pull Request Guidelines

Keep commits focused and use short, imperative summaries, for example:

- `Refactor project into congress_py package`
- `Add CLI scaffold`
- `Add bill actions client method`
- `Add read-only MCP bill tools`
- `Document testing strategy`

Pull requests should include:

- Concise description of the change.
- Test results.
- Any affected API endpoints or CLI commands.
- Fixture updates when API response shapes change.
- Notes about docs or README changes.

## Security, Legal, and Configuration Guidelines

This project is unofficial and must not imply affiliation with Congress.gov, the Library of Congress, Congress, or the U.S. government.

Do not commit:

- API keys.
- Secrets.
- `.env` files.
- Private prompts.
- Local-only configuration.
- `~/.congress/config.toml` or any copied local config file.
- Customer, client, account, or regulated data.

Use environment variables for SDK/API keys. Prefer documenting `CONGRESS_API_KEY`; keep compatibility with `CONGRESS_KEY` only if the code already supports it or the README documents it.

README and docs should include:

- Unofficial project disclaimer.
- User-owned API key requirement.
- Rate-limit note when applicable.
- No legal, legislative, lobbying, financial, or compliance advice disclaimer.
- Reminder to verify important information against official Congress.gov records.
- CLI credential resolution order.
- Clear statement that the SDK does not read `~/.congress/config.toml`; only the CLI does.

MCP tools should be read-only by default and should never expose API keys in returned output, errors, or logs.
