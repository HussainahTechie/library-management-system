"""Library Management System - command-line menu (owner: Member 1 - Team Lead)."""
from library import books, members, loans
from library.storage import load_data, save_data

MENU = """
===== Library Management System =====
 1. Add book              7. List members
 2. Search books          8. Issue book
 3. List books            9. Return book
 4. Edit book            10. Show overdue loans
 5. Delete book          11. Show a member's loans
 6. Register member      12. Find member
 0. Exit
"""


def ask_int(prompt):
    """Ask for a whole number, raising a friendly ValueError if invalid."""
    text = input(prompt).strip()
    if not text.lstrip("-").isdigit():
        raise ValueError("Please enter a whole number.")
    return int(text)


def show(items):
    if not items:
        print("Nothing to show.")
    for item in items:
        print(item)


def show_loans(data, items):
    """Print loans with book title, member name and any late fee."""
    if not items:
        print("Nothing to show.")
    for l in items:
        book = next((b["title"] for b in data["books"] if b["id"] == l["book_id"]), "?")
        who = next((m["name"] for m in data["members"] if m["id"] == l["member_id"]), "?")
        fine = loans.calculate_fine(l)
        extra = f" | late fee: {fine}" if fine else ""
        print(f"Loan {l['id']}: '{book}' -> {who} | due {l['due']}{extra}")


def handle(choice, data):
    """Run one menu action. Returns True if data changed."""
    if choice == "1":
        b = books.add_book(data, input("Title: "), input("Author: "),
                           input("ISBN: "), ask_int("Copies: "))
        print(f"Added book {b['id']}: {b['title']}")
        return True
    if choice == "2":
        show(books.search_books(data, input("Search: ")))
    elif choice == "3":
        show(books.list_books(data))
    elif choice == "4":
        book_id = ask_int("Book id: ")
        print("Leave a field empty to keep it unchanged.")
        copies = input("New number of copies: ").strip()
        books.edit_book(data, book_id, title=input("New title: "),
                        author=input("New author: "),
                        copies=int(copies) if copies.isdigit() else None)
        print("Book updated.")
        return True
    elif choice == "5":
        books.delete_book(data, ask_int("Book id: "))
        print("Book deleted.")
        return True
    elif choice == "6":
        m = members.register_member(data, input("Name: "), input("Email: "),
                                    input("Phone: "))
        print(f"Registered member {m['id']}: {m['name']}")
        return True
    elif choice == "7":
        show(members.list_members(data))
    elif choice == "8":
        l = loans.issue_book(data, ask_int("Book id: "), ask_int("Member id: "))
        print(f"Loan {l['id']} created. Due on {l['due']}.")
        return True
    elif choice == "9":
        l = loans.return_book(data, ask_int("Loan id: "))
        fine = loans.calculate_fine(l)
        print("Book returned." + (f" Late fee: {fine}" if fine else ""))
        return True
    elif choice == "10":
        show_loans(data, loans.overdue_loans(data))
    elif choice == "11":
        show_loans(data, loans.member_loans(data, ask_int("Member id: ")))
    elif choice == "12":
        show(members.find_member(data, input("Name or email: ")))
    else:
        print("Invalid choice.")
    return False


def main():
    data = load_data()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        try:
            if handle(choice, data):
                save_data(data)
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
