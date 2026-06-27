# Installation

## Requirements

- Python 3.9 or newer
- A Congress.gov API key

Request an API key from the official Congress.gov API site. Keep the key local
and do not commit it to source control.

## Install from PyPI

```bash
python -m pip install congress-py
```

## Install MCP support from PyPI

```bash
python -m pip install "congress-py[mcp]"
```

## Install from source

```bash
git clone https://github.com/talaniz/congress.py.git
cd congress.py
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

## Install development tools

```bash
.venv/bin/python -m pip install -e ".[dev]"
```

## Install documentation tools

```bash
.venv/bin/python -m pip install -e ".[docs]"
```

## Install MCP support from source

```bash
.venv/bin/python -m pip install -e ".[mcp]"
```

## Build the docs locally

```bash
.venv/bin/python -m mkdocs build --strict
```

To preview the docs locally:

```bash
.venv/bin/python -m mkdocs serve
```
