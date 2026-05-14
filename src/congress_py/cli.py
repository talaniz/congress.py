"""Command-line interface for congress_py."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Optional

import typer

from congress_py.client import CongressClient
from congress_py.exceptions import MissingAPIKeyError

CONFIG_DIR = Path.home() / ".congress"
CONFIG_FILE = CONFIG_DIR / "config.toml"
MISSING_API_KEY_MESSAGE = (
    "No Congress.gov API key found. Run congress configure or set CONGRESS_API_KEY."
)

app = typer.Typer(help="CLI for the Congress.gov API.")
congress_app = typer.Typer(help="Congress session commands.")
bills_app = typer.Typer(help="Bill commands.")


def _to_jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _to_jsonable(asdict(value))
    if hasattr(value, "_asdict"):
        return _to_jsonable(value._asdict())
    if isinstance(value, dict):
        return {key: _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(item) for item in value]
    return value


def _json_default(value: Any) -> Any:
    converted = _to_jsonable(value)
    if converted is not value:
        return converted
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def _print_json(value: Any) -> None:
    typer.echo(
        json.dumps(_to_jsonable(value), default=_json_default, indent=2, sort_keys=True)
    )


def _parse_simple_auth_toml(content: str) -> Optional[str]:
    in_auth_section = False

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            in_auth_section = line == "[auth]"
            continue
        if not in_auth_section or "=" not in line:
            continue

        key, value = line.split("=", 1)
        if key.strip() != "api_key":
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        return value.strip() or None

    return None


def _load_config_api_key(config_file: Optional[Path] = None) -> Optional[str]:
    if config_file is None:
        config_file = CONFIG_FILE

    if not config_file.exists():
        return None

    content = config_file.read_text(encoding="utf-8")
    try:
        import tomllib
    except ModuleNotFoundError:
        return _parse_simple_auth_toml(content)

    data = tomllib.loads(content)
    auth = data.get("auth", {})
    api_key = auth.get("api_key")
    if isinstance(api_key, str):
        return api_key.strip() or None
    return None


def _resolve_api_key(explicit_api_key: Optional[str]) -> str:
    if explicit_api_key:
        return explicit_api_key

    env_api_key = os.environ.get("CONGRESS_API_KEY")
    if env_api_key:
        return env_api_key

    config_api_key = _load_config_api_key()
    if config_api_key:
        return config_api_key

    raise MissingAPIKeyError(MISSING_API_KEY_MESSAGE)


def _get_client(ctx: typer.Context) -> CongressClient:
    explicit_api_key = None
    if ctx.obj:
        explicit_api_key = ctx.obj.get("api_key")

    try:
        return CongressClient(api_key=_resolve_api_key(explicit_api_key))
    except MissingAPIKeyError:
        typer.echo(MISSING_API_KEY_MESSAGE, err=True)
        raise typer.Exit(1)


def _toml_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


@app.callback()
def main(
    ctx: typer.Context,
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        help=(
            "Congress.gov API key. Defaults to CONGRESS_API_KEY "
            "or ~/.congress/config.toml."
        ),
    ),
) -> None:
    """Resolve global CLI options."""
    ctx.obj = {"api_key": api_key}


@app.command()
def configure(
    api_key: str = typer.Option(
        ...,
        "--api-key",
        prompt=True,
        hide_input=True,
        help="Congress.gov API key to save locally.",
    ),
) -> None:
    """Save a Congress.gov API key for CLI use."""
    CONFIG_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    content = f'[auth]\napi_key = "{_toml_string(api_key)}"\n'

    fd = os.open(CONFIG_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as config:
        config.write(content)

    try:
        CONFIG_FILE.chmod(0o600)
    except OSError:
        pass

    typer.echo("Configuration saved.")


@congress_app.command("current")
def congress_current(ctx: typer.Context) -> None:
    """Return the current congressional session."""
    client = _get_client(ctx)
    _print_json(client.get_current_session())


@congress_app.command("list")
def congress_list(ctx: typer.Context) -> None:
    """Return available congressional sessions."""
    client = _get_client(ctx)
    _print_json(client.get_congresses())


@bills_app.command("list")
def bills_list(
    ctx: typer.Context,
    session: Optional[int] = typer.Option(
        None,
        "--session",
        help="Congress session number to pass to the existing SDK method.",
    ),
) -> None:
    """Return bills from the existing SDK list method."""
    client = _get_client(ctx)
    _print_json(client.get_bills(session=session))


@bills_app.command("get")
def bills_get(ctx: typer.Context, congress: int, bill_type: str, number: int) -> None:
    """Return one bill by congress, bill type, and number."""
    client = _get_client(ctx)
    _print_json(client.get_bill(congress, bill_type, number))


@bills_app.command("actions")
def bills_actions(
    ctx: typer.Context, congress: int, bill_type: str, number: int
) -> None:
    """Return actions for one bill."""
    client = _get_client(ctx)
    _print_json(client.get_bill_actions(congress, bill_type, number))


@bills_app.command("summaries")
def bills_summaries(
    ctx: typer.Context, congress: int, bill_type: str, number: int
) -> None:
    """Return summaries for one bill."""
    client = _get_client(ctx)
    _print_json(client.get_bill_summaries(congress, bill_type, number))


app.add_typer(congress_app, name="congress")
app.add_typer(bills_app, name="bills")


def run() -> None:
    """Run the Typer application."""
    app()
