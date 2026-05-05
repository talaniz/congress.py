# congress_py

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
git clone https://github.com/<your-username>/congress.py.git
cd congress.py
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install -e .
```

## 🔑 Setup

You’ll need an API key from the official Congress API.

Set your environment variable:

`export CONGRESS_API_KEY=your_api_key_here`

The CLI also supports saving a local key for developer convenience:

```bash
congress configure
```

CLI credential resolution order:

1. `--api-key`
2. `CONGRESS_API_KEY`
3. `~/.congress/config.toml`

## 🧠 Usage

```
import os

from congress_py import CongressClient

client = CongressClient(os.environ["CONGRESS_API_KEY"])

# Get congressional sessions
congresses = client.get_congresses()
print(congresses[0])

# Get bills
bills = client.get_bills()
print(bills[0])
```

## 🖥️ CLI

The package installs a `congress` command. Output is JSON by default.

```bash
congress congress current
congress congress list
congress bills list
congress bills list --session 118
congress bills get 118 hr 7437
```

You can pass an API key explicitly for a single command:

```bash
congress --api-key your_api_key_here bills get 118 hr 7437
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
`.venv/bin/python -m pytest`

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
