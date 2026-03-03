
    const form = document.getElementById('loginForm');
    const submitBtn = document.getElementById('submitBtn');
    const messageContainer = document.getElementById('message-container');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;

      submitBtn.disabled = true;
      submitBtn.textContent = 'Logging in...';
      messageContainer.innerHTML = '';

      try {
        // Login request
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.detail || 'Login failed');
        }

        const data = await response.json();

        // Store tokens
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        localStorage.setItem('token_type', data.token_type);

        messageContainer.innerHTML = `
          <div class="alert alert-success" style="display: block;">
            ✓ Login successful! Redirecting...
          </div>
        `;

        // Check if user has a pet
        const petResponse = await fetch('/api/pet/me', {
          headers: { 'Authorization': `Bearer ${data.access_token}` }
        });

        setTimeout(() => {
          if (petResponse.ok) {
            window.location.href = '/home';
          } else {
            window.location.href = '/hatch';
          }
        }, 1000);

      } catch (error) {
        messageContainer.innerHTML = `
          <div class="alert alert-danger" style="display: block;">
            ✗ ${error.message}
          </div>
        `;
        submitBtn.disabled = false;
        submitBtn.textContent = 'Login';
      }
    });
