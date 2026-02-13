/* =========================
   API Configuration
========================= */

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';
const API_AUTH_URL = `${API_BASE_URL}/auth/login`;

/* =========================
   Cookies Helpers
========================= */

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  return parts.length === 2 ? parts.pop().split(';').shift() : null;
}

function setAuthToken(token) {
  // 4 hours expiration
  const maxAge = 4 * 60 * 60; // 14400 seconds
  document.cookie = `token=${encodeURIComponent(token)}; Max-Age=${maxAge}; Path=/; SameSite=Lax`;
}

function displayError(elementId, message) {
  const element = document.getElementById(elementId);
  if (element) {
    element.textContent = message;
    element.style.color = 'red';
  }
}

/* =========================
   Login API Call
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

    const data = await response.json();

    if (!response.ok) {
      displayError('login-error', data.message || 'Invalid email or password');
      return;
    }

    // تأكدي أن الباك يرجع access_token
    if (!data.access_token) {
      displayError('login-error', 'No token returned from server');
      return;
    }

    // Store token in cookie (4 hours)
    setAuthToken(data.access_token);

    // Redirect to main page
    window.location.href = 'index.html';

  } catch (error) {
    console.error(error);
    displayError('login-error', 'Network error. Please try again.');
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

      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;

      if (!email || !password) {
        displayError('login-error', 'Please enter your email and password');
        return;
      }

      loginUser(email, password);
    });
  }

});
