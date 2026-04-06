"""Module to manage congressional bill data."""
from dataclasses import dataclass


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
    url: str

    @classmethod
    def from_api_dict(cls, bill_data):
        """Create a Bill from API response dictionary"""
        return cls(
            congress=bill_data['congress'],
            latest_action_date=bill_data["latestAction"]["actionDate"],
            latest_action_text=bill_data["latestAction"]["text"],
            number=bill_data['number'],
            origin_chamber=bill_data['originChamber'],
            title=bill_data['title'],
            bill_type=bill_data['type'],
            update_date=bill_data['updateDate'],
            update_including_text=bill_data['updateDateIncludingText'],
            url=bill_data['url']
        )

    @classmethod
    def get_bill(cls, api, congress: int, bill_type: str, number: int):
        """Fetch a single bill from API"""
        url = f"{api.base_url}/{congress}/bills/{bill_type}/{number}?api_key={api.api_key}"
        data = api.get_response(url)
        return cls.from_api_dict(data['bill'])

    @classmethod
    def get_bills(cls, api, session=None):
        """Fetch multiple bills from API"""
        if session is None:
            data = api.get_response(api.bills_url)
        else:
            # Your session-specific logic here
            data = api.get_response(f"{api.bills_url}&session={session}")

        bills = data['bills']
        return [cls.from_api_dict(bill) for bill in bills]
