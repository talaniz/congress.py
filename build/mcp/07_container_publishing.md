# Session 07: Container Publishing

## Objective

Publish the congress-py Docker image to GitHub Container Registry (ghcr.io) and automate future builds via GitHub Actions. Users should be able to pull and run the MCP server with a single `docker run` command without building locally.

## Scope

- Add a GitHub Actions workflow that builds and pushes the Docker image to `ghcr.io/talaniz/congress-py` on every release tag.
- Tag images with both the release version and `latest`.
- Update documentation with the public pull and run instructions.
- Verify the published image runs correctly with `congress mcp-start` as the entry point.

## Files Likely to Change

- `.github/workflows/publish-docker.yml` — new GitHub Actions workflow
- `docs/mcp.md` — add Docker pull and run instructions
- `docs/changelog.md` — update Unreleased section
- `README.md` — add Docker usage section if not already present

## GitHub Actions Workflow

The workflow should:
1. Trigger on push of a release tag matching `v*.*.*`.
2. Build the Docker image from the existing `Dockerfile`.
3. Push to `ghcr.io/talaniz/congress-py` with tags for the version and `latest`.
4. Use `GITHUB_TOKEN` for authentication — no additional secrets needed.

## Public Usage

After publishing, users should be able to run:

```bash
docker run --rm -e CONGRESS_API_KEY=your_key ghcr.io/talaniz/congress-py:latest
```

And configure Claude Desktop or another MCP client with:

```json
{
  "mcpServers": {
    "congress": {
      "command": "docker",
      "args": ["run", "--rm", "-e", "CONGRESS_API_KEY=your_key", "ghcr.io/talaniz/congress-py:latest"]
    }
  }
}
```

## Acceptance Criteria

- GitHub Actions workflow triggers on release tags and completes successfully.
- Image is publicly available at `ghcr.io/talaniz/congress-py:latest`.
- `docker run --rm -e CONGRESS_API_KEY=your_key ghcr.io/talaniz/congress-py:latest` starts the MCP server.
- Documentation updated with pull and run instructions.
- `.venv/bin/python -m pytest` passes.

## Suggested Codex Prompt

```text
Add a GitHub Actions workflow to publish the congress-py Docker image to ghcr.io on release tags.

Requirements:
- Trigger on push of tags matching v*.*.*.
- Build from the existing Dockerfile.
- Push to ghcr.io/talaniz/congress-py with version and latest tags.
- Use GITHUB_TOKEN for authentication.
- Update docs/mcp.md with docker pull and run instructions including Claude Desktop config example.
- Update docs/changelog.md Unreleased section.
```

## Test Expectations

Run:

```bash
.venv/bin/python -m pytest
```

Also manually verify the published image after the first workflow run by pulling and running it locally.

## Commit Guidance

Suggested commit message:

```text
Add GitHub Actions workflow for Docker image publishing to ghcr.io
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