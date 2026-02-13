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

function deleteCookie(name) {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
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
   TASK 3: PLACES LIST
   Fetch and display all places
========================= */

/**
 * Fetch all places from API
 */
async function fetchPlaces() {
  const token = getCookie('token');
  const placesList = document.getElementById('places-list');
  
  if (!placesList) return;
  
  // Show loading state
  placesList.innerHTML = '<div class="loading">Loading places...</div>';
  
  try {
    const headers = {
      'Content-Type': 'application/json'
    };
    
    // Add token if authenticated
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(`${API_BASE_URL}/places`, {
      method: 'GET',
      headers: headers
    });
    
    if (!response.ok) {
      if (response.status === 401) {
        // Unauthorized - token invalid or expired
        deleteCookie('token');
        updateAuthUI();
        throw new Error('Session expired. Please login again.');
      }
      throw new Error('Failed to fetch places');
    }
    
    const places = await response.json();
    
    // Display places
    displayPlaces(places);
    
  } catch (error) {
    console.error('Error fetching places:', error);
    if (placesList) {
      placesList.innerHTML = `<p class="error">❌ ${error.message || 'Failed to load places. Please try again later.'}</p>`;
    }
  }
}

/**
 * Display places in the DOM
 * @param {Array} places - Array of place objects
 */
function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  
  if (!placesList) return;
  
  // Clear loading state
  placesList.innerHTML = '';
  
  // Check if places array is empty
  if (!places || places.length === 0) {
    placesList.innerHTML = '<p class="no-places">No places available.</p>';
    return;
  }
  
  // Create place card for each place
  places.forEach(place => {
    const placeCard = document.createElement('div');
    placeCard.className = 'place-card';
    
    // Store price in data attribute for filtering
    placeCard.dataset.price = place.price_per_night;
    placeCard.dataset.id = place.id;
    
    // Format rating
    const rating = place.average_rating 
      ? `⭐ ${place.average_rating.toFixed(1)}` 
      : '⭐ No reviews yet';
    
    // Escape HTML to prevent XSS attacks
    const name = escapeHTML(place.name);
    const description = escapeHTML(place.description || 'No description available.');
    const city = escapeHTML(place.city || 'Unknown');
    const country = escapeHTML(place.country || 'Unknown');
    
    // Create card content with View Details button
    placeCard.innerHTML = `
      <h3>${name}</h3>
      <p class="description">${description}</p>
      <p class="location">📍 ${city}, ${country}</p>
      <p class="price">💰 $${place.price_per_night}/night</p>
      <p class="rating">${rating}</p>
      <button onclick="viewPlaceDetails(${place.id})" class="details-button">View Details</button>
    `;
    
    placesList.appendChild(placeCard);
  });
}

/**
 * Navigate to place details page
 * @param {number} placeId - Place ID
 */
function viewPlaceDetails(placeId) {
  window.location.href = `place.html?id=${placeId}`;
}

/**
 * Filter places by price
 * @param {string} maxPrice - Maximum price or 'all'
 */
function filterPlacesByPrice(maxPrice) {
  const placeCards = document.querySelectorAll('.place-card');
  let visibleCount = 0;
  
  placeCards.forEach(card => {
    const price = parseFloat(card.dataset.price);
    
    if (maxPrice === 'all' || price <= parseFloat(maxPrice)) {
      card.style.display = 'block';
      visibleCount++;
    } else {
      card.style.display = 'none';
    }
  });
  
  // Show message if no places match filter
  const placesList = document.getElementById('places-list');
  const noResultsMsg = document.getElementById('no-results-message');
  
  if (visibleCount === 0) {
    if (!noResultsMsg) {
      const msg = document.createElement('p');
      msg.id = 'no-results-message';
      msg.className = 'no-places';
      msg.textContent = `No places found under $${maxPrice}`;
      placesList.appendChild(msg);
    }
  } else {
    const existingMsg = document.getElementById('no-results-message');
    if (existingMsg) existingMsg.remove();
  }
}

/**
 * Update UI based on authentication status
 */
function updateAuthUI() {
  const loginLink = document.getElementById('login-link');
  const navLogin = document.querySelector('nav a[href="login.html"]');
  
  if (getCookie('token')) {
    // Hide login links if authenticated
    if (loginLink) loginLink.style.display = 'none';
    if (navLogin) navLogin.style.display = 'none';
  } else {
    // Show login links if not authenticated
    if (loginLink) loginLink.style.display = 'inline-block';
    if (navLogin) navLogin.style.display = 'inline-block';
  }
}

/* =========================
   TASK 4: PLACE DETAILS
   Fetch and display place details
========================= */

/**
 * Get place ID from URL
 * @returns {string|null} Place ID
 */
function getPlaceIdFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('id');
}

/**
 * Fetch place details by ID
 * @param {string} placeId - Place ID
 */
async function fetchPlaceDetails(placeId) {
  const token = getCookie('token');
  const placeDetails = document.getElementById('place-details');
  const addReviewSection = document.getElementById('add-review');
  
  if (!placeDetails) return;
  
  // Show loading state
  placeDetails.innerHTML = '<div class="loading">Loading place details...</div>';
  
  try {
    const headers = {
      'Content-Type': 'application/json'
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
      method: 'GET',
      headers: headers
    });
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Place not found');
      } else if (response.status === 401) {
        throw new Error('Unauthorized access');
      } else {
        throw new Error('Failed to fetch place details');
      }
    }
    
    const place = await response.json();
    
    // Display place details
    displayPlaceDetails(place);
    
    // Show/hide review form based on authentication
    if (addReviewSection) {
      addReviewSection.style.display = token ? 'block' : 'none';
    }
    
    // Setup review form if authenticated
    if (token && addReviewSection) {
      setupReviewForm(placeId, token);
    }
    
  } catch (error) {
    console.error('Error fetching place details:', error);
    placeDetails.innerHTML = `<p class="error">❌ ${error.message}</p>`;
  }
}

