"""Data models for Congress API responses."""

from dataclasses import dataclass
from typing import Optional


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
