# Session 06: Expand Tests and Quality

## Objective

Strengthen project confidence with meaningful tests and lightweight quality checks.

## Scope

- Organize tests by layer.
- Add meaningful behavior-focused tests.
- Add optional live API smoke tests gated behind an environment variable.
- Add lint/type tooling only if it helps and remains lightweight.
- Update `tests/TESTS.md` if strategy changes.

## Files Likely to Change

- `tests/`
- `tests/TESTS.md`
- `pyproject.toml`
- `requirements.txt`
- `README.md`

## Acceptance Criteria

- Tests are cleanly separated by behavior or project layer.
- Default test run does not require a live API key.
- Tests avoid random coverage-padding.
- Optional live tests are clearly marked and skipped by default.
- Any new quality tools are documented.

## Suggested Codex Prompt

```text
Improve the test suite for meaningful behavior coverage.

Goals:
- Separate tests by project layer where useful: client, models, MCP tools, integration smoke tests.
- Add tests for error handling, pagination, missing optional fields, and secret safety.
- Do not add random tests only to increase coverage.
- Default tests must not call the live API.
- Optional live API smoke tests must be skipped unless an environment variable is set.
- Update tests/TESTS.md and README if commands change.
```

## Test Expectations

Run:

```bash
.venv/bin/python -m pytest
```

Optional live smoke tests should require explicit opt-in, for example:

```bash
CONGRESS_API_KEY=... RUN_LIVE_TESTS=1 .venv/bin/python -m pytest tests/integration
```

## Commit Guidance

Suggested commit message:

```text
Expand behavior-focused test coverage
```
