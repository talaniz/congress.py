# CLI Execution Plan

## Overview

This plan adds a small command-line interface for the existing `congress_py` SDK. The CLI should be a thin layer over `CongressClient`; it should not duplicate endpoint construction, response parsing, or model logic.

## Goals

- Provide a portfolio-friendly way to demonstrate SDK workflows from the terminal.
- Keep CLI commands read-only.
- Load the Congress API key from environment variables or explicit options.
- Return useful output without exposing secrets.
- Keep tests mocked by default.

## Non-Goals

- Do not add new API endpoints during CLI scaffold work.
- Do not implement MCP behavior here.
- Do not add broad command coverage before the SDK workflow is tested.

## Proposed Sessions

1. `01_add_cli_scaffold.md`

Future CLI sessions can add commands only after the SDK methods they call are implemented and tested.

## Definition of Done

- The CLI imports cleanly from the installed package.
- CLI behavior is covered by tests.
- README usage stays aligned with implemented commands.
- `build/build_log.md` is updated at the end of each CLI session.
