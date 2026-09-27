-- MIGRATION 002 – run this SECOND, after 001
--
-- WHY THIS FILE EXISTS
-- By the time we run this, the table already has real people saved in it.
-- We want one more column: the student's course, or the lecturer's department.
--
-- We could delete the table and build a new one with the extra column, but
-- that would throw away everyone already saved. So instead we ADD to the
-- table that is already there. Like ruling one more column into a register
-- book you have already started writing in, instead of buying a new book.
--
-- The rows that were saved before this change simply have nothing in the new
-- column (the database calls that NULL, meaning "no value yet"). That is fine
-- and expected. Their name, email and phone are all untouched.
--
-- This is what a "migration" is: one small, ordered step that moves the
-- database from how it looked yesterday to how it needs to look today.


-- Add the new column. Existing rows get NULL in it.
alter table people add column course_or_department text;
