(async function guardPage() {
  const publicPaths = ["/", "/login", "/register"];
  if (publicPaths.includes(window.location.pathname)) return;
  const accessToken  = localStorage.getItem("access_token");
  const refreshToken = localStorage.getItem("refresh_token");

  if (!accessToken) {
    redirectToLogin();
    return;
  }

  try {
    const payload    = JSON.parse(atob(accessToken.split(".")[1]));
    const nowSeconds = Math.floor(Date.now() / 1000);

    if (payload.exp && payload.exp > nowSeconds) {
      return;
    }
  } catch {
    redirectToLogin();
    return;
  }

  if (!refreshToken) {
    redirectToLogin();
    return;
  }

  try {
    const response = await fetch("/api/auth/refresh", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken })
    });

    if (!response.ok) {
      clearTokens();
      redirectToLogin();
      return;
    }

    const data = await response.json();
    localStorage.setItem("access_token", data.access_token);

  } catch {
    clearTokens();
    redirectToLogin();
  }
})();


function redirectToLogin() {
  window.location.href = "/login";
}

function clearTokens() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("token_type");
}


function getAuthHeaders() {
  return {
    "Content-Type":  "application/json",
    "Authorization": `Bearer ${localStorage.getItem("access_token")}`
  };
}
