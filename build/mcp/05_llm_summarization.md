# Session 05: LLM Summarization Layer

## Objective

Add optional LLM-powered summarization of bill summaries using the OpenAI API. Summarization should be available as a CLI command and as an MCP tool. The LLM dependency must be optional so the core SDK, CLI, and MCP server remain lightweight for users who do not need it.

## Scope

- Add a `congress bills summarize` CLI command that fetches bill summaries and returns a plain-language summary via the OpenAI API.
- Add a `summarize_bill` MCP tool that wraps the same logic.
- Add `openai` as an optional dependency group in `pyproject.toml` (e.g. `pip install congress-py[llm]`).
- Raise a clear, friendly error if the user runs a summarization command without the `llm` extra installed.
- API keys for both Congress.gov and OpenAI should be loaded from environment variables and never returned in output, logs, or errors.

## Files Likely to Change

- `src/congress_py/summarizer.py` — new file containing summarization logic
- `src/congress_py/cli.py` — add `bills summarize` command
- `src/congress_py/mcp_server.py` — add `summarize_bill` tool
- `tests/test_summarizer.py` — new test file
- `pyproject.toml` — add `llm` optional dependency group
- `docs/summarization.md` — new documentation page
- `mkdocs.yml` — add `summarization.md` to nav
- `docs/changelog.md` — update Unreleased section

## CLI Command

```bash
congress bills summarize 118 hr 7437
```

The command should:
1. Fetch bill summaries using `CongressClient.get_bill_summaries`.
2. Pass the summary text to the OpenAI API with a prompt asking for a plain-language summary.
3. Print the result to stdout.

The OpenAI model should default to `gpt-4o-mini` but be overridable via `--model`.

## Environment Variables

- `CONGRESS_API_KEY` — Congress.gov API key (existing)
- `OPENAI_API_KEY` — OpenAI API key (new)

## Acceptance Criteria

- `congress bills summarize` returns a plain-language summary for a given bill.
- `summarize_bill` MCP tool returns a plain-language summary.
- The `openai` package is not imported unless the `llm` extra is installed.
- A friendly error is raised if `OPENAI_API_KEY` is not set.
- A friendly error is raised if the `llm` extra is not installed.
- Tests mock the OpenAI API and cover happy path, missing API key, and missing dependency cases.
- `.venv/bin/python -m pytest` passes.

## Suggested Codex Prompt

```text
Add optional LLM summarization to the congress-py SDK and CLI.

Requirements:
- Add a `congress bills summarize <congress> <bill_type> <number>` CLI command.
- Add a `summarize_bill` MCP tool.
- Use the OpenAI API with gpt-4o-mini as the default model, overridable via --model.
- Add openai as an optional dependency group: pip install congress-py[llm].
- Raise a clear error if openai is not installed or OPENAI_API_KEY is not set.
- Add a docs/summarization.md documentation page.
- Update mkdocs.yml and docs/changelog.md.
- Mock the OpenAI API in tests.
```

## Test Expectations

Run:

```bash
.venv/bin/python -m pytest
```

Mock the OpenAI client in tests. Do not make live API calls.

## Commit Guidance

Suggested commit message:

```text
Add optional LLM summarization via OpenAI API
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