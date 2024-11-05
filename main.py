import json
import os
import requests

API_TOKEN = os.environ['CONGRESS_KEY']

BILLS_URL = f"https://api.congress.gov/v3/congress?api_key={API_TOKEN}"

response = requests.get(BILLS_URL)

print(type(response.text))

with open('congress_responses.txt', 'w') as f:
    f.write(response.text)
