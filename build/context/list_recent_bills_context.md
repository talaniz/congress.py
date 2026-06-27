# list_recent_bills Implementation Context

## Current State

- Current branch: `feature/list-recent-bills`
- The working tree was clean before implementation.
- `CongressClient` currently supports `get_bills(session=None, limit=20, offset=0)` and `iter_bills(session=None, limit=20, max_pages=None)`.
- `list_recent_bills` is referenced in planning docs and MCP plans but is not implemented yet.

## Relevant Project Guidance

- Make one coherent SDK change at a time.
- Keep API client methods thin, predictable, and testable.
- Do not duplicate API request logic outside `CongressClient`.
- Use mocked HTTP tests; default tests must not call the live Congress.gov API.
- Do not expose secrets or read CLI config from the SDK.
- Update docs and `build/build_log.md` when behavior changes.

## Locked Decisions

- This session is SDK-only.
- Public method signature: `CongressClient.list_recent_bills(limit: int = 10)`.
- Valid limit range: `1` through `250`.
- Invalid limits raise `ValueError("limit must be between 1 and 250")`.
- Implementation delegates to `get_bills(limit=limit, offset=0)`.
- CLI exposure is deferred.

## Intended Behavior

`list_recent_bills` returns a conservative first page of bill results from the existing bill-list endpoint. In this project context, "recent" means the first page returned by `/bill` with `offset=0`; no new Congress.gov endpoint or sort parameter is introduced.

## Intended Tests

- Default call sends `limit=10`, `offset=0`, and the API key.
- Custom limit sends that limit and `offset=0`.
- The method returns `list[Bill]` parsed from the existing bill response shape.
- `limit=0`, negative limits, and `limit=251` raise `ValueError`.
- Invalid limits do not make HTTP requests.

## Validation Command

```bash
.venv/bin/python -m pytest
```
