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
  const maxAge = 4 * 60 * 60; // 4 hours
  document.cookie = `token=${token}; Max-Age=${maxAge}; Path=/; SameSite=Lax`;
}

function deleteCookie(name) {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}


/* =========================
   ERROR HANDLING
========================= */

function displayError(message) {
  const errorElement = document.getElementById("login-error");
  if (errorElement) {
    errorElement.textContent = message;
    errorElement.style.display = "block";
  }
}

function clearError() {
  const errorElement = document.getElementById("login-error");
  if (errorElement) {
    errorElement.textContent = "";
    errorElement.style.display = "none";
  }
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
      displayError("Invalid email or password");
      return;
    }

    setAuthToken(data.access_token);
    window.location.href = "index.html";

  } catch (error) {
    displayError("Network error. Please try again.");
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

  if (!places || places.length === 0) {
    container.innerHTML = "<p>No places available.</p>";
    return;
  }

  places.forEach(place => {
    const card = document.createElement("div");
    card.className = "place-card";
    card.dataset.price = place.price_per_night;

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
   PRICE FILTER
========================= */

function setupPriceFilter() {
  const filter = document.getElementById("price-filter");
  if (!filter) return;

  filter.addEventListener("change", (e) => {
    const maxPrice = e.target.value;
    const cards = document.querySelectorAll(".place-card");

    cards.forEach(card => {
      const price = parseFloat(card.dataset.price);

      if (maxPrice === "all" || price <= parseFloat(maxPrice)) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });
  });
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

    container.innerHTML = `
      <h1>${place.name}</h1>
      <p><strong>Description:</strong> ${place.description}</p>
      <p><strong>City:</strong> ${place.city}</p>
      <p><strong>Country:</strong> ${place.country}</p>
      <p><strong>Price per night:</strong> $${place.price_per_night}</p>
      <p><strong>Rating:</strong> ${place.average_rating || 0}</p>
      <p><strong>Latitude:</strong> ${place.latitude}</p>
      <p><strong>Longitude:</strong> ${place.longitude}</p>
`;

  } catch (error) {
    container.innerHTML = "<p>Error loading place.</p>";
  }
}


/* =========================
   AUTH UI (Login / Logout + Hide Review)
========================= */

function updateAuthUI() {
  const token = getCookie("token");

  const loginLink = document.getElementById("login-link");
  const logoutLink = document.getElementById("logout-link");
  const reviewSection = document.getElementById("add-review");

  if (token) {
    if (loginLink) loginLink.style.display = "none";
    if (logoutLink) logoutLink.style.display = "inline";
    if (reviewSection) reviewSection.style.display = "block";
  } else {
    if (loginLink) loginLink.style.display = "inline";
    if (logoutLink) logoutLink.style.display = "none";
    if (reviewSection) reviewSection.style.display = "none";
  }
}


/* =========================
   DOM READY
========================= */

document.addEventListener("DOMContentLoaded", () => {

  updateAuthUI();

  // LOGIN PAGE
  const loginForm = document.getElementById("login-form");

  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      clearError();

      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value;

      if (!email || !password) {
        displayError("Please enter email and password");
        return;
      }

      loginUser(email, password);
    });
  }

  // INDEX PAGE
  if (document.getElementById("places-list")) {
    fetchPlaces();
    setupPriceFilter();
  }

  // PLACE DETAILS PAGE
  if (document.getElementById("place-details")) {
    fetchPlaceDetails();
  }

  // LOGOUT
  const logoutLink = document.getElementById("logout-link");

  if (logoutLink) {
    logoutLink.addEventListener("click", (e) => {
      e.preventDefault();
      deleteCookie("token");
      window.location.href = "login.html";
    });
  }

});
