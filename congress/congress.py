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
    
    def get_bill(self, congress: int, bill_type: str, number: int):
        """Return a bill for a given congress, bill type and number."""
        url = f"{self.base_url}/{congress}/bills/{bill_type}/{number}?api_key={self.api_key}"
        data = self.get_response(url)
        bill_data = data['bill']
        bill = Bill(
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
        return bill

    def get_bills(self, session=None):
        """Return a list of bills for a given congressional session."""
        res = []
        if session is None:
            data = self.get_response(self.bills_url)
            bills = data['bills']
            for bill in bills:
                bill = Bill(
                    congress=bill['congress'],
                    latest_action_date=bill["latestAction"]["actionDate"],
                    latest_action_text=bill["latestAction"]["text"],
                    number=bill['number'],
                    origin_chamber=bill['originChamber'],
                    title=bill['title'],
                    bill_type=bill['type'],
                    update_date=bill['updateDate'],
                    update_including_text=bill['updateDateIncludingText'],
                    url=bill['url']
                )
                res.append(bill)
            return res
        else:
            return data['bills']
