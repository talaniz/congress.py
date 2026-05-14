import json
import os
import stat
from collections import namedtuple
from unittest.mock import patch

from typer.testing import CliRunner

from congress_py import cli
from congress_py.models import Bill, BillAction, BillSummary


runner = CliRunner()


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
        source_system="Library of Congress",
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


def _fake_client_factory(instances):
    Session = namedtuple("Session", ["name", "endYear", "chambers"])

    class FakeClient:
        def __init__(self, api_key):
            self.api_key = api_key
            self.calls = []
            instances.append(self)

        def get_current_session(self):
            self.calls.append(("get_current_session",))
            return Session("118th Congress", "2024", ["House", "Senate"])

        def get_congresses(self):
            self.calls.append(("get_congresses",))
            return [{"name": "118th Congress"}]

        def get_bills(self, session=None):
            self.calls.append(("get_bills", session))
            return [_bill()]

        def get_bill(self, congress, bill_type, number):
            self.calls.append(("get_bill", congress, bill_type, number))
            return _bill(number=str(number))

        def get_bill_actions(self, congress, bill_type, number):
            self.calls.append(("get_bill_actions", congress, bill_type, number))
            return [_bill_action()]

        def get_bill_summaries(self, congress, bill_type, number):
            self.calls.append(("get_bill_summaries", congress, bill_type, number))
            return [_bill_summary()]

    return FakeClient


def test_congress_current_uses_explicit_api_key(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "CONFIG_DIR", tmp_path / ".congress")
    monkeypatch.setattr(cli, "CONFIG_FILE", tmp_path / ".congress" / "config.toml")
    instances = []

    with patch("congress_py.cli.CongressClient", _fake_client_factory(instances)):
        result = runner.invoke(
            cli.app,
            ["--api-key", "explicit-secret", "congress", "current"],
            env={"CONGRESS_API_KEY": "env-secret"},
        )

    assert result.exit_code == 0
    assert instances[0].api_key == "explicit-secret"
    assert instances[0].calls == [("get_current_session",)]
    assert "explicit-secret" not in result.output
    assert "env-secret" not in result.output
    assert '"name": "118th Congress"' in result.output


def test_bills_get_calls_existing_client_method(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "CONFIG_DIR", tmp_path / ".congress")
    monkeypatch.setattr(cli, "CONFIG_FILE", tmp_path / ".congress" / "config.toml")
    instances = []

    with patch("congress_py.cli.CongressClient", _fake_client_factory(instances)):
        result = runner.invoke(
            cli.app,
            ["--api-key", "secret", "bills", "get", "118", "hr", "7437"],
        )

    assert result.exit_code == 0
    assert instances[0].calls == [("get_bill", 118, "hr", 7437)]
    assert '"number": "7437"' in result.output
    assert "secret" not in result.output


def test_bills_get_outputs_valid_json_with_expected_fields(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "CONFIG_DIR", tmp_path / ".congress")
    monkeypatch.setattr(cli, "CONFIG_FILE", tmp_path / ".congress" / "config.toml")
    instances = []

    with patch("congress_py.cli.CongressClient", _fake_client_factory(instances)):
        result = runner.invoke(
            cli.app,
            ["--api-key", "secret", "bills", "get", "118", "hr", "7437"],
        )

    assert result.exit_code == 0
    output = json.loads(result.output)
    assert output["congress"] == 118
    assert output["number"] == "7437"
    assert output["bill_type"] == "HR"
    assert output["title"] == "Test Bill"
    assert output["latest_action_text"] == "Placed on the Union Calendar."
    assert "secret" not in result.output


def test_bills_actions_calls_existing_client_method(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "CONFIG_DIR", tmp_path / ".congress")
    monkeypatch.setattr(cli, "CONFIG_FILE", tmp_path / ".congress" / "config.toml")
    instances = []

    with patch("congress_py.cli.CongressClient", _fake_client_factory(instances)):
        result = runner.invoke(
            cli.app,
            ["--api-key", "secret", "bills", "actions", "118", "hr", "7437"],
        )

    assert result.exit_code == 0
    assert instances[0].calls == [("get_bill_actions", 118, "hr", 7437)]
    assert '"text": "Placed on the Union Calendar."' in result.output
    assert "secret" not in result.output


def test_bills_actions_outputs_valid_json_with_expected_fields(
    monkeypatch, tmp_path
):
    monkeypatch.setattr(cli, "CONFIG_DIR", tmp_path / ".congress")
    monkeypatch.setattr(cli, "CONFIG_FILE", tmp_path / ".congress" / "config.toml")
    instances = []

    with patch("congress_py.cli.CongressClient", _fake_client_factory(instances)):
        result = runner.invoke(
            cli.app,
            ["--api-key", "secret", "bills", "actions", "118", "hr", "7437"],
        )

    assert result.exit_code == 0
    output = json.loads(result.output)
    assert output[0]["action_date"] == "2024-11-01"
    assert output[0]["text"] == "Placed on the Union Calendar."
    assert output[0]["action_type"] == "Floor"
    assert "secret" not in result.output


def test_bills_summaries_calls_existing_client_method(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "CONFIG_DIR", tmp_path / ".congress")
    monkeypatch.setattr(cli, "CONFIG_FILE", tmp_path / ".congress" / "config.toml")
    instances = []

    with patch("congress_py.cli.CongressClient", _fake_client_factory(instances)):
        result = runner.invoke(
            cli.app,
            ["--api-key", "secret", "bills", "summaries", "118", "hr", "7437"],
        )

    assert result.exit_code == 0
    assert instances[0].calls == [("get_bill_summaries", 118, "hr", 7437)]
    assert (
        '"text": "This bill requires reports on supervisory technology."'
        in result.output
    )
    assert "secret" not in result.output


