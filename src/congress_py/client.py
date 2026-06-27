"""Client for the Congress.gov API."""

from collections import namedtuple

import requests

from congress_py.models import Bill, BillAction, BillSummary


class CongressClient:
    """Client for interacting with Congress API endpoints.
    
    Args:
        api_key (str): API key provided by api.congress.gov.
        session: Optional ``requests.Session``-compatible object used to make
              HTTP requests. If omitted, a new ``requests.Session`` is created.
              This is mainly useful for tests or for callers that need custom
              session configuration.

    Attributes:
        api_key: Congress.gov API key used for requests.
        base_url: Base URL for the Congress.gov API.
        congress_url: Base URL for congress/session endpoints.
        bill_url: Base URL for bill endpoints.
        session: HTTP session used to make requests.

    """

    def __init__(self, api_key, session=None):
        self.api_key = api_key
        self.base_url = "https://api.congress.gov/v3"
        self.congress_url = f"{self.base_url}/congress"
        self.bill_url = f"{self.base_url}/bill"
        self.session = session or requests.Session()

    def _convert_name_to_session(self, congress_name):
        """Convert the congress name, return the numeric Congress name string.
        
        Args:
            congress_name (str): the numerical congressional session in string
                format (ex. '3rd', '4th')
        
        Returns:
            A string, congress_name, with the suffix removed.

        """
        suffixes = ["st", "nd", "rd", "th"]
        congress_name = congress_name.replace(" Congress", "")

        for suffix in suffixes:
            if suffix in congress_name:
                congress_name = congress_name.replace(suffix, "")
        return congress_name

    def _convert_congress_to_tuple(self, congress):
        """Convert congressional session information into a named tuple.
        
        Args:
            congress: Congress data dictionary from the Congress.gov API response.

        Returns:
            A named tuple containing the congress name, end year, and chambers.
        
        """
        Session = namedtuple("Session", ["name", "endYear", "chambers"])
        chambers = []

        for session in congress["sessions"]:
            if session["chamber"] not in chambers:
                chambers.append(session["chamber"])

        return Session(congress["name"], congress["endYear"], chambers)

    def _get(self, url, params=None):
        """Return decoded JSON for a Congress API endpoint.
        
        Args:
            url: Full endpoint URL to request.
            params: Optional query parameters to include with the request. The API
                key is added automatically.

        Returns:
            Decoded JSON response as a dictionary.

        Raises:
            requests.HTTPError: If Congress.gov returns an unsuccessful HTTP status.
            requests.JSONDecodeError: If the response body is not valid JSON.

        """
        request_params = {"api_key": self.api_key}
        if params:
            request_params.update(params)

        response = self.session.get(url, params=request_params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_current_session(self):
        """Return the current congressional session.
        
        Returns:
            A named tuple containing the fields ``name``, ``endYear``, and ``chambers``.
        
        """
        data = self._get(f"{self.congress_url}/current")
        congress = data.get("congress")
        if congress is None:
            congress = data["congresses"][0]
        return self._convert_congress_to_tuple(congress)

    def get_congresses(self):
        """Return congressional session records.
        
        Returns:
            list[dict]: The raw ``congresses`` list from the API response.

        """
        data = self._get(self.congress_url)
        return data["congresses"]

    def get_bill(self, congress: int, bill_type: str, number: int):
        """Return a bill for a given congress, bill type, and number.
        
        Args:
            congress (int): A Congress number, such as ``118``.
            bill_type: Congress.gov bill type code, such as ``"hr"`` or ``"s"``.
            number: Bill number within that congress and bill type.
    
        Returns:
            Bill: A ``Bill`` model created from the API response's ``bill`` object.

        """
        url = f"{self.bill_url}/{congress}/{bill_type}/{number}"
        data = self._get(url)
        return Bill.from_api_dict(data["bill"])

    def get_bill_actions(self, congress: int, bill_type: str, number: int):
        """Return actions for a given bill.
        
        Args:
            congress: Congress number, such as ``118``.
            bill_type: Congress.gov bill type code, such as ``"hr"`` or ``"s"``.
            number: Bill number within that congress and bill type.

        Returns:
            list[BillAction]: Actions parsed from the API response's ``actions`` list.

        """
        url = f"{self.bill_url}/{congress}/{bill_type}/{number}/actions"
        data = self._get(url)
        return [BillAction.from_api_dict(action) for action in data["actions"]]

    def get_bill_summaries(self, congress: int, bill_type: str, number: int):
        """Return summaries for a given bill.
        
        Args:
            congress: Congress number, such as ``118``.
            bill_type: Congress.gov bill type code, such as ``"hr"`` or ``"s"``.
            number: Bill number within that congress and bill type.

        Returns:
            list[BillSummary]: Summaries parsed from the API response's ``summaries`` list.

        """
        url = f"{self.bill_url}/{congress}/{bill_type}/{number}/summaries"
        data = self._get(url)
        return [BillSummary.from_api_dict(summary) for summary in data["summaries"]]

    def get_bills(self, session=None, limit: int = 20, offset: int = 0):
        """Return a page of bills, optionally filtered by Congress number.
        
        Args:
            session: Optional Congress number used to filter results, such as ``118``.
            limit: Maximum number of bills to request from the API.
            offset: Number of records to skip before returning results.

        Returns:
            list[Bill]: Bills parsed from the API response's ``bills`` list.

        """
        params = {"limit": limit, "offset": offset}
        if session is not None:
            params["session"] = session

        data = self._get(self.bill_url, params=params)
        return [Bill.from_api_dict(bill) for bill in data["bills"]]

    def list_recent_bills(self, limit: int = 10):
        """Return a conservative first page of recent bills.
        
        Args:
            limit: Maximum number of bills to request. Must be between ``1``
                and ``250``.

        Returns:
            list[Bill]: Bills parsed from the API response's ``bills`` list.

        Raises:
            ValueError: If ``limit`` is outside the supported range.

        """
        if limit < 1 or limit > 250:
            raise ValueError("limit must be between 1 and 250")

        return self.get_bills(limit=limit, offset=0)

    def iter_bills(self, session=None, limit: int = 20, max_pages=None):
        """Yield bills across pages until no bills are returned.
        
        Args:
            session: Optional Congress number used to filter results, such as ``118``.
            limit: Number of bills to request per API page.
            max_pages: Optional maximum number of pages to fetch. If omitted, pages
                are fetched until the API returns an empty ``bills`` list.

        Yields:
            Bill: Bills parsed from each API response's ``bills`` list.

        """
        offset = 0
        pages_fetched = 0

        while max_pages is None or pages_fetched < max_pages:
            bills = self.get_bills(session=session, limit=limit, offset=offset)
            if not bills:
                break

            yield from bills
            pages_fetched += 1
            offset += limit
