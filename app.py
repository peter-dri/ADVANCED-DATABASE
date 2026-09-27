"""Student / lecturer registration system.

Flask + SQLite with the stdlib sqlite3 module and plain SQL (no ORM).
Data lives in data.db in the repo root; it is created on first run.
"""

import os
import sqlite3

from flask import Flask, redirect, render_template, request, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

app = Flask(__name__)


# --------------------------------------------------------------------------
# Database helpers
# --------------------------------------------------------------------------

def get_db():
    """Open a connection to data.db with rows accessible by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # SQLite ignores REFERENCES clauses unless foreign keys are switched on,
    # and the setting is per-connection, so it has to be set every time.
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Create the tables if they do not exist yet, by running schema.sql."""
    with open(SCHEMA_PATH, encoding="utf-8") as fh:
        schema = fh.read()
    conn = get_db()
    try:
        conn.executescript(schema)
        conn.commit()
    finally:
        conn.close()


# Run at import time so `flask run` works as well as `python app.py`.
init_db()


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def validate(form):
    """Return a list of human-readable problems with the submitted form."""
    errors = []
    role = form.get("role", "")

    if role not in ("student", "lecturer"):
        errors.append("Please choose a role: Student or Lecturer.")

    if not form.get("full_name", "").strip():
        errors.append("Full name is required.")

    email = form.get("email", "").strip()
    if not email:
        errors.append("Email is required.")
    elif "@" not in email:
        errors.append("Email must contain '@'.")

    if role == "student":
        if not form.get("reg_no", "").strip():
            errors.append("Registration number is required for students.")
        if not form.get("course", "").strip():
            errors.append("Course is required for students.")
        year = form.get("year_of_study", "").strip()
        if not year:
            errors.append("Year of study is required for students.")
        else:
            try:
                if not 1 <= int(year) <= 6:
                    errors.append("Year of study must be between 1 and 6.")
            except ValueError:
                errors.append("Year of study must be a whole number from 1 to 6.")

    elif role == "lecturer":
        if not form.get("staff_no", "").strip():
            errors.append("Staff number is required for lecturers.")
        if not form.get("department", "").strip():
            errors.append("Department is required for lecturers.")

    return errors


def friendly_integrity_error(exc):
    """Turn a UNIQUE constraint failure into a message a user can act on."""
    message = str(exc)
    if "people.email" in message:
        return "That email address is already registered."
    if "students.reg_no" in message:
        return "That registration number is already registered."
    if "lecturers.staff_no" in message:
        return "That staff number is already registered."
    return "Those details clash with an existing record: %s" % message


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def form():
    return render_template("form.html", errors=[], form={})


@app.route("/", methods=["POST"])
def submit():
    errors = validate(request.form)
    if errors:
        return render_template("form.html", errors=errors, form=request.form), 400

    role = request.form["role"]
    conn = get_db()
    try:
        # One transaction for both inserts: `with conn` commits if the block
        # finishes and rolls back if anything raises, so a duplicate reg_no or
        # staff_no can never leave an orphaned row behind in `people`.
        # Every value is passed as a ? parameter, never formatted into the SQL.
        with conn:
            cur = conn.execute(
                "INSERT INTO people (role, full_name, email, phone)"
                " VALUES (?, ?, ?, ?)",
                (
                    role,
                    request.form["full_name"].strip(),
                    request.form["email"].strip(),
                    request.form.get("phone", "").strip() or None,
                ),
            )
            person_id = cur.lastrowid  # the AUTOINCREMENT id just allocated

            if role == "student":
                conn.execute(
                    "INSERT INTO students (person_id, reg_no, course, year_of_study)"
                    " VALUES (?, ?, ?, ?)",
                    (
                        person_id,
                        request.form["reg_no"].strip(),
                        request.form["course"].strip(),
                        int(request.form["year_of_study"]),
                    ),
                )
            else:
                conn.execute(
                    "INSERT INTO lecturers (person_id, staff_no, department)"
                    " VALUES (?, ?, ?)",
                    (
                        person_id,
                        request.form["staff_no"].strip(),
                        request.form["department"].strip(),
                    ),
                )
    except sqlite3.IntegrityError as exc:
        # Transaction already rolled back; nothing was saved.
        return render_template(
            "form.html",
            errors=[friendly_integrity_error(exc)],
            form=request.form,
        ), 400
    finally:
        conn.close()

    return redirect(url_for("records", ok=1))


@app.route("/records")
def records():
    conn = get_db()
    try:
        # Each role's view is a JOIN of the shared table with its detail table.
        students = conn.execute(
            "SELECT p.full_name, p.email, p.phone, p.created_at,"
            "       s.reg_no, s.course, s.year_of_study"
            "  FROM people p"
            "  JOIN students s ON s.person_id = p.id"
            " ORDER BY p.id DESC"
        ).fetchall()

        lecturers = conn.execute(
            "SELECT p.full_name, p.email, p.phone, p.created_at,"
            "       l.staff_no, l.department"
            "  FROM people p"
            "  JOIN lecturers l ON l.person_id = p.id"
            " ORDER BY p.id DESC"
        ).fetchall()
    finally:
        conn.close()

    return render_template(
        "records.html",
        students=students,
        lecturers=lecturers,
        ok=request.args.get("ok") == "1",
    )


if __name__ == "__main__":
    app.run(debug=True)
