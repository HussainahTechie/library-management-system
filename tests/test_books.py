"""Tests for books.py (owner: Member 5)."""
import pytest
from library import books, loans
from library.members import register_member
from library.storage import empty_data


def make():
    data = empty_data()
    books.add_book(data, "Things Fall Apart", "Chinua Achebe", "111", 2)
    return data


def test_add_book_assigns_ids():
    data = make()
    b = books.add_book(data, "Half of a Yellow Sun", "Chimamanda Adichie", "222")
    assert b["id"] == 2 and len(data["books"]) == 2


def test_add_book_rejects_duplicate_isbn_and_bad_input():
    data = make()
    with pytest.raises(ValueError):
        books.add_book(data, "X", "Y", "111")
    with pytest.raises(ValueError):
        books.add_book(data, "", "Y", "333")
    with pytest.raises(ValueError):
        books.add_book(data, "X", "Y", "333", 0)


def test_search_is_case_insensitive():
    data = make()
    assert len(books.search_books(data, "achebe")) == 1
    assert books.search_books(data, "zzz") == []


def test_edit_book_ignores_blank_values():
    data = make()
    books.edit_book(data, 1, title="New Title", author="")
    assert data["books"][0]["title"] == "New Title"
    assert data["books"][0]["author"] == "Chinua Achebe"


def test_cannot_delete_book_on_loan():
    data = make()
    register_member(data, "Aisha", "aisha@example.com")
    loans.issue_book(data, 1, 1)
    with pytest.raises(ValueError):
        books.delete_book(data, 1)


def test_delete_book():
    data = make()
    books.delete_book(data, 1)
    assert data["books"] == []
