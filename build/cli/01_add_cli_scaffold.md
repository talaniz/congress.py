# Session CLI 01: Add CLI Scaffold

## Objective

Add the initial CLI structure without implementing new API capabilities.

## Scope

- Add a CLI entry point that can be installed with the package.
- Wire the CLI to existing `CongressClient` methods only.
- Add a minimal command such as showing help or fetching an already-supported bill workflow if appropriate.
- Add tests for argument parsing and client wiring with mocks.
- Add functional CLI output tests with `Typer` `CliRunner`.
- Update README only for commands that actually exist.

## Files Likely to Change

- `src/congress_py/cli.py`
- `pyproject.toml`
- `tests/test_cli.py`
- `README.md`

## Acceptance Criteria

- Product behavior remains read-only.
- CLI imports from `congress_py` rather than duplicating SDK logic.
- Default tests do not require a live API key.
- No new API endpoints are added.
- CLI errors do not expose API keys.
- At least one successful CLI command exits with status code 0 and emits valid JSON with expected fields from a mocked SDK response.

## Suggested Codex Prompt

```text
Add a minimal CLI scaffold for congress_py.

Requirements:
- Do not add new API endpoints.
- Keep the CLI as a thin wrapper around CongressClient.
- Add package entry point metadata.
- Add mocked tests for argument parsing and client construction.
- Add functional output tests that parse JSON from at least one successful command.
- Update README only with implemented commands.
- Run pytest and report any failures.
```

## Test Expectations

Run:

```bash
.venv/bin/python -m pytest
```

CLI tests should use mocks and should not call the live Congress API. They should verify user-visible behavior, including exit codes, friendly error messages, and JSON output shape.

## Commit Guidance

Suggested commit message:

```text
Add CLI scaffold
```

## Build Log Update

At the end of this session, append an entry to `build/build_log.md` that includes:

- Session number and title.
- Goal.
- Completed work.
- Validation, including test commands and results.
- Next recommended actions.
- Any questions asked for clarification.
- The clarifying answers received.
- Fixes made during the session, especially fixes made after test failures or review feedback.
