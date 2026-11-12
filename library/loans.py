"""Loans: issuing and returning books (owner: Member 4).

A loan is a dict:
    {"id": 1, "book_id": 1, "member_id": 1,
     "issued": "2026-11-11", "due": "2026-11-25", "returned": None}
Dates are ISO strings (YYYY-MM-DD). `returned` is None until the book is back.
"""
from datetime import date, timedelta

from library.storage import next_id

LOAN_DAYS = 14
FINE_PER_DAY = 50  # late fee per day (currency units)


def _book_exists(data, book_id):
    return any(b["id"] == book_id for b in data["books"])


def _member_exists(data, member_id):
    return any(m["id"] == member_id for m in data["members"])


def available_copies(data, book_id):
    """Return how many copies of the book are not currently on loan."""
    book = next((b for b in data["books"] if b["id"] == book_id), None)
    if book is None:
        raise ValueError(f"No book with id {book_id}.")
    on_loan = sum(1 for l in data["loans"]
                  if l["book_id"] == book_id and l["returned"] is None)
    return book["copies"] - on_loan


def issue_book(data, book_id, member_id, today=None):
    """Create a loan if the book has a free copy and the member exists."""
    today = today or date.today()
    if not _book_exists(data, book_id):
        raise ValueError(f"No book with id {book_id}.")
    if not _member_exists(data, member_id):
        raise ValueError(f"No member with id {member_id}.")
    if available_copies(data, book_id) < 1:
        raise ValueError("No copies of this book are available.")
    if any(l["book_id"] == book_id and l["member_id"] == member_id
           and l["returned"] is None for l in data["loans"]):
        raise ValueError("This member already has this book.")
    loan = {"id": next_id(data["loans"]), "book_id": book_id,
            "member_id": member_id, "issued": today.isoformat(),
            "due": (today + timedelta(days=LOAN_DAYS)).isoformat(),
            "returned": None}
    data["loans"].append(loan)
    return loan


def return_book(data, loan_id, today=None):
    """Mark a loan as returned (sets the returned date)."""
    today = today or date.today()
    loan = next((l for l in data["loans"] if l["id"] == loan_id), None)
    if loan is None:
        raise ValueError(f"No loan with id {loan_id}.")
    if loan["returned"] is not None:
        raise ValueError("This book has already been returned.")
    loan["returned"] = today.isoformat()
    return loan


def calculate_fine(loan, today=None):
    """Late fee for a loan: days overdue x FINE_PER_DAY (0 if on time)."""
    today = today or date.today()
    end = date.fromisoformat(loan["returned"]) if loan["returned"] else today
    days_late = (end - date.fromisoformat(loan["due"])).days
    return max(days_late, 0) * FINE_PER_DAY


def overdue_loans(data, today=None):
    """Return all unreturned loans whose due date has passed."""
    today = today or date.today()
    return [l for l in data["loans"]
            if l["returned"] is None and date.fromisoformat(l["due"]) < today]


def member_loans(data, member_id):
    """Return all current (unreturned) loans of a member."""
    return [l for l in data["loans"]
            if l["member_id"] == member_id and l["returned"] is None]