/**
 * Display place details in the DOM
 * @param {Object} place - Place object
 */
function displayPlaceDetails(place) {
  const placeDetails = document.getElementById('place-details');
  
  if (!placeDetails) return;
  
  const price = place.price_per_night ? `$${place.price_per_night}/night` : 'Price not available';
  const rating = place.average_rating 
    ? `⭐ ${place.average_rating.toFixed(1)} (${place.reviews?.length || 0} reviews)`
    : '⭐ No reviews yet';
  
  // Escape HTML
  const name = escapeHTML(place.name);
  const description = escapeHTML(place.description || 'No description available.');
  const city = escapeHTML(place.city || 'Unknown');
  const country = escapeHTML(place.country || 'Unknown');
  const host = escapeHTML(place.host_name || 'Unknown');
  
  // Amenities HTML
  let amenitiesHtml = '<div class="amenities-list">';
  if (place.amenities && place.amenities.length > 0) {
    place.amenities.forEach(amenity => {
      amenitiesHtml += `<span class="amenity-tag">${escapeHTML(amenity.name)}</span>`;
    });
  } else {
    amenitiesHtml = '<p class="no-amenities">No amenities listed</p>';
  }
  amenitiesHtml += '</div>';
  
  // Reviews HTML
  let reviewsHtml = '<div class="reviews-section"><h2>Reviews</h2>';
  if (place.reviews && place.reviews.length > 0) {
    reviewsHtml += '<div class="reviews-list">';
    place.reviews.forEach(review => {
      reviewsHtml += `
        <div class="review-card">
          <div class="review-header">
            <span class="review-rating">${'⭐'.repeat(review.rating)}</span>
            <span class="review-author">by ${escapeHTML(review.user_name || 'Anonymous')}</span>
          </div>
          <p class="review-text">${escapeHTML(review.text)}</p>
          <small class="review-date">${new Date(review.created_at).toLocaleDateString()}</small>
        </div>
      `;
    });
    reviewsHtml += '</div>';
  } else {
    reviewsHtml += '<p class="no-reviews">No reviews yet. Be the first to review!</p>';
  }
  reviewsHtml += '</div>';
  
  placeDetails.innerHTML = `
    <div class="place-details-container">
      <h1 class="place-title">${name}</h1>
      <div class="place-location">📍 ${city}, ${country}</div>
      <div class="place-rating-large">${rating}</div>
      <div class="place-price">💰 ${price}</div>
      <div class="place-host">🏠 Hosted by ${host}</div>
      <div class="place-description">
        <h2>About this place</h2>
        <p>${description}</p>
      </div>
      <div class="place-amenities">
        <h2>Amenities</h2>
        ${amenitiesHtml}
      </div>
    </div>
    ${reviewsHtml}
  `;
}

/**
 * Setup review form submission
 * @param {string} placeId - Place ID
 * @param {string} token - JWT token
 */
function setupReviewForm(placeId, token) {
  const reviewForm = document.getElementById('review-form');
  
  if (!reviewForm) return;
  
  reviewForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const rating = document.getElementById('rating')?.value;
    const text = document.getElementById('review-text')?.value;
    
    if (!rating || !text) {
      alert('Please fill in all fields');
      return;
    }
    
    const submitBtn = reviewForm.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';
    
    try {
      const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          rating: parseInt(rating),
          text: text
        })
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to submit review');
      }
      
      alert('✅ Review submitted successfully!');
      reviewForm.reset();
      
      // Refresh place details to show new review
      fetchPlaceDetails(placeId);
      
    } catch (error) {
      console.error('Error submitting review:', error);
      alert(`❌ ${error.message}`);
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Submit Review';
    }
  });
}

/* =========================
   Utility Functions
========================= */

/**
 * Escape HTML to prevent XSS attacks
 * @param {string} text - Raw text
 * @returns {string} Escaped HTML
 */
function escapeHTML(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/* =========================
   Event Listeners
========================= */

document.addEventListener('DOMContentLoaded', () => {

  // Get current page filename
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';

  /* ----------  LOGIN PAGE ---------- */
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

  /* ----------  INDEX PAGE (PLACES LIST) ---------- */
  if (currentPage === 'index.html' || currentPage === '') {
    // Update UI based on authentication
    updateAuthUI();
    
    // Fetch and display places
    fetchPlaces();
    
    // Setup price filter
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
      priceFilter.addEventListener('change', (event) => {
        filterPlacesByPrice(event.target.value);
      });
    }
  }

  /* ----------  PLACE DETAILS PAGE ---------- */
  if (currentPage === 'place.html') {
    const placeId = getPlaceIdFromURL();
    
    if (!placeId) {
      window.location.href = 'index.html';
      return;
    }
    
    // Update UI based on authentication
    updateAuthUI();
    
    // Fetch and display place details
    fetchPlaceDetails(placeId);
  }

});
