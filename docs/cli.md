# CLI

The package installs a `congress` command. The CLI is intentionally thin:
it resolves configuration, calls `CongressClient`, and prints JSON.

## Credentials

Credential resolution order:

1. Explicit `--api-key`
2. `CONGRESS_API_KEY`
3. `~/.congress/config.toml`

Only `congress configure` prompts for an API key. Other commands fail clearly
when no key is available.

```bash
congress configure
```

The config file format is:

```toml
[auth]
api_key = "your-api-key-here"
```

Do not commit this file or print the full API key in logs.

## Congress commands

```bash
congress congress current
congress congress list
```

## Bill commands

```bash
congress bills list
congress bills list --session 118
congress bills list --limit 50
congress bills list --session 118 --limit 25 --offset 100
congress bills list --session 118 --limit 25 --pages 3
congress bills get 118 hr 7437
congress bills actions 118 hr 7437
congress bills summaries 118 hr 7437
```

`--limit` controls the number of bills requested per API call. `--offset`
controls the starting offset in single-page mode. `--pages` switches to
multi-page iteration through the SDK iterator. When `--pages` is provided,
`--offset` is ignored because the current iterator starts from the first page.

## One-command API key

```bash
congress --api-key your_api_key_here bills get 118 hr 7437
```

Prefer environment variables or local CLI config for routine use so secrets do
not appear in shell history.
