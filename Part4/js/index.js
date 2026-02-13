/**
 * INDEX.JS - Places listing page for HBnB
 * Handles fetching and displaying places with filtering
 */

/**
 * Fetch all places
 */
async function fetchPlaces() {
    const token = getToken();
    const placesList = document.getElementById('places-list');
    
    showLoading('places-list');
    
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
            throw new Error('Failed to fetch places');
        }
        
        const places = await response.json();
        displayPlaces(places);
        
    } catch (error) {
        console.error('Error fetching places:', error);
        showError('places-list', 'Failed to load places. Please try again later.');
    }
}

/**
 * Display places in the DOM
 * @param {Array} places - Array of place objects
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    
    if (!places || places.length === 0) {
        placesList.innerHTML = '<p class="no-places">No places available.</p>';
        return;
    }
    
    placesList.innerHTML = '';
    
    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.dataset.price = place.price_per_night;
        
        const rating = place.average_rating 
            ? `⭐ ${place.average_rating.toFixed(1)}` 
            : '⭐ No reviews';
        
        placeCard.innerHTML = `
            <h3>${escapeHTML(place.name)}</h3>
            <p class="description">${escapeHTML(place.description || 'No description available.')}</p>
            <p class="location">📍 ${escapeHTML(place.city || 'Unknown')}, ${escapeHTML(place.country || 'Unknown')}</p>
            <p class="price">💰 $${place.price_per_night}/night</p>
            <p class="rating">${rating}</p>
            <button onclick="window.location.href='place.html?id=${place.id}'" class="btn-view">
                View Details
            </button>
        `;
        
        placesList.appendChild(placeCard);
    });
}

/**
 * Filter places by price
 * @param {string} maxPrice - Maximum price or 'all'
 */
function filterPlacesByPrice(maxPrice) {
    const placeCards = document.querySelectorAll('.place-card');
    
    placeCards.forEach(card => {
        const price = parseFloat(card.dataset.price);
        
        if (maxPrice === 'all' || price <= parseFloat(maxPrice)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

/**
 * Setup price filter
 */
function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            filterPlacesByPrice(event.target.value);
        });
    }
}

/**
 * Update UI based on authentication status
 */
function updateAuthUI() {
    const loginLink = document.getElementById('login-link');
    const navLogin = document.getElementById('nav-login');
    
    if (isAuthenticated()) {
        if (loginLink) loginLink.style.display = 'none';
        if (navLogin) navLogin.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'block';
        if (navLogin) navLogin.style.display = 'block';
    }
}

// Initialize index page
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    fetchPlaces();
    setupPriceFilter();
});
