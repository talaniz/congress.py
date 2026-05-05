# Testing Strategy

## Purpose

Tests should verify meaningful behavior and protect the project from regressions. Do not add random tests only to improve coverage numbers. A smaller set of clear, behavior-focused tests is better than a large pile of brittle tests that do not describe what the project is supposed to do.

## Principles

- Test behavior, not implementation details.
- Keep default tests offline and deterministic.
- Mock Congress.gov HTTP responses in unit tests.
- Use fixtures that represent real API response shapes.
- Keep test names descriptive.
- Separate tests by project layer as the project grows.
- Add regression tests when fixing bugs.
- Avoid testing private helpers directly unless the helper has important behavior that cannot be reached through public APIs.

## Suggested Test Organization

As the project grows, organize tests by layer:

```text
tests/
  TESTS.md
  fixtures/
    bill_response.json
    bill_actions_response.json
    bill_summaries_response.json
  test_client.py
  test_models.py
  test_pagination.py
  test_mcp_server.py
  integration/
    test_live_smoke.py
```

This structure is a guideline, not a rule. Keep the layout simple while the project is small.

## Client Tests

Client tests should verify that `CongressClient` behaves correctly.

Examples:

- Builds the correct endpoint path.
- Sends API keys through query params, not string-concatenated URLs.
- Includes expected parameters such as `limit`, `offset`, or `format`.
- Uses mocked HTTP responses.
- Parses expected JSON into useful return values or models.
- Handles missing optional fields.
- Raises or surfaces HTTP errors predictably.
- Does not log or expose API keys.

## Model Tests

Model tests should focus on parsing and stable behavior.

Examples:

- Parses required fields from a bill response.
- Handles optional fields that are absent or null.
- Produces stable dictionaries or serializable values when needed by MCP tools.

Avoid modeling every field before the project needs it.

## MCP Tests

MCP tests should verify the tool layer without depending on live API calls.

Examples:

- Tool validates required inputs.
- Tool calls the correct client method.
- Tool returns JSON-compatible structured output.
- Tool errors are friendly.
- Tool errors do not expose API keys or secrets.
- Tools remain read-only.

If launching the full MCP server is awkward in tests, isolate tool functions so they can be tested directly.

## Integration Tests

Live API tests should be optional and skipped by default.

Use integration tests only to verify that the project still works against the real Congress.gov API. These tests should require explicit opt-in, such as:

```bash
CONGRESS_API_KEY=... RUN_LIVE_TESTS=1 .venv/bin/python -m pytest tests/integration
```

Integration tests should be small, rate-limit aware, and not required for normal local development or CI.

## Coverage Guidance

Coverage is useful as a signal, not a scoreboard. If coverage is configured, do not write meaningless tests just to satisfy a number. Prefer improving coverage by testing important behavior:

- Error paths.
- Pagination.
- Optional fields.
- API-key handling.
- Tool validation.
- Regression scenarios.

## Test Review Checklist

Before committing test changes, check:

- Does this test describe a real behavior we care about?
- Would this test fail if the behavior broke?
- Is the test deterministic?
- Does it avoid live network access by default?
- Is the fixture small enough to understand?
- Does the test avoid secrets and local machine assumptions?
