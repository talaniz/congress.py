# Congress SDK (Python)

A lightweight Python SDK for interacting with the United States Congress API.

This project provides a simple interface for retrieving and working with legislative data such as bills and congressional sessions, with a focus on clean abstractions and ease of use.

---

## 🚀 Features

- Fetch congressional sessions
- Retrieve bills data
- Clean API client abstraction
- Testable architecture with mocked HTTP responses
- Designed to evolve into a richer legislative intelligence layer

---

## 📦 Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/<your-username>/congress-sdk.git
cd congress-sdk
pip install -r requirements.txt
```

## 🔑 Setup

You’ll need an API key from the official Congress API.

Set your environment variable:

`export CONGRESS_KEY=your_api_key_here`

## 🧠 Usage

```
from congress.congress import CongressAPI
import os

api = CongressAPI(os.environ["CONGRESS_KEY"])

# Get congressional sessions
congresses = api.get_congresses()
print(congresses[0])

# Get bills
bills = api.get_bills()
print(bills[0])
```

## 🧪 Scripts

Raw API test (bypasses SDK)
`python scripts/fetch_congress_raw.py`

Used for:
	•	debugging API responses
	•	validating raw data format

SDK test script (TODO)
`python scripts/test_congress_sdk.py`

## 🧪 Testing
`pytest`

## 🧭 Roadmap
	•	Normalize API responses into domain models (Bill, etc.)
	•	Add query parameters (pagination, filtering)
	•	Add vote and member endpoints
	•	Implement status classification for bills
	•	Add summarization layer (LLM / local models)
	•	Expose as an MCP server for AI tooling

## 💡 Why this project exists

Most developers treat APIs like raw JSON pipes.

This project explores a different approach:
	•	turning legislative data into structured, queryable objects
	•	building a foundation for higher-level insights
	•	bridging raw data → usable intelligence

## 🙌 Contributions

Open to ideas, improvements, and extensions.

If you have thoughts on:
	•	better abstractions
	•	additional endpoints
	•	data modeling

feel free to open an issue or PR.

## 📄 License
MIT