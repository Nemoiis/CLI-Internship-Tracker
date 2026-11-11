# Internship Application Tracker

A command-line app for keeping track of internship applications, built with Python and SQLite. Add an application, update its status as things progress, and search or filter your list, all from a simple menu.

I built this to get hands-on with `sqlite3`: creating tables, running parameterized queries, and handling user input safely.

## Features

- **Add** an application with company, role, status, and date (today's date or a manually entered one)
- **View** all applications in a formatted table
- **Search** by company name (partial matches work, e.g. `goog` finds `Google`)
- **Filter** by status or by date (partial dates work, e.g. `2026/11` shows everything from November)
- **Update** an application's status
- **Delete** an application by ID
- Input validation throughout: blank fields, invalid dates, and non-numeric IDs are caught and re-prompted

## Requirements

- Python 3.8 or newer
- No third-party packages. It only uses the standard library (`sqlite3`, `datetime`).

## Getting Started

```bash
git clone https://github.com/Nemoiis/CLI-Internship-Tracker.git
cd internship-tracker
python tracker.py
```

The first run creates a local `tracker.db` file automatically. Your data stays on your machine and is not part of the repository.

## Usage

```
╔════════════════════════════════════════╗
║          INTERNSHIP DATABASE           ║
╠════════════════════════════════════════╣
║  [1]  Add an Entry                     ║
║  [2]  View all Entries                 ║
║  [3]  Search by Company                ║
║  [4]  Filter Entries                   ║
║  [5]  Update an Entry's Status         ║
║  [6]  Delete an Entry                  ║
║  [0]  Exit                             ║
╚════════════════════════════════════════╝
```

Example of option 2 (View all Entries):

```
ID   Company        Role           Status      Date
---------------------------------------------------------
1    Acme           SWE Intern     Applied     2026/01/05
```

**Statuses:** `Applied`, `Interview`, `Offer`, `Rejected` (chosen by entering 1-4)

**Dates:** stored as `YYYY/MM/DD`

## How It Works

Data is stored in a single SQLite table:

| Column    | Type                | Notes                          |
|-----------|---------------------|--------------------------------|
| `custID`  | INTEGER PRIMARY KEY | Auto-assigned unique ID        |
| `company` | TEXT NOT NULL       |                                |
| `role`    | TEXT NOT NULL       |                                |
| `status`  | TEXT NOT NULL       | Applied / Interview / Offer / Rejected |
| `date`    | TEXT NOT NULL       | `YYYY/MM/DD`                   |

All queries use parameterized statements (`?` placeholders) rather than string formatting, which keeps user input from being interpreted as SQL.

## What I Practiced

- Creating tables and writing CRUD queries with `sqlite3`
- Parameterized queries and `LIKE` pattern matching
- Committing transactions and checking `cursor.rowcount` for feedback
- Validating input with `try/except` and re-prompt loops
- Organizing a script into small, single-purpose functions

## Possible Next Steps

- Summary view showing a count of applications per status
- Export to CSV
- Notes and posting-URL columns
- Confirmation prompt before deleting

## License

MIT
