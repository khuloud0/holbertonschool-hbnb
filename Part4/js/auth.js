/**
 * AUTH.JS - Authentication management for HBnB
 * Handles login, logout, and token management
 */

/**
 * Login user
 * @param {string} email - User email
 * @param {string} password - User password
 */
async function login(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Login failed');
        }

        // Store JWT token in cookie
        setCookie('token', data.access_token, 1); // Expires in 1 hour
        
        // Store user info if needed
        if (data.user) {
            localStorage.setItem('user', JSON.stringify(data.user));
        }

        // Redirect to index page
        window.location.href = 'index.html';
        
        return data;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

/**
 * Logout user
 */
function logout() {
    // Delete token cookie
    deleteCookie('token');
    
    // Clear user from localStorage
    localStorage.removeItem('user');
    
    // Redirect to login page
    window.location.href = 'login.html';
}

/**
 * Check if user is authenticated
 * @returns {boolean} True if authenticated
 */
function isAuthenticated() {
    return getCookie('token') !== null;
}

/**
 * Get JWT token
 * @returns {string|null} JWT token or null
 */
function getToken() {
    return getCookie('token');
}

/**
 * Get current user from localStorage
 * @returns {Object|null} User object or null
 */
function getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

/**
 * Setup login form
 */
function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
    
    if (!loginForm) return;
    
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const submitBtn = loginForm.querySelector('button[type="submit"]');
        
        // Disable button and show loading
        submitBtn.disabled = true;
        submitBtn.textContent = 'Logging in...';
        
        try {
            await login(email, password);
        } catch (error) {
            alert(error.message || 'Login failed. Please check your credentials.');
        } finally {
            // Re-enable button
            submitBtn.disabled = false;
            submitBtn.textContent = 'Login';
        }
    });
}

// Initialize authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    setupLoginForm();
});
