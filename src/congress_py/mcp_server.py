"""Read-only MCP server for Congress.gov workflows."""

from __future__ import annotations

import os
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Optional

from congress_py.client import CongressClient
from congress_py.exceptions import MissingAPIKeyError

CONFIG_FILE = Path.home() / ".congress" / "config.toml"
MISSING_API_KEY_MESSAGE = (
    "No Congress.gov API key found. Run congress configure or set CONGRESS_API_KEY."
)


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


def resolve_api_key(
    explicit_api_key: Optional[str] = None,
    config_file: Optional[Path] = None,
) -> str:
    """Resolve an API key for MCP startup without prompting."""
    if explicit_api_key:
        return explicit_api_key

    env_api_key = os.environ.get("CONGRESS_API_KEY")
    if env_api_key:
        return env_api_key

    config_api_key = _load_config_api_key(config_file=config_file)
    if config_api_key:
        return config_api_key

    raise MissingAPIKeyError(MISSING_API_KEY_MESSAGE)


def get_bill_tool(
    client: CongressClient,
    congress: int,
    bill_type: str,
    number: int,
) -> dict[str, Any]:
    """Return one bill through the SDK client."""
    return _to_jsonable(client.get_bill(congress, bill_type, number))


def get_bill_actions_tool(
    client: CongressClient,
    congress: int,
    bill_type: str,
    number: int,
) -> list[dict[str, Any]]:
    """Return bill actions through the SDK client."""
    return _to_jsonable(client.get_bill_actions(congress, bill_type, number))


def get_bill_summaries_tool(
    client: CongressClient,
    congress: int,
    bill_type: str,
    number: int,
) -> list[dict[str, Any]]:
    """Return bill summaries through the SDK client."""
    return _to_jsonable(client.get_bill_summaries(congress, bill_type, number))


def list_recent_bills_tool(
    client: CongressClient,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Return recent bills through the SDK client."""
    return _to_jsonable(client.list_recent_bills(limit=limit))


def create_server(client: CongressClient):
    """Create the MCP server for a configured CongressClient."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError(
            'MCP support is not installed. Install with: pip install "congress-py[mcp]"'
        ) from exc

    server = FastMCP("congress-py")

    @server.tool()
    def get_bill(congress: int, bill_type: str, number: int) -> dict[str, Any]:
        """Return one bill by congress, bill type, and number."""
        return get_bill_tool(client, congress, bill_type, number)

    @server.tool()
    def get_bill_actions(
        congress: int,
        bill_type: str,
        number: int,
    ) -> list[dict[str, Any]]:
        """Return actions for one bill."""
        return get_bill_actions_tool(client, congress, bill_type, number)

    @server.tool()
    def get_bill_summaries(
        congress: int,
        bill_type: str,
        number: int,
    ) -> list[dict[str, Any]]:
        """Return summaries for one bill."""
        return get_bill_summaries_tool(client, congress, bill_type, number)

    @server.tool()
    def list_recent_bills(limit: int = 10) -> list[dict[str, Any]]:
        """Return a conservative first page of recent bills."""
        return list_recent_bills_tool(client, limit=limit)

    return server


def run(api_key: Optional[str] = None) -> None:
    """Start the stdio MCP server."""
    resolved_api_key = resolve_api_key(api_key)
    client = CongressClient(api_key=resolved_api_key)
    server = create_server(client)
    server.run()


def main() -> None:
    """Run the MCP server from ``python -m congress_py.mcp_server``."""
    try:
        run()
    except MissingAPIKeyError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
