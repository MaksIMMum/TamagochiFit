async function handleRegister(event) {
  event.preventDefault();

  const username         = document.getElementById("username").value;
  const email            = document.getElementById("email").value;
  const password         = document.getElementById("password").value;
  const fullName         = document.getElementById("fullName").value;
  const messageContainer = document.getElementById("message-container");
  console.log("Function reached, username:", username);
  try {
    const response = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username,
        email,
        password,
        full_name: fullName || null
      })
    });

    if (!response.ok) {
      const error = await response.json();
      messageContainer.innerHTML = `
        <div class="alert alert-danger" role="alert">
          ${error.detail || "Registration failed"}
        </div>`;
      return;
    }

    console.log("✅ Registration successful, attempting auto-login...");
    messageContainer.innerHTML = `<div class="alert alert-success">Account created! Logging you in...</div>`;

    const loginResponse = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    console.log("Login response status:", loginResponse.status);

    if (!loginResponse.ok) {
      const loginError = await loginResponse.json();
      console.error("❌ Auto-login failed:", loginError);
      setTimeout(() => window.location.href = "/login", 1500);
      return;
    }

    const data = await loginResponse.json();
    console.log("✅ Auto-login successful, token received:", !!data.access_token);

    localStorage.setItem("access_token",  data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    localStorage.setItem("token_type",    data.token_type);

    console.log("Token stored, redirecting to /hatch...");
    setTimeout(() => window.location.href = "/hatch", 800);

  } catch (error) {
    console.error("❌ Caught error:", error);
    messageContainer.innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
  }
}

function goToLogin() {
  window.location.href = "/login";
}
