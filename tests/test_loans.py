"""Tests for loans.py (owner: Member 5)."""
from datetime import date

import pytest
from library import books, members, loans
from library.storage import empty_data


def make(copies=1):
    data = empty_data()
    books.add_book(data, "Book", "Author", "1", copies)
    members.register_member(data, "Aisha", "aisha@example.com")
    members.register_member(data, "Musa", "musa@example.com")
    return data


def test_issue_sets_due_date():
    data = make()
    l = loans.issue_book(data, 1, 1, today=date(2026, 11, 1))
    assert l["due"] == "2026-11-15"
    assert loans.available_copies(data, 1) == 0


def test_cannot_issue_when_no_copies_left():
    data = make(copies=1)
    loans.issue_book(data, 1, 1)
    with pytest.raises(ValueError):
        loans.issue_book(data, 1, 2)


def test_cannot_issue_unknown_book_or_member():
    data = make()
    with pytest.raises(ValueError):
        loans.issue_book(data, 99, 1)
    with pytest.raises(ValueError):
        loans.issue_book(data, 1, 99)


def test_return_frees_copy_and_cannot_return_twice():
    data = make()
    l = loans.issue_book(data, 1, 1)
    loans.return_book(data, l["id"])
    assert loans.available_copies(data, 1) == 1
    with pytest.raises(ValueError):
        loans.return_book(data, l["id"])


def test_overdue_and_fine():
    data = make()
    l = loans.issue_book(data, 1, 1, today=date(2026, 11, 1))
    assert loans.overdue_loans(data, today=date(2026, 11, 15)) == []
    late = date(2026, 11, 18)
    assert loans.overdue_loans(data, today=late) == [l]
    assert loans.calculate_fine(l, today=late) == 3 * loans.FINE_PER_DAY


def test_member_loans_only_current():
    data = make(copies=2)
    a = loans.issue_book(data, 1, 1)
    loans.return_book(data, a["id"])
    assert loans.member_loans(data, 1) == []
