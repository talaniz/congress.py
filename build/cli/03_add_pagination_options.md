# 03 Add Pagination Options to CLI

## Goal

Expose the SDK bill pagination functionality through the CLI.

The SDK already supports paginated bill retrieval through:

- `client.get_bills(session=None, limit=20, offset=0)`
- `client.iter_bills(session=None, limit=20, max_pages=None)`

The CLI should now allow users to control pagination when listing bills.

## Current State

The CLI already includes bill workflow commands, including single bill lookup and related bill workflow functionality.

This task should not duplicate existing commands. It should only update the existing bill listing command to support pagination options.

## Required CLI Changes

Update the existing bill listing command to support:

- `--limit`, default `20`
- `--offset`, default `0`
- `--pages`, optional integer

## Expected Behavior

### Single-page Mode

If `--pages` is not provided:

- Call `client.get_bills(...)`
- Pass `limit`
- Pass `offset`
- Preserve existing `session` behavior if supported by the current CLI

Examples:

```bash
congress bills --limit 50
congress bills --limit 25 --offset 100
```

### Multi-page Mode

If `--pages` is provided:

- Call `client.iter_bills(...)`
- Pass `limit`
- Pass `max_pages=pages`
- Ignore `offset` in this mode unless the SDK already supports offset-based iteration

Example:

```bash
congress bills --limit 25 --pages 3
```

## Output

Preserve existing CLI output formatting where possible.

The goal is to expose pagination behavior without changing the user-facing display unnecessarily.

## Help Text

Update CLI help text so users can discover the new options.

The help text should make clear that:

- `--limit` controls the number of bills requested per API call
- `--offset` controls the starting offset for single-page bill listing
- `--pages` enables multi-page iteration using the SDK iterator

## Tests

Add or update CLI tests for:

- Default bill listing
- Custom `--limit`
- Custom `--offset`
- Combined `--limit` and `--offset`
- Multi-page listing with `--pages`
- Existing bill workflow commands still work

## Constraints

- Do not duplicate existing commands.
- Do not change unrelated SDK behavior.
- Do not add new dependencies unless absolutely necessary.
- Preserve existing CLI output formatting where possible.
- Keep the implementation small and readable.

## Acceptance Criteria

- Existing CLI commands continue to work.
- The bill listing command supports `--limit`, `--offset`, and `--pages`.
- `--limit` and `--offset` call `client.get_bills(...)`.
- `--pages` calls `client.iter_bills(...)`.
- CLI help text includes the new pagination options.
- Tests cover the new behavior.
- All tests pass.
- No unrelated SDK behavior is changed.
- No new dependencies are introduced.
