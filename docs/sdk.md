# SDK

The SDK centers on `CongressClient`. It owns endpoint construction, API-key
handling, query parameters, HTTP session usage, timeouts, status handling, JSON
decoding, pagination helpers, and conversion into typed models.

## Create a client

```python
import os

from congress_py import CongressClient

client = CongressClient(api_key=os.environ["CONGRESS_API_KEY"])
```

The SDK may be passed a custom `requests.Session`-compatible object, which is
mainly useful for tests or callers that need custom session configuration.

## Congressional sessions

```python
current = client.get_current_session()
congresses = client.get_congresses()
```

`get_current_session()` returns a named tuple with `name`, `endYear`, and
`chambers`. `get_congresses()` returns the raw `congresses` list from the API.

## Bills

```python
bills = client.get_bills(session=118, limit=20, offset=0)
recent_bills = client.list_recent_bills(limit=10)
bill = client.get_bill(118, "hr", 7437)
```

`get_bills()` returns a single page of `Bill` models. It intentionally returns
only `list[Bill]`; raw pagination metadata is not exposed by this method.
`list_recent_bills()` is a conservative convenience wrapper for the first bill
listing page and accepts limits from `1` through `250`.

## Iterating bill pages

```python
for bill in client.iter_bills(session=118, limit=20, max_pages=3):
    print(bill.number, bill.title)
```

`iter_bills()` fetches pages with increasing offsets and stops when the API
returns an empty page or when `max_pages` is reached.

## Bill workflows

```python
bill = client.get_bill(118, "hr", 7437)
actions = client.get_bill_actions(118, "hr", 7437)
summaries = client.get_bill_summaries(118, "hr", 7437)
```

These methods return `Bill`, `list[BillAction]`, and `list[BillSummary]`.

## Error handling

Project-specific authentication exceptions live in `congress_py.exceptions`.
`MissingAPIKeyError` is used when no key is available from the expected source.
`InvalidAPIKeyError` is reserved for cases where Congress.gov rejects a
provided key.
