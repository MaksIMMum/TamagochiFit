  async function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const messageContainer = document.getElementById("message-container");

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: password
        })
      });

      if (!response.ok) {
        const error = await response.json();
        messageContainer.innerHTML = `
          <div class="alert alert-danger" role="alert">
            ${error.detail || "Login failed"}
          </div>
        `;
        return;
      }

      const data = await response.json();

      // Store tokens in localStorage
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      localStorage.setItem("token_type", data.token_type);

      // Redirect to dashboard
      messageContainer.innerHTML = `
        <div class="alert alert-success" role="alert">
          Login successful! Redirecting...
        </div>
      `;

      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 1500);

    } catch (error) {
      messageContainer.innerHTML = `
        <div class="alert alert-danger" role="alert">
          ${error.message}
        </div>
      `;
    }
  }

  function goToRegister() {
    window.location.href = "/register";
  }
