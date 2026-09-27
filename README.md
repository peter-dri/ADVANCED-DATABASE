# ADVANCED-DATABASE — Student / Lecturer Registration

A small Flask web app where a person registers as either a student or a
lecturer, and the submissions are stored in a SQLite database using plain SQL
(the stdlib `sqlite3` module, no ORM).

## Schema

The data is normalised across three tables rather than one wide table, so no
row carries columns that do not apply to it:

| Table | Holds | Key |
| --- | --- | --- |
| `people` | what both roles share: `role`, `full_name`, `email` (unique), `phone`, `created_at` | `id` (autoincrement) |
| `students` | student-only fields: `reg_no` (unique), `course`, `year_of_study` (1–6) | `person_id` → `people(id)` |
| `lecturers` | lecturer-only fields: `staff_no` (unique), `department` | `person_id` → `people(id)` |

Each detail table uses `person_id` as both its primary key and its foreign key,
which makes the relationship to `people` one-to-one, with
`ON DELETE CASCADE` so removing a person removes their details too.
`PRAGMA foreign_keys = ON` is set on every connection, since SQLite otherwise
ignores foreign keys.

A registration writes the `people` row and the role row in a single
transaction, so a duplicate registration or staff number can never leave a
half-saved person behind.

## Setup

```bash
python -m venv venv
```

Activate it — Windows:

```bat
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

Then install and run:

```bash
pip install -r requirements.txt
python app.py
```

`data.db` is created automatically on first run, and `schema.sql` is applied at
startup, so there is no separate migration step.

## URLs

- Registration form — http://127.0.0.1:5000
- Saved records — http://127.0.0.1:5000/records

## Viewing the data

**GUI:** install [DB Browser for SQLite](https://sqlitebrowser.org), then
*Open Database* → pick `data.db` → the *Browse Data* tab.

**CLI:**

```bash
sqlite3 data.db "SELECT * FROM people;"
sqlite3 data.db "SELECT * FROM students;"
sqlite3 data.db "SELECT * FROM lecturers;"
```

To see a full student record the way the app does, join the tables:

```bash
sqlite3 data.db "SELECT p.full_name, p.email, s.reg_no, s.course, s.year_of_study FROM people p JOIN students s ON s.person_id = p.id;"
```

`data.db` is gitignored — the database is local to each checkout.
