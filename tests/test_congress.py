import unittest

import requests_mock

from congress.congress import CongressAPI

class TestCongress(unittest.TestCase):

    def setUp(self):
        self.api_key = "myApiKey"

    def test_congress_initialization_validates_api_key(self):
        """Ensure the Congress object is initialized with an API key."""
        with self.assertRaises(TypeError):
            congress = CongressAPI()

    @requests_mock.Mocker()
    def test_get_current_congresses_returns_list(self, m):
        """Validate that get_congresses returns list type."""
        congresss_url = f"https://api.congress.gov/v3/congress?api_key={self.api_key}"
        f = open('tests/congress_responses.txt', 'r')
        d = f.read()

        congress = CongressAPI(self.api_key)
        m.get(congresss_url, text=d)
        response = congress.get_congresses()
        self.assertIsInstance(response, list)

    @requests_mock.Mocker()
    def test_get_bills_returns_list(self,m):
        """Validate get_bills returns a list of sessions."""
        bills_url = f"https://api.congress.gov/v3/bill?api_key={self.api_key}"
        f = open('tests/bill_responses.txt', 'r')
        d = f.read()

        m.get(bills_url, text=d)
        congress = CongressAPI(self.api_key)
        response = congress.get_bills()
        self.assertIsInstance(response, list)

if __name__ == '__main__':
    unittest.main()
