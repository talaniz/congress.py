# Session 01: Stabilize SDK

## Objective

Refactor the project into a clean SDK shape that is easy to test, document, and expose through MCP later.

## Scope

- Confirm the package layout uses `src/congress_py/`.
- Move or keep HTTP access in `src/congress_py/client.py`.
- Move data models into `src/congress_py/models.py`.
- Remove old `congress/` package imports unless backward compatibility is explicitly required.
- Update tests and docs to import from `congress_py`.
- Keep behavior equivalent where possible.

## Files Likely to Change

- `src/congress_py/client.py`
- `src/congress_py/models.py`
- `src/congress_py/__init__.py`
- `tests/test_congress.py`
- `README.md`
- `pyproject.toml`

## Acceptance Criteria

- The package imports cleanly as `congress_py`.
- `CongressClient` owns API calls and endpoint construction.
- Models do not perform network calls.
- Existing tests pass.
- README import examples use `congress_py`.
- No compatibility shim remains unless explicitly required.

## Suggested Codex Prompt

```text
Refactor this project into a clean src-based Python package named congress_py.

Goals:
- Ensure CongressClient lives in src/congress_py/client.py.
- Ensure data models live in src/congress_py/models.py.
- Update imports, tests, and README examples to use congress_py.
- Remove the old congress/ package entirely unless it is still required by tests.
- Keep behavior equivalent where possible.
- Do not add new features in this session.
- Run pytest and report any failures with the smallest proposed fix.
```

## Test Expectations

Run:

```bash
.venv/bin/python -m pytest
```

Default tests should use mocked API responses and should not require a live API key.

## Commit Guidance

Suggested commit message:

```text
Refactor project into congress_py package
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
