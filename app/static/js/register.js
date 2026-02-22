async function handleRegister(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const fullName = document.getElementById("fullName").value;
    const messageContainer = document.getElementById("message-container");

    try {
        const response = await fetch("/api/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
                full_name: fullName || null
            })
        });

        if (!response.ok) {
            const error = await response.json();
            messageContainer.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    ${error.detail || "Registration failed"}
                </div>
            `;
            return;
        }

        messageContainer.innerHTML = `
            <div class="alert alert-success" role="alert">
                Account created successfully! Redirecting to login...
            </div>
        `;

        setTimeout(() => {
            window.location.href = "/login";
        }, 2000);

    } catch (error) {
        messageContainer.innerHTML = `
            <div class="alert alert-danger" role="alert">
                ${error.message}
            </div>
        `;
    }
}

function goToLogin() {
    window.location.href = "/login";
}
