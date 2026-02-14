/* =========================
   API CONFIG
========================= */

const API_BASE_URL = "http://127.0.0.1:5000/api/v1";
const LOGIN_URL = `${API_BASE_URL}/auth/login`;

/* =========================
   COOKIE HELPERS
========================= */

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  return parts.length === 2 ? parts.pop().split(";").shift() : null;
}

function setAuthToken(token) {
  const maxAge = 4 * 60 * 60;
  document.cookie = `token=${token}; Max-Age=${maxAge}; Path=/; SameSite=Lax`;
}

function deleteCookie(name) {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

/* =========================
   LOGIN
========================= */

async function loginUser(email, password) {
  try {
    const response = await fetch(LOGIN_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (!response.ok || !data.access_token) {
      alert("Invalid email or password");
      return;
    }

    setAuthToken(data.access_token);
    window.location.href = "index.html";

  } catch (error) {
    alert("Network error. Please try again.");
  }
}

/* =========================
   FETCH PLACES (INDEX)
========================= */

async function fetchPlaces() {
  const container = document.getElementById("places-list");
  if (!container) return;

  container.innerHTML = "<p>Loading...</p>";

  try {
    const response = await fetch(`${API_BASE_URL}/places`);
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
  const container = document.getElementById("places-list");
  container.innerHTML = "";

  if (!places.length) {
    container.innerHTML = "<p>No places available.</p>";
    return;
  }

  places.forEach(place => {
    const card = document.createElement("div");
    card.className = "place-card";

    card.innerHTML = `
      <h3>${place.name}</h3>
      <p>${place.description || ""}</p>
      <p>${place.city}, ${place.country}</p>
      <p>$${place.price_per_night}/night</p>
      <button onclick="goToDetails('${place.id}')">View Details</button>
    `;

    container.appendChild(card);
  });
}

function goToDetails(id) {
  window.location.href = `place.html?id=${id}`;
}

/* =========================
   PLACE DETAILS
========================= */

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

async function fetchPlaceDetails() {
  const placeId = getPlaceIdFromURL();
  if (!placeId) return;

  const container = document.getElementById("place-details");
  if (!container) return;

  container.innerHTML = "<p>Loading...</p>";

  try {
    const response = await fetch(`${API_BASE_URL}/places/${placeId}`);
    const place = await response.json();

    if (!response.ok) {
      container.innerHTML = "<p>Place not found.</p>";
      return;
    }

    /* ===== Amenities ===== */
    let amenitiesHTML = "<p>No amenities available.</p>";

    if (place.amenities && place.amenities.length > 0) {
      amenitiesHTML = `
        <ul>
          ${place.amenities.map(a => `<li>${a.name}</li>`).join("")}
        </ul>
      `;
    }

    /* ===== Reviews ===== */
    let reviewsHTML = "<p>No reviews yet.</p>";

    if (place.reviews && place.reviews.length > 0) {
      reviewsHTML = `
        <ul>
          ${place.reviews.map(r => `
            <li>
              ⭐ ${r.rating} - ${r.text}
            </li>
          `).join("")}
        </ul>
      `;
    }

    /* ===== Final Render ===== */
    container.innerHTML = `
      <h1>${place.name}</h1>
      <p>${place.description}</p>
      <p>${place.city}, ${place.country}</p>
      <p>$${place.price_per_night}/night</p>

      <h3>Amenities:</h3>
      ${amenitiesHTML}

      <h3>Reviews:</h3>
      ${reviewsHTML}
    `;

  } catch (error) {
    container.innerHTML = "<p>Error loading place.</p>";
  }
}

/* =========================
   AUTH UI
========================= */

function updateAuthUI() {
  const loginLink = document.getElementById("login-link");
  const logoutLink = document.getElementById("logout-link");
  const token = getCookie("token");

  if (token) {
    if (loginLink) loginLink.style.display = "none";
    if (logoutLink) logoutLink.style.display = "inline";
  } else {
    if (loginLink) loginLink.style.display = "inline";
    if (logoutLink) logoutLink.style.display = "none";
  }
}

/* =========================
   DOM READY
========================= */

document.addEventListener("DOMContentLoaded", () => {

  updateAuthUI();

  if (document.getElementById("places-list")) {
    fetchPlaces();
  }

  if (document.getElementById("place-details")) {
    fetchPlaceDetails();
  }

  const logoutLink = document.getElementById("logout-link");

  if (logoutLink) {
    logoutLink.addEventListener("click", (e) => {
      e.preventDefault();
      deleteCookie("token");
      window.location.href = "login.html";
    });
  }

});
