"""
Google Directions and Route Optimization API Integration
Provides turn-by-turn directions and optimized multi-stop routing
"""

import requests
from typing import List, Dict, Optional, Tuple
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

def get_directions(origin: str, destination: str, mode: str = "driving",
                   alternatives: bool = True) -> Optional[Dict]:
    """
    Get directions between two points

    Args:
        origin: Starting location (address or lat,lon)
        destination: Ending location (address or lat,lon)
        mode: Travel mode (driving, walking, bicycling, transit)
        alternatives: Return alternative routes

    Returns:
        Directions data or None
    """
    api_key = get_api_key()
    if not api_key:
        return None

    url = "https://maps.googleapis.com/maps/api/directions/json"

    params = {
        'origin': origin,
        'destination': destination,
        'mode': mode,
        'alternatives': alternatives,
        'departure_time': 'now',  # For real-time traffic
        'key': api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Directions API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Directions API request failed: {e}")
        return None


def optimize_waypoints(origin: str, destination: str, waypoints: List[str]) -> Optional[Dict]:
    """
    Optimize the order of waypoints for shortest route

    Args:
        origin: Starting location
        destination: Ending location
        waypoints: List of intermediate locations

    Returns:
        Optimized route data or None
    """
    api_key = get_api_key()
    if not api_key or not waypoints:
        return None

    url = "https://maps.googleapis.com/maps/api/directions/json"

    # Format waypoints for optimization
    waypoints_str = "optimize:true|" + "|".join(waypoints)

    params = {
        'origin': origin,
        'destination': destination,
        'waypoints': waypoints_str,
        'mode': 'driving',
        'departure_time': 'now',
        'key': api_key
    }

    try:
        response = requests.get(url, params=params, timeout=15)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Route optimization error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Route optimization request failed: {e}")
        return None


def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable string"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        mins = seconds // 60
        return f"{mins} min"
    else:
        hours = seconds // 3600
        mins = (seconds % 3600) // 60
        return f"{hours}h {mins}m" if mins > 0 else f"{hours}h"


def format_distance(meters: int) -> str:
    """Format distance in meters to human-readable string"""
    if meters < 1000:
        return f"{meters} m"
    else:
        km = meters / 1000
        miles = km * 0.621371
        return f"{miles:.1f} mi"


def render_directions_card(directions: Dict, route_index: int = 0):
    """
    Render a directions card with turn-by-turn instructions

    Args:
        directions: Directions data from API
        route_index: Which route to display (if multiple alternatives)
    """
    if not directions or directions.get('status') != 'OK':
        st.error("❌ Could not get directions")
        return

    routes = directions.get('routes', [])
    if not routes or route_index >= len(routes):
        st.error("❌ No routes found")
        return

    route = routes[route_index]
    leg = route['legs'][0]  # First leg (origin to destination)

    # Route summary
    duration = leg['duration']['value']
    distance = leg['distance']['value']
    duration_traffic = leg.get('duration_in_traffic', {}).get('value', duration)

    st.markdown(f"""
<div style="background: #f0f8ff; padding: 15px; border-radius: 10px; border-left: 4px solid #4285f4;">
<h4 style="margin: 0;">🚗 Route {route_index + 1}</h4>
<p style="margin: 10px 0 0 0; font-size: 1.1rem;">
<strong>{format_duration(duration_traffic)}</strong> ({format_distance(distance)})
</p>
{f'<p style="margin: 5px 0 0 0; color: #e74c3c;">🚦 {format_duration(duration_traffic - duration)} delay due to traffic</p>' if duration_traffic > duration else ''}
</div>
""", unsafe_allow_html=True)

    # Turn-by-turn instructions
    with st.expander("📍 Turn-by-Turn Directions", expanded=True):
        steps = leg.get('steps', [])

        for idx, step in enumerate(steps, 1):
            instruction = step.get('html_instructions', '')
            # Remove HTML tags from instructions
            import re
            clean_instruction = re.sub('<.*?>', '', instruction)

            step_distance = step['distance']['text']
            step_duration = step['duration']['text']

            st.markdown(f"**{idx}.** {clean_instruction}")
            st.caption(f"   {step_distance} • {step_duration}")


def render_route_optimizer(activities: List[Dict], hotel_location: Tuple[float, float]):
    """
    Render route optimization widget for multiple activities

    Args:
        activities: List of activity dictionaries with 'name' and 'location'
        hotel_location: Tuple of (lat, lon) for hotel
    """
    st.subheader("🗺️ Route Optimizer")
    st.write("Plan the most efficient order to visit your activities!")

    if not activities:
        st.info("ℹ️ No activities to optimize")
        return

    # Select activities to include in route
    selected = st.multiselect(
        "Select activities to include:",
        options=[a['name'] for a in activities],
        default=[a['name'] for a in activities][:5]  # Default first 5
    )

    if len(selected) < 2:
        st.warning("⚠️ Select at least 2 activities to optimize route")
        return

    if st.button("🎯 Optimize Route", type="primary"):
        # Filter selected activities
        selected_activities = [a for a in activities if a['name'] in selected]

        # Extract locations
        waypoints = []
        for activity in selected_activities:
            loc = activity.get('location', {})
            if isinstance(loc, dict):
                lat = loc.get('lat', 0)
                lon = loc.get('lon', 0)
                waypoints.append(f"{lat},{lon}")
            elif isinstance(loc, str):
                waypoints.append(loc)

        if not waypoints:
            st.error("❌ Could not extract locations from activities")
            return

        # Optimize route
        origin = f"{hotel_location[0]},{hotel_location[1]}"
        destination = origin  # Return to hotel

        with st.spinner("Optimizing route..."):
            result = optimize_waypoints(origin, destination, waypoints)

            if result and result.get('status') == 'OK':
                route = result['routes'][0]
                waypoint_order = route.get('waypoint_order', [])

                st.success("✅ Route optimized!")

                # Display optimized order
                st.markdown("### 🎯 Recommended Visit Order:")

                total_duration = 0
                total_distance = 0

                for idx, waypoint_idx in enumerate(waypoint_order, 1):
                    activity = selected_activities[waypoint_idx]
                    st.write(f"**{idx}.** {activity['name']}")

                # Show route summary
                for leg in route['legs']:
                    total_duration += leg['duration']['value']
                    total_distance += leg['distance']['value']

                st.markdown(f"""
<div style="background: #e8f5e9; padding: 15px; border-radius: 10px; margin-top: 20px;">
<h4 style="margin: 0;">Total Route</h4>
<p style="margin: 10px 0 0 0;"><strong>⏱️ Time:</strong> {format_duration(total_duration)}</p>
<p style="margin: 5px 0 0 0;"><strong>📏 Distance:</strong> {format_distance(total_distance)}</p>
</div>
""", unsafe_allow_html=True)

                # Compare with original order
                st.info("💡 This route is optimized to minimize total drive time!")
            else:
                st.error("❌ Could not optimize route. Try with fewer locations.")


def get_route_polyline(directions: Dict, route_index: int = 0) -> Optional[str]:
    """
    Extract polyline from directions for drawing on map

    Args:
        directions: Directions data
        route_index: Which route (if multiple)

    Returns:
        Encoded polyline string or None
    """
    if not directions or directions.get('status') != 'OK':
        return None

    routes = directions.get('routes', [])
    if not routes or route_index >= len(routes):
        return None

    return routes[route_index].get('overview_polyline', {}).get('points')
