/**
 * UTILS.JS - Helper functions for HBnB
 */

/* ===============================
   API BASE URL
================================ */
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

/* ===============================
   Cookies
================================ */
function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.split('=');
        if (cookieName === name) {
            return cookieValue;
        }
    }
    return null;
}

function setCookie(name, value, hours = 1) {
    const date = new Date();
    date.setTime(date.getTime() + (hours * 60 * 60 * 1000));
    document.cookie = `${name}=${value}; expires=${date.toUTCString()}; path=/`;
}

function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

function getToken() {
    return getCookie('access_token');
}

function isAuthenticated() {
    return !!getToken();
}

/* ===============================
   Helpers
================================ */
function escapeHTML(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = '<p>Loading...</p>';
    }
}

function showError(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<p style="color:red;">❌ ${escapeHTML(message)}</p>`;
    }
}
