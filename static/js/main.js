const API = "/restaurant";
const $ = (id) => document.getElementById(id);

function setMsg(el, text, ok) {
  el.textContent = text;
  el.className = "msg " + (ok ? "ok" : "error");
}

async function loadMenu() {
  const box = $("menu-grid");
  try {
    const res = await fetch(`${API}/menu/`);
    const items = await res.json();
    box.innerHTML = "";
    if (!items.length) { box.textContent = "No menu items yet."; return; }
    items.forEach((m) => {
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `<h3></h3><div class="price"></div><small></small>`;
      card.querySelector("h3").textContent = m.title;
      card.querySelector(".price").textContent = `$${m.price}`;
      card.querySelector("small").textContent = `In stock: ${m.inventory}`;
      box.appendChild(card);
    });
  } catch (e) {
    box.textContent = "Could not load the menu.";
  }
}

async function login(ev) {
  ev.preventDefault();
  const msg = $("login-msg");
  const res = await fetch("/auth/token/login/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: $("username").value, password: $("password").value }),
  });
  const data = await res.json();
  if (res.ok) {
    sessionStorage.setItem("token", data.auth_token);
    setMsg(msg, "Logged in. You can now book a table.", true);
    loadBookings();
  } else {
    setMsg(msg, "Login failed. Check your credentials.", false);
  }
}

function authHeaders() {
  return { "Content-Type": "application/json", Authorization: `Token ${sessionStorage.getItem("token")}` };
}

async function loadBookings() {
  const list = $("booking-list");
  if (!sessionStorage.getItem("token")) { list.textContent = "Log in to see bookings."; return; }
  const res = await fetch(`${API}/booking/tables/`, { headers: authHeaders() });
  if (!res.ok) { list.textContent = "Could not load bookings."; return; }
  const rows = await res.json();
  list.innerHTML = rows.length ? "" : "No bookings yet.";
  rows.forEach((b) => {
    const li = document.createElement("li");
    li.textContent = `${b.name} - ${b.no_of_guests} guest(s) - ${new Date(b.booking_date).toLocaleString()}`;
    list.appendChild(li);
  });
}

async function book(ev) {
  ev.preventDefault();
  const msg = $("book-msg");
  if (!sessionStorage.getItem("token")) { setMsg(msg, "Please log in first.", false); return; }
  const res = await fetch(`${API}/booking/tables/`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({
      name: $("name").value,
      no_of_guests: Number($("guests").value),
      booking_date: new Date($("when").value).toISOString(),
    }),
  });
  if (res.ok) { setMsg(msg, "Table booked!", true); ev.target.reset(); loadBookings(); }
  else { setMsg(msg, "Booking failed. Check the details.", false); }
}

document.addEventListener("DOMContentLoaded", () => {
  loadMenu();
  loadBookings();
  $("login-form").addEventListener("submit", login);
  $("book-form").addEventListener("submit", book);
});
