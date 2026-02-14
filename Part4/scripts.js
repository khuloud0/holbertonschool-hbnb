/* =========================
   API CONFIG
========================= */

const API_BASE_URL = "http://127.0.0.1:5000/api/v1";


/* =========================
   COOKIE HELPERS
========================= */

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    return parts.length === 2 ? parts.pop().split(';').shift() : null;
}

function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/`;
}

function checkAuthentication() {
    return getCookie('token');
}


/* =========================
   LOGIN
========================= */

async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok || !data.access_token) {
            alert("Invalid email or password");
            return;
        }

        setCookie('token', data.access_token);
        window.location.href = "index.html";

    } catch (error) {
        alert("Network error");
    }
}


/* =========================
   FETCH PLACES
========================= */

async function fetchPlaces(token) {
    const container = document.getElementById('places-list');
    if (!container) return;

    container.innerHTML = "<p>Loading...</p>";

    try {
        const headers = { 'Content-Type': 'application/json' };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places`, {
            method: 'GET',
            headers: headers
        });

        const places = await response.json();

        if (!response.ok) {
            container.innerHTML = "<p>Failed to load places.</p>";
            return;
        }

        displayPlaces(places);

    } catch (error) {
        container.innerHTML = "<p>Error loading places.</p>";
    }
}


function displayPlaces(places) {
    const container = document.getElementById('places-list');
    container.innerHTML = "";

    if (!places || places.length === 0) {
        container.innerHTML = "<p>No places available.</p>";
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.dataset.price = place.price_per_night;

        card.innerHTML = `
            <h3>${place.name}</h3>
            <p>${place.description || ""}</p>
            <p>${place.city}, ${place.country}</p>
            <p>$${place.price_per_night}/night</p>
            <button onclick="viewPlaceDetails('${place.id}')">
                View Details
            </button>
        `;

        container.appendChild(card);
    });
}


/* =========================
   VIEW DETAILS
========================= */

function viewPlaceDetails(placeId) {
    window.location.href = `place.html?id=${placeId}`;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}


/* =========================
   FETCH PLACE DETAILS
========================= */

async function fetchPlaceDetails(token, placeId) {
    const container = document.getElementById('place-details');
    if (!container) return;

    container.innerHTML = "<p>Loading...</p>";

    try {
        const headers = { 'Content-Type': 'application/json' };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        const place = await response.json();

        if (!response.ok) {
            container.innerHTML = "<p>Place not found.</p>";
            return;
        }

        // Amenities Fix 🔥
        let amenitiesHTML = "No amenities";

        if (place.amenities && place.amenities.length > 0) {
            amenitiesHTML = place.amenities
                .map(a => a.name)
                .join(", ");
        }

        container.innerHTML = `
            <h1>${place.name}</h1>
            <p><strong>Description:</strong> ${place.description}</p>
            <p><strong>City:</strong> ${place.city}</p>
            <p><strong>Country:</strong> ${place.country}</p>
            <p><strong>Price:</strong> $${place.price_per_night}</p>
            <p><strong>Rating:</strong> ${place.average_rating || 0}</p>
            <p><strong>Amenities:</strong> ${amenitiesHTML}</p>
        `;

    } catch (error) {
        container.innerHTML = "<p>Error loading place.</p>";
    }
}


/* =========================
   DOM READY
========================= */

document.addEventListener('DOMContentLoaded', () => {

    const token = checkAuthentication();

    // LOGIN PAGE
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            loginUser(email, password);
        });
    }

    // INDEX PAGE
    if (document.getElementById('places-list')) {
        fetchPlaces(token);
    }

    // PLACE DETAILS PAGE
    if (document.getElementById('place-details')) {
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            fetchPlaceDetails(token, placeId);
        }
    }

});
