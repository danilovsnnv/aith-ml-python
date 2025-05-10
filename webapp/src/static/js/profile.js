const gatewayBaseUrl =
  document.querySelector('meta[name="api-base-url"]')?.content ||
  "http://localhost:8004";

const els = {
  root: document.getElementById("profile-content"),
};

document.addEventListener("DOMContentLoaded", () => loadProfile());

async function loadProfile() {
  try {
    const res = await fetch(`${gatewayBaseUrl}/user/me`, {
      method: "GET",
      credentials: "include",  // send cookies (access_token)
    });

    if (res.status === 401) {
      return renderAuthForms();  // not authorised
    }
    if (!res.ok) throw new Error(`Status ${res.status}`);

    const user = await res.json();  // { username: str, balance: float }
    renderProfileCard(user);
  } catch (err) {
    console.error("Profile error:", err);
    els.root.innerHTML =
      `<div class="alert alert-danger">Failed to load profile. Try later.</div>`;
  }
}

function renderProfileCard({ username, balance }) {
  els.root.innerHTML = `
    <div class="card shadow-sm card-profile">
      <div class="card-body text-center">
        <h5 class="card-title mb-3">${escapeHtml(username)}</h5>
        <p class="fs-5 mb-4">Balance: ${balance.toFixed(2)} p.</p>
        <button class="btn btn-outline-primary" id="logout-btn">Logout</button>
      </div>
    </div>`;

  document.getElementById("logout-btn").onclick = doLogout;
}

function renderAuthForms() {
  els.root.innerHTML = `
    <div class="row g-4 w-100" style="max-width:52rem">
      <div class="col-md-6">
        <h2 class="h5 mb-3">Login</h2>
        <form id="login-form" class="needs-validation" novalidate>
          <input class="form-control mb-2" name="username" placeholder="Username" required>
          <input class="form-control mb-2" type="password" name="password"
                 placeholder="Password" required>
          <button class="btn btn-primary w-100" type="submit">Log in</button>
        </form>
      </div>
      <div class="col-md-6">
        <h2 class="h5 mb-3">Register</h2>
        <form id="register-form" class="needs-validation" novalidate>
          <input class="form-control mb-2" name="username" placeholder="Username" required>
          <input class="form-control mb-2" type="password" name="password"
                 placeholder="Password" required>
          <button class="btn btn-success w-100" type="submit">Sign up</button>
        </form>
      </div>
    </div>`;

  addFormHandler("login-form", "/auth/login");
  addFormHandler("register-form", "/auth/register");
}

function addFormHandler(formId, endpoint) {
  const form = document.getElementById(formId);
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!form.checkValidity()) return form.classList.add("was-validated");

    const body = Object.fromEntries(new FormData(form).entries());
    try {
      const res = await fetch(`${gatewayBaseUrl}${endpoint}`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error(`Status ${res.status}`);
      location.reload(); // cookies set -> reload profile
    } catch (err) {
      console.error(`${endpoint} failed`, err);
      alert("Operation failed – please try again");
    }
  });
}

async function doLogout() {
  try {
    await fetch(`${gatewayBaseUrl}/auth/logout`, {
      method: "POST",
      credentials: "include",
    });
  } finally {
    location.reload(); // back to auth forms
  }
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.innerText = str;
  return div.innerHTML;
}