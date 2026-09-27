-- ADVANCED-DATABASE: student/lecturer registration schema.
--
-- Normalised into 3 tables instead of one wide table:
--   people    - the fields every person has, whatever their role
--   students  - the student-only fields, keyed 1:1 to people.id
--   lecturers - the lecturer-only fields, keyed 1:1 to people.id
-- A person therefore has exactly one row in people and one row in the
-- table matching their role. No NULL-padded columns for the "other" role.

-- Shared attributes for both roles.
CREATE TABLE IF NOT EXISTS people (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    role       TEXT NOT NULL CHECK (role IN ('student','lecturer')),
    full_name  TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    phone      TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Student-only attributes. person_id is both the primary key and the
-- foreign key, which enforces the 1:1 relationship with people.
CREATE TABLE IF NOT EXISTS students (
    person_id     INTEGER PRIMARY KEY REFERENCES people(id) ON DELETE CASCADE,
    reg_no        TEXT NOT NULL UNIQUE,
    course        TEXT NOT NULL,
    year_of_study INTEGER NOT NULL CHECK (year_of_study BETWEEN 1 AND 6)
);

-- Lecturer-only attributes, same 1:1 pattern as students.
CREATE TABLE IF NOT EXISTS lecturers (
    person_id  INTEGER PRIMARY KEY REFERENCES people(id) ON DELETE CASCADE,
    staff_no   TEXT NOT NULL UNIQUE,
    department TEXT NOT NULL
);
