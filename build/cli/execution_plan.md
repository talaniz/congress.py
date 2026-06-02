# CLI Execution Plan

## Overview

This plan adds a small command-line interface for the existing `congress_py` SDK. The CLI is a thin layer over `CongressClient`; it does not duplicate endpoint construction, response parsing, or model logic. Each session builds incrementally on the previous one, exposing SDK capabilities that are already implemented and tested.

## Goals

- Provide a portfolio-friendly way to demonstrate SDK workflows from the terminal.
- Keep CLI commands read-only and as a thin wrapper around `CongressClient`.
- Load the Congress API key from environment variables or explicit options.
- Return useful output (valid JSON from mocked SDK responses) without exposing secrets.
- Keep tests mocked by default; no live API calls in the default test suite.
- Expose existing SDK pagination capabilities through CLI options.
- Use `Typer` with `CliRunner` for functional CLI output tests.

## Non-Goals

- Do not add new API endpoints during CLI work.
- Do not implement MCP behavior here.
- Do not add commands for SDK methods that are not yet implemented and tested.
- Do not add a bill text versions command (that SDK endpoint was deferred).
- Do not duplicate existing CLI commands when extending behavior.
- Do not change unrelated SDK behavior.
- Do not add new dependencies unless absolutely necessary.

## Sessions

### 01 — Add CLI Scaffold (`01_add_cli_scaffold.md`)

Establish the initial CLI structure without implementing new API capabilities.

- Add a CLI entry point installable with the package (update `pyproject.toml`).
- Wire the CLI to existing `CongressClient` methods only.
- Add a minimal command (help, or an already-supported workflow if appropriate).
- Add mocked tests for argument parsing and client construction.
- Add functional CLI output tests with `Typer` `CliRunner`.
- Update README only for implemented commands.

**Files likely to change:** `src/congress_py/cli.py`, `pyproject.toml`, `tests/test_cli.py`, `README.md`.

### 02 — Add Bill Workflow Commands (`02_add_bill_workflow_commands.md`)

Expose the completed bill workflow SDK methods through the CLI.

- Add a bill details command calling `CongressClient.get_bill(congress, bill_type, number)`.
- Add a bill actions command calling `CongressClient.get_bill_actions(congress, bill_type, number)`.
- Add a bill summaries command calling `CongressClient.get_bill_summaries(congress, bill_type, number)`.
- Defer the bill text versions command (SDK endpoint deferred).
- Do not implement pagination in this session.
- Each new command must exit with status `0` and emit valid JSON from a mocked response.
- Tests verify the CLI calls the expected `CongressClient` method with the expected arguments.

**Files likely to change:** `src/congress_py/cli.py`, `tests/test_cli.py`, `README.md`, `build/build_log.md`.

### 03 — Add Pagination Options (`03_add_pagination_options.md`)

Extend the existing bill listing command with pagination options that map to the SDK's existing pagination methods. This session updates an existing command rather than adding a new one.

- `--limit` (default `20`): forwarded to `client.get_bills(...)` or `client.iter_bills(...)`.
- `--offset` (default `0`): forwarded to `client.get_bills(...)` in single-page mode.
- `--pages` (optional int): switches to multi-page mode via `client.iter_bills(..., max_pages=pages)`.
- Single-page mode (no `--pages`) calls `client.get_bills(...)` and preserves any existing `session` behavior.
- Multi-page mode (`--pages` provided) calls `client.iter_bills(...)` and ignores `--offset` unless the SDK supports offset-based iteration.
- Preserve existing CLI output formatting.
- Update CLI help text so users can discover the new options.

**Files likely to change:** `src/congress_py/cli.py`, `tests/test_cli.py`, `README.md`, `build/build_log.md`.

Future CLI sessions can add commands only after the SDK methods they call are implemented and tested.

## Shared Acceptance Criteria

These apply to every session:

- Product behavior remains read-only.
- CLI imports from and delegates to `CongressClient` rather than duplicating endpoint construction, response parsing, or model logic.
- Default tests do not require a live API key.
- CLI errors do not expose API keys.
- Successful CLI commands exit with status code `0` and emit valid JSON from mocked SDK responses.
- Tests verify that the CLI calls the expected `CongressClient` method with the expected arguments.
- README usage examples match implemented command names and arguments.
- No new API endpoints are added.
- No new dependencies are introduced unless absolutely necessary.
- `build/build_log.md` is updated at the end of each session.

## Session-Specific Test Coverage

**Session 01:**
- Argument parsing and client construction (mocked).
- At least one successful command exits `0` and emits valid JSON.

**Session 02:**
- Bill details: calls `get_bill(congress, bill_type, number)`, exits `0`, emits valid JSON.
- Bill actions: calls `get_bill_actions(...)`, exits `0`, emits valid JSON.
- Bill summaries: calls `get_bill_summaries(...)`, exits `0`, emits valid JSON.
- Missing required arguments produces a non-zero exit code.
- API keys are not exposed in error output.

**Session 03:**
- Default bill listing.
- Custom `--limit`.
- Custom `--offset`.
- Combined `--limit` and `--offset`.
- Multi-page listing with `--pages`.
- Existing bill workflow commands from Session 02 still work.

## Test Command

```bash
.venv/bin/python -m pytest
```

CLI tests use mocks and do not call the live Congress API. They verify user-visible behavior: exit codes, friendly error messages, and JSON output shape.

## Definition of Done

- The CLI imports cleanly from the installed package.
- All sessions' acceptance criteria are met.
- CLI behavior is covered by mocked tests, including pagination cases.
- CLI help text documents all options, including `--limit`, `--offset`, and `--pages`.
- README usage stays aligned with implemented commands.
- `build/build_log.md` contains an entry for each completed session.