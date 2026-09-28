create table people (
  id bigint generated always as identity primary key,

  role text not null check (role in ('Student','Lecturer')),

  name text not null,
  
  email text not null unique,

  phone text,

  created_at timestamptz not null default now()
);

alter table people enable row level security;

create policy "Anyone can register"
  on people
  for insert
  to anon
  with check (true);

create policy "Anyone can view"
  on people
  for select
  to anon
  using (true);

grant select, insert on people to anon;
