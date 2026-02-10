const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';
const API_AUTH_URL = `${API_BASE_URL}/auth/login`;

/* =========================
   Cookies helpers
========================= */
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  return parts.length === 2 ? parts.pop().split(';').shift() : null;
}

function setAuthToken(token) {
  document.cookie = `token=${token}; path=/`;
}

function displayError(elementId, message) {
  const element = document.getElementById(elementId);
  if (element) {
    element.textContent = message;
    element.style.color = 'red';
  }
}

/* =========================
   Login API call
========================= */
async function loginUser(email, password) {
  try {
    const response = await fetch(API_AUTH_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      throw new Error('Invalid credentials');
    }

    const data = await response.json();
    setAuthToken(data.access_token);

    // Redirect after successful login
    window.location.href = 'index.html';
  } catch (error) {
    displayError('login-error', 'Invalid email or password');
  }
}

/* =========================
   Event Listener
========================= */
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      loginUser(email, password);
    });
  }
});
