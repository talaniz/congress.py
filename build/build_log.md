# Build Log

## Session 01: Stabilize SDK - Complete

Session 01 is complete. The project was refactored into a `src`-based Python package named `congress_py`.

Completed work:

- `CongressAPI` was moved to `src/congress_py/client.py` and renamed `CongressClient`.
- `Bill` was moved to `src/congress_py/models.py`.
- Existing public methods were preserved: `get_current_session`, `get_congresses`, `get_bills`, and `get_bill`.
- Endpoint construction was updated so congress endpoints use `/congress` and bill endpoints use `/bill`.
- HTTP requests now use `requests.Session`, `params`, `timeout=10`, `raise_for_status()`, and `response.json()`.
- Tests were updated to import from `congress_py`.
- No new features were added.

Validation:

```bash
.venv/bin/python -m pytest
```

Result: `7 passed in 0.02s`.

Next recommended action: start Session 02 by adding `get_bill_actions` with tests.
