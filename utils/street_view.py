"""
Google Street View Static API Integration
Provides street-level preview images of locations
"""

import os
from typing import Optional
import streamlit as st

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

def get_street_view_url(location: str, size: str = "600x400", heading: int = None,
                        pitch: int = 0, fov: int = 90) -> str:
    """
    Get Street View static image URL

    Args:
        location: Address or lat,lon coordinates
        size: Image size (widthxheight), max 640x640
        heading: Camera heading (0-360 degrees), None for best view
        pitch: Camera pitch (-90 to 90 degrees), 0 is horizontal
        fov: Field of view (0-120 degrees), default 90

    Returns:
        Street View image URL
    """
    if not GOOGLE_MAPS_API_KEY:
        return ""

    url = "https://maps.googleapis.com/maps/api/streetview"
    params = f"?size={size}&location={location}&fov={fov}&pitch={pitch}&key={GOOGLE_MAPS_API_KEY}"

    if heading is not None:
        params += f"&heading={heading}"

    return url + params


def get_street_view_metadata(location: str) -> dict:
    """
    Check if Street View is available for a location

    Args:
        location: Address or lat,lon coordinates

    Returns:
        Metadata dictionary with availability info
    """
    if not GOOGLE_MAPS_API_KEY:
        return {"status": "NO_KEY"}

    import requests

    url = "https://maps.googleapis.com/maps/api/streetview/metadata"
    params = {
        'location': location,
        'key': GOOGLE_MAPS_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "ERROR"}
    except:
        return {"status": "ERROR"}


def render_street_view_preview(location: str, title: str = "Street View",
                                size: str = "600x300"):
    """
    Render a Street View preview image in Streamlit

    Args:
        location: Address or lat,lon coordinates
        title: Title for the preview
        size: Image size
    """
    # Check if Street View is available
    metadata = get_street_view_metadata(location)

    if metadata.get('status') == 'OK':
        st.markdown(f"### 📸 {title}")

        # Get image URL
        image_url = get_street_view_url(location, size=size)

        if image_url:
            st.image(image_url, use_container_width=True, caption=f"Street View: {location}")
        else:
            st.info("ℹ️ Street View not available - API key missing")
    elif metadata.get('status') == 'ZERO_RESULTS':
        st.info(f"ℹ️ Street View not available for {title}")
    else:
        st.info(f"ℹ️ Could not load Street View preview")


def add_street_view_to_location(location_dict: dict, size: str = "400x200") -> str:
    """
    Generate Street View HTML for a location dictionary

    Args:
        location_dict: Dictionary with 'lat', 'lon', or 'address'
        size: Image size

    Returns:
        HTML string with Street View image
    """
    if isinstance(location_dict, dict):
        if 'lat' in location_dict and 'lon' in location_dict:
            location = f"{location_dict['lat']},{location_dict['lon']}"
        elif 'address' in location_dict:
            location = location_dict['address']
        else:
            return ""
    elif isinstance(location_dict, str):
        location = location_dict
    else:
        return ""

    url = get_street_view_url(location, size=size)
    if url:
        return f'<img src="{url}" style="width:100%; border-radius: 8px;" />'
    else:
        return ""
