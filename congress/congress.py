import json
import requests

class CongressAPI(object):
    """An instance of a Congress API object."""

    def __init__(self, api_key):
        self.api_key = api_key
        self.bills_url = f"https://api.congress.gov/v3/bill?api_key={self.api_key}"
        self.congress_url = f"https://api.congress.gov/v3/congress?api_key={self.api_key}"

    def _convert_name_to_session(self, congress_name):
        """Convert the congress name, return the session number."""
        suffixes = ["st", "nd", "rd", "th"]
        congress_name = congress_name.replace(" Congress", "")

        for suffix in suffixes:
            if suffix in congress_name:
                congress_name = congress_name.replace(suffix, "")
        return congress_name

    def get_response(self, url):
        """Return the text response for a given endpoint."""
        r = requests.get(url)
        return json.loads(r.text)

    def get_congresses(self):
        """Return a list of all active congresstional sessions."""
        data = self.get_response(self.congress_url)
        return data['congresses']

    def get_bills(self):
        """Return a list of bills for a given congressional session."""
        data = self.get_response(self.bills_url)
        return data['bills']
