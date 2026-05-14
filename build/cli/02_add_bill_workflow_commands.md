# Session CLI 02: Add Bill Workflow Commands

## Objective

Expose the completed bill workflow SDK methods through the CLI without adding new API capabilities.

## Scope

- Add CLI commands for bill workflows that already exist and are tested in `CongressClient`.
- Keep the CLI as a thin wrapper around SDK methods.
- Add commands for:
  - bill details
  - bill actions
  - bill summaries
- Do not add a command for bill text versions in this session because that SDK endpoint was deferred.
- Add functional CLI output tests with `Typer` `CliRunner`.
- Use mocked client responses by default.
- Update README only for commands that actually exist.

## Files Likely to Change

- `src/congress_py/cli.py`
- `tests/test_cli.py`
- `README.md`
- `build/build_log.md`

## Acceptance Criteria

- Product behavior remains read-only.
- CLI imports from and delegates to `CongressClient` rather than duplicating endpoint construction or response parsing.
- Commands exist only for SDK methods already implemented and tested.
- No new API endpoints are added.
- No pagination behavior is implemented in this session.
- No bill text versions command is added in this session.
- Default tests do not require a live API key.
- CLI errors do not expose API keys.
- Each new successful CLI command exits with status code 0.
- Each new successful CLI command emits valid JSON from a mocked SDK response.
- Tests verify that the CLI calls the expected `CongressClient` method with the expected arguments.
- README usage examples match the implemented command names and arguments.

## Suggested Codex Prompt

```text
Add CLI commands for the completed bill workflow SDK methods.

Before making changes:
- Read AGENTS.md if present.
- Read README.md.
- Read build/build_log.md.
- Read the CLI execution plan.
- Read tests/TESTS.md if present.
- Inspect src/congress_py/cli.py.
- Inspect existing CLI tests.
- Confirm which bill workflow methods already exist on CongressClient.

Requirements:
- Keep the CLI as a thin wrapper around CongressClient.
- Add commands only for SDK methods that already exist and are tested.
- Add commands for bill details, bill actions, and bill summaries.
- Do not add a bill text versions command because that SDK endpoint was deferred.
- Do not add new API endpoints.
- Do not implement pagination.
- Do not duplicate endpoint construction, response parsing, or model logic in the CLI.
- Preserve existing CLI behavior and tests.
- Use mocked client responses in CLI tests.
- Add functional CLI output tests with Typer CliRunner.
- Verify each command exits with status code 0 and emits valid JSON for mocked successful responses.
- Verify each command calls the expected CongressClient method with the expected arguments.
- Update README only with commands that actually exist.
- Update build/build_log.md at the end of the session.

Proposed commands:
- A command for bill details that calls CongressClient.get_bill(congress, bill_type, number)
- A command for bill actions that calls CongressClient.get_bill_actions(congress, bill_type, number)
- A command for bill summaries that calls CongressClient.get_bill_summaries(congress, bill_type, number)

Before coding:
- Propose the exact command names and argument structure based on the current CLI style.
- Define acceptance criteria specific to this repo and session.
- Propose the exact tests to add or update.
- Ask any clarifying questions.
- Stop before editing files unless explicitly approved.
```

## Test Expectations

Run:

```bash
.venv/bin/python -m pytest
```

CLI tests should use mocks and should not call the live Congress API. They should verify user-visible behavior, including exit codes, friendly error messages, and JSON output shape.

Suggested CLI test coverage:

- Bill details command:
  - calls `CongressClient.get_bill` with `congress`, `bill_type`, and `number`
  - exits with status code 0
  - emits valid JSON with expected mocked fields

- Bill actions command:
  - calls `CongressClient.get_bill_actions` with `congress`, `bill_type`, and `number`
  - exits with status code 0
  - emits valid JSON with expected mocked action data

- Bill summaries command:
  - calls `CongressClient.get_bill_summaries` with `congress`, `bill_type`, and `number`
  - exits with status code 0
  - emits valid JSON with expected mocked summary data

- Error behavior:
  - missing required arguments produces a non-zero exit code
  - API keys are not exposed in error output

## Commit Guidance

Suggested commit message:

```text
Add CLI bill workflow commands
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
- Any intentionally deferred work, including the bill text versions command.
