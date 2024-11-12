import unittest

from collections import namedtuple

import requests_mock

from congress.congress import CongressAPI
from congress.bills import Bill


class TestCongressAPIValidation(unittest.TestCase):

    def test_congress_initialization_validates_api_key(self):
        """Ensure the Congress object is initialized with an API key."""
        with self.assertRaises(TypeError):
            congress = CongressAPI()


class TestCongressAPI(unittest.TestCase):

    def setUp(self):
        self.api_key = "myApiKey"
        self.congress = CongressAPI(self.api_key)
        self.Session = namedtuple("Session", ['name', 'endYear', 'chambers'])

    def return_mock_file_data(self, filename):
        """Open the file with mock data and return the contets."""
        with open(filename, 'r') as f:
            d = f.read()
            return d

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
    def test_get_current_congresses_returns_list(self, m):
        """Validate that get_congresses returns list type."""
        congresss_url = f"https://api.congress.gov/v3/congress?api_key={self.api_key}"
        d = self.return_mock_file_data('tests/congress_responses.txt')

        m.get(congresss_url, text=d)
        response = self.congress.get_congresses()
        self.assertIsInstance(response, list)

    @requests_mock.Mocker()
    def test_get_bills_returns_list(self,m):
        """Validate get_bills returns a list of bills."""
        bills_url = f"https://api.congress.gov/v3/bill?api_key={self.api_key}"
        d = self.return_mock_file_data('tests/bill_responses.txt')

        m.get(bills_url, text=d)
        response = self.congress.get_bills()
        first_bill = response[0]

        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 20)
        
        self.assertIsInstance(first_bill, Bill)
        self.assertEqual(first_bill.congress, 118)
        self.assertIsInstance(first_bill.latest_action, dict)
        self.assertEqual(first_bill.latest_action['actionDate'], "2024-11-01")
        self.assertEqual(first_bill.latest_action['text'],
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

if __name__ == '__main__':
    unittest.main()
