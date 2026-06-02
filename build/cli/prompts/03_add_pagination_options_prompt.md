Add pagination options to the existing bill listing CLI command for congress_py.

This is a Codex-assisted session. Follow AGENTS.md and the build planning workflow.

Branch:
- All work for this session must be done on the branch `features/pagination-cli`.
- Before doing anything, ensure you are on that branch:
    - If the branch does not exist, create it from the current default branch: `git checkout -b features/pagination-cli`.
    - If it already exists, check it out: `git checkout features/pagination-cli`.
- Confirm the active branch with `git status` or `git branch --show-current` before proceeding.
- Do not commit to main or any other branch during this session.
- Do not push unless explicitly instructed (per AGENTS.md).

Before making any changes, read in this order:
- AGENTS.md — repo-wide conventions, CLI rules, exception hierarchy, testing rules.
- build/build_log.md — durable project memory; prior session outcomes and deferred work.
- build/cli/execution_plan.md — the CLI lane's execution plan.
- build/cli/03_add_pagination_options.md — this session's plan and acceptance criteria.
- tests/TESTS.md (if present) — testing strategy.
- README.md — current documented CLI surface and disclaimers.
- src/congress_py/cli.py — current CLI structure, the existing bill listing command, option style, and Typer usage.
- src/congress_py/client.py — confirm signatures of:
    - client.get_bills(session=None, limit=20, offset=0)
    - client.iter_bills(session=None, limit=20, max_pages=None)
  and confirm whether iter_bills supports an offset parameter.
- src/congress_py/exceptions.py — confirm MissingAPIKeyError and CongressAuthError are wired correctly for the existing command.
- tests/test_cli.py — existing Typer CliRunner patterns, mocking style, and credential-resolution test patterns.

Summarize the current project state before making any changes. Confirm explicitly that this session is build/cli/03_add_pagination_options.md.

Scope of changes:
- Update the existing bill listing command (`congress bills list ...`). Do not add a new command.
- Add three options to that command:
    --limit (default 20)
    --offset (default 0)
    --pages (optional int)
- Single-page mode (no --pages): call client.get_bills(limit=..., offset=..., session=... if already supported by the existing command).
- Multi-page mode (--pages provided): call client.iter_bills(limit=..., max_pages=pages, session=... if already supported). Ignore --offset in this mode unless iter_bills already accepts offset.
- Preserve existing CLI output formatting. Output stays JSON and stable enough to test (per AGENTS.md). Do not introduce rich/table formatting.
- Update CLI help text so users discover the new options and understand:
    --limit controls bills per API call
    --offset controls starting offset for single-page mode
    --pages enables multi-page iteration via the SDK iterator

Constraints (from AGENTS.md and the session plan):
- Keep the CLI a thin wrapper around CongressClient. Do not duplicate HTTP, endpoint construction, query-param building, or response parsing in the CLI.
- The CLI must call CongressClient; the client remains the source of truth.
- Do not add new Congress.gov endpoints.
- Do not duplicate existing commands.
- Do not change unrelated SDK behavior.
- Do not add new dependencies.
- Do not expose API keys in errors, logs, or output.
- Preserve the credential resolution order: --api-key, then CONGRESS_API_KEY, then ~/.congress/config.toml, otherwise MissingAPIKeyError.
- Default tests must not require a live API key — use mocks.
- Preserve all existing bill workflow commands and their tests.
- Make one coherent change at a time. Do not add unrelated features.

Tests to add or update in tests/test_cli.py (Typer CliRunner + mocked CongressClient):
- Default bill listing calls client.get_bills with limit=20, offset=0.
- Custom --limit calls client.get_bills with that limit and offset=0.
- Custom --offset calls client.get_bills with limit=20 and that offset.
- Combined --limit and --offset forwards both correctly to client.get_bills.
- --pages routes to client.iter_bills with the correct limit and max_pages, and does not call client.get_bills.
- Each successful command exits with status code 0 and emits valid JSON from the mocked response.
- Existing bill workflow commands (bill details, bill actions, bill summaries) continue to pass.
- Credential-resolution tests for the bill listing command still pass; missing-key behavior still maps to MissingAPIKeyError with a friendly non-zero exit and no secret values in the message.
- Use test names that describe behavior, e.g. test_bills_list_default_calls_get_bills_with_defaults, test_bills_list_pages_uses_iter_bills.

Documentation updates:
- Update README.md to document --limit, --offset, and --pages on the bill listing command, with at least one single-page example and one multi-page example. Only document behavior that is actually implemented.
- Preserve existing README disclaimers (unofficial project, user-owned API key, no legal/legislative/financial advice, CLI credential resolution order, the note that the SDK does not read ~/.congress/config.toml).

Build log update (per AGENTS.md):
- At the end of the session, append an entry to build/build_log.md with:
    - Date of the session.
    - Session name: "CLI 03 - Add Pagination Options".
    - Goal.
    - Files changed.
    - Behavioral changes made.
    - Tests run and results (include the exact pytest command).
    - Any known issues, skipped work, or follow-up tasks (e.g., offset support inside iter_bills if the SDK does not currently support it).
    - Recommended next session or next action.
- Keep the entry factual and concise. Do not use it as a scratchpad.

Process requirements:
- Before editing any files, after completing the branch setup and file reads above, summarize:
    1. The exact signature observed for client.get_bills and client.iter_bills, including whether iter_bills accepts offset.
    2. The current bill listing command name (expected: `congress bills list`), its existing options, and whether it currently forwards --session or --api-key.
    3. The exact option names and Typer help strings to add.
    4. The exact tests to add or modify, by name.
    5. The README section to update, with the proposed example commands.
- Ask any clarifying questions, especially:
    - How --pages combined with --offset should behave (silently ignore, warn, or error). The session plan says "ignore" — confirm that's still the intent.
    - Whether to validate --limit and --pages as positive integers and how to surface validation errors (Typer's built-in validation vs. a custom check).
    - Whether the existing command already accepts --session and, if so, how it should interact with the new flags.
- Stop before editing files until the plan and clarifying answers are explicitly approved.

Validation:
- Run: .venv/bin/python -m pytest
- Report any failures and fix them with the smallest possible change before completing the session.

Commit guidance (per AGENTS.md commit style):
- Confirm the active branch is `features/pagination-cli` before staging or committing.
- Suggested commit message: `Add CLI pagination options to bill listing command`
- Before committing, run `git status`, summarize the diff, and confirm staged files are intentional.
- Do not push unless explicitly instructed.
- Do not commit secrets, .env files, ~/.congress/config.toml, or local paths.
