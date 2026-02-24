async function handleLogin(event) {
  event.preventDefault();

  const username         = document.getElementById("username").value;
  const password         = document.getElementById("password").value;
  const messageContainer = document.getElementById("message-container");

  try {
    // Step 1: Login and get tokens
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
      const error = await response.json();
      messageContainer.innerHTML = `
        <div class="alert alert-danger" role="alert">
          ${error.detail || "Login failed"}
        </div>`;
      return;
    }

    const data = await response.json();

    // Store tokens
    localStorage.setItem("access_token",  data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    localStorage.setItem("token_type",    data.token_type);

    messageContainer.innerHTML = `
      <div class="alert alert-success" role="alert">
        Login successful! Redirecting...
      </div>`;

    // Step 2: Check if the user already has a pet
    const petResponse = await fetch("/api/pet/me", {
      method: "GET",
      headers: { "Authorization": `Bearer ${data.access_token}` }
    });

    if (petResponse.ok) {
      // Has a pet — go to home
      window.location.href = "/home";
    } else {
      // No pet yet (404) — go to hatch
      window.location.href = "/hatch";
    }

  } catch (error) {
    messageContainer.innerHTML = `
      <div class="alert alert-danger" role="alert">
        ${error.message}
      </div>`;
  }
}

function goToRegister() {
  window.location.href = "/register";
}
