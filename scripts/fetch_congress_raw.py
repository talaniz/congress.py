"""Testing module for Congress API access. This script retrieves the list of
 congresses and prints some information about the response.
Make sure to set the CONGRESS_KEY environment variable with your API token
before running this script."""

import os
import requests

if __name__ == "__main__":
    api_token = os.environ.get("CONGRESS_KEY")
    if not api_token:
        raise ValueError("CONGRESS_KEY not set")

    congress_url = (
        f"https://api.congress.gov/v3/congress"
        f"?api_key={api_token}&format=json"
    )

    response = requests.get(congress_url, timeout=10)
    response.raise_for_status()

    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Body preview:", response.text[:500])
        raise

    print(type(data))
    print(data.keys())
    print("Top-level keys:", data.keys())
    print("First congress:", data["congresses"][0])
