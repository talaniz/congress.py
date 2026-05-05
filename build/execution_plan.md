# Execution Plan

## Overview

This plan turns the project into a clean, portfolio-ready Congress.gov Python SDK with a small read-only MCP server. The project should demonstrate disciplined AI-assisted development: clear repo instructions, incremental implementation, meaningful tests, safe API-key handling, and documentation that explains tradeoffs.

The goal is not to cover the entire Congress.gov API. The goal is to build a credible, well-scoped reference implementation that can be shown in an OpenAI Codex Deployment Engineer interview.

## Outcomes

By the end of this plan, the repository should have:

- A clean `src/congress_py/` package.
- A stable `CongressClient` with predictable endpoint construction.
- Typed models for the core bill workflow.
- Meaningful unit tests using mocked API responses.
- A small read-only MCP server that exposes selected Congress.gov workflows.
- README examples for SDK and MCP usage.
- Security and unofficial-project disclaimers.
- A documented testing strategy.
- A clear record of Codex-assisted development decisions.

## Guiding Principles

- Make one coherent change at a time.
- Keep tests passing after each session.
- Prefer narrow, useful workflows over broad endpoint coverage.
- Keep API access in the client layer.
- Keep MCP tools read-only and thin.
- Do not log or expose API keys.
- Avoid legal, lobbying, compliance, or financial advice claims.
- Use Codex to accelerate work, but review and test generated code before committing.

## Session Files

Work should be split across focused sessions:

1. `01_stabilize_sdk.md`
2. `02_add_bill_workflows.md`
3. `03_add_pagination_and_recent_bills.md`
4. `04_add_mcp_server.md`
5. `05_update_docs_and_examples.md`
6. `06_expand_tests_and_quality.md`

Each session should include:

- Objective.
- Scope.
- Files likely to change.
- Acceptance criteria.
- Suggested Codex prompt.
- Test expectations.
- Commit guidance.

## Proposed Milestones

### Milestone 1: Stable SDK

The SDK has a clean package layout, predictable request handling, and tests for current behavior.

### Milestone 2: Useful Bill Workflow

The SDK can fetch bill details, actions, summaries, and text versions where supported.

### Milestone 3: Safe Discovery

The SDK supports pagination and recent bill listing with safe defaults.

### Milestone 4: Read-only MCP Server

The project exposes a small set of MCP tools backed by the SDK.

### Milestone 5: Portfolio-Ready Documentation

The README and examples explain setup, usage, MCP configuration, testing, safety boundaries, and AI-assisted development notes.

## Definition of Done

The project is considered ready for interview demonstration when:

- Default tests pass without a live API key.
- Live API smoke tests are optional and clearly gated.
- The README has a working quickstart.
- `AGENTS.md` explains project conventions and safety rules.
- MCP tools are read-only and documented.
- No secrets or local-only files are tracked.
- The project can be explained in 2 minutes as an example of safe Codex-assisted development.
