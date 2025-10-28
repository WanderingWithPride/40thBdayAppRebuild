"""
Google Air Quality and Pollen API Integration
Provides air quality monitoring and pollen forecasts for outdoor activity planning
"""

import requests
from typing import Dict, Optional, List
from datetime import datetime
import streamlit as st

def get_api_key():
    """Get Google Maps API key from Streamlit secrets"""
    try:
        return st.secrets.get("GOOGLE_MAPS_API_KEY", "")
    except:
        return ""

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_air_quality(lat: float, lon: float) -> Optional[Dict]:
    """
    Get current air quality data for a location

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        Air quality data dictionary or None
    """
    api_key = get_api_key()
    if not api_key:
        return None

    url = "https://airquality.googleapis.com/v1/currentConditions:lookup"

    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'key': api_key
    }

    data = {
        "location": {
            "latitude": lat,
            "longitude": lon
        }
    }

    try:
        response = requests.post(url, headers=headers, params=params, json=data, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Air Quality API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Air Quality API request failed: {e}")
        return None


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_pollen_forecast(lat: float, lon: float, days: int = 5) -> Optional[Dict]:
    """
    Get pollen forecast for a location

    Args:
        lat: Latitude
        lon: Longitude
        days: Number of forecast days (1-5)

    Returns:
        Pollen forecast dictionary or None
    """
    api_key = get_api_key()
    if not api_key:
        return None

    url = "https://pollen.googleapis.com/v1/forecast:lookup"

    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'key': api_key,
        'days': min(days, 5)  # API max is 5 days
    }

    data = {
        "location": {
            "latitude": lat,
            "longitude": lon
        }
    }

    try:
        response = requests.post(url, headers=headers, params=params, json=data, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Pollen API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Pollen API request failed: {e}")
        return None


def get_aqi_category(aqi: int) -> str:
    """Get AQI category from numeric value"""
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"


def get_aqi_color(category: str) -> str:
    """Get color code for AQI category"""
    colors = {
        "Good": "#00e400",
        "Moderate": "#ffff00",
        "Unhealthy for Sensitive Groups": "#ff7e00",
        "Unhealthy": "#ff0000",
        "Very Unhealthy": "#8f3f97",
        "Hazardous": "#7e0023"
    }
    return colors.get(category, "#cccccc")


def get_aqi_recommendation(category: str) -> str:
    """Get health recommendation for AQI category"""
    recommendations = {
        "Good": "✅ Air quality is ideal for outdoor activities.",
        "Moderate": "✅ Air quality is acceptable. Unusually sensitive people should limit prolonged outdoor exertion.",
        "Unhealthy for Sensitive Groups": "⚠️ People with respiratory conditions should limit prolonged outdoor exertion.",
        "Unhealthy": "⚠️ Everyone should limit prolonged outdoor exertion. Sensitive groups should avoid outdoor activities.",
        "Very Unhealthy": "🚨 Everyone should avoid prolonged outdoor exertion. Sensitive groups should avoid all outdoor activities.",
        "Hazardous": "🚨 Everyone should avoid all outdoor physical activities."
    }
    return recommendations.get(category, "Unknown air quality level.")


def get_pollen_level_text(index: int) -> str:
    """Convert pollen index to text description"""
    if index == 0:
        return "None"
    elif index == 1:
        return "🟢 Very Low"
    elif index == 2:
        return "🟡 Low"
    elif index == 3:
        return "🟠 Moderate"
    elif index == 4:
        return "🔴 High"
    elif index == 5:
        return "🔴🔴 Very High"
    else:
        return "Unknown"


def get_pollen_recommendation(max_index: int) -> Dict:
    """Get health recommendation for pollen level"""
    if max_index >= 4:
        return {
            "severity": "warning",
            "icon": "⚠️",
            "message": "High pollen levels",
            "action": "Take allergy medication before outdoor activities. Consider rescheduling if very sensitive."
        }
    elif max_index >= 3:
        return {
            "severity": "info",
            "icon": "💊",
            "message": "Moderate pollen levels",
            "action": "Consider taking allergy medication if you're sensitive to pollen."
        }
    else:
        return {
            "severity": "success",
            "icon": "✅",
            "message": "Low pollen levels",
            "action": "Safe for outdoor activities, even for allergy sufferers."
        }


def render_air_quality_widget(location_name: str = "Amelia Island",
                               lat: float = 30.6074, lon: float = -81.4493):
    """
    Render air quality and pollen widget for Streamlit

    Args:
        location_name: Name of location for display
        lat: Latitude
        lon: Longitude
    """
    st.subheader(f"🌬️ Air Quality & Pollen - {location_name}")

    # Get data
    aqi_data = get_air_quality(lat, lon)
    pollen_data = get_pollen_forecast(lat, lon, days=5)

    col1, col2 = st.columns(2)

    # Air Quality Section
    with col1:
        st.markdown("### 💨 Air Quality Index")

        if aqi_data:
            # Extract AQI from response
            indexes = aqi_data.get('indexes', [])
            if indexes:
                # Get Universal AQI (most comprehensive)
                universal_aqi = next((idx for idx in indexes if idx.get('code') == 'uaqi'), indexes[0])
                aqi = universal_aqi.get('aqi', 0)
                category = get_aqi_category(aqi)
                color = get_aqi_color(category)
                recommendation = get_aqi_recommendation(category)

                # Display AQI card
                st.markdown(f"""
<div style="background: {color}; padding: 20px; border-radius: 10px; text-align: center; color: {'white' if aqi > 100 else 'black'};">
<h1 style="margin: 0; font-size: 3rem;">{aqi}</h1>
<p style="margin: 10px 0 0 0; font-size: 1.2rem; font-weight: bold;">{category}</p>
</div>
""", unsafe_allow_html=True)

                st.info(recommendation)

                # Pollutant details
                with st.expander("📊 Pollutant Details"):
                    pollutants = aqi_data.get('pollutants', [])
                    if pollutants:
                        for p in pollutants:
                            name = p.get('displayName', p.get('code', 'Unknown'))
                            conc = p.get('concentration', {})
                            value = conc.get('value', 'N/A')
                            units = conc.get('units', '')
                            st.write(f"**{name}:** {value} {units}")
            else:
                st.info("ℹ️ AQI data not available for this location")
        else:
            st.info("ℹ️ Air quality data unavailable. Check your API key or try again later.")

    # Pollen Section
    with col2:
        st.markdown("### 🌸 Pollen Forecast")

        if pollen_data:
            daily_info = pollen_data.get('dailyInfo', [])

            if daily_info:
                # Show today's pollen
                today = daily_info[0]
                date_obj = datetime.fromisoformat(today.get('date', ''))

                st.write(f"**{date_obj.strftime('%A, %B %d')}**")

                # Get pollen indexes
                tree_idx = today.get('plantInfo', [{}])[0].get('indexInfo', {}).get('value', 0) if 'plantInfo' in today else 0
                grass_idx = today.get('plantInfo', [{}])[1].get('indexInfo', {}).get('value', 0) if len(today.get('plantInfo', [])) > 1 else 0
                weed_idx = today.get('plantInfo', [{}])[2].get('indexInfo', {}).get('value', 0) if len(today.get('plantInfo', [])) > 2 else 0

                st.write(f"**🌳 Tree Pollen:** {get_pollen_level_text(tree_idx)}")
                st.write(f"**🌾 Grass Pollen:** {get_pollen_level_text(grass_idx)}")
                st.write(f"**🌿 Weed Pollen:** {get_pollen_level_text(weed_idx)}")

                # Overall recommendation
                max_index = max(tree_idx, grass_idx, weed_idx)
                rec = get_pollen_recommendation(max_index)

                if rec['severity'] == "warning":
                    st.warning(f"{rec['icon']} {rec['message']}: {rec['action']}")
                elif rec['severity'] == "info":
                    st.info(f"{rec['icon']} {rec['message']}: {rec['action']}")
                else:
                    st.success(f"{rec['icon']} {rec['message']}: {rec['action']}")

                # 5-day forecast
                with st.expander("📅 5-Day Pollen Forecast"):
                    for day in daily_info[:5]:
                        date_obj = datetime.fromisoformat(day.get('date', ''))
                        plant_info = day.get('plantInfo', [])

                        tree = plant_info[0].get('indexInfo', {}).get('value', 0) if len(plant_info) > 0 else 0
                        grass = plant_info[1].get('indexInfo', {}).get('value', 0) if len(plant_info) > 1 else 0
                        weed = plant_info[2].get('indexInfo', {}).get('value', 0) if len(plant_info) > 2 else 0

                        st.write(f"**{date_obj.strftime('%a %m/%d')}:** Tree {tree} | Grass {grass} | Weed {weed}")
            else:
                st.info("ℹ️ Pollen forecast not available")
        else:
            st.info("ℹ️ Pollen data unavailable. Check your API key or try again later.")


def check_outdoor_activity_safety(lat: float, lon: float) -> Dict:
    """
    Check if conditions are safe for outdoor activities

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        Safety assessment dictionary
    """
    aqi_data = get_air_quality(lat, lon)
    pollen_data = get_pollen_forecast(lat, lon, days=1)

    issues = []
    safe = True

    # Check AQI
    if aqi_data:
        indexes = aqi_data.get('indexes', [])
        if indexes:
            aqi = indexes[0].get('aqi', 0)
            category = get_aqi_category(aqi)

            if aqi > 150:
                safe = False
                issues.append(f"🚨 Air quality is {category} (AQI: {aqi})")
            elif aqi > 100:
                issues.append(f"⚠️ Air quality is {category} (AQI: {aqi}) - sensitive groups should be cautious")

    # Check pollen
    if pollen_data:
        daily_info = pollen_data.get('dailyInfo', [])
        if daily_info:
            plant_info = daily_info[0].get('plantInfo', [])
            if plant_info:
                max_pollen = max([p.get('indexInfo', {}).get('value', 0) for p in plant_info])
                if max_pollen >= 4:
                    issues.append("⚠️ High pollen levels - take allergy medication")

    return {
        "safe": safe,
        "issues": issues,
        "recommendation": "✅ Conditions are good for outdoor activities!" if safe and not issues else "⚠️ Outdoor conditions may affect sensitive individuals"
    }
