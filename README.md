# Library Management System

A simple, open-source command-line Library Management System written in Python.
It lets a librarian manage books and members, issue and return books, and see
which loans are overdue.

## Features
- Add, edit, delete, list and search books
- Register, edit, remove and find members
- Issue and return books (14-day loan period)
- Track overdue loans and calculate late fees
- Data saved automatically to a local JSON file (no database setup needed)

## Requirements
- Python 3.8 or newer
- No external libraries (standard library only)
- `pytest` (only if you want to run the tests)

## Installation
```bash
git clone https://github.com/<your-username-or-org>/library-management-system.git
cd library-management-system
```

## Usage
```bash
python main.py
```
Pick an option from the menu by typing its number. Your data is stored in
`data/library.json`.

## Running the tests
```bash
pip install pytest
pytest
```

## Project structure
```
main.py              Menu that connects everything
library/storage.py   Load/save data (JSON)
library/books.py     Book management
library/members.py   Member management
library/loans.py     Issuing and returning books
tests/               Unit tests
```

## Contributing
Everyone is welcome to contribute! Please read [CONTRIBUTING.md](CONTRIBUTING.md)
for how to report issues, suggest features and submit pull requests. Look for
issues labelled **good first issue** to get started.

## Team
| Member | Role |
|---|---|
| NAME 1 | Team lead, project management, `main.py`, `storage.py` |
| NAME 2 | Book management (`books.py`) |
| NAME 3 | Member management (`members.py`) |
| NAME 4 | Loans (`loans.py`) |
| NAME 5 | Documentation, tests, issue templates |

## License
Released under the [MIT License](LICENSE). You are free to use, modify and
redistribute this software under the terms of that license.
