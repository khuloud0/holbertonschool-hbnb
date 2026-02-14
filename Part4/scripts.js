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
   FETCH PLACES
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

    let amenitiesHTML = "";

    if (place.amenities && place.amenities.length > 0) {
      amenitiesHTML = `
        <h3>Amenities:</h3>
        <ul>
          ${place.amenities.map(a => `<li>${a.name}</li>`).join("")}
        </ul>
      `;
    }

    container.innerHTML = `
      <h1>${place.name}</h1>
      <p>${place.description}</p>
      <p>${place.city}, ${place.country}</p>
      <p>$${place.price_per_night}/night</p>
      ${amenitiesHTML}
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
  const reviewSection = document.getElementById("add-review");
  const token = getCookie("token");

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
   ADD REVIEW
========================= */

async function submitReview(placeId, reviewText, rating, token) {
  return fetch(`${API_BASE_URL}/reviews`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({
      place_id: placeId,
      review: reviewText,
      rating: parseInt(rating)
    })
  });
}

/* =========================
   DOM READY
========================= */

document.addEventListener("DOMContentLoaded", () => {

  updateAuthUI();

  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value;
      loginUser(email, password);
    });
  }

  if (document.getElementById("places-list")) {
    fetchPlaces();
  }

  if (document.getElementById("place-details")) {
    fetchPlaceDetails();
  }

  const reviewForm = document.getElementById("review-form");

  if (reviewForm) {

    const token = getCookie("token");

    if (!token) {
      window.location.href = "index.html";
      return;
    }

    reviewForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const placeId = getPlaceIdFromURL();
      const reviewText = document.getElementById("review-text")?.value.trim();
      const rating = document.getElementById("rating")?.value;

      if (!placeId) {
        alert("Invalid place ID");
        return;
      }

      if (!reviewText || !rating) {
        alert("Please fill all fields");
        return;
      }

      try {
        const response = await submitReview(placeId, reviewText, rating, token);

        if (response.ok) {
          alert("Review submitted successfully!");
          reviewForm.reset();
        } else {
          const errorData = await response.json();
          alert(errorData.error || "Failed to submit review");
        }

      } catch (error) {
        alert("Network error");
      }
    });
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
