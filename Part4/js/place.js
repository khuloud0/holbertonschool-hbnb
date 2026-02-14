/**
 * PLACE.JS - Place details page for HBnB
 * Handles fetching and displaying place details and reviews
 */

/**
 * Fetch place details
 */
async function fetchPlaceDetails() {
    const placeId = getUrlParameter('id');
    
    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }
    
    const token = getToken();
    showLoading('place-details');
    
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
            }
            throw new Error('Failed to fetch place details');
        }
        
        const place = await response.json();
        displayPlaceDetails(place);
        
        // Show/hide review form based on authentication
        const addReviewSection = document.getElementById('add-review');
        if (addReviewSection) {
            addReviewSection.style.display = token ? 'block' : 'none';
        }
        
        // Setup review form if authenticated
        if (token) {
            setupReviewForm(placeId, token);
        }
        
    } catch (error) {
        console.error('Error fetching place details:', error);
        showError('place-details', error.message);
    }
}

/**
 * Display place details
 * @param {Object} place - Place object
 */
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    
    const price = place.price_per_night ? `$${place.price_per_night}/night` : 'Price not available';
    const rating = place.average_rating 
        ? `⭐ ${place.average_rating.toFixed(1)} (${place.reviews?.length || 0} reviews)`
        : '⭐ No reviews yet';
    
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
            <h1 class="place-title">${escapeHTML(place.name)}</h1>
            <div class="place-location">📍 ${escapeHTML(place.city || 'Unknown')}, ${escapeHTML(place.country || 'Unknown')}</div>
            <div class="place-rating-large">${rating}</div>
            <div class="place-price">💰 ${price}</div>
            <div class="place-host">🏠 Hosted by ${escapeHTML(place.host_name || 'Unknown')}</div>
            <div class="place-description">
                <h2>About this place</h2>
                <p>${escapeHTML(place.description || 'No description available.')}</p>
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
        
        const rating = document.getElementById('rating').value;
        const text = document.getElementById('review-text').value;
        
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
            
            // Refresh place details
            fetchPlaceDetails();
            
        } catch (error) {
            console.error('Error submitting review:', error);
            alert(`❌ ${error.message}`);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit Review';
        }
    });
}

/**
 * Update UI based on authentication
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

// Initialize place details page
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    fetchPlaceDetails();
});
