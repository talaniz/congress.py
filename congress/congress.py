"""Module for managing API calls to the Congress API."""

import json
import requests

from collections import namedtuple

from congress.bills import Bill

class CongressAPI(object):
    """An instance of a Congress API object."""

    def __init__(self, api_key):
        self.base_url = "https://api.congress.gov/v3/congress"
        self.api_key = api_key
        self.bills_url = f"https://api.congress.gov/v3/bill?api_key={self.api_key}"

    def _convert_name_to_session(self, congress_name):
        """Convert the congress name, return the session number."""
        suffixes = ["st", "nd", "rd", "th"]
        congress_name = congress_name.replace(" Congress", "")

        for suffix in suffixes:
            if suffix in congress_name:
                congress_name = congress_name.replace(suffix, "")
        return congress_name

    def _convert_congress_to_tuple(self, congress):
        """Convert a dict with Congressional session information into a tuple, house and senate."""
        Session = namedtuple("Session", ['name', 'endYear', 'chambers'])
        name = congress['name']
        endYear = congress['endYear']
        chambers = []
        for session in congress['sessions']:
            if session['chamber'] not in chambers:
                chambers.append(session['chamber'])
            else:
                continue
        res = Session(name, endYear, chambers)
        return res

    def get_current_session(self):
        """Return the current congressional session."""
        res = self.get_response(f"{self.base_url}/current?api_key={self.api_key}")
        congresses = res['congresses']
        current_congress = self._convert_congress_to_tuple(congresses[0])
        return current_congress

    def get_response(self, url):
        """Return the text response for a given endpoint."""
        r = requests.get(url)
        return json.loads(r.text)

    def get_congresses(self):
        """Return a list of all active congresstional sessions."""
        data = self.get_response(f"{self.base_url}?api_key={self.api_key}")
        return data['congresses']

    def get_bills(self, session=None):
        """Return a list of bills for a given congressional session."""
        if session is None:
            data = self.get_response(self.bills_url)
            first_bill = data['bills'][0]
            bill = Bill(first_bill['congress'], first_bill['latestAction'])
            return [bill]
        else:
            return data['bills']
