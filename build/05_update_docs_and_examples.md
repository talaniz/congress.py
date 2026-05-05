# Session 05: Update Docs and Examples

## Objective

Make the project understandable, safe to use, and easy to demonstrate in an interview.

## Scope

Update documentation for:

- Project purpose.
- Installation.
- API-key setup.
- SDK quickstart.
- MCP server setup.
- Example tool usage.
- Testing.
- Security and unofficial-project disclaimers.
- AI-assisted development note.

Add small examples where helpful.

## Files Likely to Change

- `README.md`
- `examples/demo_bill_lookup.py`
- `examples/mcp_config.md`
- `AGENTS.md`
- `build/execution_plan.md` if the plan changes

## Acceptance Criteria

- README has a working quickstart.
- README clearly says the project is unofficial.
- README explains API-key setup using environment variables.
- README warns that the project does not provide legal, lobbying, compliance, financial, or legislative advice.
- README includes basic SDK and MCP examples.
- Examples do not contain secrets.

## Suggested Codex Prompt

```text
Update the documentation for this project.

Please add or improve:
- Project overview
- Installation steps
- API-key setup using environment variables
- SDK quickstart example
- MCP server setup example
- Testing instructions
- Security and unofficial-project disclaimers
- AI-assisted development note

Do not invent unsupported features. Keep examples aligned with existing code.
```

## Test Expectations

Run tests after documentation changes if examples or imports changed:

```bash
.venv/bin/python -m pytest
```

## Commit Guidance

Suggested commit message:

```text
Document SDK and MCP usage
```
