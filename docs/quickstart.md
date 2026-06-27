# Quickstart

## Configure an API key

The SDK accepts an explicit API key. It does not read local CLI config files.

```bash
export CONGRESS_API_KEY=your_api_key_here
```

For CLI-only convenience, you can save a local key:

```bash
congress configure
```

The CLI resolves credentials in this order:

1. `--api-key`
2. `CONGRESS_API_KEY`
3. `~/.congress/config.toml`

Normal CLI commands do not prompt for credentials.

## Use the SDK

```python
import os

from congress_py import CongressClient

client = CongressClient(api_key=os.environ["CONGRESS_API_KEY"])

current = client.get_current_session()
print(current.name)

bills = client.get_bills(session=118, limit=20, offset=0)
print(bills[0].title)

bill = client.get_bill(118, "hr", 7437)
actions = client.get_bill_actions(118, "hr", 7437)
summaries = client.get_bill_summaries(118, "hr", 7437)

print(bill.title)
print(actions[0].text)
print(summaries[0].text)
```

## Use the CLI

```bash
congress congress current
congress bills list --session 118 --limit 20
congress bills get 118 hr 7437
congress bills actions 118 hr 7437
congress bills summaries 118 hr 7437
```

CLI output is JSON by default.

## Start the MCP server

Install the MCP extra, then start the local stdio server:

```bash
.venv/bin/python -m pip install -e ".[mcp]"
congress mcp-start
```
