# Repository Guidelines

## Project Structure & Module Organization

This repository is a small Python SDK for the official Congress API.

- `src/congress_py/`: source package. `client.py` contains `CongressClient`, and `models.py` contains the `Bill` data model.
- `tests/`: unit tests and static mocked API responses, including `tests/test_congress.py`, `tests/congress_responses.txt`, and `tests/bill_responses.txt`.
- `scripts/`: ad hoc development scripts for raw API checks.
- `pyproject.toml`: package metadata and build configuration.
- `requirements.txt`: pinned development/test dependencies.

## Build, Test, and Development Commands

- `python3 -m venv .venv`: create a local virtual environment.
- `.venv/bin/python -m pip install -r requirements.txt`: install pinned development dependencies.
- `.venv/bin/python -m pip install -e .`: install the package in editable mode.
- `.venv/bin/python -m pytest`: run the full test suite.
- `.venv/bin/python scripts/fetch_congress_raw.py`: run the raw API debugging script. This requires `CONGRESS_KEY`.

## Coding Style & Naming Conventions

Use standard Python style with 4-space indentation. Prefer clear module-level functions, class methods, and dataclasses where they match the existing design. Keep public API methods snake_case, for example `get_current_session()` and `get_bills()`. Test methods should describe behavior, such as `test_get_bills_returns_list`.

No formatter is currently configured. The GitHub workflow runs `flake8`, so keep imports tidy, avoid undefined names, and keep lines reasonably short.

## Testing Guidelines

Tests use `unittest` with `pytest` as the runner and `requests-mock` for HTTP isolation. Keep network calls mocked in unit tests; add or update fixture response files under `tests/` when API response shapes change.

Coverage is configured in `pytest.ini` with branch coverage enabled for `src/congress_py` and `fail_under = 80`. Run `.venv/bin/python -m pytest` before opening a pull request.

## Commit & Pull Request Guidelines

Recent commit history uses short, imperative summaries such as `Refactor bill fetch logic to Bill class` and `fix bullet points`. Keep commits focused and describe the behavioral change.

Pull requests should include a concise description, test results, and any relevant issue links. For API behavior changes, mention affected endpoints and include mocked response updates when applicable. Screenshots are not needed for this backend-only package.

## Security & Configuration Tips

Do not commit API keys or raw secrets. Local API access should use `CONGRESS_KEY`, for example `export CONGRESS_KEY=your_api_key_here`. Keep generated files such as `.venv/`, coverage output, build artifacts, and `*.egg-info/` out of version control.
