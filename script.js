const db = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

document.getElementById("myForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const person = {
    role: document.querySelector('input[name="role"]:checked').value,
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    phone: document.getElementById("phone").value,
    course_or_department: document.getElementById("course").value
  };

  const result = await db.from("people").insert(person);

  if (result.error) {
    showMessage("Not saved: " + result.error.message, "red");
  } else {
    showMessage("Saved to the database!", "green");
    document.getElementById("myForm").reset();
  }
});

function showMessage(text, colour) {
  const message = document.getElementById("message");
  message.textContent = text;
  message.style.color = colour;
}
