import unittest

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

    def test_convert_name_to_session(self):
        """Validate that the congressional name is translated to the session number."""
        self.assertEqual(self.congress._convert_name_to_session("118th Congress"), "118")
        self.assertEqual(self.congress._convert_name_to_session("22nd Congress"), "22")
        self.assertEqual(self.congress._convert_name_to_session("81st Congress"), "81")
        self.assertEqual(self.congress._convert_name_to_session("93rd Congress"), "93")

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
