"""
Google Places API Integration
Provides restaurant/activity discovery, place details, and search functionality
"""

import requests
from typing import List, Dict, Optional
import streamlit as st

def get_api_key():
    """Get Google Maps API key from Streamlit secrets"""
    try:
        return st.secrets.get("GOOGLE_MAPS_API_KEY", "")
    except:
        return ""

def search_nearby_places(lat: float, lon: float, place_type: str = "restaurant",
                         radius: int = 5000, min_rating: float = None,
                         max_results: int = 20) -> List[Dict]:
    """
    Search for nearby places using Google Places API (New)

    Args:
        lat: Latitude
        lon: Longitude
        place_type: Type of place (restaurant, cafe, bar, tourist_attraction, etc)
        radius: Search radius in meters (default 5km)
        min_rating: Minimum rating filter (0-5)
        max_results: Maximum number of results

    Returns:
        List of place dictionaries
    """
    api_key = get_api_key()
    if not api_key:
        return []

    url = "https://places.googleapis.com/v1/places:searchNearby"

    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.priceLevel,places.photos,places.currentOpeningHours,places.location,places.types,places.websiteUri,places.nationalPhoneNumber'
    }

    data = {
        "includedTypes": [place_type],
        "maxResultCount": min(max_results, 20),  # API max is 20
        "locationRestriction": {
            "circle": {
                "center": {"latitude": lat, "longitude": lon},
                "radius": radius
            }
        }
    }

    if min_rating:
        data["minRating"] = min_rating

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)

        if response.status_code == 200:
            return response.json().get('places', [])
        else:
            print(f"Places API error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Places API request failed: {e}")
        return []


