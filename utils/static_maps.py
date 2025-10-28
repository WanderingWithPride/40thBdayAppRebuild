"""
Google Static Maps API Integration
Generates static map images for sharing and embedding
"""

import os
from typing import List, Dict, Optional
from urllib.parse import quote

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

def generate_static_map_url(center: str, zoom: int = 12, size: str = "600x400",
                            markers: List[Dict] = None, maptype: str = "roadmap",
                            scale: int = 2) -> str:
    """
    Generate Static Maps API URL

    Args:
        center: Center point (address or lat,lon)
        zoom: Zoom level (0-21)
        size: Image size (widthxheight), max 640x640
        markers: List of marker dictionaries with 'location', 'color', 'label'
        maptype: Map type (roadmap, satellite, terrain, hybrid)
        scale: Image scale (1 or 2 for retina)

    Returns:
        Static map image URL
    """
    if not GOOGLE_MAPS_API_KEY:
        return ""

    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    params = f"?center={quote(center)}&zoom={zoom}&size={size}&maptype={maptype}&scale={scale}"

    # Add markers
    if markers:
        for marker in markers:
            location = marker.get('location', '')
            color = marker.get('color', 'red')
            label = marker.get('label', '')

            marker_str = f"&markers=color:{color}"
            if label:
                marker_str += f"|label:{label}"
            marker_str += f"|{quote(location)}"

            params += marker_str

    params += f"&key={GOOGLE_MAPS_API_KEY}"

    return base_url + params


def generate_trip_map(hotel_location: str, activities: List[Dict],
                      size: str = "800x600") -> str:
    """
    Generate a static map showing all trip locations

    Args:
        hotel_location: Hotel address or coordinates
        activities: List of activity dictionaries with 'name' and 'location'
        size: Image size

    Returns:
        Static map URL
    """
    markers = []

    # Add hotel marker
    markers.append({
        'location': hotel_location,
        'color': 'red',
        'label': 'H'
    })

    # Add activity markers
    for idx, activity in enumerate(activities[:10]):  # Max 10 markers
        location = activity.get('location', '')
        if isinstance(location, dict):
            lat = location.get('lat', 0)
            lon = location.get('lon', 0)
            location = f"{lat},{lon}"

        if location:
            markers.append({
                'location': location,
                'color': 'blue',
                'label': str(idx + 1)
            })

    return generate_static_map_url(
        center=hotel_location,
        zoom=12,
        size=size,
        markers=markers,
        maptype="roadmap",
        scale=2
    )


def generate_route_map(origin: str, destination: str, waypoints: List[str] = None,
                       size: str = "600x400") -> str:
    """
    Generate a static map showing a route

    Args:
        origin: Starting location
        destination: Ending location
        waypoints: Optional intermediate stops
        size: Image size

    Returns:
        Static map URL with route drawn
    """
    if not GOOGLE_MAPS_API_KEY:
        return ""

    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    params = f"?size={size}&scale=2"

    # Add origin and destination markers
    params += f"&markers=color:green|label:A|{quote(origin)}"
    params += f"&markers=color:red|label:B|{quote(destination)}"

    # Add path (route)
    path_points = [origin]
    if waypoints:
        path_points.extend(waypoints)
    path_points.append(destination)

    params += "&path=color:0x0000ff|weight:5"
    for point in path_points:
        params += f"|{quote(point)}"

    params += f"&key={GOOGLE_MAPS_API_KEY}"

    return base_url + params
