# Library Management System

An open-source, command-line Library Management System written in Python.
It helps a librarian keep track of books and members, issue and return books,
and see which loans are overdue, with late fees calculated automatically.

> **Status:** complete and working. Contributions and ideas are welcome!

---

## Table of contents
1. [Purpose](#purpose)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Example session](#example-session)
7. [User guide](#user-guide)
8. [How the data is stored](#how-the-data-is-stored)
9. [Project structure](#project-structure)
10. [Running the tests](#running-the-tests)
11. [How to contribute](#how-to-contribute)
12. [Open-source principles followed](#open-source-principles-followed)
13. [Roadmap](#roadmap)
14. [Authors](#authors)
15. [License](#license)

---

## Purpose
Small libraries (schools, community centres, personal collections) often track
books on paper or in spreadsheets, which makes it hard to know who has which
book or what is overdue. This project provides a simple, free tool that anyone
can run, read, modify and improve. It was built as a group project to
demonstrate open-source collaboration.

---

## Features
- **Books:** add, edit, delete, list and search (by title, author or ISBN)
- **Members:** register, edit, remove, list and find (by name or email)
- **Loans:** issue and return books with a 14-day loan period
- **Overdue tracking:** list all overdue loans
- **Late fees:** calculated per day overdue (default 50 per day)
- **Safety checks:** no duplicate ISBNs or emails, cannot delete a book that
  is on loan, cannot remove a member who still has books, cannot issue a book
  with no free copies
- **Automatic saving:** all changes are saved to a local JSON file
- **No setup headaches:** uses only Python's standard library

---

## Requirements
- Python **3.8 or newer** ([download](https://www.python.org/downloads/))
- Git (to clone the repository)
- `pytest` (optional, only for running the tests)

No other libraries or database are needed.

---

## Installation
```bash
git clone https://github.com/HussainahTechie/library-management-system.git
cd library-management-system
```

Check that Python is installed:
```bash
python --version
```
(On some systems the command is `python3`.)

---

## Usage
Start the program:
```bash
python main.py
```
A menu appears. Type the number of an action and press Enter:

| Option | Action |
|---|---|
| 1 | Add a book |
| 2 | Search books |
| 3 | List all books |
| 4 | Edit a book |
| 5 | Delete a book |
| 6 | Register a member |
| 7 | List members |
| 8 | Issue a book to a member |
| 9 | Return a book |
| 10 | Show overdue loans |
| 11 | Show a member's current loans |
| 12 | Find a member |
| 0 | Exit |

A recommended first run: add a book (1), register a member (6), issue the
book (8), show the member's loans (11), then return it (9).
See the [User guide](#user-guide) below for a full walkthrough.

---

## Example session
```
Choose an option: 1
Title: Things Fall Apart
Author: Chinua Achebe
ISBN: 111
Copies: 2
Added book 1: Things Fall Apart

Choose an option: 6
Name: Aisha Bello
Email: aisha@example.com
Phone: 08012345678
Registered member 1: Aisha Bello

Choose an option: 8
Book id: 1
Member id: 1
Loan 1 created. Due on 2026-11-25.

Choose an option: 11
Member id: 1
Loan 1: 'Things Fall Apart' -> Aisha Bello | due 2026-11-25
```

---

## User guide
Step-by-step instructions for every feature.

### Starting the program
Open a terminal in the project folder and run:
```
python main.py
```
You will see the main menu. Type a number and press **Enter**. Type **0** to exit.
Your data is saved automatically after every change.

### Managing books

#### Add a book (option 1)
You are asked for the title, author, ISBN and number of copies.
- Title and author are required.
- ISBN must be unique (leave it blank if the book has none).
- Copies must be a whole number of 1 or more.

#### Search books (option 2)
Type any part of a title, author or ISBN. The search ignores capital letters,
so `achebe` finds "Chinua Achebe".

#### List books (option 3)
Shows every book with its id, title, author, ISBN and total copies.

#### Edit a book (option 4)
Enter the book's id, then new values. **Leave a field empty to keep it as it is.**
You cannot reduce the copies below the number currently on loan.

#### Delete a book (option 5)
Enter the book's id. A book that is currently on loan cannot be deleted.

### Managing members

#### Register a member (option 6)
Enter a name, a valid email (like `name@example.com`) and an optional phone
number. Two members cannot share the same email.

#### List members (option 7) and find members (option 12)
List shows everyone. Find searches by part of a name or email.

### Loans

#### Issue a book (option 8)
Enter the book id and member id. The system checks that:
- the book and member exist,
- at least one copy is available,
- the member does not already have this book.

The due date is **14 days** from today.

#### Return a book (option 9)
Enter the **loan id** (shown when the loan was created, or in option 11).
If the book is late, the late fee is displayed.

#### Show a member's loans (option 11)
Enter a member id to see the books they currently have and when each is due.

#### Show overdue loans (option 10)
Lists loans past their due date, with the book title, member name and late fee.

### Late fees
`late fee = days overdue x 50`

The rate can be changed by editing `FINE_PER_DAY` in `library/loans.py`.

### Common messages

| Message | Meaning and fix |
|---|---|
| `Nothing to show.` | No results. Add data first, or try a different search word. |
| `Please enter a whole number.` | A number was expected (for example an id). |
| `No book with id X.` | That id does not exist. Check with option 3. |
| `No copies of this book are available.` | All copies are on loan. Wait for a return. |
| `Cannot delete a book that is currently on loan.` | Return the book first. |
| `Cannot remove a member who still has books on loan.` | Return their books first. |
| `A book with ISBN X already exists.` | Use a different ISBN or edit the existing book. |
| `A member with email X already exists.` | Use a different email. |

### Backing up and resetting data
- **Backup:** copy `data/library.json` somewhere safe.
- **Reset:** delete `data/library.json`. The next run starts with an empty library.

---

## How the data is stored
Everything is saved in `data/library.json`, created automatically the first
time you add something. It contains three lists:

```json
{
  "books":   [{"id": 1, "title": "...", "author": "...", "isbn": "...", "copies": 2}],
  "members": [{"id": 1, "name": "...", "email": "...", "phone": "..."}],
  "loans":   [{"id": 1, "book_id": 1, "member_id": 1,
               "issued": "2026-11-11", "due": "2026-11-25", "returned": null}]
}
```
The file is plain text, so you can back it up by copying it. It is excluded
from Git (`.gitignore`) so personal data is never published.

---

## Project structure
```
library-management-system/
├── main.py                 Menu that connects everything
├── library/
│   ├── storage.py          Load/save the JSON data file
│   ├── books.py            Book management
│   ├── members.py          Member management
│   └── loans.py            Issuing, returning, overdue items, fines
├── tests/                  Automated tests (pytest)
├── CONTRIBUTING.md         How to contribute
├── LICENSE                 MIT License
└── .github/                Issue and pull request templates
```

---

## Running the tests
```bash
pip install pytest
pytest
```
All tests should pass. They cover adding, searching, editing and deleting
books, registering members, issuing and returning books, overdue loans and
late fees.

---

## How to contribute
Anyone can help, whether by reporting a bug, suggesting a feature, improving
the documentation or writing code.

1. **Browse the code:** it is all public in this repository.
2. **Report a problem or suggest an idea:** open an
   [Issue](../../issues) using the bug or feature template.
3. **Contribute code:** fork the repo, create a branch, make your change,
   run `pytest`, and open a Pull Request.
4. **Start small:** look for issues labelled **good first issue**.

Full instructions are in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Open-source principles followed
| Principle | How this project meets it |
|---|---|
| Source code availability | Full source on a public GitHub repository |
| Open-source licence | MIT License (see [LICENSE](LICENSE)) |
| Documentation | This README, the User Guide and code docstrings |
| Collaboration and version control | Git branches, pull requests and code reviews on GitHub |
| Community participation | Issue templates, CONTRIBUTING.md and "good first issue" labels |
| Transparency | All work is tracked openly through issues, commits and pull requests on GitHub |

---

## Roadmap
Ideas for future contributors (see the issue tracker):
- Export books and loans to CSV
- Report of the most borrowed books
- Configurable loan period and fine rate
- Book categories and filtering
- A graphical or web interface
- Switch storage to SQLite

---

## Authors
Built as a group project on open-source software.
Repository: https://github.com/HussainahTechie/library-management-system

---

## License
Released under the [MIT License](LICENSE). You are free to use, copy, modify,
merge, publish and distribute this software, provided the licence notice is
kept. The software is provided "as is", without warranty.
