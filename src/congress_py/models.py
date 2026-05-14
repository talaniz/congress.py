"""Data models for Congress API responses."""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Bill:
    congress: int
    latest_action_date: str
    latest_action_text: str
    number: str
    origin_chamber: str
    title: str
    bill_type: str
    update_date: str
    update_including_text: bool
    url: Optional[str] = None

    @classmethod
    def from_api_dict(cls, bill_data):
        """Create a Bill from an API response dictionary."""
        return cls(
            congress=bill_data["congress"],
            latest_action_date=bill_data["latestAction"]["actionDate"],
            latest_action_text=bill_data["latestAction"]["text"],
            number=bill_data["number"],
            origin_chamber=bill_data["originChamber"],
            title=bill_data["title"],
            bill_type=bill_data["type"],
            update_date=bill_data["updateDate"],
            update_including_text=bill_data["updateDateIncludingText"],
            url=bill_data.get("url"),
        )


@dataclass
class BillAction:
    action_date: Optional[str]
    text: Optional[str]
    action_type: Optional[str] = None
    source_system: Optional[Dict[str, Any]] = None
    url: Optional[str] = None

    @classmethod
    def from_api_dict(cls, action_data):
        """Create a BillAction from an API response dictionary."""
        return cls(
            action_date=action_data.get("actionDate"),
            text=action_data.get("text"),
            action_type=action_data.get("type"),
            source_system=action_data.get("sourceSystem"),
            url=action_data.get("url"),
        )


@dataclass
class BillSummary:
    action_date: Optional[str]
    text: Optional[str]
    update_date: Optional[str] = None
    version_code: Optional[str] = None
    action_desc: Optional[str] = None

    @classmethod
    def from_api_dict(cls, summary_data):
        """Create a BillSummary from an API response dictionary."""
        return cls(
            action_date=summary_data.get("actionDate"),
            text=summary_data.get("text"),
            update_date=summary_data.get("updateDate"),
            version_code=summary_data.get("versionCode"),
            action_desc=summary_data.get("actionDesc"),
        )
