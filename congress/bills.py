"""Module to manage congressional bill data."""
from dataclasses import dataclass


@dataclass
class Bill:
    congress: int
    latest_action: str
    number: str
    origin_chamber: str
    title: str
    bill_type: str
    update_date: str
    update_including_text: bool
    url: str
