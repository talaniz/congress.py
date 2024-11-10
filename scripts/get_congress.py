import json
import os
import requests

API_TOKEN = os.environ['CONGRESS_KEY']

CONGRESS_URL = f"https://api.congress.gov/v3/congress?api_key={API_TOKEN}"

response = requests.get(CONGRESS_URL)

print(type(json.loads(response.text)))

