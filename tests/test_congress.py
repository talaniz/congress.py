import json
import unittest

from collections import namedtuple
from urllib.parse import parse_qs, urlparse

import requests_mock

from congress_py import Bill, CongressClient


class TestCongressClientValidation(unittest.TestCase):

    def test_congress_initialization_validates_api_key(self):
        """Ensure the Congress object is initialized with an API key."""
        with self.assertRaises(TypeError):
            CongressClient()


class TestCongressClient(unittest.TestCase):

    def setUp(self):
        self.api_key = "myApiKey"
        self.congress = CongressClient(self.api_key)
        self.Session = namedtuple("Session", ['name', 'endYear', 'chambers'])

    def return_mock_file_data(self, filename):
        """Open the file with mock data and return the contets."""
        with open(filename, 'r') as f:
            d = f.read()
            return d

    def bill_data(self, number="7437"):
        """Return minimal bill data for mocked bill-listing responses."""
        return {
            "congress": 118,
            "latestAction": {
                "actionDate": "2024-11-01",
                "text": "Placed on the Union Calendar, Calendar No. 615."
            },
            "number": number,
            "originChamber": "House",
            "title": (
                "Fostering the Use of Technology to Uphold Regulatory "
                "Effectiveness in Supervision Act"
            ),
            "type": "HR",
            "updateDate": "2024-11-02",
            "updateDateIncludingText": "2024-11-02",
            "url": f"https://api.congress.gov/v3/bill/118/hr/{number}?format=json"
        }

    def request_query(self, request):
        """Return parsed query parameters from a mocked request."""
        return parse_qs(urlparse(request.url).query)

    def test_convert_name_to_session(self):
        """Validate that the congressional name is translated to the session number."""
        self.assertEqual(self.congress._convert_name_to_session("118th Congress"), "118")
        self.assertEqual(self.congress._convert_name_to_session("22nd Congress"), "22")
        self.assertEqual(self.congress._convert_name_to_session("81st Congress"), "81")
        self.assertEqual(self.congress._convert_name_to_session("93rd Congress"), "93")

    def test_convert_congress_to_tuple(self):
        """Checks that a dictionary can be converted to a series of named tuples."""
        # TODO: the dates here should be dynamically calculated or this will fail next year
        congress = {
            "endYear": "2024",
            "name": "118th Congress",
            "sessions": [
                {
                    "chamber": "House of Representatives",
                    "endDate": "2024-01-03",
                    "number": 1,
                    "startDate": "2023-01-03",
                    "type": "R"
                },
                {
                    "chamber": "Senate",
                    "endDate": "2024-01-03",
                    "number": 1,
                    "startDate": "2023-01-03",
                    "type": "R"
                },
                {
                    "chamber": "Senate",
                    "number": 2,
                    "startDate": "2024-01-03",
                    "type": "R"
                },
                {
                    "chamber": "House of Representatives",
                    "number": 2,
                    "startDate": "2024-01-03",
                    "type": "R"
                }
            ],
            "startYear": "2023",
            "url": "https://api.congress.gov/v3/congress/118?format=json"
        }
        expected_session = self.Session("118th Congress", "2024",["House of Representatives", "Senate"])

        session = self.congress._convert_congress_to_tuple(congress)

        self.assertEqual(session, expected_session)

    @requests_mock.Mocker()
    def test_get_current_session_returns_most_current_session(self, m):
        """Test that the call to get_current_session returns the most recent one."""
        congresss_url = f"https://api.congress.gov/v3/congress/current?api_key={self.api_key}"
        d = self.return_mock_file_data('tests/congress_responses.txt')

        m.get(congresss_url, text=d)
        current_session = self.congress.get_current_session()
        expected_current_session = self.Session("118th Congress", "2024",["House of Representatives", "Senate"])
        self.assertEqual(current_session, expected_current_session)

    @requests_mock.Mocker()
    def test_get_current_session_accepts_current_endpoint_item_response(self, m):
        """Validate get_current_session accepts the /congress/current response shape."""
        congress_url = f"https://api.congress.gov/v3/congress/current?api_key={self.api_key}"
        current_congress = {
            "endYear": "2026",
            "name": "119th Congress",
            "number": 119,
            "sessions": [
                {
                    "chamber": "House of Representatives",
                    "number": 1,
                    "startDate": "2025-01-03",
                    "type": "R"
                },
                {
                    "chamber": "Senate",
                    "number": 1,
                    "startDate": "2025-01-03",
                    "type": "R"
                }
            ],
            "startYear": "2025",
            "url": "https://api.congress.gov/v3/congress/119?format=json"
        }

        m.get(congress_url, json={"congress": current_congress})

        current_session = self.congress.get_current_session()
        expected_current_session = self.Session(
            "119th Congress",
            "2026",
            ["House of Representatives", "Senate"]
        )
        self.assertEqual(current_session, expected_current_session)

    @requests_mock.Mocker()
    def test_get_current_congresses_returns_list(self, m):
        """Validate that get_congresses returns list type."""
        congresss_url = f"https://api.congress.gov/v3/congress?api_key={self.api_key}"
        d = self.return_mock_file_data('tests/congress_responses.txt')

        m.get(congresss_url, text=d)
        response = self.congress.get_congresses()
        self.assertIsInstance(response, list)

    @requests_mock.Mocker()
    def test_get_bills_returns_list(self, m):
        """Validate get_bills returns a list of bills."""
        bills_url = "https://api.congress.gov/v3/bill"
        d = self.return_mock_file_data('tests/bill_responses.txt')

        m.get(bills_url, text=d)
        response = self.congress.get_bills()
        first_bill = response[0]

        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 20)

        self.assertIsInstance(first_bill, Bill)
        self.assertEqual(first_bill.congress, 118)
        self.assertEqual(first_bill.latest_action_date, "2024-11-01")
        self.assertEqual(first_bill.latest_action_text,
                         "Placed on the Union Calendar, Calendar No. 615."
                         )
        self.assertEqual(first_bill.number, "7437")
        self.assertEqual(first_bill.origin_chamber, "House")
        self.assertEqual(first_bill.title,
                         "Fostering the Use of Technology to Uphold Regulatory Effectiveness in Supervision Act"
                         )
        self.assertEqual(first_bill.bill_type, "HR")
        self.assertEqual(first_bill.update_date, "2024-11-02")
        self.assertEqual(first_bill.update_including_text, "2024-11-02")
        self.assertEqual(first_bill.url, "https://api.congress.gov/v3/bill/118/hr/7437?format=json")

    @requests_mock.Mocker()
    def test_get_bills_sends_default_pagination_params(self, m):
        """Validate get_bills sends default limit and offset params."""
        bills_url = "https://api.congress.gov/v3/bill"
        m.get(bills_url, json={"bills": [self.bill_data()]})

        self.congress.get_bills()

        query = self.request_query(m.request_history[0])
        self.assertEqual(query["api_key"], [self.api_key])
        self.assertEqual(query["limit"], ["20"])
        self.assertEqual(query["offset"], ["0"])

    @requests_mock.Mocker()
    def test_get_bills_sends_custom_pagination_params(self, m):
        """Validate get_bills sends caller-provided limit and offset params."""
        bills_url = "https://api.congress.gov/v3/bill"
        m.get(bills_url, json={"bills": [self.bill_data()]})

        self.congress.get_bills(limit=50, offset=100)

        query = self.request_query(m.request_history[0])
        self.assertEqual(query["limit"], ["50"])
        self.assertEqual(query["offset"], ["100"])

    @requests_mock.Mocker()
    def test_get_bills_preserves_session_param(self, m):
        """Validate get_bills still sends the optional session param."""
        bills_url = "https://api.congress.gov/v3/bill"
        m.get(bills_url, json={"bills": [self.bill_data()]})

        self.congress.get_bills(session=118)

        query = self.request_query(m.request_history[0])
        self.assertEqual(query["session"], ["118"])
        self.assertEqual(query["limit"], ["20"])
        self.assertEqual(query["offset"], ["0"])

    @requests_mock.Mocker()
    def test_iter_bills_yields_bills_across_pages(self, m):
        """Validate iter_bills keeps fetching until a page has no bills."""
        bills_url = "https://api.congress.gov/v3/bill"
        m.get(
            bills_url,
            [
                {"json": {"bills": [self.bill_data("1")]}},
                {"json": {"bills": [self.bill_data("2")]}},
                {"json": {"bills": []}},
            ],
        )

        bills = list(self.congress.iter_bills(limit=1))

        self.assertEqual([bill.number for bill in bills], ["1", "2"])
        self.assertEqual(self.request_query(m.request_history[0])["offset"], ["0"])
        self.assertEqual(self.request_query(m.request_history[1])["offset"], ["1"])
        self.assertEqual(self.request_query(m.request_history[2])["offset"], ["2"])

    @requests_mock.Mocker()
    def test_iter_bills_stops_at_max_pages(self, m):
        """Validate iter_bills stops when max_pages is reached."""
        bills_url = "https://api.congress.gov/v3/bill"
        m.get(
            bills_url,
            [
                {"json": {"bills": [self.bill_data("1")]}},
                {"json": {"bills": [self.bill_data("2")]}},
            ],
        )

        bills = list(self.congress.iter_bills(limit=1, max_pages=1))

        self.assertEqual([bill.number for bill in bills], ["1"])
        self.assertEqual(len(m.request_history), 1)

    @requests_mock.Mocker()
    def test_get_bill_returns_single_bill(self, m):
        """Validate get_bill fetches a single bill from the /bill endpoint."""
        bill_url = f"https://api.congress.gov/v3/bill/118/hr/7437?api_key={self.api_key}"
        d = self.return_mock_file_data('tests/bill_responses.txt')
        bill_data = json.loads(d)["bills"][0]

        m.get(bill_url, json={"bill": bill_data})

        response = self.congress.get_bill(118, "hr", 7437)

        self.assertIsInstance(response, Bill)
        self.assertEqual(response.number, "7437")

    @requests_mock.Mocker()
    def test_get_bill_accepts_item_response_without_url(self, m):
        """Validate get_bill accepts item-level bill responses without url."""
        bill_url = f"https://api.congress.gov/v3/bill/118/hr/7437?api_key={self.api_key}"
        bill_data = {
            "congress": 118,
            "latestAction": {
                "actionDate": "2024-11-01",
                "text": "Placed on the Union Calendar, Calendar No. 615."
            },
            "number": "7437",
            "originChamber": "House",
            "title": (
                "Fostering the Use of Technology to Uphold Regulatory "
                "Effectiveness in Supervision Act"
            ),
            "type": "HR",
            "updateDate": "2024-11-02",
            "updateDateIncludingText": "2024-11-02"
        }

        m.get(bill_url, json={"bill": bill_data})

        response = self.congress.get_bill(118, "hr", 7437)

        self.assertIsInstance(response, Bill)
        self.assertEqual(response.number, "7437")
        self.assertIsNone(response.url)

if __name__ == '__main__':
    unittest.main()
