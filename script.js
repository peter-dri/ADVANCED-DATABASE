// script.js – everything the page does, in 5 numbered steps.


// 1. CONNECT TO THE DATABASE
// This makes one object, called db, that we use for every question we ask
// the database. SUPABASE_URL and SUPABASE_KEY come from config.js.
const db = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);


// 2. SHOW EVERYONE WHO IS SAVED
// "async" and "await" just mean: wait for the internet to answer before
// carrying on to the next line.
async function showPeople() {
  // Ask for every column of every row, oldest first.
  const result = await db.from("people").select("*").order("id");

  const list = document.getElementById("list");
  list.textContent = "";                      // empty the table first

  if (result.error) {
    showMessage("Could not load the list: " + result.error.message, "red");
    return;
  }

  // Go through the rows one at a time and build a table row for each.
  result.data.forEach(function (person) {
    const row = document.createElement("tr");

    // The six values, in the same order as the table headings.
    const values = [
      person.id,
      person.role,
      person.name,
      person.email,
      person.phone,
      person.course_or_department
    ];

    values.forEach(function (value) {
      const cell = document.createElement("td");
      // textContent writes the value as plain text.
      // If someone typed <script> into the form, it shows up as the harmless
      // words "<script>" instead of running. Never use innerHTML here.
      // A missing value (NULL in the database) is shown as an empty cell.
      cell.textContent = (value === null || value === undefined) ? "" : value;
      row.appendChild(cell);
    });

    list.appendChild(row);
  });
}


// 3. SAVE A NEW PERSON WHEN THE FORM IS SENT
document.getElementById("myForm").addEventListener("submit", async function (event) {
  // Stop the browser reloading the page, which is its normal habit.
  event.preventDefault();

  // Collect what was typed into one object. The names on the left must match
  // the column names in the database exactly.
  const person = {
    role: document.querySelector('input[name="role"]:checked').value,
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    phone: document.getElementById("phone").value,
    course_or_department: document.getElementById("course").value
  };

  // Send it. The database checks its own rules before accepting it.
  const result = await db.from("people").insert(person);

  if (result.error) {
    // For example: the email is already in the register.
    showMessage("Not saved: " + result.error.message, "red");
  } else {
    showMessage("Saved to the database!", "green");
    document.getElementById("myForm").reset();   // empty the form
    showPeople();                                 // show the new row
  }
});


// 4. A LITTLE HELPER FOR MESSAGES
// Puts some words on the page in the colour we ask for.
function showMessage(text, colour) {
  const message = document.getElementById("message");
  message.textContent = text;
  message.style.color = colour;
}


// 5. THE REFRESH BUTTON, AND THE FIRST LOAD
document.getElementById("refresh").addEventListener("click", showPeople);

// Show the list straight away when the page opens.
showPeople();
