"""Tests for storage (Member 1 / Member 5)."""
import os
import tempfile
from library.storage import empty_data, load_data, save_data


def test_save_and_load_roundtrip():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "lib.json")
        data = empty_data()
        data["books"].append({"id": 1, "title": "Test"})
        save_data(data, path)
        assert load_data(path) == data


def test_load_missing_file_returns_empty():
    assert load_data("does-not-exist.json") == empty_data()
