"""Storage layer (owner: Member 1 - Team Lead).

All data lives in one JSON file with three lists: books, members, loans.
Every other module receives this `data` dict and modifies it in place;
main.py calls save_data() after each change.
"""
import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "library.json")


def empty_data():
    return {"books": [], "members": [], "loans": []}


def load_data(path=DATA_FILE):
    """Load data from disk, or return empty data if the file does not exist."""
    if not os.path.exists(path):
        return empty_data()
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data, path=DATA_FILE):
    """Write data to disk."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def next_id(items):
    """Return the next free integer id for a list of dicts that have an 'id'."""
    return max((item["id"] for item in items), default=0) + 1
