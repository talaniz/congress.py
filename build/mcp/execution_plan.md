# MCP Execution Plan
 
## Overview
 
The SDK and CLI layers are stable and published to PyPI. MCP work is now active. MCP tools should remain read-only, thin wrappers around `CongressClient`, and should never duplicate API request logic.
 
## Current Status

- **Session 04: MCP Server** (`build/mcp/04_add_mcp_server.md`) — Complete.
- **Session 06: PyPI MCP Extras** (`build/mcp/06_pypi_mcp_extras.md`) — Complete. Version `0.2.0` is published to PyPI with the `mcp` optional extra.

## Next Recommended Session

- **Session 05: LLM Summarization Layer** (`build/mcp/05_llm_summarization.md`) — Add optional summarization of bill summaries using the OpenAI API. Expose as a `congress bills summarize` CLI command and a `summarize_bill` MCP tool. Keep the `openai` dependency optional via `pip install congress-py[llm]`.

## Future Sessions
 
- **Session 07: Container Publishing** (`build/mcp/07_container_publishing.md`) — Add a GitHub Actions workflow to build and push the Docker image to `ghcr.io/talaniz/congress-py` on release tags. Update documentation with public pull and run instructions including a Claude Desktop config example.
## Recommended Session Order
 
04 → 06 → 05 → 07
 
Complete the MCP server and verify the install path before adding the LLM layer. Publish the container last once all features are stable.
 
## Principles
 
- MCP tools are read-only.
- API keys are loaded from environment variables and never returned in output, logs, or errors.
- The MCP layer calls `CongressClient` and does not duplicate API request logic.
- Each session ends with a build log entry in `build/build_log.md`.
## Build Log Update
 
At the end of each MCP session, append an entry to `build/build_log.md` with the session number and title, goal, completed work, validation, next recommended actions, clarification questions and answers, and fixes made during the session.
