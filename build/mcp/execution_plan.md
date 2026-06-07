# MCP Execution Plan

## Overview

The SDK and CLI layers are stable and published to PyPI. MCP work is now active. MCP tools should remain read-only, thin wrappers around `CongressClient`, and should never duplicate API request logic.

## Current Session

- `build/mcp/04_add_mcp_server.md` — Add read-only MCP server with `congress mcp-start` CLI entry point and Dockerfile.

## Future Sessions

- **Session 05: LLM Summarization Layer** — Add optional summarization of bill summaries using an LLM. Keep the LLM dependency optional so the core SDK and MCP server remain lightweight.
- **Session 06: PyPI Release of MCP Extras** — Publish the MCP server as an optional installable extra or separate package. Update Homebrew tap and pipx documentation.
- **Session 07: Container Publishing** — Publish the Docker image to a container registry (e.g. Docker Hub or GitHub Container Registry). Add CI workflow for automated builds on release.

## Principles

- MCP tools are read-only.
- API keys are loaded from environment variables and never returned in output, logs, or errors.
- The MCP layer calls `CongressClient` and does not duplicate API request logic.
- Each session ends with a build log entry in `build/build_log.md`.

## Build Log Update

At the end of each MCP session, append an entry to `build/build_log.md` with the session number and title, goal, completed work, validation, next recommended actions, clarification questions and answers, and fixes made during the session.