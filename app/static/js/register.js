
const form = document.getElementById('registerForm');
const submitBtn = document.getElementById('submitBtn');
const messageContainer = document.getElementById('message-container');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const username = document.getElementById('username').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const fullName = document.getElementById('fullName').value;

  submitBtn.disabled = true;
  submitBtn.textContent = 'Creating account...';
  messageContainer.innerHTML = '';

  try {
    // Registration request
    const response = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username,
        email,
        password,
        full_name: fullName || null
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Registration failed');
    }

    messageContainer.innerHTML = `
      <div class="alert alert-success" style="display: block;">
        ✓ Account created! Logging you in...
      </div>
    `;

    // Auto-login after successful registration
    const loginResponse = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (loginResponse.ok) {
      const data = await loginResponse.json();
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      localStorage.setItem('token_type', data.token_type);

      setTimeout(() => {
        window.location.href = '/hatch';
      }, 1000);
    } else {
      // Registration succeeded but auto-login failed
      setTimeout(() => {
        window.location.href = '/login';
      }, 1500);
    }

  } catch (error) {
    messageContainer.innerHTML = `
      <div class="alert alert-danger" style="display: block;">
        ✗ ${error.message}
      </div>
    `;
    submitBtn.disabled = false;
    submitBtn.textContent = 'Create Account';
  }
});
