"""Book management (owner: Member 2).

A book is a dict:
    {"id": 1, "title": "...", "author": "...", "isbn": "...", "copies": 3}
`copies` is the number of copies the library owns in total.
"""
from library.storage import next_id


def _find(data, book_id):
    for book in data["books"]:
        if book["id"] == book_id:
            return book
    raise ValueError(f"No book with id {book_id}.")


def _on_loan(data, book_id):
    """Number of copies of this book currently out on loan."""
    return sum(1 for l in data["loans"]
               if l["book_id"] == book_id and l["returned"] is None)


def add_book(data, title, author, isbn, copies=1):
    """Add a new book with a unique id and return it."""
    title, author, isbn = title.strip(), author.strip(), isbn.strip()
    if not title or not author:
        raise ValueError("Title and author are required.")
    if copies < 1:
        raise ValueError("Copies must be at least 1.")
    if isbn and any(b["isbn"] == isbn for b in data["books"]):
        raise ValueError(f"A book with ISBN {isbn} already exists.")
    book = {"id": next_id(data["books"]), "title": title, "author": author,
            "isbn": isbn, "copies": copies}
    data["books"].append(book)
    return book


def edit_book(data, book_id, **changes):
    """Update title, author, isbn or copies. Empty/None values are ignored."""
    book = _find(data, book_id)
    for field, value in changes.items():
        if field not in ("title", "author", "isbn", "copies"):
            raise ValueError(f"Cannot edit field '{field}'.")
        if value is None or value == "":
            continue
        if field == "copies":
            if value < _on_loan(data, book_id):
                raise ValueError("Copies cannot be less than the number on loan.")
        elif field == "isbn" and any(
                b["isbn"] == value and b["id"] != book_id for b in data["books"]):
            raise ValueError(f"A book with ISBN {value} already exists.")
        book[field] = value
    return book


def delete_book(data, book_id):
    """Delete a book. Refuses if any copy is currently on loan."""
    book = _find(data, book_id)
    if _on_loan(data, book_id) > 0:
        raise ValueError("Cannot delete a book that is currently on loan.")
    data["books"].remove(book)
    return book


def search_books(data, keyword):
    """Return books whose title, author or ISBN contains keyword (case-insensitive)."""
    kw = keyword.strip().lower()
    return [b for b in data["books"]
            if kw in b["title"].lower() or kw in b["author"].lower()
            or kw in b["isbn"].lower()]


def list_books(data):
    """Return all books."""
    return list(data["books"])
