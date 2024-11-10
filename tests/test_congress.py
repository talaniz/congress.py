import unittest

from collections import namedtuple

import requests_mock

from congress.congress import CongressAPI


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

    def test_convert_name_to_session(self):
        """Validate that the congressional name is translated to the session number."""
        self.assertEqual(self.congress._convert_name_to_session("118th Congress"), "118")
        self.assertEqual(self.congress._convert_name_to_session("22nd Congress"), "22")
        self.assertEqual(self.congress._convert_name_to_session("81st Congress"), "81")
        self.assertEqual(self.congress._convert_name_to_session("93rd Congress"), "93")

    def test_convert_congress_to_tuple(self):
        """Checks that a dictionary can be converted to a series of named tuples."""
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
        congresss_url = f"https://api.congress.gov/v3/congress?api_key={self.api_key}"
        f = open('tests/congress_responses.txt', 'r')
        d = f.read()
        f.close()

        m.get(congresss_url, text=d)
        current_session = self.congress.get_current_session()
        expected_current_session = self.Session("118th Congress", "2024",["House of Representatives", "Senate"])
        self.assertEqual(current_session, expected_current_session)

    @requests_mock.Mocker()
    def test_get_current_congresses_returns_list(self, m):
        """Validate that get_congresses returns list type."""
        congresss_url = f"https://api.congress.gov/v3/congress?api_key={self.api_key}"
        f = open('tests/congress_responses.txt', 'r')
        d = f.read()
        f.close()

        m.get(congresss_url, text=d)
        response = self.congress.get_congresses()
        self.assertIsInstance(response, list)

    @requests_mock.Mocker()
    def test_get_bills_returns_list(self,m):
        """Validate get_bills returns a list of sessions."""
        bills_url = f"https://api.congress.gov/v3/bill?api_key={self.api_key}"
        f = open('tests/bill_responses.txt', 'r')
        d = f.read()
        f.close()

        m.get(bills_url, text=d)
        response = self.congress.get_bills()
        self.assertIsInstance(response, list)

if __name__ == '__main__':
    unittest.main()
