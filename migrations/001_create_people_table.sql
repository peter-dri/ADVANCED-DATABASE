-- MIGRATION 001 – run this FIRST in Supabase SQL Editor
--
-- Copy everything in this file, paste it into the Supabase SQL Editor,
-- and press Run. You only ever need to do this once.


-- STEP 1: Make the table.
-- This is like drawing an empty register book with columns at the top.
-- Nothing is written in it yet, we are just making the blank page.
create table people (
  -- id: the row number. The database fills this in for us, 1, 2, 3...
  id bigint generated always as identity primary key,

  -- role: must be exactly 'Student' or 'Lecturer'.
  -- The "check" is like a bouncer on the door: anything else is turned away.
  role text not null check (role in ('Student','Lecturer')),

  -- name: required, because a register with no names is not much use.
  name text not null,

  -- email: required, and "unique" means no two people can share one.
  email text not null unique,

  -- phone: optional, so it is allowed to be empty.
  phone text,

  -- created_at: the date and time the row was added.
  -- "default now()" means the database stamps it for us automatically.
  created_at timestamptz not null default now()
);


-- STEP 2: Lock the table.
-- Row Level Security means "nobody may touch this table unless a rule below
-- says they may". Like locking the register in a cupboard before deciding
-- who gets a key.
alter table people enable row level security;


-- STEP 3: Hand out the keys, one rule at a time.
-- "anon" means an ordinary visitor to the website who has not logged in.

-- Key 1: a visitor may ADD a new person.
-- "with check (true)" means every new row is accepted.
create policy "Anyone can register"
  on people
  for insert
  to anon
  with check (true);

-- Key 2: a visitor may READ the list.
-- "using (true)" means they can see every row.
create policy "Anyone can view"
  on people
  for select
  to anon
  using (true);

-- Notice what is NOT here: no rule for update and no rule for delete.
-- Because we never handed out those keys, a visitor cannot change or erase
-- anyone's details. The safest rule is the one you never write.


-- STEP 4: Say which actions are allowed at all.
-- The policies above are the "who", this line is the "what".
-- A visitor gets reading and adding, and nothing else.
grant select, insert on people to anon;
