/**
 * ========== Cookie Helper Functions ==========
 */

/**
 * Get cookie value by name
 * @param {string} name - Cookie name
 * @returns {string|null} Cookie value or null if not found
 */
function getCookie(name) {
    // Split all cookies into array
    const cookies = document.cookie.split('; ');
    
    // Loop through each cookie
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.split('=');
        if (cookieName === name) {
            return cookieValue;
        }
    }
    return null;
}

/**
 * ========== Authentication Functions ==========
 */

/**
 * Check if user is authenticated by verifying JWT token in cookies
 * Show/hide login link based on authentication status
 */
function checkAuthentication() {
    // Get token from cookies
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        // User is not authenticated - show login link
        loginLink.style.display = 'block';
        // Optionally fetch public places if API allows
        // fetchPlacesPublic();
    } else {
        // User is authenticated - hide login link
        loginLink.style.display = 'none';
        // Fetch places data with authentication token
        fetchPlaces(token);
    }
}

/**
 * ========== API Functions ==========
 */

/**
 * Fetch places data from API with authentication token
 * @param {string} token - JWT authentication token
 */
async function fetchPlaces(token) {
    try {
        // Send GET request to places endpoint with auth token
        const response = await fetch('http://127.0.0.1:5000/places', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        // Check if request was successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse JSON response
        const places = await response.json();
        
        // Display places in the DOM
        displayPlaces(places);
        
    } catch (error) {
        // Handle any errors during fetch
        console.error('Error fetching places:', error);
        document.getElementById('places-list').innerHTML = 
            '<p class="error">❌ Failed to load places. Please try again later.</p>';
    }
}

/**
 * Fetch places without authentication (public endpoint)
 * Used as fallback when no token is available
 */
async function fetchPlacesPublic() {
    try {
        const response = await fetch('http://127.0.0.1:5000/places/public');
        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error('Error fetching public places:', error);
    }
}

/**
 * ========== DOM Manipulation Functions ==========
 */

/**
 * Display places in the DOM
 * @param {Array} places - Array of place objects
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    
    // Clear previous content
    placesList.innerHTML = '';

    // Check if places array is empty
    if (!places || places.length === 0) {
        placesList.innerHTML = '<p class="no-places">🏠 No places available.</p>';
        return;
    }

    // Loop through each place and create card element
    places.forEach(place => {
        // Create place card container
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        
        // Store price in data attribute for filtering
        placeCard.dataset.price = place.price_per_night;
        
        // Format rating display
        const rating = place.average_rating 
            ? `⭐ ${place.average_rating.toFixed(1)}` 
            : '⭐ No reviews yet';
        
        // Build place card HTML
        placeCard.innerHTML = `
            <h3>${escapeHTML(place.name)}</h3>
            <p class="description">${escapeHTML(place.description || 'No description available.')}</p>
            <p class="location">📍 ${escapeHTML(place.city || 'Unknown')}, ${escapeHTML(place.country || 'Unknown')}</p>
            <p class="price">💰 $${place.price_per_night}/night</p>
            <p class="rating">${rating}</p>
            <button onclick="viewPlaceDetails(${place.id})" class="btn-view">View Details</button>
        `;
        
        // Append card to places list
        placesList.appendChild(placeCard);
    });
}

/**
 * Filter places based on selected price
 * @param {string} maxPrice - Maximum price or 'all'
 */
function filterPlacesByPrice(maxPrice) {
    // Get all place cards
    const placeCards = document.querySelectorAll('.place-card');
    
    // Loop through each card and check price
    placeCards.forEach(card => {
        const price = parseFloat(card.dataset.price);
        
        // Show card if price is within filter range
        if (maxPrice === 'all' || price <= parseFloat(maxPrice)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

/**
 * Navigate to place details page
 * @param {number} placeId - ID of the place
 */
function viewPlaceDetails(placeId) {
    // Redirect to details page with place ID in URL
    window.location.href = `place-details.html?id=${placeId}`;
}

/**
 * Escape HTML special characters to prevent XSS attacks
 * @param {string} text - Raw text input
 * @returns {string} Escaped HTML string
 */
function escapeHTML(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * ========== Event Listeners ==========
 */

/**
 * Initialize page when DOM is fully loaded
 */
document.addEventListener('DOMContentLoaded', () => {
    // Check authentication status on page load
    checkAuthentication();

    // Add event listener to price filter dropdown
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            // Get selected filter value and filter places
            const maxPrice = event.target.value;
            filterPlacesByPrice(maxPrice);
        });
    }
});

/**
 * ========== Export for testing (if needed) ==========
 */
// Export functions if using modules
// export { getCookie, checkAuthentication, fetchPlaces, displayPlaces, filterPlacesByPrice };
