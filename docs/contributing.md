# Contributing

This is an unofficial portfolio project. Contributions should keep the project
small, readable, testable, and safe to publish.

## Development setup

```bash
git clone https://github.com/talaniz/congress.py.git
cd congress.py
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
```

For documentation work:

```bash
.venv/bin/python -m pip install -e ".[docs]"
```

## Tests

```bash
.venv/bin/python -m pytest
```

Default tests should use mocked HTTP. Avoid live Congress.gov calls in normal
test runs.

## Documentation

Build docs before submitting documentation changes:

```bash
.venv/bin/python -m mkdocs build --strict
```

Use hand-written docs for CLI behavior. Use the API reference page for
mkdocstrings-generated SDK documentation from `client.py`, `models.py`, and
`exceptions.py`.

## Scope

- Keep SDK methods thin and predictable.
- Keep CLI commands thin and JSON-first.
- Do not duplicate API request logic outside `CongressClient`.
- Do not add persistence, caching, authentication systems, or advice-oriented
  features unless explicitly approved.
- Do not imply affiliation with Congress.gov, the Library of Congress,
  Congress, or the U.S. government.

## Security

Do not commit API keys, `.env` files, local config files, or private notes.
Examples must not contain secrets. Error messages and docs should never expose
full API keys.
