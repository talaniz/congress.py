import sys
import types

import pytest

from congress_py import mcp_server
from congress_py.exceptions import MissingAPIKeyError
from congress_py.models import Bill, BillAction, BillSummary


def _bill(number="7437"):
    return Bill(
        congress=118,
        latest_action_date="2024-11-01",
        latest_action_text="Placed on the Union Calendar.",
        number=number,
        origin_chamber="House",
        title="Test Bill",
        bill_type="HR",
        update_date="2024-11-02",
        update_including_text=True,
        url=f"https://api.congress.gov/v3/bill/118/hr/{number}?format=json",
    )


def _bill_action():
    return BillAction(
        action_date="2024-11-01",
        text="Placed on the Union Calendar.",
        action_type="Floor",
        source_system={"name": "Library of Congress"},
        url="https://api.congress.gov/v3/bill/118/hr/7437/actions?format=json",
    )


def _bill_summary():
    return BillSummary(
        action_date="2024-03-05",
        text="This bill requires reports on supervisory technology.",
        update_date="2024-03-06T18:44:00Z",
        version_code="00",
        action_desc="Introduced in House",
    )


class FakeClient:
    def __init__(self):
        self.calls = []

    def get_bill(self, congress, bill_type, number):
        self.calls.append(("get_bill", congress, bill_type, number))
        return _bill(number=str(number))

    def get_bill_actions(self, congress, bill_type, number):
        self.calls.append(("get_bill_actions", congress, bill_type, number))
        return [_bill_action()]

    def get_bill_summaries(self, congress, bill_type, number):
        self.calls.append(("get_bill_summaries", congress, bill_type, number))
        return [_bill_summary()]

    def list_recent_bills(self, limit=10):
        self.calls.append(("list_recent_bills", limit))
        if limit < 1 or limit > 250:
            raise ValueError("limit must be between 1 and 250")
        return [_bill()]


def test_get_bill_tool_returns_json_compatible_snake_case_output():
    client = FakeClient()

    output = mcp_server.get_bill_tool(client, 118, "hr", 7437)

    assert client.calls == [("get_bill", 118, "hr", 7437)]
    assert output["latest_action_date"] == "2024-11-01"
    assert output["bill_type"] == "HR"
    assert output["number"] == "7437"


def test_get_bill_actions_tool_delegates_to_client():
    client = FakeClient()

    output = mcp_server.get_bill_actions_tool(client, 118, "hr", 7437)

    assert client.calls == [("get_bill_actions", 118, "hr", 7437)]
    assert output[0]["action_date"] == "2024-11-01"
    assert output[0]["source_system"] == {"name": "Library of Congress"}


def test_get_bill_summaries_tool_delegates_to_client():
    client = FakeClient()

    output = mcp_server.get_bill_summaries_tool(client, 118, "hr", 7437)

    assert client.calls == [("get_bill_summaries", 118, "hr", 7437)]
    assert output[0]["action_desc"] == "Introduced in House"
    assert output[0]["version_code"] == "00"


def test_list_recent_bills_tool_delegates_to_client_with_limit():
    client = FakeClient()

    output = mcp_server.list_recent_bills_tool(client, limit=25)

    assert client.calls == [("list_recent_bills", 25)]
    assert output[0]["number"] == "7437"


def test_list_recent_bills_tool_propagates_invalid_limit():
    client = FakeClient()

    with pytest.raises(ValueError, match="limit must be between 1 and 250"):
        mcp_server.list_recent_bills_tool(client, limit=251)


def test_resolve_api_key_prefers_explicit_over_environment(monkeypatch, tmp_path):
    monkeypatch.setenv("CONGRESS_API_KEY", "env-secret")

    api_key = mcp_server.resolve_api_key(
        explicit_api_key="explicit-secret",
        config_file=tmp_path / "missing.toml",
    )

    assert api_key == "explicit-secret"


def test_resolve_api_key_uses_environment(monkeypatch, tmp_path):
    monkeypatch.setenv("CONGRESS_API_KEY", "env-secret")

    api_key = mcp_server.resolve_api_key(config_file=tmp_path / "missing.toml")

    assert api_key == "env-secret"


def test_resolve_api_key_uses_config_file(monkeypatch, tmp_path):
    monkeypatch.delenv("CONGRESS_API_KEY", raising=False)
    config_file = tmp_path / "config.toml"
    config_file.write_text('[auth]\napi_key = "config-secret"\n', encoding="utf-8")

    api_key = mcp_server.resolve_api_key(config_file=config_file)

    assert api_key == "config-secret"


def test_resolve_api_key_raises_for_missing_credentials(monkeypatch, tmp_path):
    monkeypatch.delenv("CONGRESS_API_KEY", raising=False)

    with pytest.raises(MissingAPIKeyError):
        mcp_server.resolve_api_key(config_file=tmp_path / "missing.toml")


def test_create_server_registers_expected_tools(monkeypatch):
    class FakeFastMCP:
        def __init__(self, name):
            self.name = name
            self.tools = {}

        def tool(self):
            def decorator(func):
                self.tools[func.__name__] = func
                return func

            return decorator

    fake_fastmcp_module = types.ModuleType("mcp.server.fastmcp")
    fake_fastmcp_module.FastMCP = FakeFastMCP
    monkeypatch.setitem(sys.modules, "mcp", types.ModuleType("mcp"))
    monkeypatch.setitem(sys.modules, "mcp.server", types.ModuleType("mcp.server"))
    monkeypatch.setitem(sys.modules, "mcp.server.fastmcp", fake_fastmcp_module)

    server = mcp_server.create_server(FakeClient())

    assert server.name == "congress-py"
    assert set(server.tools) == {
        "get_bill",
        "get_bill_actions",
        "get_bill_summaries",
        "list_recent_bills",
    }
