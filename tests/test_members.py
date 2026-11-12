"""Tests for members.py (owner: Member 5)."""
import pytest
from library import members, books, loans
from library.storage import empty_data


def test_register_member():
    data = empty_data()
    m = members.register_member(data, " Aisha ", "Aisha@Example.com", "0800")
    assert m["name"] == "Aisha" and m["email"] == "aisha@example.com"


def test_duplicate_and_invalid_email_rejected():
    data = empty_data()
    members.register_member(data, "Aisha", "aisha@example.com")
    with pytest.raises(ValueError):
        members.register_member(data, "Other", "AISHA@example.com")
    with pytest.raises(ValueError):
        members.register_member(data, "Bad", "not-an-email")


def test_find_member():
    data = empty_data()
    members.register_member(data, "Aisha Bello", "aisha@example.com")
    assert len(members.find_member(data, "bello")) == 1


def test_cannot_remove_member_with_loan():
    data = empty_data()
    members.register_member(data, "Aisha", "aisha@example.com")
    books.add_book(data, "Book", "Author", "1")
    loans.issue_book(data, 1, 1)
    with pytest.raises(ValueError):
        members.remove_member(data, 1)


def test_remove_member():
    data = empty_data()
    members.register_member(data, "Aisha", "aisha@example.com")
    members.remove_member(data, 1)
    assert data["members"] == []