def test_bills_summaries_outputs_valid_json_with_expected_fields(
    monkeypatch, tmp_path
):
    monkeypatch.setattr(cli, "CONFIG_DIR", tmp_path / ".congress")
    monkeypatch.setattr(cli, "CONFIG_FILE", tmp_path / ".congress" / "config.toml")
    instances = []

    with patch("congress_py.cli.CongressClient", _fake_client_factory(instances)):
        result = runner.invoke(
            cli.app,
            ["--api-key", "secret", "bills", "summaries", "118", "hr", "7437"],
        )

    assert result.exit_code == 0
    output = json.loads(result.output)
    assert output[0]["action_date"] == "2024-03-05"
    assert output[0]["text"] == (
        "This bill requires reports on supervisory technology."
    )
    assert output[0]["version_code"] == "00"
    assert "secret" not in result.output


def test_bills_actions_missing_argument_fails_without_exposing_api_key(
    monkeypatch, tmp_path
):
    monkeypatch.setattr(cli, "CONFIG_DIR", tmp_path / ".congress")
    monkeypatch.setattr(cli, "CONFIG_FILE", tmp_path / ".congress" / "config.toml")

    result = runner.invoke(
        cli.app,
        ["--api-key", "secret", "bills", "actions", "118", "hr"],
    )

    assert result.exit_code != 0
    assert "secret" not in result.output


def test_congress_current_outputs_valid_json_with_expected_fields(
    monkeypatch, tmp_path
):
    monkeypatch.setattr(cli, "CONFIG_DIR", tmp_path / ".congress")
    monkeypatch.setattr(cli, "CONFIG_FILE", tmp_path / ".congress" / "config.toml")
    instances = []

    with patch("congress_py.cli.CongressClient", _fake_client_factory(instances)):
        result = runner.invoke(
            cli.app,
            ["--api-key", "secret", "congress", "current"],
        )

    assert result.exit_code == 0
    output = json.loads(result.output)
    assert output == {
        "chambers": ["House", "Senate"],
        "endYear": "2024",
        "name": "118th Congress",
    }
    assert instances[0].calls == [("get_current_session",)]
    assert "secret" not in result.output


def test_bills_list_passes_session_option(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "CONFIG_DIR", tmp_path / ".congress")
    monkeypatch.setattr(cli, "CONFIG_FILE", tmp_path / ".congress" / "config.toml")
    instances = []

    with patch("congress_py.cli.CongressClient", _fake_client_factory(instances)):
        result = runner.invoke(
            cli.app,
            ["--api-key", "secret", "bills", "list", "--session", "118"],
        )

    assert result.exit_code == 0
    assert instances[0].calls == [("get_bills", 118)]


def test_env_api_key_is_used_when_explicit_key_is_absent(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "CONFIG_DIR", tmp_path / ".congress")
    monkeypatch.setattr(cli, "CONFIG_FILE", tmp_path / ".congress" / "config.toml")
    instances = []

    with patch("congress_py.cli.CongressClient", _fake_client_factory(instances)):
        result = runner.invoke(
            cli.app,
            ["congress", "list"],
            env={"CONGRESS_API_KEY": "env-secret"},
        )

    assert result.exit_code == 0
    assert instances[0].api_key == "env-secret"
    assert instances[0].calls == [("get_congresses",)]
    assert "env-secret" not in result.output


def test_config_api_key_is_used_when_env_and_explicit_key_are_absent(
    monkeypatch, tmp_path
):
    config_dir = tmp_path / ".congress"
    config_file = config_dir / "config.toml"
    config_dir.mkdir()
    config_file.write_text('[auth]\napi_key = "config-secret"\n', encoding="utf-8")
    monkeypatch.setattr(cli, "CONFIG_DIR", config_dir)
    monkeypatch.setattr(cli, "CONFIG_FILE", config_file)
    instances = []

    with patch("congress_py.cli.CongressClient", _fake_client_factory(instances)):
        result = runner.invoke(
            cli.app,
            ["congress", "list"],
            env={"CONGRESS_API_KEY": ""},
        )

    assert result.exit_code == 0
    assert instances[0].api_key == "config-secret"
    assert "config-secret" not in result.output


def test_missing_api_key_fails_without_prompting(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "CONFIG_DIR", tmp_path / ".congress")
    monkeypatch.setattr(cli, "CONFIG_FILE", tmp_path / ".congress" / "config.toml")

    result = runner.invoke(
        cli.app,
        ["congress", "current"],
        env={"CONGRESS_API_KEY": ""},
    )

    assert result.exit_code == 1
    assert (
        "No Congress.gov API key found. Run congress configure or set CONGRESS_API_KEY."
        in result.output
    )


def test_configure_writes_config_without_printing_api_key(monkeypatch, tmp_path):
    config_dir = tmp_path / ".congress"
    config_file = config_dir / "config.toml"
    monkeypatch.setattr(cli, "CONFIG_DIR", config_dir)
    monkeypatch.setattr(cli, "CONFIG_FILE", config_file)

    result = runner.invoke(cli.app, ["configure"], input="saved-secret\n")

    assert result.exit_code == 0
    assert "Configuration saved." in result.output
    assert "saved-secret" not in result.output
    assert config_file.read_text(encoding="utf-8") == (
        '[auth]\napi_key = "saved-secret"\n'
    )
    if os.name != "nt":
        assert stat.S_IMODE(config_file.stat().st_mode) == 0o600
