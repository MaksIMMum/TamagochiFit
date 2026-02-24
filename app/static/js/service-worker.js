async function handleLogin(event) {
  event.preventDefault();

  const username         = document.getElementById("username").value;
  const password         = document.getElementById("password").value;
  const messageContainer = document.getElementById("message-container");

  try {
    console.log("🔍 Step 1: Attempting login with username:", username);

    // Step 1: Login and get tokens
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    console.log("📊 Login response status:", response.status);

    if (!response.ok) {
      const error = await response.json();
      console.error("❌ Login failed:", error);
      messageContainer.innerHTML = `
        <div class="alert alert-danger" role="alert">
          ${error.detail || "Login failed"}
        </div>`;
      return;
    }

    const data = await response.json();
    console.log("✅ Login successful!");
    console.log("📋 Token type:", data.token_type);
    console.log("⏰ Expires in:", data.expires_in, "seconds");
    console.log("🔑 Access token (first 20 chars):", data.access_token.substring(0, 20) + "...");

    // Store tokens
    localStorage.setItem("access_token",  data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    localStorage.setItem("token_type",    data.token_type);

    console.log("💾 Tokens stored in localStorage");

    messageContainer.innerHTML = `
      <div class="alert alert-success" role="alert">
        Login successful! Checking pet status...
      </div>`;

    // WAIT a moment before checking pet status
    await new Promise(resolve => setTimeout(resolve, 500));

    console.log("🔍 Step 2: Checking pet status at /api/pet/me");

    // Step 2: Check if the user already has a pet
    const petResponse = await fetch("/api/pet/me", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${data.access_token}`,
        "Content-Type": "application/json"
      }
    });

    console.log("📊 Pet response status:", petResponse.status);

    const petResponseText = await petResponse.text();
    console.log("📄 Pet response body:", petResponseText);

    if (petResponse.ok) {
      console.log("✅ User has a pet! Redirecting to /home");
      window.location.href = "/home";
    } else if (petResponse.status === 404) {
      console.log("⚠️  User has no pet yet. Redirecting to /hatch");
      window.location.href = "/hatch";
    } else {
      try {
        const error = JSON.parse(petResponseText);
        console.error("❌ Unexpected error:", error);
        throw new Error(error.detail || "Failed to check pet status");
      } catch (e) {
        throw new Error("Server error: " + petResponseText);
      }
    }

  } catch (error) {
    console.error("❌ CAUGHT ERROR:", error);
    console.error("Stack:", error.stack);
    messageContainer.innerHTML = `
      <div class="alert alert-danger" role="alert">
        ${error.message}
      </div>`;
  }
}

function goToRegister() {
  window.location.href = "/register";
}
