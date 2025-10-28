"""
Google Geocoding API Integration
Converts addresses to coordinates and vice versa
"""

import requests
from typing import Optional, Dict, Tuple
import streamlit as st
import os

def get_api_key():
    """Get Google Maps API key from environment variables or Streamlit secrets"""
    # First try environment variable
    api_key = os.getenv('GOOGLE_MAPS_API_KEY', '')
    if api_key:
        return api_key

    # Fall back to Streamlit secrets
    try:
        return st.secrets.get("GOOGLE_MAPS_API_KEY", "")
    except:
        return ""

@st.cache_data(ttl=86400)  # Cache for 24 hours
def geocode_address(address: str) -> Optional[Dict]:
    """
    Convert address to coordinates

    Args:
        address: Street address or place name

    Returns:
        Geocoding result dictionary or None
    """
    api_key = get_api_key()
    if not api_key:
        return None

    url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        'address': address,
        'key': api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK' and data.get('results'):
                return data['results'][0]
        return None
    except Exception as e:
        print(f"Geocoding request failed: {e}")
        return None


@st.cache_data(ttl=86400)  # Cache for 24 hours
def reverse_geocode(lat: float, lon: float) -> Optional[Dict]:
    """
    Convert coordinates to address

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        Reverse geocoding result dictionary or None
    """
    api_key = get_api_key()
    if not api_key:
        return None

    url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        'latlng': f"{lat},{lon}",
        'key': api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK' and data.get('results'):
                return data['results'][0]
        return None
    except Exception as e:
        print(f"Reverse geocoding request failed: {e}")
        return None


def get_coordinates(address: str) -> Optional[Tuple[float, float]]:
    """
    Get coordinates from address (simplified)

    Args:
        address: Street address

    Returns:
        Tuple of (lat, lon) or None
    """
    result = geocode_address(address)
    if result:
        location = result.get('geometry', {}).get('location', {})
        return (location.get('lat'), location.get('lng'))
    return None


def get_formatted_address(lat: float, lon: float) -> Optional[str]:
    """
    Get formatted address from coordinates (simplified)

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        Formatted address string or None
    """
    result = reverse_geocode(lat, lon)
    if result:
        return result.get('formatted_address')
    return None


def validate_address(address: str) -> Dict:
    """
    Validate an address

    Args:
        address: Address to validate

    Returns:
        Validation result with status and details
    """
    result = geocode_address(address)

    if result:
        return {
            "valid": True,
            "formatted_address": result.get('formatted_address'),
            "coordinates": result.get('geometry', {}).get('location', {}),
            "place_id": result.get('place_id'),
            "types": result.get('types', [])
        }
    else:
        return {
            "valid": False,
            "error": "Address not found or invalid"
        }
