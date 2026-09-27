# My School Register

A small website where a student or lecturer fills in a form, and their details
are saved in a real database on the internet (Supabase, which is PostgreSQL).
The saved people are then listed in a table on the same page.

It is built with plain HTML, CSS and JavaScript. There is nothing to install
and nothing to build — you open the file and it works.

## The files

| File | What it does |
| --- | --- |
| `index.html` | The page itself: the form and the table. |
| `style.css` | The colours, spacing and fonts. |
| `script.js` | Saves the form to the database and lists what is saved. |
| `config.js` | Your two Supabase settings. You must edit this one. |
| `migrations/001_create_people_table.sql` | Makes the table and its safety rules. Run first. |
| `migrations/002_add_course_or_department.sql` | Adds one more column later. Run second. |

## Setup

1. Go to [supabase.com](https://supabase.com) and create a free account and a
   new project. Wait a minute for it to finish setting up.
2. In the left-hand menu, open the **SQL Editor**.
3. Open `migrations/001_create_people_table.sql`, copy all of it, paste it into
   the SQL Editor, and press **Run**. You should see "Success".
4. Do the same with `migrations/002_add_course_or_department.sql`. Run them in
   this order, 001 then 002.
5. Go to **Project Settings → API Keys** and copy two things:
   - the **Project URL**
   - the **publishable** key (older projects call this the **anon** key)
6. Open `config.js` and paste them in, replacing the placeholder text.
7. Open `index.html` in your browser by double-clicking it. Fill in the form
   and press Save.

If nothing saves, open the browser console (press F12) and read the red text.
It is almost always a typo in `config.js`.

## Demo for the lecturer

Three things to show, in this order.

### A. Data arrives in the database

Put two windows side by side: the website on one side, and the Supabase
**Table Editor** (with the `people` table open) on the other.

1. Fill in the form on the website and press **Save**.
2. The green words "Saved to the database!" appear, and the new person shows up
   in the table at the bottom of the page.
3. Press **Refresh** in the Supabase Table Editor. The same person is now a row
   in the real database.

Point out the two columns nobody typed: `id` and `created_at`. The database
filled those in by itself — `id` counts the rows, and `created_at` stamps the
date and time.

### B. The database protects itself

The point here is that the rules live in the *database*, not in the web page.
Even a broken or dishonest page cannot get past them.

| Try this | What happens | Which rule stopped it |
| --- | --- | --- |
| Register a second person with an email that is already saved | Red message: "Not saved: duplicate key value violates unique constraint" | `email text not null unique` |
| Send a role that is not Student or Lecturer | The row is refused | `check (role in ('Student','Lecturer'))` |

The second one is worth showing properly, because the form's radio buttons
only offer the two allowed words. To get around the page and talk straight to
the database, open the browser console (F12) on the website and paste:

```js
await db.from("people").insert({ role: "Headmaster", name: "Sneaky", email: "sneaky@example.com" })
```

Read the error out loud: the database rejected `Headmaster` because of the
CHECK rule. This is the difference between checking in the page (polite
suggestion) and checking in the database (actual rule).

You can also mention what visitors **cannot** do. Migration 001 gives them
permission to add and to view, and deliberately gives no permission to change
or delete. So nobody can edit or erase another person's details.

### C. How migrations work

A migration is one numbered file holding one small change to the database.
Together they are the history of how the database got to be the way it is.

| File | The change it makes | When it ran |
| --- | --- | --- |
| `001_create_people_table.sql` | Creates `people` with role, name, email, phone, created_at, and the security rules | First |
| `002_add_course_or_department.sql` | Adds the `course_or_department` column | Second, later |

**The live demo.** This is the part that makes migrations click, so do it on a
fresh project if you can:

1. Run **only** `001`.
2. On the website, register two people. They save fine — there is no
   course/department column yet, so that box is simply ignored.
3. Now run `002`.
4. Refresh the Supabase Table Editor. There is a new `course_or_department`
   column, and the two people from step 2 are **still there**, with the new
   column empty (`NULL`) for them.
5. Register a third person, this time filling in the course box. Their row has
   it; the older two still do not.

That is the whole idea: the database changed shape without losing anybody.

**The four rules of migrations**

1. Run them in number order: 001, then 002, then 003.
2. Never edit a migration that has already run. It has already done its job on
   the real database, so changing the file now would be a lie about history.
3. For the next change, add a new file: `003_something.sql`.
4. Keep them all in Git, so anyone who clones this project can rebuild the
   same database from scratch by running them in order.

## Good to know

**The key in `config.js` is meant to be public.** It is not a password, and it
is safe in a public GitHub repository. Anyone can read it in the page source —
that is normal and by design. The security comes from Row Level Security in
migration 001: the key only lets a visitor do the things the policies allow,
which here is adding a person and viewing the list.

**Anyone can view the list.** That is what the "Anyone can view" policy says,
so treat everything saved as public. Use made-up names, emails and phone
numbers for the demo, never real personal details of real people.

**Publishing it for free.** Because it is only HTML, CSS and JavaScript, GitHub
can host it: in your repository go to **Settings → Pages**, set the branch to
`main`, and save. After a minute GitHub gives you a public web address for the
site.