def get_place_details(place_id: str) -> Optional[Dict]:
    """
    Get detailed information about a specific place

    Args:
        place_id: Google Place ID

    Returns:
        Place details dictionary or None
    """
    api_key = get_api_key()
    if not api_key:
        return None

    url = f"https://places.googleapis.com/v1/places/{place_id}"

    headers = {
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'id,displayName,formattedAddress,rating,userRatingCount,priceLevel,photos,currentOpeningHours,reviews,websiteUri,nationalPhoneNumber,businessStatus,location,types,editorialSummary,accessibilityOptions'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Place details error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Place details request failed: {e}")
        return None


def get_place_photo_url(photo_reference: Dict, max_width: int = 400) -> str:
    """
    Get URL for a place photo

    Args:
        photo_reference: Photo reference from Places API
        max_width: Maximum width in pixels

    Returns:
        Photo URL
    """
    api_key = get_api_key()
    if not api_key or not photo_reference:
        return ""

    # Extract photo name from reference
    photo_name = photo_reference.get('name', '')
    if not photo_name:
        return ""

    # Construct photo URL
    return f"https://places.googleapis.com/v1/{photo_name}/media?maxWidthPx={max_width}&key={api_key}"


def search_restaurants_by_cuisine(lat: float, lon: float, cuisine: str = None,
                                   min_rating: float = 3.5, radius: int = 8000) -> List[Dict]:
    """
    Search for restaurants filtered by cuisine type

    Args:
        lat: Latitude
        lon: Longitude
        cuisine: Cuisine type (italian, mexican, seafood, etc) - optional
        min_rating: Minimum rating (default 3.5)
        radius: Search radius in meters (default 8km ≈ 5 miles)

    Returns:
        List of restaurant dictionaries
    """
    results = search_nearby_places(
        lat=lat,
        lon=lon,
        place_type="restaurant",
        radius=radius,
        min_rating=min_rating,
        max_results=20
    )

    # Filter by cuisine if specified
    if cuisine and results:
        cuisine = cuisine.lower()
        filtered = []
        for place in results:
            # Check if cuisine keyword is in place name or types
            name = place.get('displayName', {}).get('text', '').lower()
            types = [t.lower() for t in place.get('types', [])]

            if cuisine in name or any(cuisine in t for t in types):
                filtered.append(place)

        return filtered if filtered else results  # Return all if no cuisine match

    return results


def get_price_symbols(price_level: int) -> str:
    """Convert price level to dollar signs"""
    if price_level == 0:
        return "Free"
    elif price_level == 1:
        return "$"
    elif price_level == 2:
        return "$$"
    elif price_level == 3:
        return "$$$"
    elif price_level == 4:
        return "$$$$"
    else:
        return "N/A"


def render_places_search_widget(location_name: str = "Amelia Island",
                                 lat: float = 30.6074, lon: float = -81.4493):
    """
    Render an interactive places search widget for Streamlit

    Args:
        location_name: Name of location for display
        lat: Latitude
        lon: Longitude
    """
    st.subheader(f"🔍 Discover Near {location_name}")

    # Search filters
    col1, col2, col3 = st.columns(3)

    with col1:
        search_type = st.selectbox(
            "Looking for",
            ["restaurant", "cafe", "bar", "tourist_attraction", "shopping_mall", "park"],
            format_func=lambda x: x.replace('_', ' ').title()
        )

    with col2:
        if search_type == "restaurant":
            cuisine = st.selectbox(
                "Cuisine",
                ["Any", "Italian", "Seafood", "American", "Mexican", "Asian", "French", "Indian"]
            )
        else:
            cuisine = "Any"

    with col3:
        min_rating = st.slider("Min Rating", 0.0, 5.0, 3.5, 0.5)

    # Search button
    if st.button("🔍 Search", type="primary", use_container_width=True):
        with st.spinner(f"Searching for {search_type}s nearby..."):
            if search_type == "restaurant" and cuisine != "Any":
                results = search_restaurants_by_cuisine(lat, lon, cuisine, min_rating)
            else:
                results = search_nearby_places(lat, lon, search_type, min_rating=min_rating)

            if results:
                st.success(f"✅ Found {len(results)} places!")

                for idx, place in enumerate(results):
                    display_name = place.get('displayName', {}).get('text', 'Unknown')
                    rating = place.get('rating', 0)
                    rating_count = place.get('userRatingCount', 0)
                    price = get_price_symbols(place.get('priceLevel', 0))
                    address = place.get('formattedAddress', 'Address not available')

                    with st.expander(f"⭐ {rating:.1f} - {display_name} ({price})", expanded=(idx < 3)):
                        col_a, col_b = st.columns([2, 1])

                        with col_a:
                            st.write(f"**📍 Address:** {address}")
                            st.write(f"**⭐ Rating:** {rating:.1f}/5 ({rating_count:,} reviews)")
                            st.write(f"**💰 Price:** {price}")

                            # Opening hours
                            opening_hours = place.get('currentOpeningHours', {})
                            if opening_hours:
                                is_open = opening_hours.get('openNow', False)
                                if is_open:
                                    st.success("✅ Open Now")
                                else:
                                    st.error("🔴 Currently Closed")

                            # Phone & website
                            phone = place.get('nationalPhoneNumber')
                            if phone:
                                st.write(f"**📞 Phone:** {phone}")

                            website = place.get('websiteUri')
                            if website:
                                st.markdown(f"**🌐 Website:** [{website}]({website})")

                        with col_b:
                            # Display photo if available
                            photos = place.get('photos', [])
                            if photos:
                                photo_url = get_place_photo_url(photos[0], max_width=300)
                                if photo_url:
                                    st.image(photo_url, use_container_width=True)

                            # Action buttons
                            place_id = place.get('id', '')
                            if st.button("📋 More Details", key=f"details_{idx}"):
                                details = get_place_details(place_id)
                                if details:
                                    st.json(details)
            else:
                st.warning("❌ No results found. Try adjusting your filters or search radius.")
                st.info("💡 Tip: Lower the minimum rating or change the cuisine type.")
