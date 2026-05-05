"""Client for the official Congress API."""

from collections import namedtuple

import requests

from congress_py.models import Bill


class CongressClient:
    """Client for interacting with Congress API endpoints."""

    def __init__(self, api_key, session=None):
        self.api_key = api_key
        self.base_url = "https://api.congress.gov/v3"
        self.congress_url = f"{self.base_url}/congress"
        self.bill_url = f"{self.base_url}/bill"
        self.session = session or requests.Session()

    def _convert_name_to_session(self, congress_name):
        """Convert the congress name, return the session number."""
        suffixes = ["st", "nd", "rd", "th"]
        congress_name = congress_name.replace(" Congress", "")

        for suffix in suffixes:
            if suffix in congress_name:
                congress_name = congress_name.replace(suffix, "")
        return congress_name

    def _convert_congress_to_tuple(self, congress):
        """Convert congressional session information into a named tuple."""
        Session = namedtuple("Session", ["name", "endYear", "chambers"])
        chambers = []

        for session in congress["sessions"]:
            if session["chamber"] not in chambers:
                chambers.append(session["chamber"])

        return Session(congress["name"], congress["endYear"], chambers)

    def _get(self, url, params=None):
        """Return decoded JSON for a Congress API endpoint."""
        request_params = {"api_key": self.api_key}
        if params:
            request_params.update(params)

        response = self.session.get(url, params=request_params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_current_session(self):
        """Return the current congressional session."""
        data = self._get(f"{self.congress_url}/current")
        congress = data.get("congress")
        if congress is None:
            congress = data["congresses"][0]
        return self._convert_congress_to_tuple(congress)

    def get_congresses(self):
        """Return a list of all active congressional sessions."""
        data = self._get(self.congress_url)
        return data["congresses"]

    def get_bill(self, congress: int, bill_type: str, number: int):
        """Return a bill for a given congress, bill type, and number."""
        url = f"{self.bill_url}/{congress}/{bill_type}/{number}"
        data = self._get(url)
        return Bill.from_api_dict(data["bill"])

    def get_bills(self, session=None):
        """Return a list of bills for a given congressional session."""
        params = {}
        if session is not None:
            params["session"] = session

        data = self._get(self.bill_url, params=params)
        return [Bill.from_api_dict(bill) for bill in data["bills"]]
