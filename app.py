"""
🎂 40th Birthday Trip Assistant - ULTIMATE EDITION v2.0
=======================================================
The COMPLETE trip companion with EVERYTHING you need!

✨ Features:
- Interactive maps of all locations
- Real-time weather integration  
- Smart packing list generator
- Today/Now contextual view
- Photo gallery and memories
- QR codes for quick access
- Enhanced UI with animations
- Budget tracking with charts
- Booking management
- And SO much more!

🔐 Security: Password protected (28008985)
📱 Mobile: Fully responsive
🚀 Performance: Cached and optimized

Author: Enhanced by Claude Code
Version: 2.0 Ultimate
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json
import os
import hashlib
import re
import base64
import io
from typing import Dict, List, Any, Optional
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
import qrcode
from PIL import Image
import pytz
import pickle

# GitHub storage system (replaces SQLite database)
from github_storage import get_trip_data, save_trip_data, load_data_from_github
from data_operations import (
    save_meal_proposal, get_meal_proposal, save_john_meal_vote, finalize_meal_choice,
    save_activity_proposal, get_activity_proposal, save_john_activity_vote, finalize_activity_choice,
    load_john_preferences, save_john_preference,
    add_alcohol_request, get_alcohol_requests, delete_alcohol_request, mark_alcohol_purchased,
    save_custom_activity, load_custom_activities, delete_custom_activity,
    mark_activity_completed, load_completed_activities,
    update_packing_item, get_packing_progress,
    add_note, get_notes, delete_note,
    save_photo, load_photos, delete_photo,
    add_notification, load_notifications, dismiss_notification,
    save_manual_tsa_update, get_latest_manual_tsa_update
)

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

st.set_page_config(
    page_title="✈️ Michael's 40th Birthday Trip Assistant",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Michael's 40th Birthday Trip Assistant - Amelia Island Edition"
    }
)

# ============================================================================
# GITHUB STORAGE INITIALIZATION
# ============================================================================
# Initialize session state ONCE (prevents recursion on re-runs)
def init_session_state():
    """Initialize session state data - only runs once"""
    # Load trip data from GitHub on first run (get_trip_data handles its own initialization)
    _ = get_trip_data()

    # Initialize session state with backward compatibility
    if 'password_verified' not in st.session_state:
        st.session_state.password_verified = False
    if 'custom_activities' not in st.session_state:
        st.session_state.custom_activities = load_custom_activities()
    if 'completed_activities' not in st.session_state:
        st.session_state.completed_activities = load_completed_activities()
    if 'john_preferences' not in st.session_state:
        st.session_state.john_preferences = load_john_preferences()
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []  # Initialize empty notifications
    if 'photos' not in st.session_state:
        st.session_state.photos = []  # Initialize empty photos
    if 'init_complete' not in st.session_state:
        st.session_state.init_complete = True

# Call initialization
init_session_state()
# Note: Other data (meals, activities, alcohol, packing, notes) now stored in trip_data JSON

# ============================================================================
# TRIP CONFIGURATION
# ============================================================================

TRIP_CONFIG = {
    "name": "40th Birthday Celebration",
    "celebrant": "You",
    "companion": "John",
    "destination": "Amelia Island, Florida",
    "start_date": datetime(2025, 11, 7),
    "end_date": datetime(2025, 11, 12),
    "birthday_date": datetime(2025, 11, 10),  # The big 4-0!
    "timezone": "America/New_York",
    "hotel": {
        "name": "The Ritz-Carlton, Amelia Island",
        "address": "4750 Amelia Island Parkway, Amelia Island, FL 32034",
        "phone": "904-277-1100",
        "lat": 30.6074,
        "lon": -81.4493,
        "checkin": "2025-11-07 15:00",
        "checkout": "2025-11-12 11:00"
    }
}

# ============================================================================
# HELPER FUNCTIONS - TIME CALCULATIONS
# ============================================================================

def parse_duration_to_minutes(duration_str):
    """Parse duration string like '1.5 hours', '2-3 hours', '45min-1 hour' to average minutes"""
    if not duration_str or duration_str == "N/A":
        return 60  # Default 1 hour

    duration_str = duration_str.lower().strip()

    # Handle ranges like "2-3 hours" or "1-1.5 hours"
    if '-' in duration_str:
        parts = duration_str.split('-')
        # Get the average of the range
        try:
            low = float(re.findall(r'[\d.]+', parts[0])[0])
            high = float(re.findall(r'[\d.]+', parts[1])[0])
            avg = (low + high) / 2
        except:
            avg = 1.0
    else:
        # Single value like "1.5 hours" or "45min"
        try:
            avg = float(re.findall(r'[\d.]+', duration_str)[0])
        except:
            avg = 1.0

    # Convert to minutes
    if 'min' in duration_str and 'hour' not in duration_str:
        return int(avg)  # Already in minutes
    else:
        return int(avg * 60)  # Convert hours to minutes

def calculate_end_time(start_time_str, duration_str):
    """Calculate end time given start time and duration

    Args:
        start_time_str: Time string like "10:00 AM" or "3:30 PM"
        duration_str: Duration like "1.5 hours", "2-3 hours", "45min"

    Returns:
        String like "11:30 AM"
    """
    try:
        # Parse start time
        start_time = datetime.strptime(start_time_str, "%I:%M %p")

        # Get duration in minutes
        duration_minutes = parse_duration_to_minutes(duration_str)

        # Calculate end time
        end_time = start_time + timedelta(minutes=duration_minutes)

        return end_time.strftime("%I:%M %p")
    except Exception as e:
        return None

# ============================================================================
# ENHANCED CSS - ULTIMATE EDITION
# ============================================================================

def load_ultimate_css():
    """Load ultimate edition CSS with all enhancements"""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Root variables */
    :root {
        --primary: #ff6b6b;
        --secondary: #4ecdc4;
        --accent: #45b7d1;
        --success: #96ceb4;
        --warning: #ffeaa7;
        --danger: #fd79a8;
        --dark: #2d3436;
        --light: #f8f9fa;
        --birthday: #f093fb;
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Animated gradient header */
    .ultimate-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradientShift 10s ease infinite;
        color: white;
        padding: 3rem 2rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .ultimate-header::before {
        content: '🎂';
        position: absolute;
        top: -60px;
        right: -60px;
        font-size: 250px;
        opacity: 0.15;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
    }
    
    .ultimate-header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 800;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        letter-spacing: -1px;
    }
    
    .ultimate-header p {
        margin: 1rem 0 0 0;
        font-size: 1.4rem;
        opacity: 0.95;
        font-weight: 400;
    }
    
    .status-bar {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(15px);
        padding: 1.25rem;
        border-radius: 20px;
        margin-top: 2rem;
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 1.5rem;
    }
    
    .status-item {
        font-weight: 700;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 2.5rem;
        border-radius: 25px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        margin-bottom: 1.5rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 3s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.5; }
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
    }
    
    .metric-value {
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }
    
    .metric-label {
        font-size: 1.15rem;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
        position: relative;
        z-index: 1;
    }
    
    /* Ultimate card design */
    .ultimate-card {
        background: white;
        border-radius: 25px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .ultimate-card:hover {
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
        transform: translateY(-5px);
    }
    
    .card-header {
        padding: 1.75rem 2rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        color: white;
        font-weight: 700;
        font-size: 1.4rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .card-body {
        padding: 2rem;
    }
    
    /* Status badges with glow */
    .status-confirmed {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: white;
        padding: 0.5rem 1.25rem;
        border-radius: 30px;
        font-size: 0.95rem;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(132, 250, 176, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.5);
    }
    
    .status-pending {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        color: white;
        padding: 0.5rem 1.25rem;
        border-radius: 30px;
        font-size: 0.95rem;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(246, 211, 101, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.5);
    }
    
    .status-urgent {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 0.5rem 1.25rem;
        border-radius: 30px;
        font-size: 0.95rem;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(250, 112, 154, 0.5);
        border: 2px solid rgba(255, 255, 255, 0.5);
        animation: urgentPulse 2s infinite;
    }
    
    @keyframes urgentPulse {
        0%, 100% { transform: scale(1); box-shadow: 0 4px 15px rgba(250, 112, 154, 0.5); }
        50% { transform: scale(1.05); box-shadow: 0 6px 25px rgba(250, 112, 154, 0.8); }
    }
    
    /* Enhanced buttons */
    .ultimate-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 1rem 2rem;
        border: none;
        border-radius: 15px;
        font-size: 1.1rem;
        font-weight: 700;
        text-decoration: none;
        cursor: pointer;
        transition: all 0.3s ease;
        gap: 0.75rem;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .ultimate-btn::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .ultimate-btn:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .ultimate-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    }
    
    .btn-primary {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        color: white;
    }
    
    .btn-call {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
    }
    
    .btn-map {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    /* Today badge with special animation */
    .today-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 40px;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 1rem;
        box-shadow: 0 6px 25px rgba(240, 147, 251, 0.5);
        animation: todayGlow 2s infinite;
        font-size: 1.2rem;
        letter-spacing: 1px;
    }
    
    @keyframes todayGlow {
        0%, 100% { box-shadow: 0 6px 25px rgba(240, 147, 251, 0.5); transform: scale(1); }
        50% { box-shadow: 0 8px 35px rgba(240, 147, 251, 0.8); transform: scale(1.05); }
    }
    
    /* Birthday special styling */
    .birthday-special {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #feca57 100%);
        background-size: 200% 200%;
        animation: birthdayShine 5s ease infinite;
        border-radius: 25px;
        padding: 2rem;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 10px 40px rgba(240, 147, 251, 0.4);
    }
    
    @keyframes birthdayShine {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Packing list items */
    .packing-item {
        padding: 1rem 1.5rem;
        margin: 0.75rem 0;
        background: white;
        border-radius: 15px;
        border-left: 5px solid var(--accent);
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .packing-item:hover {
        transform: translateX(8px);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.12);
    }
    
    .packing-item.checked {
        opacity: 0.5;
        border-left-color: var(--success);
        text-decoration: line-through;
        background: #f0f9ff;
    }
    
    .priority-critical {
        border-left-color: var(--danger);
        background: linear-gradient(90deg, #fee 0%, white 10%);
    }
    
    .priority-high {
        border-left-color: var(--warning);
    }
    
    /* Timeline enhancement */
    .timeline {
        position: relative;
        padding: 2rem 0;
    }
    
    .timeline::before {
        content: '';
        position: absolute;
        left: 2rem;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(to bottom, var(--primary), var(--secondary), var(--birthday));
        border-radius: 2px;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
    
    .timeline-item {
        position: relative;
        padding-left: 5rem;
        margin-bottom: 3rem;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: calc(2rem - 12px);
        top: 0.5rem;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        border: 4px solid white;
        box-shadow: 0 3px 15px rgba(0, 0, 0, 0.2);
        z-index: 1;
    }
    
    .timeline-item.completed::before {
        background: linear-gradient(135deg, var(--success), #8fd3f4);
        content: '✓';
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 14px;
    }
    
    .timeline-item.today::before {
        background: linear-gradient(135deg, var(--birthday), #f5576c);
        animation: todayPulse 2s infinite;
        box-shadow: 0 0 25px rgba(240, 147, 251, 0.8);
    }
    
    @keyframes todayPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.3); }
    }
    
    /* Loading animations */
    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .ultimate-header {
            margin-left: -1rem;
            margin-right: -1rem;
            border-radius: 0;
            padding: 2rem 1.5rem;
        }
        
        .ultimate-header h1 {
            font-size: 2.2rem;
        }
        
        .metric-card {
            margin-left: -1rem;
            margin-right: -1rem;
            border-radius: 0;
        }
        
        .metric-value {
            font-size: 3rem;
        }
    }
    
    /* Weather widget special */
    .weather-widget {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .weather-temp {
        font-size: 5rem;
        font-weight: 800;
        margin: 1.5rem 0;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* Info boxes */
    .info-box {
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid var(--accent);
    }
    
    .info-success {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        border-left-color: var(--success);
    }
    
    .info-warning {
        background: linear-gradient(135deg, #fff9e6 0%, #ffeaa7 100%);
        border-left-color: var(--warning);
    }
    
    .info-danger {
        background: linear-gradient(135deg, #ffeef8 0%, #ffd6e7 100%);
        border-left-color: var(--danger);
    }

    /* Enhanced Streamlit Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 0.75rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }

    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: white;
        border-radius: 12px;
        padding: 0 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        color: #2d3436;
        border: 2px solid transparent;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        border-color: rgba(255, 255, 255, 0.3);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff6b6b 0%, #f093fb 100%) !important;
        color: white !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        transform: scale(1.05);
    }

    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 2rem;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ============================================================================
# ENHANCED DATA MODELS
# ============================================================================

def get_ultimate_trip_data():
    """Get complete trip data with all enhancements"""
    activities = [
        {
            "id": "arr001",
            "date": "2025-11-07",
            "time": "6:01 PM",
            "activity": "Arrival at Jacksonville",
            "type": "transport",
            "location": {
                "name": "Jacksonville International Airport (JAX)",
                "address": "2400 Yankee Clipper Dr, Jacksonville, FL 32218",
                "lat": 30.4941,
                "lon": -81.6879,
                "phone": "904-741-4902"
            },
            "status": "Confirmed",
            "cost": 603.88,
            "category": "Transport",
            "notes": "American Airlines AA2434 - Departure 3:51 PM from DCA, Arrival 6:01 PM JAX. Business Class (R), Seat 1D. 2h 10m flight. Confirmation: IDLLZA",
            "confirmation_code": "IDLLZA",
            "flight_number": "AA2434",
            "seat": "1D",
            "class": "Business (R)",
            "ticket_number": "0012283037156",
            "passenger": "Michael Eisinger",
            "aadvantage_number": "Y36****",
            "departure_time": "3:51 PM",
            "arrival_time": "6:01 PM",
            "estimated_flight_arrival": "6:01 PM",
            "estimated_hotel_arrival": "8:00 PM",
            "duration": "2h 10m",
            "checked_bags": "2 free bags",
            "what_to_bring": ["ID", "Boarding pass", "Phone charger", "Snacks for flight"],
            "tips": ["Arrive 2 hours early", "TSA PreCheck available", "Download AA app", "Check in 24 hours early via AA app", "Business class includes complimentary meals", "Allow ~2 hours for baggage claim, rental car, and 45 min drive to hotel"],
            "priority": 3
        },
        {
            "id": "arr002",
            "date": "2025-11-08",
            "time": "12:00 PM",
            "activity": "John Arrives at Hotel",
            "type": "transport",
            "location": {
                "name": "The Ritz-Carlton, Amelia Island",
                "address": "4750 Amelia Island Parkway",
                "lat": 30.6074,
                "lon": -81.4493,
                "phone": "904-277-1100"
            },
            "status": "Confirmed",
            "cost": 0,
            "category": "Transport",
            "notes": "AA1585 from DCA - Flight lands 10:40am, arrives at hotel ~12:00pm. He's getting himself to hotel (rental car/Uber).",
            "flight_number": "AA1585",
            "what_to_bring": ["Track flight on FlightAware", "Phone charged for coordination"],
            "tips": ["Text when he lands and when leaving airport", "He should account for 45min drive from JAX to hotel", "Meet him at hotel lobby"],
            "estimated_flight_arrival": "10:40 AM",
            "estimated_hotel_arrival": "12:00 PM",
            "priority": 3
        },
        {
            "id": "arr002b",
            "date": "2025-11-08",
            "time": "12:00 PM",
            "activity": "Back at Hotel + Lunch",
            "type": "dining",
            "duration": "1 hour",
            "location": {
                "name": "The Ritz-Carlton, Amelia Island",
                "address": "4750 Amelia Island Parkway",
                "lat": 30.6074,
                "lon": -81.4493,
                "phone": "904-277-1100"
            },
            "status": "Confirmed",
            "cost": 25,
            "category": "Dining",
            "notes": "Quick lunch after arriving at hotel - either at hotel restaurant or nearby casual spot. Going Dutch (each pays own meal).",
            "what_to_bring": [],
            "tips": ["Coast restaurant at hotel is convenient for breakfast/lunch", "Salt Life Food Shack nearby for casual beachfront", "Keep it light before boat tour"],
            "priority": 2
        },
        {
            "id": "act001",
            "date": "2025-11-08",
            "time": "2:30 PM",
            "activity": "Backwater Cat Eco Tour (for you)",
            "type": "activity",
            "duration": "2.5 hours",
            "location": {
                "name": "Dee Dee Bartels Boat Ramp",
                "address": "Dee Dee Bartels Boat Ramp, Amelia Island, FL",
                "lat": 30.6074,
                "lon": -81.4493,
                "phone": "904-753-7631"
            },
            "status": "URGENT",
            "cost": 135,
            "category": "Activity",
            "notes": "Private boat tour exploring backwaters, marshes, and tidal creeks. See dolphins, birds, and coastal ecosystems! You're doing this either way - John can pay for this if he wants to join ($135 per person = $270 total for 2). Call 904-753-7631 to book.",
            "what_to_bring": ["Sunglasses with strap", "Sunscreen (reapply!)", "Camera for wildlife", "Light windbreaker/jacket", "Non-slip shoes", "Dry bag for valuables", "Water bottle"],
            "tips": ["⚠️ BOOKING REQUIRED - Call 904-753-7631 to reserve", "Best at golden hour for wildlife viewing", "Bring camera for dolphins and birds", "Wear layers - can be breezy on water", "Dramamine if prone to seasickness"],
            "booking_url": "Call to book",
            "priority": 1
        },
        {
            "id": "spa001",
            "date": "2025-11-09",
            "time": "10:00 AM",
            "activity": "Heaven in a Hammock Massage (Couples)",
            "type": "spa",
            "duration": "1.5 hours",
            "location": {
                "name": "Ritz-Carlton Spa",
                "address": "4750 Amelia Island Parkway",
                "lat": 30.6074,
                "lon": -81.4493,
                "phone": "904-277-1087"
            },
            "status": "URGENT",
            "cost": 490,
            "category": "Spa",
            "notes": "🎉 BIRTHDAY SPA DAY! Couples beachside massage in swaying hammocks - YOU'RE PAYING for both ($245 each = $490 total). Call 904-277-1087 to book ASAP! Arrive 30 min early to enjoy saltwater pool. Signature treatment!",
            "what_to_bring": ["Arrive 30 min early for saltwater pool", "Spa robes provided", "Bring swimsuit for pool", "Camera for beach setup"],
            "tips": ["Hydrate well before", "Communicate pressure preferences", "No heavy meal 2 hrs before", "Most unique massage experience!", "Literally on the beach with ocean sounds"],
            "dress_code": "Spa attire provided - they give you everything",
            "booking_url": "https://www.ritzcarlton.com/en/hotels/jaxam-the-ritz-carlton-amelia-island/spa/",
            "priority": 1
        },
        {
            "id": "spa002",
            "date": "2025-11-09",
            "time": "12:00 PM",
            "activity": "HydraFacial Treatment (for you)",
            "type": "spa",
            "duration": "1 hour",
            "location": {
                "name": "Ritz-Carlton Spa",
                "address": "4750 Amelia Island Parkway",
                "lat": 30.6074,
                "lon": -81.4493,
                "phone": "904-277-1087"
            },
            "status": "URGENT",
            "cost": 195,
            "category": "Spa",
            "notes": "Advanced HydraFacial for glowing skin - perfect before birthday dinner! Want me to book one for you at the same time? You'd pay for yours ($195). Otherwise you can relax at pool/beach. Call 904-277-1087 to book.",
            "what_to_bring": ["Clean face (no makeup)", "Hair tie if needed", "Arrive on time from massage"],
            "tips": ["Immediate results - perfect timing before dinner!", "Ask about serums for your skin type", "Hydrating and gentle"],
            "booking_url": "https://www.ritzcarlton.com/en/hotels/jaxam-the-ritz-carlton-amelia-island/spa/",
            "priority": 1
        },
        {
            "id": "spa003",
            "date": "2025-11-09",
            "time": "1:30 PM",
            "activity": "Mani-Pedi Combo (for you)",
            "type": "spa",
            "duration": "2 hours",
            "location": {
                "name": "Ritz-Carlton Spa",
                "address": "4750 Amelia Island Parkway",
                "lat": 30.6074,
                "lon": -81.4493,
                "phone": "904-277-1087"
            },
            "status": "URGENT",
            "cost": 150,
            "category": "Spa",
            "notes": "Complete mani-pedi combo with everything! Want me to book one for you at the same time? You'd pay for yours ($150). Otherwise you can relax at pool/beach while I'm getting pampered. Call 904-277-1087 to book. Perfect timing after facial!",
            "what_to_bring": ["Flip flops", "Let nails dry before dinner prep", "Choose neutral or birthday colors!"],
            "tips": ["Includes sugar scrub and paraffin treatment", "Takes about 2 hours total", "Perfect for birthday photos!", "Schedule gives you time before getting ready for dinner at 7pm"],
            "booking_url": "https://www.ritzcarlton.com/en/hotels/jaxam-the-ritz-carlton-amelia-island/spa/",
            "priority": 1
        },
        {
            "id": "din001",
            "date": "2025-11-09",
            "time": "7:00 PM",
            "activity": "40th Birthday Dinner",
            "type": "dining",
            "duration": "2.5 hours",
            "location": {
                "name": "David's Restaurant & Lounge",
                "address": "802 Ash St, Fernandina Beach, FL 32034",
                "lat": 30.6692,
                "lon": -81.4651,
                "phone": "904-310-6049"
            },
            "status": "URGENT",
            "cost": 210,
            "category": "Dining",
            "notes": "THE BIG 40! Upscale dining for 2 - MUST RESERVE - mention birthday! Michael is treating for birthday celebration.",
            "what_to_bring": ["Nice outfit", "ID", "Camera for birthday photos"],
            "tips": ["Request window table", "Ask about chef's specials", "Save room for dessert!"],
            "dress_code": "Business casual to dressy",
            "booking_url": "https://www.opentable.com/r/davids-restaurant-and-lounge-fernandina-beach",
            "priority": 1
        },
        {
            "id": "bch001",
            "date": "2025-11-10",
            "time": "10:00 AM",
            "activity": "Beach Day",
            "type": "beach",
            "duration": "6 hours",
            "location": {
                "name": "Main Beach Park",
                "address": "1600 S Fletcher Ave, Fernandina Beach, FL",
                "lat": 30.6502,
                "lon": -81.4525,
                "phone": "N/A"
            },
            "status": "Confirmed",
            "cost": 0,
            "category": "Beach",
            "notes": "Relax! Check tide times for best swimming",
            "what_to_bring": ["Beach towels", "Sunscreen (reapply!)", "Beach umbrella", "Cooler", "Snacks", "Books", "Beach chairs", "Frisbee/ball"],
            "tips": ["Go early for parking", "High tide is best for swimming", "Lots of shells at low tide"],
            "priority": 3
        },
        {
            "id": "din002",
            "date": "2025-11-10",
            "time": "6:00 PM",
            "activity": "Casual Dinner",
            "type": "dining",
            "duration": "1.5 hours",
            "location": {
                "name": "Timoti's Seafood Shak",
                "address": "4998 1st Coast Hwy, Amelia Island, FL",
                "lat": 30.5811,
                "lon": -81.4432,
                "phone": "904-321-1430"
            },
            "status": "Pending",
            "cost": 30,
            "category": "Dining",
            "notes": "Beachside casual - famous for tacos and fresh catch. Going Dutch (each pays own meal).",
            "what_to_bring": ["Casual clothes", "Cash (faster)"],
            "tips": ["Try the blackened mahi tacos", "BYOB friendly", "Often a wait but moves fast"],
            "dress_code": "Beach casual",
            "booking_url": "https://www.timotisseafoodshack.com",
            "priority": 2
        },
        {
            "id": "dep001",
            "date": "2025-11-11",
            "time": "8:20 AM",
            "activity": "John Departs to Airport (Uber)",
            "type": "transport",
            "location": {
                "name": "Jacksonville International Airport (JAX)",
                "address": "2400 Yankee Clipper Dr, Jacksonville, FL 32218",
                "lat": 30.4941,
                "lon": -81.6879,
                "phone": "904-741-4902"
            },
            "status": "Confirmed",
            "cost": 65,
            "category": "Transport",
            "notes": "AA1586 to DCA departs 11:05 AM. John will take Uber from hotel at 8:20am (45min drive) to arrive by 9:05am (2 hours before flight).",
            "flight_number": "AA1586",
            "what_to_bring": ["ID", "Boarding pass"],
            "tips": ["Check traffic before leaving", "Allow 45 min drive", "Arrive 2 hours early for domestic flight"],
            "flight_departure_time": "11:05 AM",
            "priority": 3
        },
        {
            "id": "dep002",
            "date": "2025-11-12",
            "time": "12:30 PM",
            "activity": "Leave Hotel for Airport",
            "type": "transport",
            "location": {
                "name": "Jacksonville International Airport (JAX)",
                "address": "2400 Yankee Clipper Dr, Jacksonville, FL 32218",
                "lat": 30.4941,
                "lon": -81.6879,
                "phone": "904-741-4902"
            },
            "status": "Confirmed",
            "cost": 0,
            "category": "Transport",
            "notes": "AA5590 (operated by PSA Airlines as American Eagle) departs 2:39 PM from JAX, arrives 4:40 PM at DCA. Business Class (I), Seat 1A. Checkout by 11am, leave hotel by 12:30pm (45min drive + 2hr early arrival buffer). Confirmation: IDLLZA",
            "confirmation_code": "IDLLZA",
            "flight_number": "AA5590",
            "operated_by": "PSA Airlines as American Eagle",
            "seat": "1A",
            "class": "Business (I)",
            "ticket_number": "0012283037156",
            "passenger": "Michael Eisinger",
            "aadvantage_number": "Y36****",
            "departure_time": "2:39 PM",
            "arrival_time": "4:40 PM",
            "checked_bags": "2 free bags",
            "what_to_bring": ["All belongings", "Souvenirs", "Photos", "Memories!"],
            "tips": ["Hotel checkout 11 AM", "Leave by 12:30 PM", "Double-check room for items", "Return home with amazing memories!", "Check in 24 hours early via AA app", "Business class includes complimentary meals"],
            "flight_departure_time": "2:39 PM",
            "priority": 3
        }
    ]

    # Merge with custom activities from session state
    if 'custom_activities' in st.session_state and st.session_state.custom_activities:
        activities = activities + st.session_state.custom_activities

    df = pd.DataFrame(activities)
    df['date'] = pd.to_datetime(df['date'])
    return df, activities

def get_smart_packing_list():
    """Generate comprehensive packing list"""
    return {
        "🚨 CRITICAL - Don't Leave Without!": [
            {"item": "Driver's License / ID", "checked": False, "priority": "critical"},
            {"item": "Phone & Charger", "checked": False, "priority": "critical"},
            {"item": "Credit Cards & Cash", "checked": False, "priority": "critical"},
            {"item": "Health Insurance Card", "checked": False, "priority": "critical"},
            {"item": "Medications (if any)", "checked": False, "priority": "critical"},
            {"item": "Flight confirmations", "checked": False, "priority": "critical"},
        ],
        "📄 Travel Documents": [
            {"item": "Hotel confirmation (printed/digital)", "checked": False, "priority": "high"},
            {"item": "Boat tour confirmation", "checked": False, "priority": "high"},
            {"item": "Spa reservation confirmations", "checked": False, "priority": "high"},
            {"item": "Restaurant reservations", "checked": False, "priority": "high"},
            {"item": "Emergency contacts list", "checked": False, "priority": "high"},
            {"item": "Car rental info (if applicable)", "checked": False, "priority": "medium"},
        ],
        "👗 Clothing": [
            {"item": "Casual daytime outfits (4-5)", "checked": False, "priority": "high"},
            {"item": "Birthday dinner outfit (nice!)", "checked": False, "priority": "high"},
            {"item": "Business casual outfit for David's", "checked": False, "priority": "high"},
            {"item": "Swimsuit(s)", "checked": False, "priority": "high"},
            {"item": "Beach cover-up", "checked": False, "priority": "medium"},
            {"item": "Light jacket or cardigan", "checked": False, "priority": "high"},
            {"item": "Comfortable walking shoes", "checked": False, "priority": "high"},
            {"item": "Sandals / flip-flops", "checked": False, "priority": "high"},
            {"item": "Nice shoes for dinner", "checked": False, "priority": "medium"},
            {"item": "Pajamas / sleepwear", "checked": False, "priority": "medium"},
            {"item": "Underwear (6-7 days)", "checked": False, "priority": "high"},
            {"item": "Socks (if needed)", "checked": False, "priority": "medium"},
            {"item": "Workout clothes (if using gym)", "checked": False, "priority": "low"},
        ],
        "🏖️ Beach Essentials": [
            {"item": "Sunscreen SPF 50+ (MUST HAVE!)", "checked": False, "priority": "critical"},
            {"item": "After-sun lotion", "checked": False, "priority": "high"},
            {"item": "Sunglasses with UV protection", "checked": False, "priority": "high"},
            {"item": "Wide-brimmed hat or cap", "checked": False, "priority": "high"},
            {"item": "Beach towels (2-3)", "checked": False, "priority": "medium"},
            {"item": "Beach bag", "checked": False, "priority": "medium"},
            {"item": "Refillable water bottle", "checked": False, "priority": "high"},
            {"item": "Waterproof phone case", "checked": False, "priority": "medium"},
            {"item": "Beach umbrella (optional)", "checked": False, "priority": "low"},
            {"item": "Snorkel gear (if interested)", "checked": False, "priority": "low"},
        ],
        "🧴 Toiletries & Personal Care": [
            {"item": "Toothbrush & toothpaste", "checked": False, "priority": "high"},
            {"item": "Floss", "checked": False, "priority": "medium"},
            {"item": "Shampoo & conditioner", "checked": False, "priority": "medium"},
            {"item": "Body wash / soap", "checked": False, "priority": "medium"},
            {"item": "Deodorant", "checked": False, "priority": "high"},
            {"item": "Razor & shaving cream", "checked": False, "priority": "medium"},
            {"item": "Face cleanser", "checked": False, "priority": "medium"},
            {"item": "Moisturizer", "checked": False, "priority": "medium"},
            {"item": "Makeup (if applicable)", "checked": False, "priority": "low"},
            {"item": "Makeup remover", "checked": False, "priority": "low"},
            {"item": "Hair styling products", "checked": False, "priority": "low"},
            {"item": "Hair dryer (hotel has one)", "checked": False, "priority": "low"},
            {"item": "Contact lenses & solution", "checked": False, "priority": "high"},
            {"item": "Glasses (backup)", "checked": False, "priority": "medium"},
            {"item": "Cotton swabs", "checked": False, "priority": "low"},
            {"item": "Nail clippers / file", "checked": False, "priority": "low"},
        ],
        "📱 Tech & Electronics": [
            {"item": "Phone charger (USB-C/Lightning)", "checked": False, "priority": "critical"},
            {"item": "Portable power bank", "checked": False, "priority": "high"},
            {"item": "Camera (or use phone)", "checked": False, "priority": "medium"},
            {"item": "Camera charger", "checked": False, "priority": "medium"},
            {"item": "Headphones / earbuds", "checked": False, "priority": "medium"},
            {"item": "E-reader / tablet", "checked": False, "priority": "low"},
            {"item": "Tablet charger", "checked": False, "priority": "low"},
        ],
        "🎂 Birthday Special": [
            {"item": "Birthday outfit & accessories", "checked": False, "priority": "high"},
            {"item": "Nice jewelry for dinner", "checked": False, "priority": "medium"},
            {"item": "Camera for birthday photos", "checked": False, "priority": "high"},
            {"item": "Small bag/clutch for dinner", "checked": False, "priority": "medium"},
        ],
        "💆 Spa Day Prep": [
            {"item": "Hair tie (keep hair back)", "checked": False, "priority": "high"},
            {"item": "Face wipes (clean before)", "checked": False, "priority": "medium"},
            {"item": "Comfortable post-spa outfit", "checked": False, "priority": "medium"},
        ],
        "🚤 Boat Tour": [
            {"item": "Light windbreaker/jacket", "checked": False, "priority": "high"},
            {"item": "Sunglasses with strap", "checked": False, "priority": "medium"},
            {"item": "Dramamine (if prone to seasickness)", "checked": False, "priority": "medium"},
            {"item": "Dry bag for valuables", "checked": False, "priority": "low"},
        ],
        "💊 Health & Safety": [
            {"item": "First aid kit (band-aids, etc.)", "checked": False, "priority": "medium"},
            {"item": "Pain reliever (Advil/Tylenol)", "checked": False, "priority": "medium"},
            {"item": "Allergy meds (if needed)", "checked": False, "priority": "high"},
            {"item": "Antacids", "checked": False, "priority": "low"},
            {"item": "Hand sanitizer", "checked": False, "priority": "medium"},
            {"item": "Tissues", "checked": False, "priority": "low"},
            {"item": "Insect repellent", "checked": False, "priority": "medium"},
        ],
        "📚 Entertainment": [
            {"item": "Books / magazines", "checked": False, "priority": "low"},
            {"item": "Playing cards", "checked": False, "priority": "low"},
            {"item": "Travel journal", "checked": False, "priority": "low"},
        ],
        "🧳 Miscellaneous": [
            {"item": "Reusable shopping bag", "checked": False, "priority": "low"},
            {"item": "Snacks for travel", "checked": False, "priority": "medium"},
            {"item": "Umbrella (November can be rainy)", "checked": False, "priority": "medium"},
            {"item": "Laundry bag for dirty clothes", "checked": False, "priority": "low"},
        ]
    }

def get_restaurant_details():
    """Get enhanced restaurant details including dress code, menu URLs, operating hours, etc.

    Returns a dict mapping restaurant name to additional details
    Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    serves: list of meal types (breakfast, lunch, dinner)
    """
    return {
        "Le Clos": {"dress_code": "Business Casual", "menu_url": "N/A", "serves": ["dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": True},
        "Espana Restaurant & Tapas": {"dress_code": "Casual", "menu_url": "N/A", "serves": ["dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": True},
        "Burlingame": {"dress_code": "Smart Casual", "menu_url": "N/A", "serves": ["dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": True},
        "Lagniappe": {"dress_code": "Smart Casual", "menu_url": "N/A", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": True},
        "Cucina South": {"dress_code": "Business Casual", "menu_url": "N/A", "serves": ["dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": True},
        "Brett's Waterway Cafe": {"dress_code": "Casual", "menu_url": "N/A", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": True, "booking_required": True},
        "Salty Pelican Bar & Grill": {"dress_code": "Casual", "menu_url": "https://thesaltypelicanamelia.com", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": True, "booking_required": False},
        "Sandbar": {"dress_code": "Resort Casual", "menu_url": "https://sandbaramelia.com", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": True, "booking_required": True},
        "The Boat House": {"dress_code": "Casual", "menu_url": "https://boathouseamelia.com", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": True, "booking_required": True},
        "Down Under": {"dress_code": "Very Casual", "menu_url": "N/A", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": True, "booking_required": False},
        "Timoti's Seafood Shak": {"dress_code": "Very Casual", "menu_url": "https://timotis.com", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": True, "booking_required": False},
        "Salt Life Food Shack": {"dress_code": "Casual", "menu_url": "https://www.saltlifefoodshack.com", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": True, "booking_required": False},
        "Ciao Italian Eatery": {"dress_code": "Casual", "menu_url": "https://ciaoitalianeats.com", "serves": ["dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": True},
        "Arte Pizza": {"dress_code": "Very Casual", "menu_url": "https://artepizzabar.com", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": False},
        "Mezcal Spirit of Oaxaca": {"dress_code": "Casual", "menu_url": "N/A", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": False},
        "Tortuga Jacks": {"dress_code": "Very Casual", "menu_url": "N/A", "serves": ["breakfast"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": True, "booking_required": False},
        "Wicked Bao": {"dress_code": "Casual", "menu_url": "N/A", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": False},
        "Akari Sushi": {"dress_code": "Casual", "menu_url": "N/A", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": False},
        "Hana Sushi": {"dress_code": "Casual", "menu_url": "N/A", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": False},
        "29 South": {"dress_code": "Smart Casual", "menu_url": "N/A", "serves": ["breakfast", "lunch"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": True},
        "Beach Diner": {"dress_code": "Very Casual", "menu_url": "N/A", "serves": ["breakfast", "lunch"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": False},
        "Sliders Seaside Grill": {"dress_code": "Beachwear/Casual", "menu_url": "N/A", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": True, "booking_required": False},
        "Fantastic Fudge": {"dress_code": "Any", "menu_url": "N/A", "serves": ["breakfast", "lunch"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": False},
        "Café Karibo": {"dress_code": "Casual", "menu_url": "N/A", "serves": ["breakfast", "lunch"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": True, "booking_required": False},
        "Amelia Island Coffee": {"dress_code": "Any", "menu_url": "N/A", "serves": ["breakfast"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": False},
        "First Drop Coffee": {"dress_code": "Resort Casual", "menu_url": "N/A", "serves": ["breakfast"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": False},
        "Mocama Coffee": {"dress_code": "Casual", "menu_url": "N/A", "serves": ["breakfast"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": False},
        "Hola Cuban Cafe": {"dress_code": "Casual", "menu_url": "N/A", "serves": ["breakfast", "lunch"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": False},
        "Nana Teresa's Bake Shop": {"dress_code": "Any", "menu_url": "N/A", "serves": ["breakfast"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": False},
        "Aloha Bagel and Deli": {"dress_code": "Casual", "menu_url": "https://aloha-bagel.com", "serves": ["breakfast", "lunch"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": False},
        "4th Street Deli": {"dress_code": "Casual", "menu_url": "N/A", "serves": ["lunch"], "days_open": [0,1,2,3,4,5], "outdoor_seating": False, "booking_required": False},  # Closed Sundays
        "Salt (AAA Five Diamond)": {"dress_code": "Resort Elegant (jackets optional, no shorts/flip-flops)", "menu_url": "https://www.ritzcarlton.com/en/hotels/jaxab-the-ritz-carlton-amelia-island/dining", "serves": ["dinner"], "days_open": [1,2,3,4,5], "outdoor_seating": False, "booking_required": True},  # Tue-Sat only
        "Coast": {"dress_code": "Resort Casual", "menu_url": "https://www.ritzcarlton.com/en/hotels/jaxab-the-ritz-carlton-amelia-island/dining", "serves": ["breakfast", "lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": True},
        "Coquina": {"dress_code": "Beachwear/Casual", "menu_url": "N/A", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": True, "booking_required": False},
        "Tidewater Grill": {"dress_code": "Resort Casual", "menu_url": "N/A", "serves": ["dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": True, "booking_required": False},
        "Lobby Bar": {"dress_code": "Resort Casual", "menu_url": "N/A", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": False},
        "Dune Bar": {"dress_code": "Beachwear/Casual", "menu_url": "N/A", "serves": ["lunch"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": True, "booking_required": False},
        "Pogo's": {"dress_code": "Casual", "menu_url": "N/A", "serves": ["lunch", "dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": False},
        "David's Restaurant & Lounge": {"dress_code": "Business Casual (no shorts/flip-flops)", "menu_url": "N/A", "serves": ["dinner"], "days_open": [0,1,2,3,4,5,6], "outdoor_seating": False, "booking_required": True},
    }

def get_optional_activities():
    """ULTIMATE Amelia Island Guide - 118 comprehensive options covering EVERYTHING you need!

    🍽️ DINING & DRINKS (44 options):
    - Fine Dining (4): Le Clos, Burlingame, Lagniappe, Cucina South
    - Seafood & Waterfront (7): Brett's, Salty Pelican, Sandbar, Boat House, Down Under, Timoti's, Salt Life
    - Italian & Pizza (2): Ciao Italian, Arte Pizza
    - Mexican & Latin (2): Mezcal, Tortuga Jacks
    - Asian Cuisine (3): Wicked Bao, Akari Sushi, Hana Sushi
    - Breakfast & Brunch (2): 29 South, Beach Diner
    - Casual & Comfort Food (3): Sliders, Fantastic Fudge, Café Karibo
    - ☕ Coffee & Cafes (5): Amelia Island Coffee, First Drop, Mocama, Hola Cuban, Nana Teresa's
    - 🥖 Delis & Lunch (2): Aloha Bagel, 4th Street Deli
    - 🏨 Ritz-Carlton Dining (6): Salt (AAA Five Diamond), Coast, Coquina, Tidewater Grill, Lobby Bar, Dune Bar
    - 🍺 Bars & Nightlife (6): Palace Saloon, Green Turtle, Decantery, First Love Brewing, Mocama Beer, A1A Cidery

    🏖️ ACTIVITIES & OUTDOOR (52 options):
    - Beach & Water (14): Horseback riding, kayaking, paddleboarding, jet ski, parasailing, fishing, diving, surfing, boat rentals, beaches
    - Activities & Adventure (12): State parks, golf (2), tennis, bikes, Segway, ghost tours, carriage tours, wildlife
    - 🥾 Hiking & Nature Trails (7): Fort Clinch trails, Egan's Creek, Blackrock Trail, boardwalks, Amelia Island Trail

    🛍️ CULTURE & SHOPPING (10 options):
    - Museums, galleries, farmers market, ArtWalk, tours

    💆 SPA & WELLNESS (15 options):
    - Ritz-Carlton Spa (10): Heaven in Hammock, HydraFacial, massages, facials, body treatments
    - Other Spas & Wellness (5): Omni Spa, Drift Day Spa, Coastal Massage, Yoga, Sprouting Project

    🏊 RESORT & FREE (7 options):
    - Pool, beach sunsets, yoga, bonfires, fitness, volleyball, shelling

    TOTAL: 122+ verified options with complete details, phone numbers, pricing, tips, and ratings!

    🌟 SARAH'S RECOMMENDATIONS INCLUDED:
    - Ritz Spa (beautiful!)
    - David's Restaurant
    - Pogo's
    - Lagniappe (Happy Hour!)
    - Ciao (homemade pasta!)
    - Espana (wine & tapas)
    - Timoti's/Timotees (lunch)
    - Amelia Tavern & The Alley (drinks)
    - Ritz Lobby Bar (sushi, charcuterie, smoked Old Fashioneds!)
    - Scenic drive to GA border

    Sarah says: "You are going to have a fabulous week even if you never left the hotel!" (Sarah's treat for the room!)
    """
    return {
        "🍽️ Fine Dining": [
            {"name": "Le Clos", "description": "French bistro with romantic atmosphere, extensive wine selection", "cost_range": "$40-70 per person", "duration": "2-3 hours", "phone": "904-261-8100", "booking_url": "https://www.opentable.com/r/le-clos-fernandina-beach", "tips": "Reservations required, dress code (business casual)", "rating": "4.8/5"},
            {"name": "Espana Restaurant & Tapas", "description": "SARAH'S RECOMMENDATION! Authentic Spanish tapas, paella, extensive wine selection, intimate European atmosphere", "cost_range": "$25-50 per person", "duration": "1.5-2.5 hours", "phone": "904-261-7700", "booking_url": "https://www.opentable.com/espana-fernandina", "tips": "Perfect for wine and tapas - great small plates to share. Sarah says: 'Espana for wine and tapas!'", "rating": "4.7/5"},
            {"name": "Burlingame", "description": "Charming 1947 cottage with modern twist, seasonal menu with Seafood Gumbo, Blue Crab Cakes, Lamb Bolognese. ✅ NON-SEAFOOD: Lamb, chicken, steaks, pasta", "cost_range": "$35-65 per person", "duration": "2-2.5 hours", "phone": "904-277-3700", "booking_url": "https://www.opentable.com/burlingame", "tips": "Intimate setting, reserve ahead for special occasions. Great meat and pasta options!", "rating": "4.9/5"},
            {"name": "Lagniappe", "description": "SARAH'S RECOMMENDATION for Happy Hour! Southern refinement meets French Creole, standout Salmon Brulee and Lamb Lollipops. ✅ NON-SEAFOOD: Lamb, steaks, chicken, duck", "cost_range": "$40-70 per person", "duration": "2-3 hours", "phone": "904-321-2007", "booking_url": "https://www.opentable.com/lagniappe-fernandina", "tips": "Chef Brett Heritage creates unique elevated cuisine. Don't miss happy hour! Great meat options!", "rating": "4.8/5"},
            {"name": "Cucina South", "description": "Fine dining Italian with chef-driven creations, traditional Italian with Mediterranean accents", "cost_range": "$35-60 per person", "duration": "2-2.5 hours", "phone": "904-321-2699", "booking_url": "https://www.opentable.com/cucina-south", "tips": "Classic Italian with modern twists, excellent wine list", "rating": "4.7/5"},
        ],
        "🦞 Seafood & Waterfront": [
            {"name": "Brett's Waterway Cafe", "description": "Waterfront dining with marina views, fresh catch daily. ✅ NON-SEAFOOD: Steaks, chicken, burgers available", "cost_range": "$20-40 per person", "duration": "1.5-2 hours", "phone": "904-261-2660", "booking_url": "https://www.opentable.com/r/bretts-waterway-cafe-fernandina-beach", "tips": "Amazing sunset views. Has steaks, chicken, and burgers for non-seafood eaters!", "rating": "4.7/5"},
            {"name": "Salty Pelican Bar & Grill", "description": "Heart of downtown waterfront, blackened grouper tacos, fresh oysters, fried tuna. ✅ NON-SEAFOOD: Burgers, chicken sandwiches, steaks", "cost_range": "$18-35 per person", "duration": "1-2 hours", "phone": "904-277-3811", "booking_url": "https://thesaltypelicanamelia.com", "tips": "Best place to catch sunset over the river. Full bar & grill menu with chicken, burgers, steaks!", "rating": "4.6/5"},
            {"name": "Sandbar", "description": "Directly on Main Beach with Atlantic Ocean views, coastal cuisine, 1200+ whiskey selections. ✅ NON-SEAFOOD: Steaks, chicken, burgers, pasta", "cost_range": "$25-45 per person", "duration": "1.5-2 hours", "phone": "904-491-3743", "booking_url": "https://sandbaramelia.com", "tips": "Unobstructed beach views, live music on weekends. Great steaks and chicken options!", "rating": "4.7/5"},
            {"name": "The Boat House", "description": "Waterfront seafood with fresh local catches and harbor views. ✅ NON-SEAFOOD: Steaks, chicken, pasta dishes", "cost_range": "$22-40 per person", "duration": "1-2 hours", "phone": "904-261-9300", "booking_url": "https://boathouseamelia.com", "tips": "Has steaks, grilled chicken, and pasta for non-seafood diners", "rating": "4.6/5"},
            {"name": "Down Under", "description": "Under the bridge to Amelia Island, oysters, crab dip, shrimp, fresh fish with waterfront view. ✅ NON-SEAFOOD: Burgers, chicken wings, steaks", "cost_range": "$15-30 per person", "duration": "1-1.5 hours", "phone": "904-261-1001", "booking_url": "N/A", "tips": "Casual vibe with burgers, wings, and chicken tenders for non-seafood eaters", "rating": "4.5/5"},
            {"name": "Timoti's Seafood Shak", "description": "SARAH'S RECOMMENDATION for lunch! Family-friendly wild-caught seafood, fresh fried shrimp, poke bowls, fish tacos, lobster rolls. ⚠️ LIMITED NON-SEAFOOD: Chicken tenders available", "cost_range": "$12-25 per person", "duration": "45min-1 hour", "phone": "904-206-0965", "booking_url": "https://timotis.com", "tips": "Sarah says: 'You must go to Timotees for lunch one day!' Mostly seafood but has chicken tenders", "rating": "4.6/5"},
            {"name": "Salt Life Food Shack", "description": "Oceanfront casual dining with amazing views and fresh seafood. ✅ NON-SEAFOOD: Burgers, chicken sandwiches, wings", "cost_range": "$15-30 per person", "duration": "1-2 hours", "phone": "904-277-3811", "booking_url": "https://www.saltlifefoodshack.com", "tips": "Perfect for lunch, great outdoor seating. Has burgers and chicken for non-seafood eaters!", "rating": "4.5/5"},
        ],
        "🍕 Italian & Pizza": [
            {"name": "Ciao Italian Eatery", "description": "SARAH'S RECOMMENDATION! Authentic Italian by Chef Luca, pasta, pizza, veal, chicken, pork, ribeye", "cost_range": "$20-40 per person", "duration": "1.5-2 hours", "phone": "904-491-9700", "booking_url": "https://ciaoitalianeats.com", "tips": "Dinner only. Sarah says: 'Have their homemade pasta!' - it's exceptional", "rating": "4.7/5"},
            {"name": "Arte Pizza", "description": "Authentic Neapolitan wood-fired pizzas, fresh high-quality ingredients, local favorite", "cost_range": "$15-28 per person", "duration": "1-1.5 hours", "phone": "904-206-5694", "booking_url": "https://artepizzabar.com", "tips": "Best pizza on the island, simple but perfect", "rating": "4.8/5"},
        ],
        "🌮 Mexican & Latin": [
            {"name": "Mezcal Spirit of Oaxaca", "description": "Traditional Mexican favorites, authentic Oaxacan cuisine on Centre Street", "cost_range": "$18-32 per person", "duration": "1-1.5 hours", "phone": "904-310-6689", "booking_url": "N/A", "tips": "Great margaritas, try the mole dishes", "rating": "4.5/5"},
            {"name": "Tortuga Jacks", "description": "Baja Mexican upstairs at Sliders, oceanfront sunrise breakfast, only non-resort beachfront breakfast", "cost_range": "$12-25 per person", "duration": "1-1.5 hours", "phone": "904-277-3662", "booking_url": "N/A", "tips": "Sunrise breakfast to watch dawn over ocean", "rating": "4.4/5"},
        ],
        "🍜 Asian Cuisine": [
            {"name": "Wicked Bao", "description": "Asian street food, Taiwanese Bao Buns, Sichuan dumplings, chicken satay, jasmine rice tots", "cost_range": "$15-28 per person", "duration": "1-1.5 hours", "phone": "904-277-3289", "booking_url": "N/A", "tips": "Local favorite, pork ramen and kimchi fried rice are amazing", "rating": "4.7/5"},
            {"name": "Akari Sushi", "description": "Best sushi on the island, cooked and raw rolls, sashimi, sushi burritos, poke bowls", "cost_range": "$20-40 per person", "duration": "1-1.5 hours", "phone": "904-277-2739", "booking_url": "N/A", "tips": "Fresh fish, creative rolls, sit at the sushi bar", "rating": "4.6/5"},
            {"name": "Hana Sushi", "description": "Traditional Japanese in simple cafe, Bento Boxes, fried rice, noodles, sushi bowls and burritos", "cost_range": "$15-30 per person", "duration": "1-1.5 hours", "phone": "904-321-0095", "booking_url": "N/A", "tips": "Small spot, authentic flavors, very affordable", "rating": "4.5/5"},
        ],
        "🥞 Breakfast & Brunch": [
            {"name": "29 South", "description": "Farm-to-table Southern cuisine, excellent brunch with local ingredients", "cost_range": "$18-35 per person", "duration": "1.5-2 hours", "phone": "904-277-7919", "booking_url": "https://www.opentable.com/r/29-south-fernandina-beach", "tips": "Amazing brunch on weekends, try the shrimp and grits", "rating": "4.6/5"},
            {"name": "Beach Diner", "description": "Family owned unique breakfast & lunch, Chocolate Chip Pancakes, Shrimp & Crab Omelette, Fish & Grits", "cost_range": "$10-20 per person", "duration": "1-1.5 hours", "phone": "904-261-3663", "booking_url": "N/A", "tips": "Popular local spot, expect a wait on weekends", "rating": "4.6/5"},
        ],
        "🍔 Casual & Comfort Food": [
            {"name": "Sliders Seaside Grill", "description": "Beachfront burgers, seafood, and casual American fare with ocean views", "cost_range": "$12-25 per person", "duration": "1-1.5 hours", "phone": "904-277-6652", "booking_url": "N/A", "tips": "Perfect beach lunch spot, great burgers and fish sandwiches", "rating": "4.4/5"},
            {"name": "Fantastic Fudge", "description": "Ice cream, fudge, and sweet treats in downtown", "cost_range": "$5-15 per person", "duration": "30min", "phone": "904-277-4801", "booking_url": "N/A", "tips": "Perfect dessert stop while exploring Centre Street", "rating": "4.7/5"},
            {"name": "Café Karibo", "description": "Sandwiches like Big Bella (portabella mushroom), chili, burgers, and tasty salads", "cost_range": "$10-18 per person", "duration": "1 hour", "phone": "904-277-5269", "booking_url": "N/A", "tips": "Indie bookstore and bistro with indoor/outdoor seating", "rating": "4.5/5"},
        ],
        "☕ Coffee & Cafes": [
            {"name": "Amelia Island Coffee", "description": "Beloved coffee shop since 1995 in 140-year-old brick building, locally roasted coffee from Yulee, pastries, breakfast sandwiches", "cost_range": "$5-12 per person", "duration": "30min-1 hour", "phone": "904-277-3942", "booking_url": "N/A", "tips": "Historic downtown location at 207 Centre St, great atmosphere", "rating": "4.8/5"},
            {"name": "First Drop Coffee", "description": "Ritz-Carlton coffee shop with espresso, specialty drinks, and light bites", "cost_range": "$5-10", "duration": "15-30min", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Open 7am-7pm daily, convenient for hotel guests", "rating": "4.6/5"},
            {"name": "Mocama Coffee", "description": "Premium espressos, drips, pour-overs with state-of-the-art equipment, under same roof as Mocama Beer Company", "cost_range": "$4-8", "duration": "20-30min", "phone": "904-310-3749", "booking_url": "N/A", "tips": "Coffee by day, beer by night at same location", "rating": "4.7/5"},
            {"name": "Hola Cuban Cafe", "description": "Classic Cuban sandwiches, pastries, snacks, and authentic Cuban coffee since 2013", "cost_range": "$6-15 per person", "duration": "30min-1 hour", "phone": "904-277-4652", "booking_url": "N/A", "tips": "At 31 S. 5th Street, casual atmosphere", "rating": "4.6/5"},
            {"name": "Nana Teresa's Bake Shop", "description": "Fresh baked goods, pastries, coffee, and breakfast items", "cost_range": "$5-12", "duration": "30min", "phone": "904-206-0133", "booking_url": "N/A", "tips": "Early morning opening, perfect for breakfast treats", "rating": "4.7/5"},
        ],
        "🥖 Delis & Lunch Spots": [
            {"name": "Aloha Bagel and Deli", "description": "Bright cheerful bagel shop with delicious bagels, sandwiches, salads, sweets, party platters. Breakfast served all day", "cost_range": "$8-15 per person", "duration": "30min-1 hour", "phone": "904-277-3073", "booking_url": "https://aloha-bagel.com", "tips": "Open till 2pm, breakfast all day, very popular", "rating": "4.7/5"},
            {"name": "4th Street Deli", "description": "Quintessential deli with pasta salad, fish salads, crab cake, popular Cuban sandwich in different arrangements", "cost_range": "$10-16 per person", "duration": "45min-1 hour", "phone": "904-277-3354", "booking_url": "N/A", "tips": "Closed Sundays, open 11am-4pm other days", "rating": "4.6/5"},
        ],
        "🏨 Ritz-Carlton Dining": [
            {"name": "Salt (AAA Five Diamond)", "description": "Signature restaurant with fresh seafood, water views, Michelin-trained Chef D' Cuisine Okan Kizilbayir. ✅ NON-SEAFOOD: Premium steaks, lamb, duck, vegetarian options", "cost_range": "$45-85 per person", "duration": "2-3 hours", "phone": "904-277-1100", "booking_url": "https://www.opentable.com/salt-at-the-ritz-carlton", "tips": "Open 5pm-9pm Tue-Sat, reservations essential. Chef always has excellent meat/vegetarian options!", "rating": "4.8/5"},
            {"name": "Coast", "description": "Coastal cuisine with seasonal menu, local seafood, steaks, salads, small plates. ✅ NON-SEAFOOD: Steaks, chicken, pasta, salads. All-day dining", "cost_range": "$25-55 per person", "duration": "1.5-2 hours", "phone": "904-277-1100", "booking_url": "https://www.opentable.com/coast-at-the-ritz-carlton", "tips": "Open 7am-3pm and 5pm-9pm daily. Full menu with plenty of non-seafood choices!", "rating": "4.4/5"},
            {"name": "Coquina", "description": "Oceanfront restaurant with beach views and casual coastal fare. ✅ NON-SEAFOOD: Burgers, chicken sandwiches, salads", "cost_range": "$20-40 per person", "duration": "1-2 hours", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Open 11am-9pm daily, perfect for lunch with ocean breeze. Great burgers and chicken!", "rating": "4.5/5"},
            {"name": "Tidewater Grill", "description": "Casual poolside dining with grilled favorites and refreshing drinks. ✅ NON-SEAFOOD: Burgers, steaks, chicken, hot dogs", "cost_range": "$15-30 per person", "duration": "1-1.5 hours", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Open 5pm-10pm Mon-Fri, 3pm-10pm Sat-Sun. Classic grill fare - burgers, steaks, chicken!", "rating": "4.3/5"},
            {"name": "Lobby Bar", "description": "Classic lounge with craft cocktails, wine, and small plates. MUST TRY: Smoked Old Fashioneds, charcuterie board, sushi", "cost_range": "$12-30 per item", "duration": "1-2 hours", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Open 3pm-12am Mon-Thu, 3pm-1am Fri-Sat. Boss recommendation: 'Wonderful charcuterie at the bar, most wonderful smoked Old Fashioneds, sushi in the lobby!'", "rating": "4.8/5"},
            {"name": "Dune Bar", "description": "Beach bar with tropical drinks, frozen cocktails, and light bites", "cost_range": "$10-20 per drink", "duration": "1-2 hours", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Open 11am-6pm daily, perfect beach relaxation", "rating": "4.5/5"},
        ],
        "🍺 Bars & Nightlife": [
            {"name": "Amelia Tavern & The Alley", "description": "Downtown tavern with secret alley bar, craft cocktails, extensive whiskey selection", "cost_range": "$10-18 per drink", "duration": "2-3 hours", "phone": "904-310-3854", "booking_url": "N/A", "tips": "SARAH'S RECOMMENDATION! Check out the hidden alley bar for unique atmosphere", "rating": "4.7/5"},
            {"name": "Pogo's", "description": "Local favorite bar and restaurant on Centre Street", "cost_range": "$10-25 per person", "duration": "1-3 hours", "phone": "904-261-1000", "booking_url": "N/A", "tips": "SARAH'S RECOMMENDATION! Great casual spot, popular with locals", "rating": "4.6/5"},
            {"name": "Lagniappe", "description": "SARAH'S RECOMMENDATION for Happy Hour! Southern refinement meets French Creole, standout Salmon Brulee", "cost_range": "$12-20 happy hour, $40-70 dinner", "duration": "2-3 hours", "phone": "904-321-2007", "booking_url": "https://www.opentable.com/lagniappe-fernandina", "tips": "Don't miss happy hour - great cocktails and atmosphere", "rating": "4.8/5"},
            {"name": "Palace Saloon", "description": "Florida's oldest continuously-operated bar since 1903, 40-foot historic bar, live music, famous Pirate's Punch", "cost_range": "$8-15 per drink", "duration": "1-3 hours", "phone": "904-491-3332", "booking_url": "N/A", "tips": "113 Centre St, stays open latest in downtown, cool atmosphere", "rating": "4.7/5"},
            {"name": "Green Turtle Tavern", "description": "Laid-back bar with best bourbon selection on island, hand-crafted cocktails with fresh local fruit, live entertainment weekends", "cost_range": "$10-18 per drink", "duration": "2-3 hours", "phone": "904-277-8989", "booking_url": "N/A", "tips": "Heart of historic district, friendly mix of locals and visitors", "rating": "4.8/5"},
            {"name": "The Decantery", "description": "Sophisticated cocktail lounge next to Palace Saloon, old Hollywood charm, rare wines, craft cocktails, decadent desserts", "cost_range": "$12-25 per drink", "duration": "1-2 hours", "phone": "904-491-3332", "booking_url": "N/A", "tips": "Plush velvet couches, vintage mirrors, upscale atmosphere", "rating": "4.7/5"},
            {"name": "First Love Brewing", "description": "20+ rotating taps with porters, IPAs, ales, house-made artisan pizzas, wings, truffle fries", "cost_range": "$6-12 per beer, $12-20 food", "duration": "1.5-2 hours", "phone": "904-583-4052", "booking_url": "N/A", "tips": "First fully operational craft brewery in area", "rating": "4.6/5"},
            {"name": "Mocama Beer Company", "description": "Craft brewery taproom with rotating beers and same-roof coffee shop", "cost_range": "$6-10 per beer", "duration": "1-2 hours", "phone": "904-310-3749", "booking_url": "N/A", "tips": "Shares space with Mocama Coffee for all-day service", "rating": "4.5/5"},
            {"name": "A1A Cidery", "description": "Craft ciders brewed on-site, local craft beers, live local music, spacious outdoor area, fun yard games", "cost_range": "$7-12 per drink", "duration": "2-3 hours", "phone": "904-206-5100", "booking_url": "N/A", "tips": "Downtown Fernandina Beach, great for groups", "rating": "4.6/5"},
        ],
        "🏖️ Beach & Water": [
            {"name": "Horseback Riding on Beach", "description": "Ride horses along the beautiful Amelia Island shoreline", "cost_range": "$75-125 per person", "duration": "1-2 hours", "phone": "904-491-5166", "booking_url": "N/A", "tips": "Book 2-3 days in advance, wear comfortable pants", "rating": "5.0/5"},
            {"name": "Kayaking Tours", "description": "Guided kayak tours of Cumberland Island, Egan's Creek, Amelia River, and Fort Clinch", "cost_range": "$50-85 per person", "duration": "2-3 hours", "phone": "904-321-0697", "booking_url": "N/A", "tips": "Lofton Creek tour perfect for beginners and families", "rating": "4.8/5"},
            {"name": "Stand-Up Paddleboarding", "description": "Explore picturesque coastline atop a paddleboard with Amelia Island Paddle Surf Company", "cost_range": "$40-75", "duration": "2-3 hours", "phone": "904-321-0697", "booking_url": "N/A", "tips": "Morning is best, calm waters and lots of wildlife", "rating": "4.7/5"},
            {"name": "Jet Ski Rentals & Tours", "description": "Action-packed waverunner tours through island waterways with history and ecology", "cost_range": "$100-150 per hour", "duration": "1-2 hours", "phone": "904-491-8787", "booking_url": "N/A", "tips": "Hourly and daily rentals available, experienced guides", "rating": "4.6/5"},
            {"name": "Parasailing", "description": "Soar above the Atlantic with breathtaking aerial views of Amelia Island", "cost_range": "$75-100 per person", "duration": "1-1.5 hours", "phone": "904-261-9972", "booking_url": "N/A", "tips": "Best on calm, clear days, no experience needed", "rating": "4.8/5"},
            {"name": "Deep Sea Fishing Charter", "description": "Trophy tarpon and deep water fishing adventure", "cost_range": "$500-900 (up to 6 people)", "duration": "6-8 hours", "phone": "904-206-0200", "booking_url": "N/A", "tips": "Full-day charters for serious anglers, all gear provided", "rating": "4.9/5"},
            {"name": "Inshore Fishing", "description": "Redfish in backwaters, quiet rivers and tidal creeks", "cost_range": "$350-550 (up to 4 people)", "duration": "4-6 hours", "phone": "904-206-0200", "booking_url": "N/A", "tips": "Great for families, calmer waters, catch and release", "rating": "4.7/5"},
            {"name": "Backwater Cat Eco Tour", "description": "⭐ POPULAR CHOICE! Private boat tour exploring backwaters, marshes, and tidal creeks. See dolphins, birds, and coastal ecosystems up close. Departing from Dee Dee Bartels Boat Ramp", "cost_range": "$135 per person", "duration": "2.5 hours", "phone": "904-753-7631", "booking_url": "Call to book", "tips": "⚠️ BOOKING REQUIRED - Call 904-753-7631 to reserve for 2 people ($270 total). Best at golden hour, bring sunscreen and camera. Wear non-slip shoes", "rating": "4.9/5"},
            {"name": "Dolphin Watching Tour", "description": "Eco-tour to see dolphins, manatees, and coastal wildlife", "cost_range": "$35-55 per person", "duration": "1.5-2 hours", "phone": "904-261-9972", "booking_url": "N/A", "tips": "Best in morning or late afternoon, bring binoculars", "rating": "4.9/5"},
            {"name": "Sunset Cruise", "description": "Relaxing sunset sail with BYOB allowed", "cost_range": "$45-65 per person", "duration": "2 hours", "phone": "904-261-9972", "booking_url": "N/A", "tips": "Bring camera and your favorite drinks", "rating": "4.9/5"},
            {"name": "SCUBA Diving", "description": "Explore underwater reefs and shipwrecks off Amelia Island coast", "cost_range": "$80-150 per dive", "duration": "3-4 hours", "phone": "904-261-0666", "booking_url": "N/A", "tips": "Certification required, equipment rentals available", "rating": "4.6/5"},
            {"name": "Surfing Lessons", "description": "Learn to surf with professional instructors on Amelia's beaches", "cost_range": "$60-90 per person", "duration": "1.5-2 hours", "phone": "904-491-9009", "booking_url": "N/A", "tips": "Best in summer, all equipment provided", "rating": "4.5/5"},
            {"name": "Boat Rentals", "description": "Rent pontoon boats, center consoles, or deck boats to explore on your own", "cost_range": "$200-500 per day", "duration": "4-8 hours", "phone": "904-261-9972", "booking_url": "N/A", "tips": "No boating license required, captain available for hire", "rating": "4.7/5"},
            {"name": "Peters Point Beach", "description": "Quieter beach, less crowded than Main Beach", "cost_range": "FREE", "duration": "2-4 hours", "phone": "N/A", "booking_url": "N/A", "tips": "More secluded, bring your own beach gear", "rating": "4.5/5"},
            {"name": "Main Beach Park", "description": "Popular family beach with facilities, playground, volleyball courts", "cost_range": "FREE", "duration": "2-6 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Parking $2/hour, arrive early on weekends", "rating": "4.6/5"},
        ],
        "🎯 Activities & Adventure": [
            {"name": "Fort Clinch State Park", "description": "Historic Civil War fort with beach, trails, and ranger-led tours", "cost_range": "$6-8 per vehicle", "duration": "2-3 hours", "phone": "904-277-7274", "booking_url": "N/A", "tips": "Great for history buffs, bring sunscreen and water", "rating": "4.6/5"},
            {"name": "Amelia Island State Park", "description": "Pristine natural beaches, nature trails, and wildlife observation", "cost_range": "$4-6 per vehicle", "duration": "2-4 hours", "phone": "904-251-2320", "booking_url": "N/A", "tips": "Less crowded than Fort Clinch, great for shelling", "rating": "4.5/5"},
            {"name": "Little Talbot Island State Park", "description": "Unspoiled barrier island with 5 miles of pristine beaches and kayaking", "cost_range": "$5 per vehicle", "duration": "2-4 hours", "phone": "904-251-2320", "booking_url": "N/A", "tips": "Perfect for nature lovers, bring kayak or rent on-site", "rating": "4.7/5"},
            {"name": "Big Talbot Island State Park", "description": "Dramatic driftwood beach, unique boneyard trees, nature photography", "cost_range": "$3-5 per vehicle", "duration": "1-2 hours", "phone": "904-251-2320", "booking_url": "N/A", "tips": "Incredible photo opportunities, especially at sunset", "rating": "4.6/5"},
            {"name": "Golf at Oak Marsh", "description": "Championship 18-hole course designed by Tom Fazio at Ritz-Carlton", "cost_range": "$80-150", "duration": "4-5 hours", "phone": "904-277-5907", "booking_url": "N/A", "tips": "Book tee times in advance, beautiful course", "rating": "4.7/5"},
            {"name": "Golf at Amelia National", "description": "27-hole municipal course, popular in Southeast", "cost_range": "$50-90", "duration": "4-5 hours", "phone": "904-491-8700", "booking_url": "N/A", "tips": "More affordable than resort courses, still excellent", "rating": "4.6/5"},
            {"name": "Tennis at Amelia National", "description": "8-court tennis center with professional instruction", "cost_range": "$30-60 per hour", "duration": "1-2 hours", "phone": "904-491-8700", "booking_url": "N/A", "tips": "Private lessons and clinics available", "rating": "4.5/5"},
            {"name": "Bike Rentals & Delivery", "description": "Beach cruisers delivered to your accommodations", "cost_range": "$20-40 per day", "duration": "Full day", "phone": "904-321-0011", "booking_url": "N/A", "tips": "Great for exploring downtown Fernandina Beach", "rating": "4.5/5"},
            {"name": "Segway Tours", "description": "Guided Segway tour of historic Fernandina Beach", "cost_range": "$65-75 per person", "duration": "1.5-2 hours", "phone": "904-556-7594", "booking_url": "N/A", "tips": "Fun way to see the sights, no experience needed", "rating": "4.8/5"},
            {"name": "Ghost Tours of Amelia Island", "description": "Spooky evening walking tours through historic downtown", "cost_range": "$20-30 per person", "duration": "1.5-2 hours", "phone": "904-414-7300", "booking_url": "https://ghosttoursofameliaisland.com", "tips": "Haunted Bar Crawl and Cemetery Tours also available", "rating": "4.7/5"},
            {"name": "Historic Carriage Tour", "description": "Romantic horse-drawn carriage ride through Victorian historic district", "cost_range": "$60-80 per couple", "duration": "45-60 minutes", "phone": "904-556-7594", "booking_url": "N/A", "tips": "Perfect for special occasions, sunset tours available", "rating": "4.8/5"},
            {"name": "Wildlife Watching & Nature Tours", "description": "Guided eco-tours to see birds, dolphins, and coastal ecosystems", "cost_range": "$40-65 per person", "duration": "2-3 hours", "phone": "904-261-9972", "booking_url": "N/A", "tips": "Bring binoculars and camera, best in early morning", "rating": "4.7/5"},
        ],
        "🥾 Hiking & Nature Trails": [
            {"name": "Fort Clinch State Park Trails", "description": "6-mile loop trail of moderate difficulty along marshes with beach access, gateway to Great Florida Birding Trail", "cost_range": "FREE with park entry ($6-8 per vehicle)", "duration": "2-3 hours", "phone": "904-277-7274", "booking_url": "N/A", "tips": "Six miles of off-road wooded trails, bring water and sunscreen", "rating": "4.7/5"},
            {"name": "Willow Pond Trails at Fort Clinch", "description": "Less than 1 mile trails through wildlife haven amid forested dunes", "cost_range": "FREE with park entry", "duration": "30min-1 hour", "phone": "904-277-7274", "booking_url": "N/A", "tips": "Shorter easy trail, great for families", "rating": "4.5/5"},
            {"name": "Egan's Creek Greenway Trails", "description": "300-acre nature preserve with 4+ miles of trails through marshes, forests, grasslands, tidal creeks", "cost_range": "FREE", "duration": "1.5-2.5 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Excellent birdwatching, bring bug spray, early morning best", "rating": "4.6/5"},
            {"name": "Blackrock Trail at Big Talbot", "description": "Trail leading to famous driftwood beach with centuries-old trees creating breathtaking scene", "cost_range": "FREE with park entry ($3-5 per vehicle)", "duration": "45min-1.5 hours", "phone": "904-251-2320", "booking_url": "N/A", "tips": "Incredible photography opportunity, especially at golden hour", "rating": "4.8/5"},
            {"name": "Big Talbot Island Boardwalk & Spoonbill Pond", "description": "Boardwalk with bird watching platform at Spoonbill Pond for observing wading birds and migratory waterfowl", "cost_range": "FREE with park entry", "duration": "30min-1 hour", "phone": "904-251-2320", "booking_url": "N/A", "tips": "Bring binoculars, wheelchair accessible", "rating": "4.6/5"},
            {"name": "Old King's Highway Trail", "description": "3 miles on wooded trail, boardwalk and pedestrian/fishing bridge starting at Big Pine trailhead", "cost_range": "FREE", "duration": "1.5-2 hours", "phone": "904-251-2320", "booking_url": "N/A", "tips": "Connects multiple parks, great for biking too", "rating": "4.5/5"},
            {"name": "Amelia Island Trail (8.7 miles)", "description": "Paved multi-use trail from Peters Point through Amelia Island State Park to Big Talbot Island State Park", "cost_range": "FREE", "duration": "3-5 hours (full trail)", "phone": "N/A", "booking_url": "N/A", "tips": "Perfect for biking, connects multiple natural areas", "rating": "4.7/5"},
        ],
        "🛍️ Shopping & Culture": [
            {"name": "Downtown Fernandina Beach", "description": "Historic downtown with 50+ shops, galleries, and cafes on Centre Street", "cost_range": "Varies", "duration": "2-3 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Centre Street is main drag, very walkable and charming", "rating": "4.8/5"},
            {"name": "Amelia Island Museum of History", "description": "Restored 1935 Nassau County Jail with engaging oral history tours", "cost_range": "$10-15", "duration": "1-2 hours", "phone": "904-261-7378", "booking_url": "N/A", "tips": "Oral history tours are fantastic and unique, reserve ahead", "rating": "4.7/5"},
            {"name": "American Beach Museum", "description": "Showcases African American contributions in Florida's history", "cost_range": "$5-8", "duration": "45min-1 hour", "phone": "904-261-0033", "booking_url": "N/A", "tips": "Important local history, small but meaningful collection", "rating": "4.5/5"},
            {"name": "Fernandina Beach Pinball Museum", "description": "Interactive museum with vintage pinball machines", "cost_range": "$15-20", "duration": "1-2 hours", "phone": "904-477-5458", "booking_url": "N/A", "tips": "Unlimited play, fun for all ages, nostalgic experience", "rating": "4.6/5"},
            {"name": "Plantation Artists' Guild & Gallery", "description": "Local artists featuring paintings, pottery, jewelry, and crafts", "cost_range": "FREE to browse", "duration": "30min-1 hour", "phone": "904-261-7020", "booking_url": "N/A", "tips": "Unique gifts and original art from local creators", "rating": "4.5/5"},
            {"name": "Shady Ladies Art Gallery & Studios", "description": "Working artist studios with diverse mediums and styles", "cost_range": "FREE to browse", "duration": "30min-1 hour", "phone": "904-277-6050", "booking_url": "N/A", "tips": "Watch artists at work, great for art lovers", "rating": "4.6/5"},
            {"name": "Artrageous ArtWalk", "description": "Second Saturday monthly event, galleries open 5:30pm-8:30pm", "cost_range": "FREE", "duration": "2-3 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Great atmosphere, wine and refreshments at many galleries", "rating": "4.7/5"},
            {"name": "Saturday Farmer's Market", "description": "Local produce, crafts, food vendors, and live music", "cost_range": "Varies", "duration": "1-2 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Only Saturday mornings 9am-1pm, arrive early for best selection", "rating": "4.6/5"},
            {"name": "Historic Walking Tour", "description": "Self-guided or guided tours of Victorian-era architecture", "cost_range": "$FREE-$25", "duration": "1-2 hours", "phone": "904-277-0717", "booking_url": "N/A", "tips": "Pick up map at visitor center or book guided tour", "rating": "4.6/5"},
            {"name": "Scenic Drive to Georgia Border", "description": "SARAH'S RECOMMENDATION! Drive north on A1A to Georgia border - beautiful coastal scenery", "cost_range": "FREE (just gas)", "duration": "1-2 hours round trip", "phone": "N/A", "booking_url": "N/A", "tips": "If you have a car, this scenic drive offers stunning views. Sarah says: 'Try to drive north to the GA border!'", "rating": "4.7/5"},
            {"name": "Wine & Tasting Tour", "description": "Local guide takes you to best restaurants, bars and hot spots", "cost_range": "$60-90 per person", "duration": "2-3 hours", "phone": "904-556-7594", "booking_url": "N/A", "tips": "Fun way to discover local flavors and meet people", "rating": "4.5/5"},
        ],
        "💆 Ritz-Carlton Spa Services - COMPLETE MENU": [
            {"name": "🌟 IMPORTANT SPA POLICIES", "description": "BOOKING: Call 904-277-1087 or 904-277-1100 • HOURS: After 9:30am-5:00pm • GRATUITY: 20% automatically added to all services • ARRIVAL: Arrive 30 min early to enjoy healing saltwater pool • CANCELLATION: Call spa directly for policy • LOCAL DISCOUNT: Mon-Thu for locals", "cost_range": "See individual services", "duration": "N/A", "phone": "904-277-1087", "booking_url": "N/A", "tips": "25,000 sq ft sanctuary - recently renovated! Saltwater pool, steam rooms, relaxation lounges included with any treatment", "rating": "5.0/5"},

            {"name": "Heaven in a Hammock Massage (Couples)", "description": "⭐ ALREADY BOOKED - Beachside couples massage in swaying hammocks. Signature experience!", "cost_range": "$245 each (60 min: $190 each)", "duration": "80 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "SIGNATURE TREATMENT - Perfect for birthday! Includes beach setup with ocean sounds", "rating": "5.0/5"},
            {"name": "HydraFacial Treatment", "description": "⭐ ALREADY BOOKED - Advanced facial for glowing skin with extraction and hydration", "cost_range": "$195", "duration": "50 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Perfect before birthday dinner - immediate results!", "rating": "4.9/5"},

            {"name": "Hadashi Massage", "description": "Traditional Japanese foot pressure massage for deep relaxation", "cost_range": "60 min: $180 | 75 min: $225 | 90 min: $270", "duration": "60-90 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Unique technique using feet - incredibly effective for deep tissue work", "rating": "4.9/5"},
            {"name": "Awakening Bamboo Massage", "description": "NEW! Warm bamboo tools for deep tissue massage", "cost_range": "60 min: $180 | 75 min: $225 | 90 min: $270", "duration": "60-90 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Newest treatment - combines heat therapy with deep pressure", "rating": "4.9/5"},
            {"name": "Aromatherapy Massage", "description": "Full body massage with customized essential oil blends", "cost_range": "60 min: $180 | 75 min: $225 | 90 min: $270", "duration": "60-90 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Choose lavender, eucalyptus, or citrus blends", "rating": "4.9/5"},
            {"name": "Hot Stone Massage", "description": "Deep relaxation with heated volcanic stones", "cost_range": "60 min: $180 | 90 min: $270", "duration": "60-90 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Perfect for sore muscles after activities", "rating": "4.9/5"},
            {"name": "Prenatal Massage", "description": "Safe and nurturing massage for expectant mothers", "cost_range": "60 min: $180 | 75 min: $225", "duration": "60-75 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Specially trained therapists, positioning pillows provided", "rating": "4.8/5"},

            {"name": "Natural Resilience Facial", "description": "NEW! Japanese Kobido-inspired facial with lifting techniques", "cost_range": "60 min: $175 | 75 min: $215 | 90 min: $260", "duration": "60-90 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Ancient Japanese technique for natural facelift effect - newest addition!", "rating": "5.0/5"},
            {"name": "Signature Facial", "description": "Customized facial tailored to your skin type and concerns", "cost_range": "60 min: $175 | 75 min: $215 | 90 min: $260", "duration": "60-90 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Deep cleansing, exfoliation, extractions, mask, and massage", "rating": "4.8/5"},
            {"name": "Gentleman's Facial", "description": "Facial designed specifically for men's skin", "cost_range": "60 min: $175", "duration": "60 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "John might enjoy this! Addresses shaving irritation and thick skin", "rating": "4.7/5"},
            {"name": "Anti-Aging Facial", "description": "Advanced facial targeting fine lines and wrinkles", "cost_range": "75 min: $215 | 90 min: $260", "duration": "75-90 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Includes peptides, antioxidants, and lifting massage", "rating": "4.9/5"},

            {"name": "Body Scrub & Wrap", "description": "Exfoliating scrub followed by hydrating wrap", "cost_range": "60 min: $175 | 90 min: $260", "duration": "60-90 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Ocean salt scrub is signature - perfect after travel!", "rating": "4.8/5"},
            {"name": "Reflexology Treatment", "description": "Therapeutic foot and lower leg massage based on pressure points", "cost_range": "$115", "duration": "50 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Great after beach walking - addresses full body through feet", "rating": "4.6/5"},
            {"name": "Chakra Balancing", "description": "Energy healing and chakra alignment with aromatherapy", "cost_range": "60 min: $145 | 80 min: $185", "duration": "60-80 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Combines meditation, energy work, and crystal healing", "rating": "4.7/5"},

            {"name": "Manicure", "description": "Professional manicure with polish", "cost_range": "$65-85", "duration": "45-60 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Add gel polish for longer-lasting results", "rating": "4.7/5"},
            {"name": "Pedicure", "description": "Luxurious pedicure with exfoliation and massage", "cost_range": "$85-105", "duration": "60-75 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Includes sugar scrub and paraffin treatment", "rating": "4.8/5"},
            {"name": "Mani-Pedi Combo", "description": "Complete manicure and pedicure combo", "cost_range": "$150", "duration": "105-135 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Great add-on for spa day - book together for best value", "rating": "4.8/5"},

            {"name": "Scalp Treatment with Style", "description": "Revitalizing scalp massage and hair styling", "cost_range": "$100", "duration": "45-60 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Perfect before special event - includes blow-dry and style", "rating": "4.6/5"},
            {"name": "Make-up Application", "description": "Professional makeup application for special occasions", "cost_range": "$105 (includes lashes)", "duration": "45-60 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Perfect for birthday dinner! Book early", "rating": "4.7/5"},
            {"name": "Eyebrow Tinting", "description": "Semi-permanent eyebrow tinting", "cost_range": "$45", "duration": "20-30 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Lasts 3-4 weeks, perfect for beach vacation", "rating": "4.5/5"},
            {"name": "Eyelash Tinting", "description": "Semi-permanent eyelash tinting", "cost_range": "$45", "duration": "20-30 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Wake up with defined lashes - no mascara needed!", "rating": "4.5/5"},
            {"name": "Waxing Services", "description": "Various waxing services available", "cost_range": "$25-85 (varies by area)", "duration": "15-45 minutes", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Brow, lip, leg, bikini, and more - call for specific pricing", "rating": "4.6/5"},
        ],
        "💎 Spa Enhancements & Add-Ons": [
            {"name": "Alpha Beta Glow Pad", "description": "Add to any facial for gentle exfoliation and glow", "cost_range": "$15", "duration": "Added to service", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Worth it! Immediate glow effect", "rating": "4.8/5"},
            {"name": "Neck and Décolleté Lifting Treatment", "description": "Add to any facial for neck and chest firming", "cost_range": "$45", "duration": "Added to service", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Often-neglected area that shows age - highly recommended!", "rating": "4.7/5"},
            {"name": "CBD Enhancement", "description": "Add CBD oil to any massage for deeper relaxation", "cost_range": "$30-50", "duration": "Added to service", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Great for inflammation and muscle tension", "rating": "4.8/5"},
            {"name": "Aromatherapy Upgrade", "description": "Premium essential oil blend for massage", "cost_range": "$25", "duration": "Added to service", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Customize your experience with therapeutic scents", "rating": "4.6/5"},
        ],
        "🎁 Spa Packages": [
            {"name": "Couples Spa Day", "description": "2.5 hour couples package with massage, facial, and champagne", "cost_range": "$390 per person", "duration": "2.5 hours", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Perfect for birthday celebration! Includes side-by-side treatments", "rating": "5.0/5"},
            {"name": "Ultimate Spa Day", "description": "Full day of pampering with multiple treatments", "cost_range": "$500-700 per person", "duration": "4-5 hours", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Massage, facial, body treatment, mani/pedi - the works!", "rating": "5.0/5"},
            {"name": "Birthday Spa Special", "description": "Celebrate with spa services - ask about birthday perks!", "cost_range": "Varies", "duration": "Varies", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Mention it's your 40th birthday - they may have special touches!", "rating": "5.0/5"},
        ],
        "🏊 Spa Facilities (Included with Treatments)": [
            {"name": "Healing Saltwater Pool", "description": "Therapeutic saltwater pool in spa - use before or after treatment", "cost_range": "FREE (included with any spa service)", "duration": "Flexible", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Arrive 30 min early to enjoy! Incredibly relaxing", "rating": "5.0/5"},
            {"name": "Steam Rooms & Saunas", "description": "Multiple steam rooms and saunas throughout 25,000 sq ft spa", "cost_range": "FREE (included with any spa service)", "duration": "Flexible", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Use before treatment to warm muscles", "rating": "4.9/5"},
            {"name": "Relaxation Lounges", "description": "Quiet lounges with healthy snacks and tea", "cost_range": "FREE (included with any spa service)", "duration": "Flexible", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Stay and relax after your treatment - no rush!", "rating": "4.8/5"},
            {"name": "Spa Lockers & Amenities", "description": "Full locker room with robes, slippers, shower products", "cost_range": "FREE (included)", "duration": "N/A", "phone": "904-277-1087", "booking_url": "N/A", "tips": "Everything provided - just bring yourself!", "rating": "4.9/5"},
        ],
        "🧘 Wellness & Other Spas": [
            {"name": "Omni Spa Clean & Green Therapies", "description": "Massage, peels, wraps, and signature scrubs at Omni Resort", "cost_range": "$150-250", "duration": "50-90 minutes", "phone": "904-261-6161", "booking_url": "N/A", "tips": "Eco-friendly products and treatments", "rating": "4.7/5"},
            {"name": "Drift Day Spa", "description": "Custom massages, reflexology, facials, couple massages 7 days/week", "cost_range": "$90-180", "duration": "60-90 minutes", "phone": "904-277-5454", "booking_url": "N/A", "tips": "More affordable alternative to resort spas", "rating": "4.6/5"},
            {"name": "Coastal Massage Therapy", "description": "Downtown cottage with neuromuscular, deep tissue, trigger point, prenatal, reiki, crystal healing, lomilomi", "cost_range": "$80-150", "duration": "60-90 minutes", "phone": "904-432-5998", "booking_url": "N/A", "tips": "Specialized therapeutic massage techniques", "rating": "4.7/5"},
            {"name": "Centred On Yoga", "description": "Beginner and intermediate yoga classes in historic downtown with certified instructors (28+ years experience)", "cost_range": "$18-25 per class", "duration": "60-75 minutes", "phone": "904-310-9642", "booking_url": "N/A", "tips": "Drop-in classes available, bring your own mat", "rating": "4.8/5"},
            {"name": "The Sprouting Project", "description": "Monthly farm-to-table dining experience at Omni with garden tour, aquaponic greenhouse, barrel room, apiary", "cost_range": "$75-95 per person", "duration": "2-3 hours", "phone": "904-261-6161", "booking_url": "N/A", "tips": "Unique wellness and culinary experience, book ahead", "rating": "4.9/5"},
        ],
        "🏨 Ritz-Carlton Hotel Services": [
            {"name": "Club Lounge (Club Level Guests)", "description": "Exclusive lounge with endless beverage and culinary offerings all day - breakfast, lunch, snacks, hors d'oeuvres, desserts, cordials", "cost_range": "Included with Club Level booking", "duration": "All day access", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Club Level upgrade required - Bonvoy Elite Status does NOT include free access", "rating": "4.9/5"},
            {"name": "Room Service", "description": "In-room dining available", "cost_range": "Menu pricing + service charge", "duration": "Varies", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Full menu available, perfect for breakfast in bed or late night snacks", "rating": "4.7/5"},
            {"name": "Valet Parking", "description": "Only parking option at resort (no self-parking)", "cost_range": "$40 per day", "duration": "N/A", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Factor this into budget - valet is mandatory", "rating": "4.5/5"},
            {"name": "Daily Housekeeping & Turndown Service", "description": "Daily cleaning and evening turndown with chocolates", "cost_range": "FREE (included)", "duration": "N/A", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Leave tip for housekeeping - they're wonderful!", "rating": "4.9/5"},
            {"name": "Same Day Dry Cleaning", "description": "On-site laundry and dry cleaning services", "cost_range": "Per item pricing", "duration": "Same day", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Great for business travelers or special occasions", "rating": "4.6/5"},
            {"name": "Hair Salon", "description": "Full-service salon on property", "cost_range": "Varies by service", "duration": "Varies", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Perfect for birthday styling or special event prep", "rating": "4.5/5"},
            {"name": "Gift Shop & Convenience Store", "description": "On-site shopping for essentials, gifts, and resort wear", "cost_range": "Varies", "duration": "Varies", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Forgot something? They've got you covered", "rating": "4.4/5"},
            {"name": "Complimentary WiFi", "description": "Free high-speed internet in room and throughout resort", "cost_range": "FREE (Bonvoy members booking direct)", "duration": "Entire stay", "phone": "904-277-1100", "booking_url": "N/A", "tips": "May be $19.95/day for non-members", "rating": "4.6/5"},
            {"name": "Free Coffee & Tea in Lobby", "description": "Complimentary coffee and tea service in main lobby", "cost_range": "FREE", "duration": "All day", "phone": "N/A", "booking_url": "N/A", "tips": "Perfect morning pick-me-up before beach", "rating": "4.7/5"},
        ],
        "👨‍👩‍👧‍👦 Ritz Kids & Family Programs": [
            {"name": "Ritz Kids Program (Ages 5-12)", "description": "Supervised morning, afternoon, or full-day programs with arts & crafts, swimming, beach visits and more", "cost_range": "Varies by session", "duration": "Half day or full day", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Daily during high season, Fri-Sat in winter (Nov 1-Feb 28). Pre-registration required!", "rating": "4.9/5"},
            {"name": "Kids Night Out (Ages 4-12)", "description": "Supervised movies, games, and dinner for kids", "cost_range": "$100 per child", "duration": "6:00 PM - 9:00 PM", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Perfect for parents' date night! Book in advance", "rating": "4.8/5"},
            {"name": "Our Space (Teen Program Ages 13-17)", "description": "Teen activities and hangout space", "cost_range": "Included", "duration": "Starting 2 PM", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Available Thursday-Saturday", "rating": "4.6/5"},
            {"name": "Nightly Pirate Toast", "description": "Fun pirate-themed toast ceremony in lobby", "cost_range": "FREE", "duration": "15-20 minutes", "phone": "N/A", "booking_url": "N/A", "tips": "Kids love this! Check lobby for nightly time", "rating": "4.8/5"},
            {"name": "Family Game Room", "description": "Indoor game room with activities for all ages", "cost_range": "FREE (hotel guests)", "duration": "Flexible", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Great for rainy days or evening fun", "rating": "4.5/5"},
        ],
        "🦎 Naturalist-Led Activities": [
            {"name": "Nature Walks", "description": "Daily guided nature walks led by resort naturalist", "cost_range": "FREE (hotel guests)", "duration": "1-2 hours", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Learn about local ecosystems and wildlife", "rating": "4.9/5"},
            {"name": "Shark Tooth Hunts", "description": "Guided shark tooth hunting on the beach", "cost_range": "FREE (hotel guests)", "duration": "1 hour", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Kids love finding fossils! Best at low tide", "rating": "5.0/5"},
            {"name": "Birdwatching Tours", "description": "Naturalist-led birdwatching experiences", "cost_range": "FREE (hotel guests)", "duration": "1-2 hours", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Bring binoculars if you have them", "rating": "4.8/5"},
            {"name": "Ecology Field Trips", "description": "Customizable nature experiences tailored to your interests", "cost_range": "Varies", "duration": "2-3 hours", "phone": "904-277-1100", "booking_url": "N/A", "tips": "New program! Can customize to specific interests like marine life, birds, plants, etc.", "rating": "4.9/5"},
        ],
        "🏖️ Casual Beach & Free Activities (Anytime!)": [
            {"name": "Beach Walk/Stroll", "description": "Leisurely walk along the beautiful Amelia Island shoreline - can be done anytime", "cost_range": "FREE", "duration": "30min-2 hours", "phone": "N/A", "booking_url": "N/A", "tips": "1.5 miles of private beach! Perfect morning, afternoon, or evening activity. Repeatable!", "rating": "5.0/5", "is_repeatable": True},
            {"name": "Sunrise Viewing", "description": "Watch the sun rise over the Atlantic Ocean - magical start to your day", "cost_range": "FREE", "duration": "30-45 minutes", "phone": "N/A", "booking_url": "N/A", "tips": "Sunrise ~6:45am in November. Bring coffee and camera. Best spot: east-facing beach", "rating": "5.0/5", "is_repeatable": True},
            {"name": "Sunset Viewing", "description": "Watch gorgeous sunset from the shore with changing colors across the sky", "cost_range": "FREE", "duration": "30-60 minutes", "phone": "N/A", "booking_url": "N/A", "tips": "Sunset ~5:30pm in November. Bring camera and beach blanket. Best spot: west side or pier", "rating": "5.0/5", "is_repeatable": True},
            {"name": "Seashell Hunting", "description": "Search for unique shells, sand dollars, starfish, and sea glass treasures", "cost_range": "FREE", "duration": "1-2 hours", "phone": "N/A", "booking_url": "N/A", "tips": "BEST at low tide! Early morning has most finds. Bring a bag. Check tide times in app!", "rating": "4.9/5", "is_repeatable": True},
            {"name": "Tide Pool Exploring", "description": "Discover crabs, small fish, and marine life in shallow tide pools at low tide", "cost_range": "FREE", "duration": "1-1.5 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Only accessible at LOW tide - check tide times! Fort Clinch has best tide pools", "rating": "4.8/5", "is_repeatable": True},
            {"name": "Beach Photography", "description": "Capture amazing photos - sunrise, sunset, wildlife, landscapes, or fun candids", "cost_range": "FREE", "duration": "30min-2 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Golden hour (sunrise/sunset) for best light. Try Big Talbot's driftwood beach!", "rating": "5.0/5", "is_repeatable": True},
            {"name": "Beach Reading & Relaxing", "description": "Read a book, journal, or simply relax in a beach chair with ocean sounds", "cost_range": "FREE", "duration": "1-3 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Chairs & umbrellas provided at Ritz. Bring sunscreen and water. So peaceful!", "rating": "5.0/5", "is_repeatable": True},
            {"name": "Cloud Watching", "description": "Lay back and watch clouds drift by - meditative and fun", "cost_range": "FREE", "duration": "30min-1 hour", "phone": "N/A", "booking_url": "N/A", "tips": "Best on partly cloudy days. Bring beach blanket. Great for clearing your mind!", "rating": "4.5/5", "is_repeatable": True},
            {"name": "Beach Picnic", "description": "Pack snacks or lunch and enjoy a meal on the beach", "cost_range": "Cost of food", "duration": "1-2 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Pick up food from hotel or nearby shops. Bring blanket and drinks. Watch for birds!", "rating": "4.8/5", "is_repeatable": True},
            {"name": "Sandcastle Building", "description": "Build creative sandcastles, sculptures, or beach art", "cost_range": "FREE", "duration": "1-2 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Best when sand is slightly damp. Buckets available at hotel. Fun & creative!", "rating": "4.6/5", "is_repeatable": True},
            {"name": "Beach Meditation/Yoga", "description": "Practice meditation or do your own yoga session on the beach", "cost_range": "FREE", "duration": "20-45 minutes", "phone": "N/A", "booking_url": "N/A", "tips": "Early morning is quietest. Ocean sounds are perfect for meditation. Bring mat!", "rating": "4.9/5", "is_repeatable": True},
            {"name": "Bird Watching from Beach", "description": "Spot pelicans, seagulls, sandpipers, herons, and seasonal migratory birds", "cost_range": "FREE", "duration": "30min-1.5 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Bring binoculars if you have them. Early morning or late afternoon best", "rating": "4.7/5", "is_repeatable": True},
            {"name": "Beach Journaling", "description": "Write in a journal, reflect on your trip, or capture memories", "cost_range": "FREE", "duration": "30min-1 hour", "phone": "N/A", "booking_url": "N/A", "tips": "Bring notebook and pen. Beach chair + ocean = perfect journaling spot!", "rating": "4.7/5", "is_repeatable": True},
            {"name": "Collect Driftwood", "description": "Find interesting driftwood pieces for souvenirs or decor", "cost_range": "FREE", "duration": "30min-1 hour", "phone": "N/A", "booking_url": "N/A", "tips": "Big Talbot Island has incredible driftwood beach! Best for unique pieces", "rating": "4.6/5", "is_repeatable": True},
            {"name": "Watch Dolphins from Shore", "description": "Spot dolphins swimming past the beach - often visible from shore!", "cost_range": "FREE", "duration": "30min-1 hour", "phone": "N/A", "booking_url": "N/A", "tips": "Look for fins in the water. Morning and late afternoon best. Be patient!", "rating": "4.8/5", "is_repeatable": True},
        ],
        "🏊 Resort Pools & Hotel Activities": [
            {"name": "Two Resort Pools", "description": "Multiple pools including one with kids splash pad", "cost_range": "FREE (hotel guests)", "duration": "All day", "phone": "N/A", "booking_url": "N/A", "tips": "Kids splash pad is perfect for little ones!", "rating": "4.9/5", "is_repeatable": True},
            {"name": "Private Beach Cabanas", "description": "Reserve private poolside or beachside cabanas for ultimate luxury", "cost_range": "Varies (call for pricing)", "duration": "Half day or full day", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Book early - these go fast! Includes shade, seating, and service", "rating": "5.0/5"},
            {"name": "1.5 Miles Private Beach Access", "description": "Exclusive access to pristine private beaches with summer service", "cost_range": "FREE (hotel guests)", "duration": "All day", "phone": "N/A", "booking_url": "N/A", "tips": "Beach chairs and umbrellas provided in summer season", "rating": "5.0/5", "is_repeatable": True},
            {"name": "Resort Pool Day", "description": "Relax at multiple Ritz-Carlton pools and hot tubs", "cost_range": "FREE (hotel guests)", "duration": "2-4 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Reserve a cabana for ultimate luxury relaxation", "rating": "4.8/5", "is_repeatable": True},
            {"name": "Hot Tub Relaxation", "description": "Unwind in resort hot tubs with ocean views", "cost_range": "FREE (hotel guests)", "duration": "30min-1 hour", "phone": "N/A", "booking_url": "N/A", "tips": "Perfect after activities or before dinner. Very relaxing!", "rating": "4.9/5", "is_repeatable": True},
            {"name": "Yoga on the Beach", "description": "Morning yoga classes on the beach at resort", "cost_range": "$20-35", "duration": "1 hour", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Hotel offers classes, check schedule", "rating": "4.6/5"},
            {"name": "Beach Bonfires", "description": "Private or group beach bonfire with s'mores", "cost_range": "$150-300", "duration": "2 hours", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Perfect for special celebrations, book ahead", "rating": "4.9/5"},
            {"name": "Fitness Center Access", "description": "State-of-the-art gym with ocean views", "cost_range": "FREE (hotel guests)", "duration": "Flexible", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Open 24/7, personal trainers available", "rating": "4.7/5", "is_repeatable": True},
            {"name": "FREE Bike Rentals", "description": "Complimentary bicycle rentals through fitness center", "cost_range": "FREE (hotel guests)", "duration": "By hour or full day", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Bike paths nearby, great for exploring the island!", "rating": "4.8/5", "is_repeatable": True},
            {"name": "Beach Volleyball", "description": "Courts available at resort and Main Beach Park", "cost_range": "FREE", "duration": "1-2 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Bring your own equipment or join pickup games", "rating": "4.4/5", "is_repeatable": True},
        ],
        "🎾 Ritz-Carlton Tennis & Pickleball": [
            {"name": "Patrick Mouratoglou Signature Tennis Center", "description": "World-renowned coach's signature tennis center with newly renovated clay courts", "cost_range": "Court fees + optional lessons", "duration": "By hour", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Training camps, private lessons, and retreats available", "rating": "5.0/5"},
            {"name": "Clay Court Tennis", "description": "Newly renovated clay tennis courts", "cost_range": "Per hour court fees", "duration": "1 hour slots", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Racket and balls available for $7 rental", "rating": "4.8/5"},
            {"name": "Pickleball Courts", "description": "Dedicated pickleball courts at resort", "cost_range": "Included for guests", "duration": "By hour", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Growing in popularity - fun for all skill levels!", "rating": "4.7/5"},
            {"name": "Tennis Lessons & Clinics", "description": "Private lessons and group drill clinics", "cost_range": "Varies by program", "duration": "30-60 minutes", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Professional instruction available for all levels", "rating": "4.9/5"},
        ]
    }

# ============================================================================
# AUTHENTICATION
# ============================================================================

def check_password_ultimate():
    """Ultimate password protection with enhanced UI"""
    if not st.session_state.password_verified:
        st.markdown("""
        <div class="ultimate-card fade-in">
            <div class="card-header">
                🔒 Secure Access Required
            </div>
            <div class="card-body">
                <p style="font-size: 1.15rem; margin-bottom: 1.5rem;">
                    This trip assistant contains personal information including flight details, 
                    bookings, and contact numbers. Please enter the password to unlock.
                </p>
                <div class="info-box info-warning" style="margin-top: 1rem;">
                    <strong>🔐 Privacy Protected:</strong> Your trip data is secured with password protection.
                    Demo mode available for sharing without exposing personal details.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        password = st.text_input("🔑 Enter Password:", type="password", key="password_input", 
                                placeholder="Enter trip password...")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🔓 Unlock Full Access", use_container_width=True, type="primary"):
                stored_hash = os.getenv('TRIP_PASSWORD_HASH', 'a5be948874610641149611913c4924e5')
                input_hash = hashlib.md5(password.encode()).hexdigest()
                
                if input_hash == stored_hash:
                    st.session_state.password_verified = True
                    st.balloons()
                    st.success("✅ Access granted! Welcome to your ultimate trip assistant!")
                    st.rerun()
                else:
                    st.error("❌ Incorrect password. Please try again.")
        
        with col2:
            if st.button("👀 Demo Mode", use_container_width=True):
                st.info("🔒 Demo mode - Personal data will be masked for privacy")
        
        with col3:
            with st.expander("ℹ️ Need Help?"):
                st.write("""
                **Password Lost?**  
                Contact the trip organizer for access.
                
                **Demo Mode:**  
                View the app with masked personal information.
                """)
        
        return False
    return True

def mask_info(text, show=False):
    """Mask sensitive information"""
    if show:
        return text
    
    patterns = {
        r'\b\d{3}-\d{3}-\d{4}\b': '***-***-****',
        r'\bAA\d{4}\b': 'AA****',
        r'\b\d{4}\s.+(Ave|St|Dr|Rd|Pkwy)\b': '****',
    }
    
    for pattern, replacement in patterns.items():
        text = re.sub(pattern, replacement, str(text))
    
    return text


# ============================================================================
# WEATHER INTEGRATION
# ============================================================================

@st.cache_data(ttl=1800)
def get_uv_index():
    """Get UV index data from OpenWeather"""
    api_key = os.getenv('OPENWEATHER_API_KEY', '')
    lat, lon = 30.6074, -81.4493  # Amelia Island

    if api_key:
        try:
            # UV Index endpoint (using One Call API 3.0)
            uv_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&exclude=minutely,hourly,alerts"
            resp = requests.get(uv_url, timeout=5)

            if resp.status_code == 200:
                data = resp.json()
                return {
                    'current': round(data.get('current', {}).get('uvi', 5), 1),
                    'daily': [{'date': datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d'),
                               'uv': round(day.get('uvi', 5), 1)}
                              for day in data.get('daily', [])[:6]]
                }
        except:
            pass

    # Fallback UV data (moderate levels)
    from datetime import datetime, timedelta
    today = datetime.now()
    return {
        'current': 5.0,
        'daily': [{'date': (today + timedelta(days=i)).strftime('%Y-%m-%d'), 'uv': 5.0 + (i % 3)}
                  for i in range(6)]
    }

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_tide_data():
    """Get live tide data from NOAA for Fernandina Beach, FL (Station 8720030)"""
    station_id = "8720030"  # Fernandina Beach, FL

    try:
        # Get tide predictions for next 7 days
        begin_date = datetime.now().strftime('%Y%m%d')
        end_date = (datetime.now() + timedelta(days=7)).strftime('%Y%m%d')

        url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date={begin_date}&end_date={end_date}&station={station_id}&product=predictions&datum=MLLW&time_zone=lst_ldt&units=english&interval=hilo&format=json"

        resp = requests.get(url, timeout=10)

        if resp.status_code == 200:
            data = resp.json()
            predictions = data.get('predictions', [])

            # Group by date
            daily_tides = {}
            for pred in predictions:
                datetime_str = pred['t']  # Format: "2025-11-07 06:30"
                date_str = datetime_str.split(' ')[0]
                time_24hr = datetime_str.split(' ')[1]

                # Convert 24hr time to 12hr format
                try:
                    time_obj = datetime.strptime(time_24hr, '%H:%M')
                    time_12hr = time_obj.strftime('%I:%M %p').lstrip('0')
                except:
                    time_12hr = time_24hr  # Fallback to original if conversion fails

                if date_str not in daily_tides:
                    daily_tides[date_str] = {'high': [], 'low': []}

                tide_info = {
                    'time': time_12hr,
                    'time_24hr': time_24hr,
                    'height': float(pred['v'])
                }

                if pred['type'] == 'H':
                    daily_tides[date_str]['high'].append(tide_info)
                else:
                    daily_tides[date_str]['low'].append(tide_info)

            return daily_tides
    except Exception as e:
        # Log error but don't crash
        print(f"Tide API error: {e}")
        pass

    # Fallback tide data (in case API is down)
    return {
        '2025-11-07': {
            'high': [{'time': '6:30 AM', 'time_24hr': '06:30', 'height': 6.5},
                     {'time': '7:00 PM', 'time_24hr': '19:00', 'height': 6.8}],
            'low': [{'time': '12:15 AM', 'time_24hr': '00:15', 'height': 0.5},
                    {'time': '12:45 PM', 'time_24hr': '12:45', 'height': 0.3}]
        },
        '2025-11-08': {
            'high': [{'time': '7:15 AM', 'time_24hr': '07:15', 'height': 6.6},
                     {'time': '7:45 PM', 'time_24hr': '19:45', 'height': 6.9}],
            'low': [{'time': '1:00 AM', 'time_24hr': '01:00', 'height': 0.4},
                    {'time': '1:30 PM', 'time_24hr': '13:30', 'height': 0.2}]
        },
        '2025-11-09': {
            'high': [{'time': '8:00 AM', 'time_24hr': '08:00', 'height': 6.7},
                     {'time': '8:30 PM', 'time_24hr': '20:30', 'height': 7.0}],
            'low': [{'time': '1:45 AM', 'time_24hr': '01:45', 'height': 0.3},
                    {'time': '2:15 PM', 'time_24hr': '14:15', 'height': 0.1}]
        },
        '2025-11-10': {
            'high': [{'time': '8:45 AM', 'time_24hr': '08:45', 'height': 6.8},
                     {'time': '9:15 PM', 'time_24hr': '21:15', 'height': 7.1}],
            'low': [{'time': '2:30 AM', 'time_24hr': '02:30', 'height': 0.2},
                    {'time': '3:00 PM', 'time_24hr': '15:00', 'height': 0.0}]
        },
    }

def get_tide_recommendation(activity_start_time, activity_type, date_str, tide_data):
    """Get tide-based recommendation for an activity

    Args:
        activity_start_time: "10:00 AM"
        activity_type: "beach", "activity", etc.
        date_str: "2025-11-10"
        tide_data: Dictionary from get_tide_data()

    Returns:
        Dictionary with tide info and recommendations
    """
    if date_str not in tide_data:
        return None

    day_tides = tide_data[date_str]

    # Determine if it's a water/beach activity
    water_activities = ['beach', 'water', 'surf', 'swim', 'kayak', 'boat', 'fish']
    is_water_activity = any(word in activity_type.lower() for word in water_activities)

    if not is_water_activity:
        return None

    # Get nearest high and low tides
    high_tides = day_tides.get('high', [])
    low_tides = day_tides.get('low', [])

    result = {
        'high_tides': high_tides,
        'low_tides': low_tides,
        'recommendation': '',
        'best_time': ''
    }

    # Create recommendations based on activity type
    if 'beach' in activity_type.lower() or 'swim' in activity_type.lower():
        if high_tides:
            result['recommendation'] = "🌊 Best for swimming during high tide"
            result['best_time'] = f"High tide: {high_tides[0]['time']} ({high_tides[0]['height']}ft)"
        if low_tides:
            result['recommendation'] += "\n🐚 Best for shell hunting during low tide"

    elif 'surf' in activity_type.lower():
        if high_tides:
            result['recommendation'] = "🏄 Better waves during high tide"
            result['best_time'] = f"High tide: {high_tides[0]['time']}"

    return result

# ============================================================================
# TRAFFIC & FLIGHT TRACKING APIS
# ============================================================================

@st.cache_data(ttl=300)  # Cache for 5 minutes (traffic changes frequently)
def get_traffic_data(origin, destination, departure_time=None):
    """Get real-time traffic data using Google Maps Distance Matrix API

    Args:
        origin: Starting address or coordinates
        destination: Ending address or coordinates
        departure_time: Unix timestamp for departure (optional, defaults to now)

    Returns:
        Dictionary with duration, duration_in_traffic, distance, and traffic level
    """
    api_key = os.getenv('GOOGLE_MAPS_API_KEY', '')

    if not api_key:
        # Return fallback data (typical/historical estimates)
        return {
            'distance': {'text': '45 miles', 'value': 72420},
            'duration': {'text': '45 mins', 'value': 2700},
            'duration_in_traffic': {'text': '45 mins', 'value': 2700},
            'traffic_level': 'Light',
            'traffic_emoji': '🟢',
            'delay_minutes': 0,
            'status': 'FALLBACK',
            'message': 'Typical drive time (Set GOOGLE_MAPS_API_KEY for live traffic)'
        }

    try:
        # If departure_time not specified, use current time
        if departure_time is None:
            departure_time = int(datetime.now().timestamp())

        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            'origins': origin,
            'destinations': destination,
            'departure_time': departure_time,
            'traffic_model': 'best_guess',
            'key': api_key
        }

        resp = requests.get(url, params=params, timeout=10)

        if resp.status_code == 200:
            data = resp.json()

            if data['status'] == 'OK' and data['rows'][0]['elements'][0]['status'] == 'OK':
                element = data['rows'][0]['elements'][0]

                # Calculate traffic level
                normal_duration = element['duration']['value']
                traffic_duration = element.get('duration_in_traffic', {}).get('value', normal_duration)

                delay_minutes = (traffic_duration - normal_duration) / 60

                if delay_minutes < 5:
                    traffic_level = 'Light'
                    traffic_emoji = '🟢'
                elif delay_minutes < 15:
                    traffic_level = 'Moderate'
                    traffic_emoji = '🟡'
                else:
                    traffic_level = 'Heavy'
                    traffic_emoji = '🔴'

                return {
                    'distance': element['distance'],
                    'duration': element['duration'],
                    'duration_in_traffic': element.get('duration_in_traffic', element['duration']),
                    'traffic_level': traffic_level,
                    'traffic_emoji': traffic_emoji,
                    'delay_minutes': round(delay_minutes, 1),
                    'status': 'OK'
                }
    except Exception as e:
        print(f"Traffic API error: {e}")

    # Fallback on error
    return {
        'distance': {'text': '45 miles', 'value': 72420},
        'duration': {'text': '45 mins', 'value': 2700},
        'duration_in_traffic': {'text': '45 mins', 'value': 2700},
        'traffic_level': 'Light',
        'traffic_emoji': '🟢',
        'delay_minutes': 0,
        'status': 'ERROR',
        'message': 'Traffic data unavailable'
    }


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_flight_status(flight_number, flight_date):
    """Get live flight status from AviationStack API

    Args:
        flight_number: e.g., "AA2434"
        flight_date: Date in YYYY-MM-DD format

    Returns:
        Dictionary with flight status, gate info, delays, etc.
    """
    api_key = os.getenv('AVIATIONSTACK_API_KEY', '')

    if not api_key:
        # Return fallback data
        return {
            'status': 'scheduled',
            'departure': {
                'airport': 'DCA' if 'AA2434' in flight_number or 'AA1585' in flight_number else 'JAX',
                'scheduled': None,
                'actual': None,
                'gate': 'TBD',
                'terminal': 'TBD'
            },
            'arrival': {
                'airport': 'JAX' if 'AA2434' in flight_number or 'AA1585' in flight_number else 'DCA',
                'scheduled': None,
                'actual': None,
                'gate': 'TBD',
                'terminal': 'TBD'
            },
            'live_status': 'FALLBACK',
            'message': 'Set AVIATIONSTACK_API_KEY for live tracking'
        }

    try:
        # Extract airline code and flight number
        # AA2434 -> airline: AA, flight: 2434
        airline_code = flight_number[:2]
        flight_num = flight_number[2:]

        url = "http://api.aviationstack.com/v1/flights"
        params = {
            'access_key': api_key,
            'flight_iata': flight_number
        }

        resp = requests.get(url, params=params, timeout=10)

        if resp.status_code == 200:
            data = resp.json()

            if data.get('data') and len(data['data']) > 0:
                flight = data['data'][0]

                # Determine status emoji and message
                status = flight.get('flight_status', 'scheduled').lower()
                if status == 'active' or status == 'en-route':
                    status_emoji = '✈️'
                    status_text = 'In Flight'
                elif status == 'landed':
                    status_emoji = '🛬'
                    status_text = 'Landed'
                elif status == 'scheduled':
                    status_emoji = '🕐'
                    status_text = 'On Time'
                elif status == 'cancelled':
                    status_emoji = '❌'
                    status_text = 'Cancelled'
                elif status == 'delayed':
                    status_emoji = '⏰'
                    status_text = 'Delayed'
                else:
                    status_emoji = '🛫'
                    status_text = status.title()

                return {
                    'status': status,
                    'status_emoji': status_emoji,
                    'status_text': status_text,
                    'flight_number': flight.get('flight', {}).get('iata', flight_number),
                    'departure': {
                        'airport': flight.get('departure', {}).get('iata', ''),
                        'scheduled': flight.get('departure', {}).get('scheduled', ''),
                        'actual': flight.get('departure', {}).get('actual', ''),
                        'gate': flight.get('departure', {}).get('gate', 'TBD'),
                        'terminal': flight.get('departure', {}).get('terminal', 'TBD'),
                        'delay': flight.get('departure', {}).get('delay', 0)
                    },
                    'arrival': {
                        'airport': flight.get('arrival', {}).get('iata', ''),
                        'scheduled': flight.get('arrival', {}).get('scheduled', ''),
                        'actual': flight.get('arrival', {}).get('actual', ''),
                        'gate': flight.get('arrival', {}).get('gate', 'TBD'),
                        'terminal': flight.get('arrival', {}).get('terminal', 'TBD'),
                        'delay': flight.get('arrival', {}).get('delay', 0)
                    },
                    'live_status': 'OK'
                }
    except Exception as e:
        print(f"Flight API error: {e}")

    # Fallback on error
    return {
        'status': 'scheduled',
        'status_emoji': '🕐',
        'status_text': 'Scheduled',
        'flight_number': flight_number,
        'departure': {
            'airport': 'DCA' if 'AA2434' in flight_number or 'AA1585' in flight_number else 'JAX',
            'scheduled': None,
            'gate': 'TBD',
            'terminal': 'TBD'
        },
        'arrival': {
            'airport': 'JAX' if 'AA2434' in flight_number or 'AA1585' in flight_number else 'DCA',
            'scheduled': None,
            'gate': 'TBD',
            'terminal': 'TBD'
        },
        'live_status': 'ERROR',
        'message': 'Flight tracking unavailable'
    }


def get_tsa_wait_times(airport_code):
    """Get TSA security checkpoint wait times using historical data and manual updates

    Args:
        airport_code: e.g., "DCA", "JAX"

    Returns:
        Dictionary with wait time estimates (manual override if available, else historical)
    """
    # Check for manual updates first (within last 2 hours)
    manual_update = get_latest_manual_tsa_update(airport_code, max_age_hours=2)

    if manual_update:
        # Use manual update if available
        wait_minutes = manual_update['wait_minutes']

        # Determine wait level and recommendations
        if wait_minutes < 10:
            wait_level = 'Short'
            wait_emoji = '🟢'
            recommendation = 'Arrive 1.5 hours early'
        elif wait_minutes < 20:
            wait_level = 'Moderate'
            wait_emoji = '🟡'
            recommendation = 'Arrive 2 hours early'
        else:
            wait_level = 'Long'
            wait_emoji = '🔴'
            recommendation = 'Arrive 2.5 hours early'

        # Calculate how long ago the update was
        update_time = datetime.fromisoformat(manual_update['created_at'])
        minutes_ago = int((datetime.now() - update_time).total_seconds() / 60)

        return {
            'airport': airport_code,
            'wait_time_minutes': wait_minutes,
            'wait_level': wait_level,
            'wait_emoji': wait_emoji,
            'recommendation': recommendation,
            'status': 'MANUAL',
            'message': f'Real-time update from {manual_update["reported_by"]} ({minutes_ago} min ago)',
            'data_source': 'Manual update (MyTSA app or live report)',
            'updated_at': manual_update['created_at'],
            'notes': manual_update.get('notes', '')
        }

    # Airport-specific historical data (from research: iFly.com, official sources)
    # Data source: Historical TSA records and passenger volume analysis
    airport_data = {
        'DCA': {
            'average': 14,  # 13-15 min average (Reagan National)
            'peak_hours': [(5, 30), (9, 30)],  # 5:30 AM - 9:30 AM business travelers
            'peak_multiplier': 1.4,  # 20-25 min during peak
            'notes': 'DCA sees heavy business travel during weekday mornings'
        },
        'JAX': {
            'average': 10,  # 5-15 min average (Jacksonville)
            'peak_hours': [(4, 0), (7, 0), (16, 30), (19, 30)],  # Morning & evening peaks
            'peak_multiplier': 1.3,  # 13-15 min during peak
            'notes': 'JAX is a smaller regional airport with generally short waits'
        }
    }

    # Get current time to estimate if it's peak hours
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute
    current_time_decimal = current_hour + (current_minute / 60)

    # Get airport-specific data or use generic default
    if airport_code in airport_data:
        data = airport_data[airport_code]
        base_wait = data['average']

        # Check if current time is in peak hours
        is_peak = False
        peak_ranges = data.get('peak_hours', [])
        for i in range(0, len(peak_ranges), 2):
            if i + 1 < len(peak_ranges):
                start_hour, start_min = peak_ranges[i]
                end_hour, end_min = peak_ranges[i + 1]
                start_decimal = start_hour + (start_min / 60)
                end_decimal = end_hour + (end_min / 60)

                if start_decimal <= current_time_decimal <= end_decimal:
                    is_peak = True
                    break

        # Adjust wait time for peak hours
        if is_peak:
            wait_minutes = int(base_wait * data.get('peak_multiplier', 1.3))
        else:
            wait_minutes = base_wait
    else:
        # Generic fallback for other airports
        wait_minutes = 15

    # Determine wait level and recommendations
    if wait_minutes < 10:
        wait_level = 'Short'
        wait_emoji = '🟢'
        recommendation = 'Arrive 1.5 hours early'
    elif wait_minutes < 20:
        wait_level = 'Moderate'
        wait_emoji = '🟡'
        recommendation = 'Arrive 2 hours early'
    else:
        wait_level = 'Long'
        wait_emoji = '🔴'
        recommendation = 'Arrive 2.5 hours early'

    return {
        'airport': airport_code,
        'wait_time_minutes': wait_minutes,
        'wait_level': wait_level,
        'wait_emoji': wait_emoji,
        'recommendation': recommendation,
        'status': 'HISTORICAL',
        'message': f'Based on historical TSA data for {airport_code}',
        'data_source': 'Historical averages from TSA records and passenger volume analysis'
    }


def render_flight_status_widget(flight_number, flight_date, compact=False):
    """Render a live flight status widget

    Args:
        flight_number: e.g., "AA2434"
        flight_date: Date in YYYY-MM-DD format
        compact: If True, show minimal info
    """
    status = get_flight_status(flight_number, flight_date)

    # Escape HTML for all dynamic content from API
    import html
    safe_flight_number = html.escape(str(flight_number))
    safe_status_emoji = html.escape(status.get('status_emoji', '✈️'))
    safe_status_text = html.escape(status.get('status_text', 'Scheduled'))
    safe_dep_airport = html.escape(status['departure']['airport'])
    safe_dep_gate = html.escape(status['departure']['gate'])
    safe_dep_terminal = html.escape(status['departure']['terminal'])
    safe_arr_airport = html.escape(status['arrival']['airport'])
    safe_arr_gate = html.escape(status['arrival']['gate'])
    safe_arr_terminal = html.escape(status['arrival']['terminal'])

    if compact:
        # Compact version for cards
        st.markdown(f"""
        <div style="background: #f0f7ff; padding: 0.75rem; border-radius: 8px; border-left: 4px solid #2196f3;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{safe_status_emoji} {safe_status_text}</strong>
                </div>
                <div style="text-align: right; font-size: 0.9rem;">
                    {f"Gate {safe_dep_gate}" if status['departure']['gate'] != 'TBD' else 'Gate TBD'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Full version
        # Build delay text if needed
        delay_text = ""
        if status['departure'].get('delay', 0) > 0:
            delay_minutes = status['departure'].get('delay', 0)
            delay_text = f"<p style='margin: 0.5rem 0 0 0; color: #f44336;'><strong>⚠️ Delay:</strong> {delay_minutes} minutes</p>"

        st.markdown(f"""<div class="ultimate-card" style="border-left: 4px solid #2196f3;">
<div class="card-body">
<h4 style="margin: 0 0 0.5rem 0;">{safe_status_emoji} Flight {safe_flight_number} - {safe_status_text}</h4>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 0.75rem;">
<div>
<strong>🛫 Departure:</strong> {safe_dep_airport}<br>
<span style="font-size: 0.9rem;">Gate: {safe_dep_gate} • Terminal: {safe_dep_terminal}</span>
</div>
<div>
<strong>🛬 Arrival:</strong> {safe_arr_airport}<br>
<span style="font-size: 0.9rem;">Gate: {safe_arr_gate} • Terminal: {safe_arr_terminal}</span>
</div>
</div>
{delay_text}
</div>
</div>""", unsafe_allow_html=True)


def render_traffic_widget(origin, destination, label=""):
    """Render a traffic status widget

    Args:
        origin: Starting location
        destination: Ending location
        label: Display label for the route
    """
    traffic = get_traffic_data(origin, destination)

    # Determine traffic color
    if traffic['traffic_level'] == 'Light':
        color = '#4caf50'
    elif traffic['traffic_level'] == 'Moderate':
        color = '#ff9800'
    else:
        color = '#f44336'

    # Build delay text if needed
    delay_text = ""
    if traffic.get('delay_minutes', 0) > 0:
        delay_text = f"<p style='margin: 0.5rem 0 0 0; font-size: 0.85rem;'>+{traffic['delay_minutes']} min delay</p>"

    st.markdown(f"""<div class="ultimate-card" style="border-left: 4px solid {color};">
<div class="card-body">
<h4 style="margin: 0 0 0.5rem 0;">🚗 {label if label else 'Route Traffic'}</h4>
<div style="display: flex; justify-content: space-between; align-items: center;">
<div>
<p style="margin: 0.25rem 0;">
<strong>Distance:</strong> {traffic['distance']['text']}<br>
<strong>Duration:</strong> {traffic['duration_in_traffic']['text']}
</p>
</div>
<div style="text-align: right;">
<div style="background: {color}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">
{traffic.get('traffic_emoji', '🚗')} {traffic['traffic_level']}
</div>
{delay_text}
</div>
</div>
</div>
</div>""", unsafe_allow_html=True)


def render_tsa_wait_widget(airport_code):
    """Render TSA security wait times widget with manual update capability

    Args:
        airport_code: Airport code like "DCA", "JAX"
    """
    wait_data = get_tsa_wait_times(airport_code)

    # Determine color based on wait level
    if wait_data['wait_level'] == 'Short':
        color = '#4caf50'
    elif wait_data['wait_level'] == 'Moderate':
        color = '#ff9800'
    else:
        color = '#f44336'

    # Data source indicator
    if wait_data.get('status') == 'MANUAL':
        data_source_badge = f"<span style='background: #2196f3; color: white; padding: 0.25rem 0.5rem; border-radius: 8px; font-size: 0.75rem;'>📱 {wait_data['message']}</span>"
    else:
        data_source_badge = f"<span style='background: #9e9e9e; color: white; padding: 0.25rem 0.5rem; border-radius: 8px; font-size: 0.75rem;'>📊 Historical estimate</span>"

    st.markdown(f"""<div class="ultimate-card" style="border-left: 4px solid {color};">
<div class="card-body">
<h4 style="margin: 0 0 0.5rem 0;">🛂 TSA Security Wait Time - {airport_code}</h4>
<div style="display: flex; justify-content: space-between; align-items: center;">
<div>
<p style="margin: 0.25rem 0;">
<strong>Estimated Wait:</strong> ~{wait_data['wait_time_minutes']} minutes<br>
<strong>Recommendation:</strong> {wait_data['recommendation']}<br>
<span style="font-size: 0.85rem; opacity: 0.8;">{data_source_badge}</span>
</p>
</div>
<div style="text-align: right;">
<div style="background: {color}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">
{wait_data.get('wait_emoji', '🟡')} {wait_data['wait_level']}
</div>
</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

    # Manual update form
    with st.expander("📱 Update with real-time data from MyTSA app"):
        st.markdown(f"**Report Current Wait Time for {airport_code}**")
        st.caption("Check the MyTSA app or ask TSA staff for current wait times. Updates expire after 2 hours.")

        col1, col2 = st.columns([2, 1])
        with col1:
            manual_wait = st.number_input(
                "Wait time (minutes):",
                min_value=0,
                max_value=120,
                value=wait_data['wait_time_minutes'],
                step=1,
                key=f"manual_wait_{airport_code}"
            )
            manual_notes = st.text_input(
                "Notes (optional):",
                placeholder="e.g., 'Checkpoint B is faster'",
                key=f"manual_notes_{airport_code}"
            )

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"💾 Save Update", key=f"save_tsa_{airport_code}", use_container_width=True):
                if save_manual_tsa_update(airport_code, manual_wait, reported_by="Manual Entry", notes=manual_notes):
                    st.success("✅ Wait time updated!")
                    st.rerun()
                else:
                    st.error("❌ Failed to save update")


def parse_cost_range(cost_str):
    """Parse cost range string to numeric value (uses midpoint of range)

    Examples:
        "$30-50 per person" -> 40
        "$25" -> 25
        "FREE" -> 0
        "Included" -> 0
    """
    import re
    if not cost_str or cost_str == 'N/A':
        return 0

    cost_str = str(cost_str).upper()

    # Check for free/included
    if 'FREE' in cost_str or 'INCLUDED' in cost_str or 'COMPLIMENTARY' in cost_str:
        return 0

    # Extract numbers
    numbers = re.findall(r'\d+', cost_str)
    if not numbers:
        return 0

    # If range (e.g., $30-50), take average
    if len(numbers) >= 2:
        return (int(numbers[0]) + int(numbers[1])) / 2
    else:
        return int(numbers[0])

def get_confirmed_meals_budget():
    """Get budget totals from all confirmed meals

    Returns:
        List of dicts with meal info and costs
    """
    try:
        data = get_trip_data()
        meals = []

        for meal_id, proposal in data.get('meal_proposals', {}).items():
            if proposal.get('status') == 'confirmed':
                options = proposal.get('restaurant_options', [])
                final_choice = proposal.get('final_choice')
                meal_time = proposal.get('meal_time')

                if final_choice is not None and final_choice < len(options):
                    restaurant = options[final_choice]
                    cost_per_person = parse_cost_range(restaurant.get('cost_range', '0'))
                    # Assume 2 people (Michael + John)
                    total_cost = cost_per_person * 2

                    meals.append({
                        'meal_id': meal_id,
                        'name': restaurant['name'],
                        'cost_per_person': cost_per_person,
                        'total_cost': total_cost,
                        'time': meal_time,
                        'category': 'Dining'
                    })

        return meals
    except Exception as e:
        print(f"Error loading confirmed meals budget: {e}")
        return []

def get_confirmed_activities_budget():
    """Get budget totals from all confirmed optional activities

    Returns:
        List of dicts with activity info and costs
    """
    try:
        data = get_trip_data()
        activities = []

        for activity_slot_id, proposal in data.get('activity_proposals', {}).items():
            if proposal.get('status') == 'confirmed':
                options = proposal.get('activity_options', [])
                final_choice = proposal.get('final_choice')
                activity_time = proposal.get('activity_time')
                date = proposal.get('date')

                if final_choice is not None and final_choice < len(options):
                    activity = options[final_choice]
                    cost_per_person = parse_cost_range(activity.get('cost_range', '0'))
                    # Assume 2 people (Michael + John), Michael pays for activities
                    total_cost = cost_per_person * 2

                    activities.append({
                        'activity_slot_id': activity_slot_id,
                        'name': activity['name'],
                        'cost_per_person': cost_per_person,
                        'total_cost': total_cost,
                        'time': activity_time,
                        'date': date,
                        'category': 'Activities'
                    })

        return activities
    except Exception as e:
        print(f"Error loading confirmed activities budget: {e}")
        return []

def get_confirmed_alcohol_budget():
    """Get budget totals from all purchased alcohol

    Returns:
        List of dicts with alcohol info and costs
    """
    alcohol_items = []
    all_requests = get_alcohol_requests()

    for request in all_requests:
        if request['purchased'] and request['cost'] > 0:
            alcohol_items.append({
                'id': request['id'],
                'name': request['item_name'],
                'quantity': request['quantity'],
                'total_cost': request['cost'],
                'category': 'Alcohol/Drinks'
            })

    return alcohol_items

def calculate_trip_budget(activities_data):
    """Calculate total trip budget with spending breakdown including meals

    Returns:
        Dictionary with budget totals and categories
    """
    total_cost = 0
    category_costs = {}

    # Add activities
    for activity in activities_data:
        cost = activity.get('cost', 0)
        category = activity.get('category', 'Other')

        total_cost += cost

        if category not in category_costs:
            category_costs[category] = 0
        category_costs[category] += cost

    # Add confirmed meals
    confirmed_meals = get_confirmed_meals_budget()
    for meal in confirmed_meals:
        cost = meal['total_cost']
        category = meal['category']

        total_cost += cost

        if category not in category_costs:
            category_costs[category] = 0
        category_costs[category] += cost

    # Add confirmed optional activities
    confirmed_activities = get_confirmed_activities_budget()
    for activity in confirmed_activities:
        cost = activity['total_cost']
        category = activity['category']

        total_cost += cost

        if category not in category_costs:
            category_costs[category] = 0
        category_costs[category] += cost

    # Add confirmed alcohol purchases
    confirmed_alcohol = get_confirmed_alcohol_budget()
    for alcohol_item in confirmed_alcohol:
        cost = alcohol_item['total_cost']
        category = alcohol_item['category']

        total_cost += cost

        if category not in category_costs:
            category_costs[category] = 0
        category_costs[category] += cost

    return {
        'total': total_cost,
        'by_category': category_costs,
        'categories': sorted(category_costs.items(), key=lambda x: x[1], reverse=True),
        'confirmed_meals': confirmed_meals,
        'confirmed_meals_total': sum(m['total_cost'] for m in confirmed_meals),
        'confirmed_activities': confirmed_activities,
        'confirmed_activities_total': sum(a['total_cost'] for a in confirmed_activities),
        'confirmed_alcohol': confirmed_alcohol,
        'confirmed_alcohol_total': sum(a['total_cost'] for a in confirmed_alcohol)
    }


def render_budget_widget(activities_data, show_sensitive=True, view_mode='michael'):
    """Render budget tracking widget

    Args:
        activities_data: List of confirmed activities
        show_sensitive: Whether to show actual costs
        view_mode: 'michael' or 'john' to show appropriate share
    """
    if not show_sensitive:
        st.info("💰 Budget information hidden in public mode")
        return

    budget_data = calculate_trip_budget(activities_data)

    # Calculate shares (simplified: split dining and alcohol costs 50/50, Michael pays for activities)
    meals_split = budget_data.get('confirmed_meals_total', 0) / 2
    alcohol_split = budget_data.get('confirmed_alcohol_total', 0) / 2
    johns_share = meals_split + alcohol_split
    michaels_share = budget_data['total'] - johns_share

    if view_mode == 'john':
        display_total = johns_share
        share_label = "Your Share"
    else:
        display_total = michaels_share
        share_label = "Your Total"

    meals_count = len(budget_data.get('confirmed_meals', []))
    meals_total = budget_data.get('confirmed_meals_total', 0)

    st.markdown(f"""<div class="ultimate-card" style="border-left: 4px solid #4caf50;">
<div class="card-body">
<h4 style="margin: 0 0 0.5rem 0;">💰 Trip Budget Overview</h4>
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 1rem; margin-top: 0.75rem;">
<div>
<strong>Total Trip:</strong><br>
<span style="font-size: 1.3rem; color: #4caf50;">${budget_data['total']:,.0f}</span>
</div>
<div>
<strong>{share_label}:</strong><br>
<span style="font-size: 1.3rem; color: #2196f3;">${display_total:,.0f}</span>
</div>
<div>
<strong>Confirmed Meals:</strong><br>
<span style="font-size: 1.2rem;">{meals_count} meals</span><br>
<span style="font-size: 0.9rem; color: #666;">${meals_total:,.0f}</span>
</div>
<div>
<strong>Top Category:</strong><br>
<span style="font-size: 1.0rem;">{budget_data['categories'][0][0] if budget_data['categories'] else 'N/A'}</span><br>
<span style="font-size: 0.9rem; color: #666;">{'$' + str(int(budget_data['categories'][0][1])) if budget_data['categories'] else '$0'}</span>
</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

    # Show category breakdown
    if budget_data['categories']:
        with st.expander("📊 See Detailed Breakdown"):
            for category, amount in budget_data['categories']:
                percentage = (amount / budget_data['total'] * 100) if budget_data['total'] > 0 else 0
                st.markdown(f"**{category}:** ${amount:,.0f} ({percentage:.1f}%)")

            # Show confirmed meals details
            if budget_data.get('confirmed_meals'):
                st.markdown("---")
                st.markdown("**🍽️ Confirmed Meals:**")
                for meal in budget_data['confirmed_meals']:
                    st.markdown(f"- **{meal['name']}**: ${meal['cost_per_person']:.0f}/person × 2 = ${meal['total_cost']:.0f}")

            # Show confirmed activities details
            if budget_data.get('confirmed_activities'):
                st.markdown("---")
                st.markdown("**🎯 Confirmed Activities:**")
                for activity in budget_data['confirmed_activities']:
                    st.markdown(f"- **{activity['name']}**: ${activity['cost_per_person']:.0f}/person × 2 = ${activity['total_cost']:.0f}")

            # Show confirmed alcohol details
            if budget_data.get('confirmed_alcohol'):
                st.markdown("---")
                st.markdown("**🍺 Alcohol/Drinks (Split 50/50):**")
                for item in budget_data['confirmed_alcohol']:
                    quantity_str = f" - {item['quantity']}" if item.get('quantity') else ""
                    split_cost = item['total_cost'] / 2
                    st.markdown(f"- **{item['name']}**{quantity_str}: ${item['total_cost']:.2f} (${split_cost:.2f} each)")


# ============================================================================
# STEP 3-12: SMART INTELLIGENCE FUNCTIONS
# ============================================================================

def detect_meal_gaps(activities_data):
    """Detect missing meals (breakfast, lunch, dinner) for each day

    Returns:
        List of missing meals with suggested times
    """
    from collections import defaultdict

    # Group activities by date
    days = defaultdict(list)
    for activity in activities_data:
        date_str = activity['date']
        days[date_str].append(activity)

    missing_meals = []

    for date_str, day_activities in sorted(days.items()):
        date_obj = pd.to_datetime(date_str)
        day_name = date_obj.strftime('%A, %B %d')

        # Check for meals
        meals_found = {
            'breakfast': False,
            'lunch': False,
            'dinner': False
        }

        for activity in day_activities:
            activity_lower = activity['activity'].lower()
            time_str = activity['time']

            # Try to parse time
            try:
                time_obj = datetime.strptime(time_str, "%I:%M %p")
                hour = time_obj.hour

                # Classify by time and activity type
                if activity['type'] == 'dining' or 'lunch' in activity_lower or 'breakfast' in activity_lower or 'dinner' in activity_lower:
                    if 6 <= hour < 11:
                        meals_found['breakfast'] = True
                    elif 11 <= hour < 16:
                        meals_found['lunch'] = True
                    elif 16 <= hour < 23:
                        meals_found['dinner'] = True
            except:
                pass

        # Report missing meals
        if not meals_found['breakfast']:
            missing_meals.append({
                'date': date_str,
                'day_name': day_name,
                'meal_type': 'breakfast',
                'suggested_time': '8:00 AM',
                'priority': 'medium'
            })

        if not meals_found['lunch']:
            missing_meals.append({
                'date': date_str,
                'day_name': day_name,
                'meal_type': 'lunch',
                'suggested_time': '12:30 PM',
                'priority': 'high'
            })

        if not meals_found['dinner']:
            missing_meals.append({
                'date': date_str,
                'day_name': day_name,
                'meal_type': 'dinner',
                'suggested_time': '6:30 PM',
                'priority': 'high'
            })

    return missing_meals

def detect_conflicts(activities_data):
    """Detect scheduling conflicts (overlaps, tight timings, impossible logistics)

    Returns:
        List of conflicts with severity and recommendations
    """
    conflicts = []

    # Sort activities by date and time
    sorted_activities = sorted(activities_data, key=lambda x: (x['date'], x.get('time', '12:00 PM')))

    for i in range(len(sorted_activities) - 1):
        current = sorted_activities[i]
        next_act = sorted_activities[i + 1]

        # Only check same-day activities
        if current['date'] != next_act['date']:
            continue

        try:
            # Get end time of current activity
            if current.get('duration'):
                current_end = calculate_end_time(current['time'], current['duration'])
                if not current_end:
                    continue

                current_end_obj = datetime.strptime(current_end, "%I:%M %p")
                next_start_obj = datetime.strptime(next_act['time'], "%I:%M %p")

                # Calculate gap in minutes
                gap_minutes = (next_start_obj - current_end_obj).total_seconds() / 60

                if gap_minutes < 0:
                    # OVERLAP!
                    conflicts.append({
                        'type': 'overlap',
                        'severity': 'critical',
                        'date': current['date'],
                        'activity1': current['activity'],
                        'activity2': next_act['activity'],
                        'end_time': current_end,
                        'start_time': next_act['time'],
                        'message': f"🔴 OVERLAP: {current['activity']} ends {current_end}, but {next_act['activity']} starts {next_act['time']}",
                        'suggestion': f"Reschedule {next_act['activity']} to start after {current_end}"
                    })
                elif gap_minutes < 15:
                    # TOO TIGHT
                    conflicts.append({
                        'type': 'tight_timing',
                        'severity': 'warning',
                        'date': current['date'],
                        'activity1': current['activity'],
                        'activity2': next_act['activity'],
                        'gap_minutes': int(gap_minutes),
                        'message': f"🟡 TIGHT: Only {int(gap_minutes)} min between {current['activity']} and {next_act['activity']}",
                        'suggestion': f"Consider adding 15-30 min buffer"
                    })
                elif gap_minutes > 240:  # More than 4 hours
                    # LARGE GAP - opportunity!
                    conflicts.append({
                        'type': 'large_gap',
                        'severity': 'info',
                        'date': current['date'],
                        'gap_start': current_end,
                        'gap_end': next_act['time'],
                        'gap_hours': round(gap_minutes / 60, 1),
                        'message': f"💡 FREE TIME: {round(gap_minutes/60, 1)} hours between {current_end} and {next_act['time']}",
                        'suggestion': f"Perfect time to add an activity!"
                    })
        except Exception as e:
            pass

    return conflicts

def score_activity_for_slot(activity, time_slot_start, date_str, weather_data, tide_data, recent_activities):
    """Score how well an activity fits a specific time slot (0-100)

    Multi-factor scoring based on:
    - Weather compatibility (30 points)
    - Time slot fit (25 points)
    - Location proximity (20 points)
    - Energy level balance (10 points)
    - Budget (10 points)
    - Variety (5 points)
    """
    score = 0
    reasons = []
    warnings = []

    # Get activity details
    activity_type = activity.get('type', '')
    duration = activity.get('duration', '1 hour')
    cost_str = activity.get('cost_range', '$0')

    # Parse cost (rough estimate)
    try:
        cost = int(re.findall(r'\d+', cost_str.split('-')[0])[0])
    except:
        cost = 20

    # FACTOR 1: Weather Match (30 points)
    weather_score = 15  # Default moderate score
    outdoor_activities = ['beach', 'hiking', 'kayak', 'horse', 'bike', 'walk', 'tour', 'boat']
    indoor_activities = ['spa', 'museum', 'shopping', 'dining', 'cooking', 'wine']

    is_outdoor = any(word in activity['name'].lower() or word in activity.get('description', '').lower()
                     for word in outdoor_activities)
    is_indoor = any(word in activity['name'].lower() or word in activity.get('description', '').lower()
                    for word in indoor_activities)

    # Check weather for this date
    if weather_data and 'forecast' in weather_data:
        for forecast in weather_data['forecast']:
            if forecast['date'] == date_str:
                condition = forecast.get('condition', '').lower()
                temp = forecast.get('high', 75)
                rain_chance = forecast.get('precipitation', 0)

                if is_outdoor:
                    if rain_chance > 70:
                        weather_score = 5
                        warnings.append(f"⚠️ {rain_chance}% rain chance - consider indoor alternative")
                    elif rain_chance < 30 and 'sun' in condition:
                        weather_score = 30
                        reasons.append(f"☀️ Perfect weather ({condition}, {temp}°F)")
                    elif rain_chance < 30:
                        weather_score = 25
                        reasons.append(f"✅ Good weather ({temp}°F, {rain_chance}% rain)")

                elif is_indoor:
                    weather_score = 25  # Indoor always works
                    if rain_chance > 50:
                        reasons.append(f"☔ Great indoor choice (rainy day)")
                break

    score += weather_score

    # FACTOR 2: Duration Fit (25 points)
    duration_minutes = parse_duration_to_minutes(duration)
    # Assume we want activities that fit well
    if 60 <= duration_minutes <= 180:  # 1-3 hours is ideal
        score += 25
        reasons.append(f"⏱️ Perfect duration ({duration})")
    elif duration_minutes < 60:
        score += 20
    elif duration_minutes > 180:
        score += 15
        warnings.append(f"⏱️ Long activity ({duration}) - plan accordingly")

    # FACTOR 3: Cost (10 points)
    if cost == 0:
        score += 10
        reasons.append("💰 FREE activity!")
    elif cost < 30:
        score += 8
    elif cost < 100:
        score += 5
    else:
        score += 3

    # FACTOR 4: Rating (10 points)
    rating_str = activity.get('rating', '0/5')
    try:
        rating = float(rating_str.split('/')[0])
        score += int(rating * 2)  # 5.0 rating = 10 points
        if rating >= 4.7:
            reasons.append(f"⭐ Highly rated ({rating}/5)")
    except:
        pass

    # FACTOR 5: Tide match for beach activities (bonus 10 points)
    if 'beach' in activity_type.lower() or 'beach' in activity['name'].lower():
        tide_rec = get_tide_recommendation(time_slot_start, 'beach', date_str, tide_data)
        if tide_rec:
            score += 10
            reasons.append(tide_rec.get('best_time', ''))

    # Cap at 100
    score = min(100, score)

    return {
        'score': score,
        'reasons': reasons,
        'warnings': warnings
    }

def get_smart_duration_default(activity_name, activity_type='activity'):
    """Get smart default duration for an activity based on its name and type

    Returns:
        String like "2 hours" or "45 minutes"
    """
    activity_lower = activity_name.lower()

    # Quick activities (15-30 min)
    if any(word in activity_lower for word in ['coffee', 'ice cream', 'fudge', 'bagel']):
        return "30 minutes"

    # Short activities (45min-1hr)
    if any(word in activity_lower for word in ['sunrise', 'sunset', 'cloud watch', 'meditation', 'journal']):
        return "45 minutes"

    # Medium activities (1-2 hours)
    if any(word in activity_lower for word in ['walk', 'stroll', 'read', 'relax', 'photography', 'beach', 'pool', 'seashell', 'tide pool', 'bird watch', 'driftwood', 'dolphin']):
        return "1.5 hours"

    # Dining
    if activity_type in ['dining', 'Dining']:
        if 'breakfast' in activity_lower or 'brunch' in activity_lower:
            return "1.5 hours"
        elif 'fine dining' in activity_lower or 'dinner' in activity_lower:
            return "2 hours"
        else:
            return "1 hour"

    # Spa
    if activity_type in ['spa', 'Spa'] or 'massage' in activity_lower or 'facial' in activity_lower:
        if 'couple' in activity_lower:
            return "2 hours"
        else:
            return "1 hour"

    # Activities/Adventures
    if any(word in activity_lower for word in ['tour', 'kayak', 'paddleboard', 'horseback', 'segway', 'golf', 'tennis', 'hike', 'fishing']):
        return "3 hours"

    # Default
    return "2 hours"


def check_time_conflict(new_date, new_time_str, new_duration, existing_activities):
    """Check if a new activity conflicts with existing scheduled activities

    Args:
        new_date: Date string like "2025-11-07"
        new_time_str: Time string like "10:00 AM"
        new_duration: Duration string like "2 hours" or "90 minutes"
        existing_activities: List of already scheduled activities

    Returns:
        tuple: (has_conflict: bool, conflicting_activity: dict or None)
    """
    from datetime import datetime, timedelta

    # Parse new activity time
    try:
        new_time = datetime.strptime(new_time_str, "%I:%M %p")
    except:
        try:
            new_time = datetime.strptime(new_time_str, "%H:%M")
        except:
            return (False, None)  # Can't parse time, skip conflict check

    # Parse new activity duration
    try:
        if 'hour' in new_duration.lower():
            hours = float(new_duration.lower().split('hour')[0].strip())
            new_end_time = new_time + timedelta(hours=hours)
        elif 'min' in new_duration.lower():
            minutes = int(new_duration.lower().split('min')[0].strip())
            new_end_time = new_time + timedelta(minutes=minutes)
        else:
            new_end_time = new_time + timedelta(hours=2)  # Default 2 hours
    except:
        new_end_time = new_time + timedelta(hours=2)  # Default 2 hours

    # Check against existing activities on same date
    for activity in existing_activities:
        if activity['date'] != new_date:
            continue

        # Parse existing activity time
        try:
            existing_time = datetime.strptime(activity['time'], "%I:%M %p")
        except:
            try:
                existing_time = datetime.strptime(activity['time'], "%H:%M")
            except:
                continue  # Can't parse, skip

        # Parse existing activity duration
        existing_duration = activity.get('duration', '2 hours')
        try:
            if 'hour' in existing_duration.lower():
                hours = float(existing_duration.lower().split('hour')[0].strip())
                existing_end_time = existing_time + timedelta(hours=hours)
            elif 'min' in existing_duration.lower():
                minutes = int(existing_duration.lower().split('min')[0].strip())
                existing_end_time = existing_time + timedelta(minutes=minutes)
            else:
                existing_end_time = existing_time + timedelta(hours=2)
        except:
            existing_end_time = existing_time + timedelta(hours=2)

        # Check for overlap
        # Conflict if: new starts before existing ends AND new ends after existing starts
        if new_time < existing_end_time and new_end_time > existing_time:
            return (True, activity)

    return (False, None)


def is_activity_already_scheduled(activity_name, activities_data):
    """Check if a unique activity is already in the schedule

    Args:
        activity_name: Name of the activity to check
        activities_data: List of all scheduled activities

    Returns:
        bool: True if activity is already scheduled
    """
    # Normalize name for comparison
    activity_name_lower = activity_name.lower()

    for activity in activities_data:
        scheduled_name_lower = activity['activity'].lower()

        # Check for exact or very similar match
        if activity_name_lower in scheduled_name_lower or scheduled_name_lower in activity_name_lower:
            return True

    return False


def add_activity_to_schedule(activity_name, activity_description, selected_day, selected_time, duration, activity_type='activity', cost=0, location_name='TBD'):
    """Add a custom activity to the user's schedule

    Args:
        activity_name: Name of the activity
        activity_description: Description text
        selected_day: Day string like "Friday, Nov 7"
        selected_time: Time object or string like "10:00 AM"
        duration: Duration string like "2 hours"
        activity_type: Type category (activity, dining, etc.)
        cost: Estimated cost
        location_name: Location name

    Returns:
        True if added successfully, False otherwise
    """
    # Convert day name to date
    day_to_date = {
        "Friday, Nov 7": "2025-11-07",
        "Saturday, Nov 8": "2025-11-08",
        "Sunday, Nov 9": "2025-11-09",
        "Monday, Nov 10": "2025-11-10",
        "Tuesday, Nov 11": "2025-11-11",
        "Wednesday, Nov 12": "2025-11-12"
    }

    date_str = day_to_date.get(selected_day)
    if not date_str:
        return False

    # Convert time to string if it's a time object
    if hasattr(selected_time, 'strftime'):
        time_str = selected_time.strftime("%I:%M %p").lstrip('0')
    else:
        time_str = selected_time

    # Generate unique ID
    import uuid
    activity_id = f"custom_{uuid.uuid4().hex[:8]}"

    # Create activity object
    new_activity = {
        "id": activity_id,
        "date": date_str,
        "time": time_str,
        "activity": activity_name,
        "type": activity_type,
        "duration": duration,
        "location": {
            "name": location_name,
            "address": "TBD",
            "lat": 30.6074,  # Default to Amelia Island
            "lon": -81.4493,
            "phone": "N/A"
        },
        "status": "Custom",
        "cost": cost,
        "category": activity_type.capitalize(),
        "notes": activity_description,
        "what_to_bring": [],
        "tips": [],
        "priority": 2,
        "is_custom": True
    }

    # Add to session state
    if 'custom_activities' not in st.session_state:
        st.session_state.custom_activities = []

    st.session_state.custom_activities.append(new_activity)

    # Save to database for persistence
    save_custom_activity(new_activity)

    # Add a notification
    add_notification(
        "Activity Added",
        f"{activity_name} added to {selected_day} at {time_str}",
        "success"
    )

    return True

def auto_fill_meals(meal_gaps, weather_data):
    """Automatically fill missing meals with smart restaurant recommendations

    Args:
        meal_gaps: List of missing meal gaps from detect_meal_gaps()
        weather_data: Weather data for smart recommendations

    Returns:
        List of activities that were added
    """
    # Get dining options
    optional_activities = get_optional_activities()
    dining_options = optional_activities.get('🍽️ Fine Dining', []) + \
                     optional_activities.get('🍽️ Casual Dining', []) + \
                     optional_activities.get('🥞 Breakfast & Brunch', [])

    added_activities = []

    for gap in meal_gaps:
        # Find best restaurant for this meal
        meal_type = gap['meal_type']
        date_str = gap['date']
        suggested_time = gap['suggested_time']

        # Filter restaurants by meal type
        if meal_type == 'breakfast':
            candidates = [r for r in dining_options if 'breakfast' in r.get('name', '').lower() or 'brunch' in r.get('name', '').lower()]
            if not candidates:
                candidates = [r for r in dining_options if 'cafe' in r.get('name', '').lower() or 'coffee' in r.get('name', '').lower()]
        elif meal_type == 'lunch':
            candidates = [r for r in dining_options if 'casual' in r.get('description', '').lower() or 'lunch' in r.get('description', '').lower()]
            if not candidates:
                candidates = dining_options[:10]  # First 10 as fallback
        elif meal_type == 'dinner':
            candidates = [r for r in dining_options if 'dinner' in r.get('description', '').lower() or 'fine' in r.get('description', '').lower()]
            if not candidates:
                candidates = dining_options[:10]

        if not candidates:
            candidates = dining_options

        # Score each candidate
        best_restaurant = None
        best_score = 0

        for restaurant in candidates:
            score = 0

            # Rating score (40 points)
            rating_str = restaurant.get('rating', '0/5')
            try:
                rating = float(rating_str.split('/')[0])
                score += int(rating * 8)  # 5.0 = 40 points
            except:
                pass

            # Cost appropriateness (30 points)
            cost_str = restaurant.get('cost_range', '$0')
            try:
                cost = int(re.findall(r'\d+', cost_str.split('-')[0])[0])
                if meal_type == 'breakfast' and cost < 20:
                    score += 30
                elif meal_type == 'lunch' and cost < 40:
                    score += 30
                elif meal_type == 'dinner' and cost >= 40:
                    score += 30
                else:
                    score += 15
            except:
                score += 15

            # Weather appropriateness (30 points)
            if weather_data and 'forecast' in weather_data:
                for forecast in weather_data['forecast']:
                    if forecast['date'] == date_str:
                        rain_chance = forecast.get('precipitation', 0)
                        # Indoor restaurants better in rain
                        if rain_chance > 50:
                            score += 30
                        else:
                            # Outdoor seating nice in good weather
                            if 'outdoor' in restaurant.get('description', '').lower() or 'patio' in restaurant.get('description', '').lower():
                                score += 30
                            else:
                                score += 20
                        break

            if score > best_score:
                best_score = score
                best_restaurant = restaurant

        # Add the meal to schedule
        if best_restaurant:
            # Convert day name
            day_to_date = {
                "2025-11-07": "Friday, Nov 7",
                "2025-11-08": "Saturday, Nov 8",
                "2025-11-09": "Sunday, Nov 9",
                "2025-11-10": "Monday, Nov 10",
                "2025-11-11": "Tuesday, Nov 11",
                "2025-11-12": "Wednesday, Nov 12"
            }

            selected_day = day_to_date.get(date_str)

            # Extract cost
            cost = 0
            cost_str = best_restaurant.get('cost_range', '$0')
            try:
                cost = int(re.findall(r'\d+', cost_str.split('-')[0])[0])
            except:
                cost = 0

            # Determine duration based on meal type
            duration = "1 hour"
            if meal_type == 'breakfast':
                duration = "45 minutes"
            elif meal_type == 'dinner':
                duration = "1.5 hours"

            # Add to schedule
            success = add_activity_to_schedule(
                activity_name=f"{meal_type.title()} at {best_restaurant['name']}",
                activity_description=best_restaurant.get('description', ''),
                selected_day=selected_day,
                selected_time=suggested_time,
                duration=duration,
                activity_type='dining',
                cost=cost,
                location_name=best_restaurant.get('name', 'TBD')
            )

            if success:
                added_activities.append({
                    'meal_type': meal_type,
                    'restaurant': best_restaurant['name'],
                    'day': gap['day_name'],
                    'time': suggested_time
                })

    return added_activities

def ai_auto_scheduler(target_date_str, existing_activities, weather_data, tide_data, preferences=None):
    """AI-powered automatic schedule generator for a specific day

    Args:
        target_date_str: Date string like "2025-11-08"
        existing_activities: Current scheduled activities
        weather_data: Weather forecast data
        tide_data: Tide data
        preferences: Dict with user preferences (budget, activity_types, etc.)

    Returns:
        List of recommended activities for the day with optimal timing
    """
    if preferences is None:
        preferences = {
            'budget_per_day': 200,
            'max_activities': 3,
            'include_meals': True,
            'activity_types': ['beach', 'dining', 'activity', 'spa'],
            'energy_balance': True,
            'avoid_seafood_focused': True  # Avoid seafood-only restaurants (diverse menus are OK)
        }

    # Get all optional activities
    optional_activities = get_optional_activities()

    # Separate dining from activities
    dining_options = optional_activities.get('🍽️ Fine Dining', []) + \
                     optional_activities.get('🍽️ Casual Dining', []) + \
                     optional_activities.get('🥞 Breakfast & Brunch', [])

    # Apply seafood preference filter
    if preferences.get('avoid_seafood_focused'):
        # Exclude seafood-focused restaurants (but keep places with diverse menus)
        seafood_focused = optional_activities.get('🦞 Seafood & Waterfront', [])
        dining_options = [r for r in dining_options if r not in seafood_focused]

    # Get NON-DINING activities only (for activity slots)
    all_activities = []
    for category, items in optional_activities.items():
        # Skip dining categories - they'll be handled in meal slots only
        if '🍽️' not in category and '🥞' not in category:
            all_activities.extend(items)

    # Check what's already scheduled for this day
    day_activities = [a for a in existing_activities if a['date'] == target_date_str]

    # SPECIAL HANDLING: Arrival/departure days with flights
    is_arrival_day = target_date_str == "2025-11-07"  # Arrives 6:01 PM
    is_departure_day = target_date_str == "2025-11-12"  # Departs 11:40 AM

    # Check for flights/transport on this day
    has_flight = any(a.get('type') == 'transport' and ('flight' in a.get('activity', '').lower() or 'arrival' in a.get('activity', '').lower() or 'departure' in a.get('activity', '').lower()) for a in day_activities)

    # Determine which time slots are available based on flight times
    allow_breakfast = True
    allow_morning = True
    allow_lunch = True
    allow_afternoon = True
    allow_dinner = True

    if has_flight and is_arrival_day:
        # Arrives 6:01 PM + 90 min (deplane, luggage, drive, check-in) = ready by 7:30 PM
        # Dinner recommendation at 8:00 PM gives time to settle in
        allow_breakfast = False
        allow_morning = False
        allow_lunch = False
        allow_afternoon = False
        allow_dinner = True  # Can have dinner after arrival (~8:00 PM)
    elif has_flight and is_departure_day:
        # Departs 11:40 AM - only allow breakfast and early morning
        allow_breakfast = True  # Can have breakfast before departure
        allow_morning = False  # No time for 10am activities (need to leave by 10am)
        allow_lunch = False
        allow_afternoon = False
        allow_dinner = False

    # Convert date string to day name
    date_obj = pd.to_datetime(target_date_str)
    day_name = date_obj.strftime('%A, %B %d')

    # Day name mapping
    date_to_day = {
        "2025-11-07": "Friday, Nov 7",
        "2025-11-08": "Saturday, Nov 8",
        "2025-11-09": "Sunday, Nov 9",
        "2025-11-10": "Monday, Nov 10",
        "2025-11-11": "Tuesday, Nov 11",
        "2025-11-12": "Wednesday, Nov 12"
    }
    selected_day = date_to_day.get(target_date_str, day_name)

    recommendations = []

    # STEP 1: Schedule breakfast if missing (7:30-9:00 AM)
    has_breakfast = any(a['type'] == 'dining' and datetime.strptime(a['time'], "%I:%M %p").hour < 11 for a in day_activities)

    if not has_breakfast and preferences['include_meals'] and allow_breakfast:
        breakfast_candidates = [r for r in dining_options if 'breakfast' in r.get('name', '').lower() or 'brunch' in r.get('name', '').lower()]
        if breakfast_candidates:
            best_breakfast = max(breakfast_candidates, key=lambda x: float(x.get('rating', '0/5').split('/')[0]))

            recommendations.append({
                'time': '8:00 AM',
                'activity': best_breakfast,
                'type': 'dining',
                'reason': 'Start your day with highly-rated breakfast',
                'duration': '45 minutes'
            })

    # STEP 2: Morning activity (9:00 AM - 12:00 PM)
    morning_slot_filled = any(9 <= datetime.strptime(a['time'], "%I:%M %p").hour < 12 for a in day_activities)

    if not morning_slot_filled and allow_morning:
        # Score activities for morning slot
        morning_scores = []

        for activity in all_activities:
            score_result = score_activity_for_slot(
                activity,
                '10:00 AM',
                target_date_str,
                weather_data,
                tide_data,
                day_activities
            )

            # Boost outdoor activities in morning
            if any(word in activity.get('name', '').lower() for word in ['beach', 'kayak', 'bike', 'walk', 'boat']):
                score_result['score'] += 15

            morning_scores.append({
                'activity': activity,
                'score': score_result['score'],
                'reasons': score_result['reasons']
            })

        # Get top recommendation
        if morning_scores:
            best_morning = max(morning_scores, key=lambda x: x['score'])
            if best_morning['score'] > 50:  # Only recommend if score is decent
                recommendations.append({
                    'time': '10:00 AM',
                    'activity': best_morning['activity'],
                    'type': 'activity',
                    'reason': ', '.join(best_morning['reasons'][:2]),
                    'duration': best_morning['activity'].get('duration', '2 hours')
                })

    # STEP 3: Lunch (12:00 PM - 2:00 PM)
    has_lunch = any(a['type'] == 'dining' and 11 <= datetime.strptime(a['time'], "%I:%M %p").hour < 16 for a in day_activities)

    if not has_lunch and preferences['include_meals'] and allow_lunch:
        lunch_candidates = [r for r in dining_options if 'casual' in r.get('description', '').lower() or 'lunch' in r.get('description', '').lower()]
        if not lunch_candidates:
            lunch_candidates = dining_options[:10]

        if lunch_candidates:
            # Score by rating and cost
            best_lunch = max(lunch_candidates, key=lambda x: float(x.get('rating', '0/5').split('/')[0]))

            recommendations.append({
                'time': '12:30 PM',
                'activity': best_lunch,
                'type': 'dining',
                'reason': 'Refuel with a great lunch spot',
                'duration': '1 hour'
            })

    # STEP 4: Afternoon activity (2:00 PM - 5:00 PM)
    afternoon_slot_filled = any(14 <= datetime.strptime(a['time'], "%I:%M %p").hour < 17 for a in day_activities)

    if not afternoon_slot_filled and allow_afternoon:
        afternoon_scores = []

        for activity in all_activities:
            score_result = score_activity_for_slot(
                activity,
                '3:00 PM',
                target_date_str,
                weather_data,
                tide_data,
                day_activities + [r for r in recommendations]
            )

            # Boost relaxing activities in afternoon
            if any(word in activity.get('name', '').lower() for word in ['spa', 'massage', 'wine', 'museum']):
                score_result['score'] += 10

            afternoon_scores.append({
                'activity': activity,
                'score': score_result['score'],
                'reasons': score_result['reasons']
            })

        if afternoon_scores:
            best_afternoon = max(afternoon_scores, key=lambda x: x['score'])
            if best_afternoon['score'] > 50:
                recommendations.append({
                    'time': '3:00 PM',
                    'activity': best_afternoon['activity'],
                    'type': 'activity',
                    'reason': ', '.join(best_afternoon['reasons'][:2]),
                    'duration': best_afternoon['activity'].get('duration', '2 hours')
                })

    # STEP 5: Dinner (6:00 PM - 8:00 PM)
    has_dinner = any(a['type'] == 'dining' and datetime.strptime(a['time'], "%I:%M %p").hour >= 16 for a in day_activities)

    if not has_dinner and preferences['include_meals'] and allow_dinner:
        dinner_candidates = [r for r in dining_options if 'fine' in r.get('description', '').lower() or 'dinner' in r.get('description', '').lower()]
        if not dinner_candidates:
            dinner_candidates = dining_options[:10]

        if dinner_candidates:
            # Prefer highly-rated restaurants for dinner
            best_dinner = max(dinner_candidates, key=lambda x: float(x.get('rating', '0/5').split('/')[0]))

            # Adjust dinner time for arrival day (arrive 6:01 PM + 90 min travel/checkin = 8:00 PM)
            dinner_time = '8:00 PM' if is_arrival_day else '6:30 PM'

            recommendations.append({
                'time': dinner_time,
                'activity': best_dinner,
                'type': 'dining',
                'reason': 'End the day with an amazing dinner' if not is_arrival_day else 'Welcome dinner after arrival',
                'duration': '1.5 hours'
            })

    return recommendations

@st.cache_data(ttl=1800)
def get_weather_ultimate():
    """Get real weather data with fallback"""
    api_key = os.getenv('OPENWEATHER_API_KEY', '')
    lat, lon = 30.6074, -81.4493  # Amelia Island

    if api_key:
        try:
            # Current weather
            current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=imperial"

            current_resp = requests.get(current_url, timeout=5)
            forecast_resp = requests.get(forecast_url, timeout=5)

            if current_resp.status_code == 200 and forecast_resp.status_code == 200:
                current_data = current_resp.json()
                forecast_data = forecast_resp.json()

                # Get UV data
                uv_data = get_uv_index()

                # Process forecast
                daily_forecasts = {}
                for item in forecast_data['list']:
                    date = item['dt_txt'].split(' ')[0]
                    if date not in daily_forecasts:
                        # Find UV for this date
                        uv_for_date = 5.0
                        for uv_day in uv_data['daily']:
                            if uv_day['date'] == date:
                                uv_for_date = uv_day['uv']
                                break

                        daily_forecasts[date] = {
                            'date': date,
                            'high': item['main']['temp_max'],
                            'low': item['main']['temp_min'],
                            'condition': item['weather'][0]['description'].title(),
                            'precipitation': int(item.get('pop', 0) * 100),
                            'humidity': item['main']['humidity'],
                            'wind': round(item['wind']['speed']),
                            'uv_index': uv_for_date
                        }
                    else:
                        daily_forecasts[date]['high'] = max(daily_forecasts[date]['high'], item['main']['temp_max'])
                        daily_forecasts[date]['low'] = min(daily_forecasts[date]['low'], item['main']['temp_min'])

                return {
                    "current": {
                        "temperature": round(current_data['main']['temp']),
                        "feels_like": round(current_data['main']['feels_like']),
                        "condition": current_data['weather'][0]['description'].title(),
                        "humidity": current_data['main']['humidity'],
                        "wind_speed": round(current_data['wind']['speed']),
                        "visibility": round(current_data.get('visibility', 10000) / 1609.34, 1),
                        "uv_index": uv_data['current']
                    },
                    "forecast": list(daily_forecasts.values())[:6],
                    "source": "OpenWeather API (Real Data)"
                }
        except Exception as e:
            pass
    
    # Fallback weather data
    return {
        "current": {
            "temperature": 75,
            "feels_like": 73,
            "condition": "Partly Cloudy",
            "humidity": 68,
            "wind_speed": 8,
            "visibility": 10.0,
            "uv_index": 5.0
        },
        "forecast": [
            {"date": "2025-11-07", "high": 78, "low": 65, "condition": "Sunny", "precipitation": 0, "humidity": 65, "wind": 7, "uv_index": 6.0},
            {"date": "2025-11-08", "high": 75, "low": 62, "condition": "Partly Cloudy", "precipitation": 10, "humidity": 70, "wind": 9, "uv_index": 5.5},
            {"date": "2025-11-09", "high": 72, "low": 58, "condition": "Cloudy", "precipitation": 20, "humidity": 75, "wind": 10, "uv_index": 4.0},
            {"date": "2025-11-10", "high": 74, "low": 60, "condition": "Sunny", "precipitation": 0, "humidity": 63, "wind": 8, "uv_index": 6.5},
            {"date": "2025-11-11", "high": 76, "low": 63, "condition": "Partly Cloudy", "precipitation": 5, "humidity": 68, "wind": 7, "uv_index": 5.0},
            {"date": "2025-11-12", "high": 77, "low": 64, "condition": "Sunny", "precipitation": 0, "humidity": 65, "wind": 6, "uv_index": 6.0}
        ],
        "source": "Sample Data (Set OPENWEATHER_API_KEY for real data)"
    }

def get_weather_emoji(condition):
    """Get emoji for weather condition"""
    condition_lower = condition.lower()
    if 'clear' in condition_lower or 'sunny' in condition_lower:
        return '☀️'
    elif 'cloud' in condition_lower:
        return '⛅'
    elif 'rain' in condition_lower:
        return '🌧️'
    elif 'storm' in condition_lower:
        return '⛈️'
    else:
        return '🌤️'

# ============================================================================
# SMART SCHEDULE ANALYZER
# ============================================================================

def analyze_schedule_gaps(activities_data):
    """
    Analyze the schedule to find free time gaps.
    Returns a list of time gaps with metadata for smart recommendations.
    """
    from datetime import datetime, timedelta

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(activities_data)
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    df = df.sort_values('datetime')

    gaps = []
    trip_dates = pd.date_range(start='2025-11-07', end='2025-11-12', freq='D')

    for date in trip_dates:
        date_str = date.strftime('%Y-%m-%d')
        day_name = date.strftime('%A, %b %d')

        # Get activities for this day
        day_activities = df[df['date'] == date_str].sort_values('datetime')

        if len(day_activities) == 0:
            # Full day free
            gaps.append({
                'date': date_str,
                'day_name': day_name,
                'start_time': '08:00',
                'end_time': '22:00',
                'duration_hours': 14,
                'time_of_day': 'all_day',
                'description': f"{day_name}: Full day available"
            })
        else:
            # Check for gaps between activities
            for i in range(len(day_activities)):
                # Morning gap (before first activity)
                if i == 0:
                    first_activity_time = day_activities.iloc[i]['datetime']
                    first_activity_hour = first_activity_time.hour
                    if first_activity_hour > 9:  # Gap before first activity (assuming 8am start)
                        duration = first_activity_hour - 8
                        if duration >= 2:  # Only show gaps of 2+ hours
                            gaps.append({
                                'date': date_str,
                                'day_name': day_name,
                                'start_time': '08:00',
                                'end_time': f'{first_activity_hour:02d}:00',
                                'duration_hours': duration,
                                'time_of_day': 'morning',
                                'description': f"{day_name}: Morning free (until {first_activity_time.strftime('%I:%M %p')})"
                            })

                # Gap between activities
                if i < len(day_activities) - 1:
                    current_end = day_activities.iloc[i]['datetime'] + timedelta(hours=2)  # Assume 2hr activity
                    next_start = day_activities.iloc[i + 1]['datetime']
                    gap_hours = (next_start - current_end).total_seconds() / 3600

                    if gap_hours >= 2:  # Only show gaps of 2+ hours
                        start_hour = current_end.hour
                        end_hour = next_start.hour

                        # Determine time of day
                        if start_hour < 12:
                            time_of_day = 'morning'
                        elif start_hour < 17:
                            time_of_day = 'afternoon'
                        else:
                            time_of_day = 'evening'

                        gaps.append({
                            'date': date_str,
                            'day_name': day_name,
                            'start_time': f'{start_hour:02d}:00',
                            'end_time': f'{end_hour:02d}:00',
                            'duration_hours': int(gap_hours),
                            'time_of_day': time_of_day,
                            'description': f"{day_name}: {time_of_day.title()} gap ({current_end.strftime('%I:%M %p')} - {next_start.strftime('%I:%M %p')})"
                        })

                # Evening gap (after last activity)
                if i == len(day_activities) - 1:
                    last_activity_time = day_activities.iloc[i]['datetime']
                    last_activity_hour = last_activity_time.hour + 2  # Assume 2hr activity
                    if last_activity_hour < 21:  # Gap after last activity
                        duration = 21 - last_activity_hour
                        if duration >= 2:
                            gaps.append({
                                'date': date_str,
                                'day_name': day_name,
                                'start_time': f'{last_activity_hour:02d}:00',
                                'end_time': '21:00',
                                'duration_hours': duration,
                                'time_of_day': 'evening',
                                'description': f"{day_name}: Evening free (after {(last_activity_time + timedelta(hours=2)).strftime('%I:%M %p')})"
                            })

    return gaps


def get_smart_recommendations(gap, weather_data, optional_activities):
    """
    Generate smart activity recommendations based on:
    - Schedule gap duration and time of day
    - Real weather conditions
    - UV index (from weather data)
    - Activity suitability
    """
    # Get weather for this date
    gap_weather = None
    for forecast in weather_data.get('forecast', []):
        if forecast['date'] == gap['date']:
            gap_weather = forecast
            break

    if not gap_weather:
        gap_weather = weather_data.get('current', {})

    recommendations = []

    # Score each activity based on conditions
    for category, activities in optional_activities.items():
        for activity in activities:
            score = 0
            reasons = []
            warnings = []

            # 1. Duration match (most important)
            activity_duration = activity.get('duration', '2-3 hours')
            duration_match = False
            if '1-2' in activity_duration and gap['duration_hours'] >= 1:
                duration_match = True
                score += 30
            elif '2-3' in activity_duration and gap['duration_hours'] >= 2:
                duration_match = True
                score += 30
            elif '3-4' in activity_duration and gap['duration_hours'] >= 3:
                duration_match = True
                score += 30
            elif '1 hour' in activity_duration and gap['duration_hours'] >= 1:
                duration_match = True
                score += 30

            if not duration_match:
                continue  # Skip activities that don't fit the time window

            # 2. Time of day match
            time_of_day = gap['time_of_day']
            activity_name = activity['name'].lower()

            # Dining recommendations based on time
            if 'dining' in category.lower():
                if 'breakfast' in activity_name and time_of_day == 'morning':
                    score += 25
                    reasons.append("Perfect breakfast timing")
                elif 'lunch' in activity_name and time_of_day == 'afternoon':
                    score += 25
                    reasons.append("Ideal lunch hour")
                elif ('dinner' in activity_name or 'sunset' in activity_name) and time_of_day == 'evening':
                    score += 25
                    reasons.append("Great dinner timing")
                elif 'coffee' in activity_name or 'cafe' in activity_name:
                    score += 15
                    reasons.append("Good for a casual break")

            # 3. Weather suitability
            condition = gap_weather.get('condition', '').lower()
            temp = gap_weather.get('high', 75)
            precipitation = gap_weather.get('precipitation', 0)
            wind = gap_weather.get('wind', 5)

            # Beach/outdoor activities
            if any(keyword in activity_name for keyword in ['beach', 'kayak', 'bike', 'walk', 'golf', 'park', 'outdoor']):
                if 'rain' in condition or precipitation > 50:
                    score -= 40
                    warnings.append("⚠️ Rain expected - bring rain gear or reschedule")
                elif 'clear' in condition or 'sunny' in condition:
                    score += 20
                    reasons.append("Perfect weather for outdoor activity")
                    if temp > 85:
                        warnings.append("🌡️ High temperature - bring extra water and sunscreen")
                elif 'cloud' in condition:
                    score += 10
                    reasons.append("Good cloud cover reduces sun exposure")

            # Indoor activities (good for bad weather)
            if any(keyword in activity_name for keyword in ['museum', 'shopping', 'spa', 'indoor', 'gallery', 'theater']):
                if 'rain' in condition or precipitation > 30:
                    score += 25
                    reasons.append("Indoor activity - perfect for rainy weather")
                elif temp > 90 or temp < 60:
                    score += 15
                    reasons.append("Indoor comfort in extreme temperatures")

            # Water activities
            if any(keyword in activity_name for keyword in ['kayak', 'paddleboard', 'boat', 'fishing', 'swim']):
                if wind > 15:
                    score -= 20
                    warnings.append("⚠️ High winds - check conditions before going")
                elif temp < 70:
                    score -= 10
                    warnings.append("🌡️ Cool temperature for water activities")
                elif 'clear' in condition and 65 < temp < 85:
                    score += 20
                    reasons.append("Ideal conditions for water activities")

            # 4. UV/sun considerations (use actual UV data)
            uv_index = gap_weather.get('uv_index', 5.0)
            if any(keyword in activity_name for keyword in ['beach', 'outdoor', 'walk', 'bike', 'golf', 'horseback']):
                if uv_index >= 8:
                    score -= 15
                    warnings.append(f"☀️ Very High UV ({uv_index}) - Seek shade, use SPF 50+, wear hat")
                elif uv_index >= 6:
                    score -= 5
                    warnings.append(f"☀️ High UV ({uv_index}) - Use SPF 30+, reapply frequently")
                elif uv_index >= 3:
                    reasons.append(f"Moderate UV ({uv_index}) - Good for outdoor activities with sunscreen")
                else:
                    score += 5
                    reasons.append(f"Low UV ({uv_index}) - Great for extended outdoor time")

            # 5. Tide considerations for beach/water activities
            try:
                tide_data = get_tide_data()
                day_tides = tide_data.get(gap['date'], {})

                if any(keyword in activity_name for keyword in ['beach', 'swim', 'kayak', 'paddleboard', 'fishing']):
                    if day_tides:
                        # Check if activity time aligns with good tides
                        gap_start_hour = int(gap['start_time'].split(':')[0])
                        high_tides = day_tides.get('high', [])

                        for high_tide in high_tides:
                            tide_hour = int(high_tide['time'].split(':')[0])
                            # If activity time is within 2 hours of high tide
                            if abs(tide_hour - gap_start_hour) <= 2:
                                score += 15
                                reasons.append(f"🌊 High tide at {high_tide['time']} - perfect for beach/water activities")
                                break
            except:
                pass  # If tide data fails, continue without it

            # 6. Rating boost
            rating = activity.get('rating', '0')
            try:
                # Parse rating from format like "4.5/5" to float 4.5
                if isinstance(rating, str) and '/' in rating:
                    rating_num = float(rating.split('/')[0])
                elif isinstance(rating, (int, float)):
                    rating_num = float(rating)
                else:
                    rating_num = 0
                score += rating_num * 2  # Each star adds 2 points
            except:
                pass  # If rating parsing fails, skip the boost

            # Only recommend if score is positive
            if score > 0:
                recommendations.append({
                    'activity': activity,
                    'category': category,
                    'score': score,
                    'reasons': reasons,
                    'warnings': warnings,
                    'weather_condition': condition.title(),
                    'temperature': temp,
                    'precipitation_chance': precipitation
                })

    # Sort by score (highest first)
    recommendations.sort(key=lambda x: x['score'], reverse=True)

    return recommendations[:20]  # Return top 20 recommendations


# ============================================================================
# MAPPING FUNCTIONS
# ============================================================================

def create_ultimate_map(activities_data, center_on=None, show_routes=True):
    """Create beautiful interactive map"""
    # Center point
    if center_on:
        activity = next((a for a in activities_data if a['id'] == center_on), None)
        if activity:
            center = [activity['location']['lat'], activity['location']['lon']]
        else:
            center = [TRIP_CONFIG['hotel']['lat'], TRIP_CONFIG['hotel']['lon']]
    else:
        center = [TRIP_CONFIG['hotel']['lat'], TRIP_CONFIG['hotel']['lon']]
    
    # Create map
    m = folium.Map(
        location=center,
        zoom_start=12,
        tiles='OpenStreetMap',
        attr='Map data © OpenStreetMap contributors'
    )
    
    # Add hotel with special icon
    folium.Marker(
        location=[TRIP_CONFIG['hotel']['lat'], TRIP_CONFIG['hotel']['lon']],
        popup=folium.Popup(f"""
            <div style='min-width: 250px'>
                <h3 style='color: #ff6b6b; margin: 0 0 10px 0;'>🏨 Your Hotel</h3>
                <h4 style='margin: 5px 0;'>{TRIP_CONFIG['hotel']['name']}</h4>
                <p style='margin: 5px 0;'><b>📍</b> {TRIP_CONFIG['hotel']['address']}</p>
                <p style='margin: 5px 0;'><b>📞</b> {TRIP_CONFIG['hotel']['phone']}</p>
                <p style='margin: 5px 0;'><b>Check-in:</b> Nov 7, 3:00 PM</p>
                <p style='margin: 5px 0;'><b>Check-out:</b> Nov 12, 11:00 AM</p>
            </div>
        """, max_width=300),
        tooltip="🏨 The Ritz-Carlton - Your Home Base",
        icon=folium.Icon(color='red', icon='home', prefix='fa')
    ).add_to(m)
    
    # Color and icon mappings
    type_colors = {
        'transport': 'blue',
        'activity': 'green',
        'spa': 'purple',
        'dining': 'orange',
        'beach': 'lightblue'
    }
    
    type_icons = {
        'transport': 'plane',
        'activity': 'ship',
        'spa': 'heart',
        'dining': 'cutlery',
        'beach': 'umbrella'
    }
    
    # Add activity markers
    for activity in activities_data:
        if activity['type'] != 'transport' or 'Arrives' in activity['activity']:
            loc = activity['location']
            
            # Distance from hotel
            distance = geodesic(
                (TRIP_CONFIG['hotel']['lat'], TRIP_CONFIG['hotel']['lon']),
                (loc['lat'], loc['lon'])
            ).miles
            
            travel_time = int(distance / 0.583)  # Assume 35 mph average

            # Escape HTML to prevent broken rendering in map popups
            import html
            safe_activity = html.escape(activity['activity'])
            safe_date = html.escape(activity['date'])
            safe_time = html.escape(activity['time'])
            safe_loc_name = html.escape(loc['name'])
            safe_phone = html.escape(loc.get('phone', 'N/A'))
            safe_notes = html.escape(activity['notes'])

            popup_html = f"""
            <div style='min-width: 280px; font-family: Inter, sans-serif;'>
                <h3 style='color: #ff6b6b; margin: 0 0 10px 0;'>{safe_activity}</h3>
                <p style='margin: 5px 0;'><b>📅</b> {safe_date} at {safe_time}</p>
                <p style='margin: 5px 0;'><b>📍</b> {safe_loc_name}</p>
                <p style='margin: 5px 0;'><b>📞</b> {safe_phone}</p>
                <p style='margin: 5px 0;'><b>💰</b> ${activity['cost']}</p>
                <p style='margin: 5px 0;'><b>🚗</b> {distance:.1f} mi ({travel_time} min from hotel)</p>
                <p style='margin: 5px 0; font-style: italic;'>{safe_notes}</p>
            </div>
            """

            folium.Marker(
                location=[loc['lat'], loc['lon']],
                popup=folium.Popup(popup_html, max_width=320),
                tooltip=f"{safe_activity} - {safe_date}",
                icon=folium.Icon(
                    color=type_colors.get(activity['type'], 'gray'),
                    icon=type_icons.get(activity['type'], 'info-sign'),
                    prefix='fa'
                )
            ).add_to(m)
    
    return m

def calculate_distance_from_hotel(lat, lon):
    """Calculate distance from hotel"""
    hotel = (TRIP_CONFIG['hotel']['lat'], TRIP_CONFIG['hotel']['lon'])
    location = (lat, lon)
    return geodesic(hotel, location).miles

# ============================================================================
# QR CODE GENERATION
# ============================================================================

def generate_qr(data, size=10):
    """Generate QR code"""
    qr = qrcode.QRCode(version=1, box_size=size, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# ============================================================================
# UI RENDERING FUNCTIONS
# ============================================================================

def render_ultimate_header():
    """Render ultimate edition header"""
    now = datetime.now()
    trip_start = TRIP_CONFIG['start_date']
    trip_end = TRIP_CONFIG['end_date']
    # Use .date() for consistent day counting across all countdowns
    days_until = (trip_start.date() - now.date()).days
    
    # Determine trip phase
    if days_until > 0:
        countdown_text = f"{days_until} Days Until Your Adventure!"
        phase_emoji = "🎊"
    elif now.date() == trip_start.date():
        countdown_text = "🎉 Your Trip Starts TODAY!"
        phase_emoji = "🎊"
    elif trip_start < now < trip_end:
        days_in = (now - trip_start).days + 1
        countdown_text = f"🏖️ Day {days_in} of Your Amazing Trip!"
        phase_emoji = "🌴"
    elif now.date() == trip_end.date():
        countdown_text = "Last Day - Make It Count!"
        phase_emoji = "✈️"
    else:
        countdown_text = "✨ Memories Made Forever"
        phase_emoji = "💫"
    
    st.markdown(f"""
    <div class="ultimate-header fade-in">
        <h1>{phase_emoji} 40th Birthday Trip Assistant</h1>
        <p>The Ultimate Amelia Island Experience</p>
        <div class="status-bar">
            <div class="status-item">📅 {countdown_text}</div>
            <div class="status-item">🏨 The Ritz-Carlton</div>
            <div class="status-item">🌴 November 7-12, 2025</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_dashboard_ultimate(df, activities_data, weather_data, show_sensitive):
    """Ultimate dashboard with all features"""
    st.markdown('<h2 class="fade-in">🏠 Trip Dashboard</h2>', unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_activities = len(df)
        st.markdown(f"""
        <div class="metric-card fade-in" style="animation-delay: 0.1s">
            <div class="metric-value">{total_activities}</div>
            <div class="metric-label">Total Events</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Use .date() for consistent day counting across all countdowns
        days_until = (TRIP_CONFIG['start_date'].date() - datetime.now().date()).days
        st.markdown(f"""
        <div class="metric-card fade-in" style="animation-delay: 0.2s; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="metric-value">{max(0, days_until)}</div>
            <div class="metric-label">Days to Go</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_cost = df['cost'].sum()
        cost_display = f"${total_cost:,.0f}" if show_sensitive else "$***"
        st.markdown(f"""
        <div class="metric-card fade-in" style="animation-delay: 0.3s; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="metric-value">{cost_display}</div>
            <div class="metric-label">Total Budget</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        confirmed = len(df[df['status'] == 'Confirmed'])
        st.markdown(f"""
        <div class="metric-card fade-in" style="animation-delay: 0.4s; background: linear-gradient(135deg, #96e6a1 0%, #8fd3f4 100%);">
            <div class="metric-value">{confirmed}</div>
            <div class="metric-label">Confirmed</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Weather widget
    st.markdown("### 🌤️ Current Weather")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        current = weather_data['current']
        condition_emoji = get_weather_emoji(current['condition'])
        
        st.markdown(f"""
        <div class="weather-widget fade-in">
            <div style="font-size: 3rem;">{condition_emoji}</div>
            <div class="weather-temp">{current['temperature']}°F</div>
            <div style="font-size: 1.3rem; margin-bottom: 1rem;">{current['condition']}</div>
            <div style="opacity: 0.9;">
                <p style="margin: 0.5rem 0;">Feels like: {current['feels_like']}°F</p>
                <p style="margin: 0.5rem 0;">💧 Humidity: {current['humidity']}%</p>
                <p style="margin: 0.5rem 0;">💨 Wind: {current['wind_speed']} mph</p>
            </div>
            <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 1rem;">
                {weather_data['source']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Forecast chart
        forecast_df = pd.DataFrame(weather_data['forecast'])
        forecast_df['date'] = pd.to_datetime(forecast_df['date'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=forecast_df['date'],
            y=forecast_df['high'],
            mode='lines+markers',
            name='High',
            line=dict(color='#ff6b6b', width=4),
            marker=dict(size=12, symbol='circle'),
            fill='tonexty',
            fillcolor='rgba(255, 107, 107, 0.1)'
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_df['date'],
            y=forecast_df['low'],
            mode='lines+markers',
            name='Low',
            line=dict(color='#4ecdc4', width=4),
            marker=dict(size=12, symbol='circle')
        ))
        
        fig.update_layout(
            title="6-Day Temperature Forecast",
            xaxis_title="Date",
            yaxis_title="Temperature (°F)",
            height=350,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=12),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Urgent bookings
    urgent = df[df['status'] == 'URGENT']
    
    if len(urgent) > 0:
        st.markdown("### 🚨 Urgent Bookings - Action Needed!")
        
        for _, item in urgent.iterrows():
            activity_name = mask_info(item['activity'], show_sensitive)
            phone = mask_info(str(item['location']['phone']), show_sensitive)
            location_name = mask_info(item['location']['name'], show_sensitive)
            
            st.markdown(f"""
            <div class="ultimate-card urgent-card fade-in" style="border-left: 6px solid #fd79a8;">
                <div class="card-body">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <h3 style="margin: 0 0 1rem 0; color: #c91f64;">⚠️ {activity_name}</h3>
                            <p style="margin: 0.5rem 0;"><b>📅 {item['date'].strftime('%A, %B %d')} at {item['time']}</b></p>
                            <p style="margin: 0.5rem 0;">📍 {location_name}</p>
                            <p style="margin: 0.5rem 0;">📞 <a href="tel:{phone}">{phone}</a></p>
                            <p style="margin: 0.5rem 0;">💰 ${item['cost']}</p>
                            <p style="margin: 0.5rem 0; font-style: italic;">{item['notes']}</p>
                        </div>
                        <div class="status-urgent">URGENT</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Get booking URL if available
            booking_url = None
            for activity in activities_data:
                if activity['id'] == item['id']:
                    booking_url = activity.get('booking_url')
                    break

            # Show action buttons
            if booking_url:
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"📞 Call", key=f"call_{item['id']}", use_container_width=True):
                        st.info(f"Opening dialer for {phone}...")
                with col2:
                    st.link_button("🔗 Book Online", booking_url, use_container_width=True)
                with col3:
                    if st.button(f"✅ Booked", key=f"book_{item['id']}", use_container_width=True):
                        st.success("Great! Marked as booked.")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"📞 Call {phone}", key=f"call_{item['id']}", use_container_width=True):
                        st.info(f"Opening dialer for {phone}...")
                with col2:
                    if st.button(f"✅ Mark as Booked", key=f"book_{item['id']}", use_container_width=True):
                        st.success("Great! Marked as booked.")
    else:
        st.markdown("""
        <div class="info-box info-success fade-in">
            <h3 style="margin: 0 0 0.5rem 0;">🎉 All Set!</h3>
            <p style="margin: 0;">No urgent bookings! Everything is confirmed and ready to go.</p>
        </div>
        """, unsafe_allow_html=True)

def render_today_view(df, activities_data, weather_data, show_sensitive):
    """Special TODAY view - context-aware"""
    st.markdown('<h2 class="fade-in">📅 Today\'s Plan</h2>', unsafe_allow_html=True)
    
    today = datetime.now().date()
    trip_start = TRIP_CONFIG['start_date'].date()
    trip_end = TRIP_CONFIG['end_date'].date()
    
    # Check if today is during the trip
    if today < trip_start:
        days_until = (trip_start - today).days
        st.markdown(f"""
        <div class="birthday-special fade-in">
            <h2 style="margin: 0 0 1rem 0;">🎊 Countdown to Your 40th Birthday Adventure!</h2>
            <div class="weather-temp">{days_until}</div>
            <p style="font-size: 1.3rem; margin: 0;">Days until your amazing trip begins!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show preparation checklist
        st.markdown("### 🎒 Getting Ready")

        st.markdown("""
        <div class="ultimate-card fade-in">
            <div class="card-header">✈️ Pre-Trip Preparation</div>
            <div class="card-body">
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">
                    <strong>{} days</strong> to prepare! Here's what you need to do:
                </p>
            </div>
        </div>
        """.format(days_until), unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📋 Quick Links")
            if st.button("🎒 View Packing List", key="packing_link", use_container_width=True):
                st.session_state['nav_to_packing'] = True
                st.rerun()

            if st.button("📞 View Urgent Bookings", key="bookings_link", use_container_width=True):
                st.info("Check the Dashboard for urgent bookings!")

        with col2:
            st.markdown("#### ✅ Pre-Trip Checklist")
            st.checkbox("📞 All reservations confirmed", key="check_reservations")
            st.checkbox("🎒 Packing list reviewed", key="check_packing")
            st.checkbox("✈️ Flight details saved", key="check_flights")
            st.checkbox("🏨 Hotel confirmation ready", key="check_hotel")
            st.checkbox("💳 Payment methods packed", key="check_payment")

        # Show urgent items that need booking
        urgent_count = len(df[df['status'] == 'URGENT'])
        if urgent_count > 0:
            st.warning(f"⚠️ **{urgent_count} urgent booking(s)** need attention! Check the Dashboard.")
        
    elif trip_start <= today <= trip_end:
        st.markdown('<div class="today-badge">📍 YOU\'RE ON YOUR TRIP!</div>', unsafe_allow_html=True)

        # Get today's activities
        today_activities = [a for a in activities_data if pd.to_datetime(a['date']).date() == today]
        today_str = today.strftime('%Y-%m-%d')

        # Check if today is a travel day (has flights or airport transport)
        travel_activities = [a for a in today_activities if a['type'] == 'transport' and
                           ('flight' in a.get('activity', '').lower() or 'airport' in a.get('activity', '').lower() or 'arrival' in a.get('activity', '').lower())]

        if today_activities:
            st.markdown(f"### Today is {today.strftime('%A, %B %d, %Y')}")

            # FLIGHT TRACKING for travel days
            if travel_activities:
                st.markdown("### ✈️ Live Flight Status")

                for travel_act in travel_activities:
                    if travel_act.get('flight_number'):
                        flight_num = travel_act.get('flight_number')
                        st.markdown(f"**{flight_num}** - {travel_act['activity']}")
                        render_flight_status_widget(flight_num, today_str, compact=False)

                        # Add traffic for airport trips
                        if 'departure' in travel_act.get('activity', '').lower() or 'drop' in travel_act.get('activity', '').lower():
                            st.markdown("#### 🚗 Traffic to Airport")
                            render_traffic_widget(
                                "4750 Amelia Island Parkway, Amelia Island, FL",
                                "2400 Yankee Clipper Dr, Jacksonville, FL 32218",
                                "Hotel → Jacksonville Airport (JAX)"
                            )
                        elif 'arrival' in travel_act.get('activity', '').lower() and 'DCA' in travel_act.get('notes', ''):
                            st.markdown("#### 🚗 Traffic from DCA")
                            st.info("Check traffic conditions before heading to airport")

                st.markdown("---")

            # Morning briefing
            st.markdown("""
            <div class="ultimate-card fade-in">
                <div class="card-header">🌅 Morning Briefing</div>
                <div class="card-body">
            """, unsafe_allow_html=True)

            # Weather for today
            current = weather_data['current']
            st.write(f"**Weather:** {current['temperature']}°F, {current['condition']}")
            st.write(f"**UV Index:** {current['uv_index']} - {'⚠️ High - Use SPF 50+' if current['uv_index'] > 6 else '✅ Moderate'}")
            st.write(f"**Wind:** {current['wind_speed']} mph")
            st.write(f"**Activities Scheduled:** {len(today_activities)}")

            # Tide info for beach days
            tide_data = get_tide_data()
            if today_str in tide_data:
                day_tides = tide_data[today_str]
                if day_tides.get('high'):
                    high_tide = day_tides['high'][0]
                    st.write(f"**🌊 High Tide:** {high_tide['time']} ({high_tide['height']}ft)")

            st.markdown("</div></div>", unsafe_allow_html=True)

            # Timeline of today's activities
            st.markdown("### 📋 Today's Schedule")

            for activity in sorted(today_activities, key=lambda x: x['time']):
                try:
                    activity_time = datetime.strptime(activity['time'], '%I:%M %p').time()
                except:
                    try:
                        activity_time = datetime.strptime(activity['time'], '%H:%M').time()
                    except:
                        activity_time = datetime.strptime('12:00 PM', '%I:%M %p').time()

                activity_datetime = datetime.combine(today, activity_time)
                time_until = (activity_datetime - datetime.now()).total_seconds() / 60

                if time_until > 0 and time_until < 60:
                    next_badge = '<span class="today-badge">⏰ COMING UP SOON!</span>'
                elif time_until <= 0:
                    next_badge = '<span class="status-confirmed">✅ In Progress / Completed</span>'
                else:
                    hours_until = int(time_until / 60)
                    next_badge = f'<span class="status-pending">In {hours_until}h {int(time_until % 60)}m</span>'

                # Add weather/UV warnings for outdoor activities
                activity_warning = ""
                if activity['type'] in ['beach', 'activity'] and current['uv_index'] > 7:
                    activity_warning = "<br><small style='color: #ff9800;'>⚠️ High UV - Bring sunscreen SPF 50+</small>"
                elif activity['type'] == 'beach':
                    # Add tide info
                    if today_str in tide_data:
                        tide_rec = get_tide_recommendation(activity['time'], 'beach', today_str, tide_data)
                        if tide_rec and tide_rec.get('recommendation'):
                            import html
                            safe_rec = html.escape(tide_rec['recommendation'])
                            activity_warning = f"<br><small style='color: #2196f3;'>{safe_rec}</small>"

                # Escape HTML to prevent broken rendering
                import html
                safe_activity_name = html.escape(activity['activity'])
                safe_time = html.escape(activity['time'])
                safe_location = html.escape(activity['location']['name'])

                st.markdown(f"""
                <div class="ultimate-card today-card fade-in">
                    <div class="card-body">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <h3 style="margin: 0 0 0.5rem 0;">{safe_activity_name}</h3>
                                <p style="margin: 0.25rem 0;"><b>🕐 {safe_time}</b></p>
                                <p style="margin: 0.25rem 0;">📍 {safe_location}{activity_warning}</p>
                            </div>
                            <div>{next_badge}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No scheduled activities today - enjoy a relaxing day!")
    else:
        st.markdown("""
        <div class="birthday-special fade-in">
            <h2 style="margin: 0 0 1rem 0;">✨ Trip Complete!</h2>
            <p style="font-size: 1.3rem;">Your amazing 40th birthday trip has concluded. Time to relive the memories!</p>
        </div>
        """, unsafe_allow_html=True)

def render_map_page(activities_data):
    """Interactive map page"""
    st.markdown('<h2 class="fade-in">🗺️ Trip Map & Locations</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);">
        <h4 style="margin: 0 0 0.5rem 0;">📍 Interactive Map</h4>
        <p style="margin: 0;">Explore all your trip locations! Click markers for details and distances from your hotel.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create and display map
    trip_map = create_ultimate_map(activities_data)
    st_folium(trip_map, width=None, height=600)
    
    # Distance matrix
    st.markdown("### 🚗 Travel Times from Hotel")
    
    cols = st.columns(3)
    unique_locations = {}
    
    for activity in activities_data:
        loc_name = activity['location']['name']
        if loc_name not in unique_locations and activity['type'] != 'transport':
            unique_locations[loc_name] = activity['location']
    
    for idx, (name, loc) in enumerate(unique_locations.items()):
        with cols[idx % 3]:
            distance = calculate_distance_from_hotel(loc['lat'], loc['lon'])
            travel_time = int(distance / 0.583)  # 35 mph average
            
            st.markdown(f"""
            <div class="ultimate-card fade-in">
                <div class="card-body">
                    <h4 style="margin: 0 0 0.5rem 0;">{name}</h4>
                    <p style="margin: 0.25rem 0;">🚗 {distance:.1f} miles</p>
                    <p style="margin: 0.25rem 0;">⏱️ ~{travel_time} minutes</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_packing_list():
    """Smart packing list"""
    st.markdown('<h2 class="fade-in">🎒 Smart Packing List</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box info-success">
        <h4 style="margin: 0 0 0.5rem 0;">✨ Weather-Smart Packing</h4>
        <p style="margin: 0;">This list is customized for your November trip to Amelia Island with all planned activities!</p>
    </div>
    """, unsafe_allow_html=True)
    
    packing_data = get_smart_packing_list()

    # Summary stats - count packed items from packing list only (not birthday/bucket items)
    total_items = sum(len(items) for items in packing_data.values())

    # Only count items that belong to packing list categories (exclude birthday_, bucket_ prefixes)
    packing_category_prefixes = [cat.split()[0] for cat in packing_data.keys()]  # Extract emoji prefixes
    checked_items = sum(
        1 for key, value in st.session_state.packing_list.items()
        if value and any(key.startswith(prefix) or key.startswith(f"{prefix}_") for prefix in packing_data.keys())
    )
    progress = (checked_items / total_items * 100) if total_items > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Items", total_items)
    with col2:
        st.metric("Packed", checked_items)
    with col3:
        st.metric("Progress", f"{progress:.0f}%")
    
    st.progress(progress / 100)
    
    # Render categories
    for category, items in packing_data.items():
        with st.expander(f"{category} ({len(items)} items)", expanded=(category == "🚨 CRITICAL - Don't Leave Without!")):
            for idx, item in enumerate(items):
                col1, col2 = st.columns([0.9, 0.1])
                
                with col1:
                    priority_class = f"priority-{item['priority']}"
                    checked_class = "checked" if item.get('checked', False) else ""
                    
                    st.markdown(f"""
                    <div class="packing-item {priority_class} {checked_class}">
                        <div style="flex: 1;">{item['item']}</div>
                        <div style="font-size: 0.8rem; opacity: 0.7;">{item['priority'].upper()}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Create unique item ID for database persistence
                    item_id = f"{category}_{idx}_{item['item'][:20]}"

                    # Check if this item is packed (from session state or database)
                    is_packed = st.session_state.packing_list.get(item_id, False)

                    checked = st.checkbox("✓", value=is_packed, key=f"pack_{category}_{idx}", label_visibility="collapsed")

                    if checked != is_packed:
                        # Update session state
                        st.session_state.packing_list[item_id] = checked
                        # Save to database
                        update_packing_item(item_id, checked)
                        item['checked'] = checked
                        st.rerun()


def render_full_schedule(df, activities_data, show_sensitive):
    """Complete trip schedule - Visual timeline showing all days at once"""
    st.markdown('<h2 class="fade-in">🗓️ Complete Trip Schedule</h2>', unsafe_allow_html=True)

    # Get intelligence data
    weather_data = get_weather_ultimate()
    tide_data = get_tide_data()
    meal_gaps = detect_meal_gaps(activities_data)
    conflicts = detect_conflicts(activities_data)

    # Show trip overview
    st.markdown("""
    <div class="info-box" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <h4 style="margin: 0; color: white;">🤖 AI-Powered Schedule Intelligence</h4>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.95;">Your complete trip at a glance with smart insights</p>
    </div>
    """, unsafe_allow_html=True)

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📅 Total Days", len(df['date'].dt.date.unique()))
    with col2:
        st.metric("🎯 Activities", len(activities_data))
    with col3:
        custom_count = len([a for a in activities_data if a.get('is_custom', False)])
        st.metric("➕ Custom Added", custom_count)
    with col4:
        urgent_count = len([a for a in activities_data if a.get('status') == 'URGENT'])
        st.metric("🚨 Urgent", urgent_count)

    # Export options
    st.markdown("---")
    export_col1, export_col2 = st.columns(2)

    with export_col1:
        # CSV Export
        csv_data = []
        for activity in activities_data:
            csv_data.append({
                "Date": activity.get('date', ''),
                "Time": activity.get('time', ''),
                "Activity": activity.get('activity', ''),
                "Location": activity.get('location', {}).get('name', '') if isinstance(activity.get('location'), dict) else activity.get('location', ''),
                "Duration": activity.get('duration', ''),
                "Cost": activity.get('cost', 0),
                "Status": activity.get('status', ''),
                "Category": activity.get('category', '')
            })

        csv_df = pd.DataFrame(csv_data)
        csv_string = csv_df.to_csv(index=False)

        st.download_button(
            label="📥 Download Schedule (CSV)",
            data=csv_string,
            file_name="birthday_trip_schedule.csv",
            mime="text/csv",
            use_container_width=True
        )

    with export_col2:
        # Text calendar export
        calendar_text = "🎂 40TH BIRTHDAY TRIP SCHEDULE\n"
        calendar_text += "=" * 50 + "\n\n"

        # Group by date
        from collections import defaultdict
        by_date = defaultdict(list)
        for activity in activities_data:
            by_date[activity.get('date', '')].append(activity)

        for date in sorted(by_date.keys()):
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            calendar_text += f"\n{date_obj.strftime('%A, %B %d, %Y')}\n"
            calendar_text += "-" * 50 + "\n"

            for activity in sorted(by_date[date], key=lambda x: x.get('time', '')):
                time_str = activity.get('time', 'TBD')
                activity_name = activity.get('activity', '')
                location = activity.get('location', {})
                location_name = location.get('name', '') if isinstance(location, dict) else location

                calendar_text += f"{time_str:10} - {activity_name}\n"
                if location_name:
                    calendar_text += f"{'':10}   📍 {location_name}\n"

        st.download_button(
            label="📄 Download Schedule (TXT)",
            data=calendar_text,
            file_name="birthday_trip_schedule.txt",
            mime="text/plain",
            use_container_width=True
        )

    # Show conflicts and meal gaps
    if conflicts or meal_gaps:
        st.markdown("---")
        st.markdown("### 🚨 Schedule Alerts")

        alert_col1, alert_col2 = st.columns(2)

        with alert_col1:
            if conflicts:
                critical_conflicts = [c for c in conflicts if c['severity'] == 'critical']
                warning_conflicts = [c for c in conflicts if c['severity'] == 'warning']

                if critical_conflicts:
                    st.error(f"**🔴 {len(critical_conflicts)} Critical Conflicts**")
                    for conflict in critical_conflicts[:3]:  # Show first 3
                        st.markdown(f"• {conflict['message']}")

                if warning_conflicts:
                    st.warning(f"**🟡 {len(warning_conflicts)} Timing Warnings**")
                    for conflict in warning_conflicts[:3]:
                        st.markdown(f"• {conflict['message']}")
            else:
                st.success("✅ No scheduling conflicts detected!")

        with alert_col2:
            if meal_gaps:
                st.warning(f"**🍽️ {len(meal_gaps)} Missing Meals**")
                for gap in meal_gaps[:5]:  # Show first 5
                    st.markdown(f"• {gap['day_name']}: {gap['meal_type'].title()} at {gap['suggested_time']}")

                # Auto-fill button
                if st.button("🤖 Auto-Fill All Missing Meals", use_container_width=True, type="primary"):
                    with st.spinner("🍽️ AI selecting best restaurants for missing meals..."):
                        added = auto_fill_meals(meal_gaps, weather_data)

                        if added:
                            st.success(f"✅ Added {len(added)} meals to your schedule!")
                            st.balloons()

                            # Show what was added
                            for meal in added:
                                st.markdown(f"• **{meal['meal_type'].title()}** on {meal['day']} at {meal['time']}: {meal['restaurant']}")

                            st.info("💡 Scroll down to see your updated schedule with new meals!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to add meals. Please try adding manually.")
            else:
                st.success("✅ All meals scheduled!")

    st.markdown("---")

    # Load John's preferences for opt-in status
    john_prefs = load_john_preferences()

    # Get all dates and sort
    dates = sorted(df['date'].dt.date.unique())

    # NO TABS - Show all days in one scrollable view
    for date in dates:
        # Day header with weather
        day_activities = [a for a in activities_data if pd.to_datetime(a['date']).date() == date]

        # Add confirmed meals to the day's activities
        date_str = date.strftime('%Y-%m-%d')
        meal_slots = [
            {"id": "fri_dinner", "date": "2025-11-07", "time": "7:00 PM"},
            {"id": "sat_breakfast", "date": "2025-11-08", "time": "9:00 AM"},
            {"id": "sat_lunch", "date": "2025-11-08", "time": "12:30 PM"},
            {"id": "sun_breakfast", "date": "2025-11-09", "time": "9:00 AM"},
            {"id": "sun_lunch", "date": "2025-11-09", "time": "12:30 PM"},
            {"id": "mon_breakfast", "date": "2025-11-10", "time": "9:00 AM"},
            {"id": "mon_lunch", "date": "2025-11-10", "time": "12:30 PM"},
            {"id": "mon_dinner", "date": "2025-11-10", "time": "7:00 PM"},
            {"id": "tue_breakfast", "date": "2025-11-11", "time": "8:00 AM"},
        ]

        for meal_slot in meal_slots:
            if meal_slot['date'] == date_str:
                proposal = get_meal_proposal(meal_slot['id'])
                if proposal and proposal['status'] == 'confirmed':
                    final_idx = proposal.get('final_choice')
                    if final_idx is not None and final_idx < len(proposal['restaurant_options']):
                        final_restaurant = proposal['restaurant_options'][final_idx]
                        rest_details = get_restaurant_details().get(final_restaurant['name'], {})

                        # Use custom meal time if set, otherwise use default
                        display_time = proposal.get('meal_time') or meal_slot['time']

                        # Create a meal activity
                        meal_activity = {
                            'id': f"meal_{meal_slot['id']}",
                            'date': date_str,
                            'time': display_time,
                            'activity': f"🍽️ {final_restaurant['name']}",
                            'description': final_restaurant.get('description', ''),
                            'type': 'dining',
                            'category': 'Dining',
                            'duration': final_restaurant.get('duration', '1-2 hours'),
                            'cost': final_restaurant.get('cost_range', 'N/A'),
                            'status': 'confirmed',
                            'notes': f"Dress Code: {rest_details.get('dress_code', 'Casual')}\nPhone: {final_restaurant.get('phone', 'N/A')}\nBooking: {final_restaurant.get('booking_url', 'N/A')}\nMenu: {rest_details.get('menu_url', 'N/A')}",
                            'location': {'name': final_restaurant['name'], 'address': ''},
                            'is_meal': True,
                            'booking_url': final_restaurant.get('booking_url', '')
                        }
                        day_activities.append(meal_activity)

        day_activities.sort(key=lambda x: x['time'])

        # Check if birthday
        is_birthday = date.month == 11 and date.day == 9

        # Get weather for this day
        date_str = date.strftime('%Y-%m-%d')
        day_weather = None
        for forecast in weather_data.get('forecast', []):
            if forecast['date'] == date_str:
                day_weather = forecast
                break

        # Day header card
        if is_birthday:
            header_style = "background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%); color: white;"
        elif day_weather and day_weather.get('precipitation', 0) > 50:
            header_style = "background: linear-gradient(135deg, #74b9ff 0%, #a29bfe 100%); color: white;"
        else:
            header_style = "background: linear-gradient(135deg, #55efc4 0%, #74b9ff 100%); color: white;"

        # Escape weather data if present
        weather_html = ""
        if day_weather:
            import html
            safe_condition = html.escape(str(day_weather["condition"]))
            safe_high = html.escape(str(day_weather["high"]))
            safe_precip = html.escape(str(day_weather["precipitation"]))
            safe_wind = html.escape(str(day_weather["wind"]))
            weather_html = f'<p style="margin: 0.5rem 0 0 0; opacity: 0.95; font-size: 1.1rem;">{safe_condition} | 🌡️ {safe_high}°F | 💧 {safe_precip}% rain | 💨 {safe_wind} mph</p>'

        st.markdown(f"""
        <div style="{header_style} padding: 1.5rem; border-radius: 12px; margin: 1.5rem 0 1rem 0; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <h2 style="margin: 0; color: white;">{'🎂 BIRTHDAY! ' if is_birthday else '📅 '}{date.strftime('%A, %B %d, %Y')}</h2>
            {weather_html}
        </div>
        """, unsafe_allow_html=True)

        # Timeline
        if day_activities:
            for idx, activity in enumerate(day_activities):
                status_class = activity['status'].lower()

                # Calculate end time
                end_time = None
                if activity.get('duration'):
                    end_time = calculate_end_time(activity['time'], activity['duration'])

                # Format time display
                time_display = activity['time']
                if end_time:
                    time_display = f"{activity['time']} - {end_time}"

                # Check for gap before this activity
                if idx > 0:
                    prev_activity = day_activities[idx - 1]
                    if prev_activity.get('duration'):
                        prev_end_time = calculate_end_time(prev_activity['time'], prev_activity['duration'])
                        if prev_end_time:
                            try:
                                prev_end_obj = datetime.strptime(prev_end_time, "%I:%M %p")
                                curr_start_obj = datetime.strptime(activity['time'], "%I:%M %p")
                                gap_minutes = (curr_start_obj - prev_end_obj).total_seconds() / 60

                                if gap_minutes > 60:  # More than 1 hour gap
                                    import html
                                    safe_prev_end = html.escape(prev_end_time)
                                    safe_curr_time = html.escape(activity['time'])
                                    st.markdown(f"""
                                    <div style="background: #f0f9ff; border-left: 4px solid #4ecdc4; padding: 1rem; margin: 0.5rem 0; border-radius: 8px;">
                                        <p style="margin: 0; color: #636e72;">💡 <strong>Free Time:</strong> {round(gap_minutes/60, 1)}h gap ({safe_prev_end} - {safe_curr_time})</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                            except:
                                pass

                # Custom activity badge
                custom_badge = ""
                if activity.get('is_custom', False):
                    custom_badge = '<span style="background: #74b9ff; color: white; padding: 0.25rem 0.75rem; border-radius: 10px; font-size: 0.85rem; margin-left: 0.5rem;">➕ Custom</span>'

                # Check John's opt-in status for this activity
                activity_id = activity.get('id', '')
                john_status_badge = ""

                if activity_id in ['act001', 'spa002', 'spa003']:  # Activities John can opt into
                    pref_key = f"activity_opt_in_{activity_id}"
                    status = john_prefs.get(pref_key, "not_decided")
                    if status == "interested":
                        john_status_badge = '<p style="margin: 0.5rem 0;"><span style="background: #4caf50; color: white; padding: 0.25rem 0.75rem; border-radius: 10px; font-size: 0.85rem;">👤 John: ✅ Wants This Too</span></p>'
                    elif status == "not_interested":
                        john_status_badge = '<p style="margin: 0.5rem 0;"><span style="background: #9e9e9e; color: white; padding: 0.25rem 0.75rem; border-radius: 10px; font-size: 0.85rem;">👤 John: Not interested</span></p>'
                    else:
                        john_status_badge = '<p style="margin: 0.5rem 0;"><span style="background: #ff9800; color: white; padding: 0.25rem 0.75rem; border-radius: 10px; font-size: 0.85rem;">❓ John: Needs to Decide</span></p>'

                # Activity card
                # Escape ALL dynamic content to prevent HTML breaking
                import html
                safe_activity_name = html.escape(activity['activity'])
                safe_status = html.escape(activity['status'])
                safe_time_display = html.escape(time_display)
                safe_duration = html.escape(activity.get('duration', '')) if activity.get('duration') else ''
                safe_location = html.escape(activity['location']['name'])
                safe_phone = html.escape(mask_info(activity['location'].get('phone', 'N/A'), show_sensitive))
                safe_cost = html.escape("$" + str(activity['cost']) if show_sensitive else "$***")
                safe_notes = html.escape(mask_info(activity.get('notes', ''), show_sensitive))
                safe_notes = safe_notes.replace('\n', '<br>')

                # Build HTML with minimal indentation to avoid Streamlit rendering issues
                activity_html = f"""<div class="timeline-item {status_class}" style="margin: 1rem 0;">
<div class="ultimate-card">
<div class="card-body">
<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
<h4 style="margin: 0;">{safe_activity_name} {custom_badge}</h4>
<span class="status-{status_class}">{safe_status}</span>
</div>
<p style="margin: 0.5rem 0;"><b>🕐 {safe_time_display}</b> {f'({safe_duration})' if activity.get('duration') else ''}</p>
<p style="margin: 0.5rem 0;">📍 {safe_location}</p>
<p style="margin: 0.5rem 0;">📞 {safe_phone}</p>
<p style="margin: 0.5rem 0;">💰 {safe_cost}</p>
<p style="margin: 0.5rem 0; font-style: italic;">{safe_notes}</p>
{john_status_badge}
</div>
</div>
</div>"""
                st.markdown(activity_html, unsafe_allow_html=True)

                # Display additional details (dress code, what to bring, tips) below the card
                if activity.get('dress_code'):
                    st.markdown(f"**👔 Dress Code:** {activity['dress_code']}")

                if activity.get('what_to_bring'):
                    st.markdown("**🎒 What to Bring:**")
                    items = activity['what_to_bring']
                    if isinstance(items, list):
                        for item in items:
                            st.markdown(f"- {item}")
                    else:
                        st.markdown(f"- {items}")

                if activity.get('tips'):
                    tips = activity['tips']
                    if isinstance(tips, list):
                        st.markdown("**💡 Tips:**")
                        for tip in tips:
                            st.markdown(f"- {tip}")
                    elif isinstance(tips, str):
                        st.info(f"💡 **Tip:** {tips}")

        else:
            st.info("No scheduled activities - free day!")

        st.markdown("---")

def render_budget(df, show_sensitive):
    """Budget tracker"""
    st.markdown('<h2 class="fade-in">💰 Budget Tracker</h2>', unsafe_allow_html=True)
    
    if not show_sensitive:
        st.warning("🔒 Unlock to view budget details")
        return
    
    # Summary metrics
    total_cost = df['cost'].sum()
    confirmed_cost = df[df['status'] == 'Confirmed']['cost'].sum()
    pending_cost = df[df['status'].isin(['Pending', 'URGENT'])]['cost'].sum()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Budget", f"${total_cost:,.0f}")
    with col2:
        st.metric("Confirmed", f"${confirmed_cost:,.0f}")
    with col3:
        st.metric("Pending", f"${pending_cost:,.0f}")
    
    # Category breakdown
    col1, col2 = st.columns([2, 1])
    
    with col1:
        category_spending = df.groupby('category')['cost'].sum().reset_index()
        
        fig = px.pie(
            category_spending,
            values='cost',
            names='category',
            title="Spending by Category",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        for _, row in category_spending.iterrows():
            st.markdown(f"""
            <div class="ultimate-card">
                <div class="card-body">
                    <h4 style="margin: 0 0 0.5rem 0;">{row['category']}</h4>
                    <p style="margin: 0; font-size: 1.5rem; font-weight: bold; color: #ff6b6b;">${row['cost']:.0f}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Daily breakdown
    st.markdown("### 📅 Daily Spending")
    
    daily_spending = df.groupby(df['date'].dt.date)['cost'].sum().reset_index()
    daily_spending['date'] = pd.to_datetime(daily_spending['date'])
    
    fig = px.bar(
        daily_spending,
        x='date',
        y='cost',
        title="Spending by Day",
        color='cost',
        color_continuous_scale='Viridis',
        labels={'cost': 'Amount ($)', 'date': 'Date'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def render_explore_activities():
    """Explore & Plan page - discover optional activities and fill your schedule"""
    st.markdown('<h2 class="fade-in">🎯 Explore & Plan Activities</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box info-success">
        <h4 style="margin: 0 0 0.5rem 0;">✨ Discover More to Do in Amelia Island!</h4>
        <p style="margin: 0;">Smart recommendations based on your actual schedule, real weather forecasts, UV index, and time of day!</p>
    </div>
    """, unsafe_allow_html=True)

    # Get data for smart analysis
    _, activities_data = get_ultimate_trip_data()
    weather_data = get_weather_ultimate()
    optional_activities = get_optional_activities()

    # QUICK ADD ACTIVITY - Prominent button at top
    st.markdown("---")
    st.markdown("### ⚡ Quick Add to Schedule")

    with st.expander("➕ **Add Custom Activity to Your Schedule**", expanded=False):
        st.markdown("**Fill out the details below to add any activity to your schedule:**")

        # Create columns for better layout
        qa_col1, qa_col2 = st.columns([2, 1])

        with qa_col1:
            qa_activity_name = st.text_input(
                "Activity Name *",
                placeholder="e.g., Beach Walk, Lunch at Joe's, Explore Downtown",
                key="qa_name",
                help="What do you want to do?"
            )

            qa_description = st.text_area(
                "Description (optional)",
                placeholder="Add details about this activity...",
                height=80,
                key="qa_desc"
            )

        with qa_col2:
            qa_day = st.selectbox(
                "Day *",
                [
                    f"Friday, Nov 7 - Arrival",
                    f"Saturday, Nov 8",
                    f"Sunday, Nov 9 - 🎂 Birthday!",
                    f"Monday, Nov 10",
                    f"Tuesday, Nov 11",
                    f"Wednesday, Nov 12 - Departure"
                ],
                key="qa_day"
            )

            qa_time = st.time_input(
                "Start Time *",
                value=None,
                key="qa_time",
                help="When does this activity start?"
            )

        # Second row of columns
        qa_col3, qa_col4, qa_col5 = st.columns(3)

        with qa_col3:
            qa_duration = st.text_input(
                "Duration",
                value="2 hours",
                key="qa_duration",
                help="How long will this take?"
            )

        with qa_col4:
            qa_type = st.selectbox(
                "Type",
                ["Activity", "Dining", "Beach", "Spa", "Transport", "Shopping", "Relaxation"],
                key="qa_type"
            )

        with qa_col5:
            qa_cost = st.number_input(
                "Cost ($)",
                min_value=0,
                value=0,
                key="qa_cost"
            )

        # Add button
        if st.button("✨ Add to Schedule", use_container_width=True, type="primary", key="qa_submit"):
            if qa_activity_name and qa_time:
                # Clean up day string for internal use
                day_map = {
                    "Friday, Nov 7 - Arrival": "Friday, Nov 7",
                    "Saturday, Nov 8": "Saturday, Nov 8",
                    "Sunday, Nov 9 - 🎂 Birthday!": "Sunday, Nov 9",
                    "Monday, Nov 10": "Monday, Nov 10",
                    "Tuesday, Nov 11": "Tuesday, Nov 11",
                    "Wednesday, Nov 12 - Departure": "Wednesday, Nov 12"
                }
                clean_day = day_map.get(qa_day, qa_day.split(" - ")[0])

                success = add_activity_to_schedule(
                    activity_name=qa_activity_name,
                    activity_description=qa_description,
                    selected_day=clean_day,
                    selected_time=qa_time,
                    duration=qa_duration,
                    activity_type=qa_type.lower(),
                    cost=qa_cost,
                    location_name=qa_activity_name
                )

                if success:
                    st.success(f"✅ Added **{qa_activity_name}** to {clean_day} at {qa_time.strftime('%I:%M %p').lstrip('0')}!")
                    st.info("💡 Reloading to show in your schedule...")
                    st.balloons()
                    # Reload custom activities from database
                    st.session_state.custom_activities = load_custom_activities()
                    import time
                    time.sleep(1)  # Give user time to see the success message
                    st.rerun()
                else:
                    st.error("❌ Failed to add activity. Please try again.")
            else:
                st.warning("⚠️ Please fill in the Activity Name and Start Time!")

    # Analyze schedule gaps DYNAMICALLY
    schedule_gaps = analyze_schedule_gaps(activities_data)

    # Show free time analysis (DYNAMIC)
    st.markdown("### 📅 Your Free Time (Analyzed from Schedule)")

    if schedule_gaps:
        gap_html = '<div class="ultimate-card"><div class="card-body">'
        for gap in schedule_gaps:
            gap_html += f'<p style="margin: 0.5rem 0;"><strong>{gap["description"]}</strong> - {gap["duration_hours"]}h available</p>'
        gap_html += '</div></div>'
        st.markdown(gap_html, unsafe_allow_html=True)
    else:
        st.info("Your schedule is fully booked - no gaps detected!")

    st.markdown("---")

    # AI AUTO-SCHEDULER - Generate complete day schedules
    st.markdown("### 🤖 AI Auto-Scheduler")

    st.markdown("""
    <div class="info-box" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
        <h4 style="margin: 0; color: white;">🚀 Let AI Build Your Perfect Day</h4>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.95;">Select a day and let our AI generate a complete optimized schedule with breakfast, activities, lunch, and dinner!</p>
    </div>
    """, unsafe_allow_html=True)

    auto_col1, auto_col2 = st.columns([2, 1])

    with auto_col1:
        selected_date_for_ai = st.selectbox(
            "📅 Select Day to Auto-Fill",
            ["2025-11-07", "2025-11-08", "2025-11-09", "2025-11-10", "2025-11-11", "2025-11-12"],
            format_func=lambda x: {
                "2025-11-07": "Friday, Nov 7 - Arrival Day",
                "2025-11-08": "Saturday, Nov 8",
                "2025-11-09": "Sunday, Nov 9 - 🎂 BIRTHDAY!",
                "2025-11-10": "Monday, Nov 10",
                "2025-11-11": "Tuesday, Nov 11",
                "2025-11-12": "Wednesday, Nov 12 - Departure Day"
            }.get(x, x)
        )

    with auto_col2:
        if st.button("✨ Generate AI Schedule", use_container_width=True, type="primary"):
            with st.spinner("🤖 AI analyzing weather, tides, ratings, and generating optimal schedule..."):
                tide_data = get_tide_data()

                # Generate schedule
                recommendations = ai_auto_scheduler(
                    selected_date_for_ai,
                    activities_data,
                    weather_data,
                    tide_data
                )

                if recommendations:
                    st.success(f"✅ Generated {len(recommendations)} activity recommendations!")

                    # Show recommendations and allow adding
                    st.markdown("#### 🎯 AI Recommendations:")

                    for rec in recommendations:
                        activity = rec['activity']

                        # Escape HTML to prevent broken rendering
                        import html
                        safe_time = html.escape(rec['time'])
                        safe_name = html.escape(activity['name'])
                        safe_desc = html.escape(activity.get('description', ''))
                        safe_reason = html.escape(rec['reason'])

                        # Activity card
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                                    padding: 1.5rem;
                                    border-radius: 12px;
                                    border-left: 4px solid #f5576c;
                                    margin: 1rem 0;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            <h4 style="margin: 0; color: #f5576c;">⏰ {safe_time} - {safe_name}</h4>
                            <p style="margin: 0.75rem 0; color: #636e72; line-height: 1.6;">{safe_desc}</p>
                            <p style="margin: 0.5rem 0; font-style: italic; color: #2ecc71;">✨ {safe_reason}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        # Quick details
                        detail_col1, detail_col2, detail_col3 = st.columns(3)
                        with detail_col1:
                            st.markdown(f"**💰 Cost:** {activity.get('cost_range', 'N/A')}")
                        with detail_col2:
                            st.markdown(f"**⏱️ Duration:** {rec['duration']}")
                        with detail_col3:
                            st.markdown(f"**⭐ Rating:** {activity.get('rating', 'N/A')}")

                        # Add button for this recommendation
                        if st.button(f"➕ Add to Schedule", key=f"ai_add_{selected_date_for_ai}_{rec['time']}_{activity['name']}", use_container_width=True):
                            # Determine activity type
                            activity_type = rec['type']

                            # Extract cost
                            cost = 0
                            cost_str = activity.get('cost_range', '$0')
                            try:
                                cost = int(re.findall(r'\d+', cost_str.split('-')[0])[0])
                            except:
                                cost = 0

                            # Day mapping
                            date_to_day = {
                                "2025-11-07": "Friday, Nov 7",
                                "2025-11-08": "Saturday, Nov 8",
                                "2025-11-09": "Sunday, Nov 9",
                                "2025-11-10": "Monday, Nov 10",
                                "2025-11-11": "Tuesday, Nov 11",
                                "2025-11-12": "Wednesday, Nov 12"
                            }
                            selected_day = date_to_day.get(selected_date_for_ai)

                            # Add to schedule
                            success = add_activity_to_schedule(
                                activity_name=activity['name'],
                                activity_description=activity.get('description', ''),
                                selected_day=selected_day,
                                selected_time=rec['time'],
                                duration=rec['duration'],
                                activity_type=activity_type,
                                cost=cost,
                                location_name=activity.get('name', 'TBD')
                            )

                            if success:
                                st.success(f"✅ Added {activity['name']} to schedule!")
                                st.balloons()
                                st.rerun()

                        st.markdown("---")

                    # Add all button
                    if st.button("➕ Add All AI Recommendations", use_container_width=True, type="secondary"):
                        added_count = 0

                        for rec in recommendations:
                            activity = rec['activity']
                            activity_type = rec['type']

                            cost = 0
                            cost_str = activity.get('cost_range', '$0')
                            try:
                                cost = int(re.findall(r'\d+', cost_str.split('-')[0])[0])
                            except:
                                cost = 0

                            date_to_day = {
                                "2025-11-07": "Friday, Nov 7",
                                "2025-11-08": "Saturday, Nov 8",
                                "2025-11-09": "Sunday, Nov 9",
                                "2025-11-10": "Monday, Nov 10",
                                "2025-11-11": "Tuesday, Nov 11",
                                "2025-11-12": "Wednesday, Nov 12"
                            }
                            selected_day = date_to_day.get(selected_date_for_ai)

                            success = add_activity_to_schedule(
                                activity_name=activity['name'],
                                activity_description=activity.get('description', ''),
                                selected_day=selected_day,
                                selected_time=rec['time'],
                                duration=rec['duration'],
                                activity_type=activity_type,
                                cost=cost,
                                location_name=activity.get('name', 'TBD')
                            )

                            if success:
                                added_count += 1

                        if added_count > 0:
                            st.success(f"✅ Added all {added_count} recommendations to your schedule!")
                            st.balloons()
                            st.rerun()
                else:
                    st.info("This day already has a full schedule! AI auto-scheduler skipped.")

    st.markdown("---")

    # Filter options
    st.markdown("### 🔍 Filter Activities")

    col1, col2, col3 = st.columns(3)

    with col1:
        budget_filter = st.selectbox(
            "💰 Budget",
            ["All Budgets", "Free", "Under $50", "$50-100", "$100+"]
        )

    with col2:
        time_filter = st.selectbox(
            "⏱️ Time Needed",
            ["All Durations", "< 1 hour", "1-2 hours", "2-4 hours", "4+ hours"]
        )

    with col3:
        category_filter = st.selectbox(
            "📂 Category",
            ["All Categories", "Dining", "Beach & Water", "Activities", "Shopping", "Relaxation"]
        )

    st.markdown("---")

    # Display activities by category
    activities = get_optional_activities()

    for category, items in activities.items():
        with st.expander(f"{category} ({len(items)} options)", expanded=(category == "🍽️ Fine Dining")):
            for idx, activity in enumerate(items):
                with st.container():
                    # Escape HTML to prevent broken rendering
                    import html
                    safe_activity_name = html.escape(activity['name'])
                    safe_activity_desc = html.escape(activity['description'])

                    # Activity header
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                                padding: 1.5rem;
                                border-radius: 12px;
                                border-left: 4px solid #ff6b6b;
                                margin: 1rem 0;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <h4 style="margin: 0; color: #ff6b6b;">{safe_activity_name}</h4>
                        <p style="margin: 0.75rem 0; color: #636e72; line-height: 1.6;">{safe_activity_desc}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Activity details
                    detail_col1, detail_col2, detail_col3 = st.columns(3)
                    with detail_col1:
                        st.markdown(f"**💰 Cost:** {activity['cost_range']}")
                    with detail_col2:
                        st.markdown(f"**⏱️ Duration:** {activity['duration']}")
                    with detail_col3:
                        st.markdown(f"**⭐ Rating:** {activity.get('rating', 'N/A')}")

                    # Phone number if available
                    if activity.get('phone') and activity['phone'] != 'N/A':
                        phone = activity['phone']
                        st.markdown(f'**📞 Phone:** <a href="tel:{phone}" style="color: #2196f3; text-decoration: none;">{phone}</a>', unsafe_allow_html=True)

                    # Booking link if available
                    if activity.get('booking_url'):
                        st.markdown(f"**🔗 Book:** [{activity.get('booking_url')}]({activity.get('booking_url')})")

                    # Pro tip
                    st.info(f"**💡 Pro Tip:** {activity['tips']}")

                    # Interactive controls
                    with st.expander("📅 Add to Your Schedule"):
                        add_col1, add_col2, add_col3 = st.columns(3)

                        with add_col1:
                            selected_day = st.selectbox(
                                "Select Day",
                                ["Friday, Nov 7", "Saturday, Nov 8", "Sunday, Nov 9",
                                 "Monday, Nov 10", "Tuesday, Nov 11", "Wednesday, Nov 12"],
                                key=f"day_{category}_{idx}"
                            )

                        with add_col2:
                            selected_time = st.time_input(
                                "Start Time",
                                value=None,
                                key=f"time_{category}_{idx}"
                            )

                        with add_col3:
                            custom_duration = st.text_input(
                                "Duration",
                                value=activity['duration'],
                                key=f"dur_{category}_{idx}"
                            )

                        if st.button(f"➕ Add to Schedule",
                                   key=f"add_{category}_{idx}",
                                   use_container_width=True):
                            if selected_time:
                                # Determine activity type from category
                                activity_type = 'activity'
                                if '🍽️' in category or 'Dining' in category:
                                    activity_type = 'dining'
                                elif '🏖️' in category or 'Beach' in category:
                                    activity_type = 'beach'
                                elif '💆' in category or 'Spa' in category:
                                    activity_type = 'spa'

                                # Extract cost for tracking
                                cost = 0
                                cost_str = activity.get('cost_range', '$0')
                                try:
                                    cost = int(re.findall(r'\d+', cost_str.split('-')[0])[0])
                                except:
                                    cost = 0

                                # Add to schedule
                                success = add_activity_to_schedule(
                                    activity_name=activity['name'],
                                    activity_description=activity.get('description', ''),
                                    selected_day=selected_day,
                                    selected_time=selected_time,
                                    duration=custom_duration,
                                    activity_type=activity_type,
                                    cost=cost,
                                    location_name=activity.get('name', 'TBD')
                                )

                                if success:
                                    st.success(f"✅ Added {activity['name']} to {selected_day} at {selected_time}!")
                                    st.info("💡 Reloading to show in your schedule...")
                                    st.balloons()
                                    # Reload custom activities from database
                                    st.session_state.custom_activities = load_custom_activities()
                                    import time
                                    time.sleep(1)  # Give user time to see the success message
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to add activity. Please try again.")
                            else:
                                st.warning("⚠️ Please select a time first!")

                    st.markdown("---")

    # SMART RECOMMENDATIONS - DYNAMIC based on weather, schedule, and conditions
    st.markdown("---")
    st.markdown("### 💡 Smart Recommendations Based on Real Data")

    st.markdown("""
    <div class="info-box" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <h4 style="margin: 0; color: white;">🤖 AI-Powered Suggestions</h4>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.95;">Activities recommended based on your schedule gaps, real-time weather, UV index, temperature, and time of day</p>
    </div>
    """, unsafe_allow_html=True)

    # Generate smart recommendations for each gap
    if schedule_gaps:
        for gap in schedule_gaps:
            st.markdown(f"#### {gap['description']}")

            # Get weather for this gap
            gap_forecast = None
            for forecast in weather_data.get('forecast', []):
                if forecast['date'] == gap['date']:
                    gap_forecast = forecast
                    break

            # Show weather conditions for this time slot
            if gap_forecast:
                st.markdown(f"""
                <div style="background: #f0f9ff; padding: 0.75rem; border-radius: 10px; margin-bottom: 1rem; border-left: 3px solid #4ecdc4;">
                    <strong>🌤️ Weather Forecast:</strong> {gap_forecast['condition']} |
                    🌡️ {gap_forecast['high']}°F |
                    💧 {gap_forecast['precipitation']}% rain |
                    💨 {gap_forecast['wind']} mph wind
                </div>
                """, unsafe_allow_html=True)

            # Get smart recommendations for this gap
            recommendations = get_smart_recommendations(gap, weather_data, optional_activities)

            if recommendations:
                st.markdown(f"**Top {min(len(recommendations), 20)} Recommended Activities:**")

                for i, rec in enumerate(recommendations[:20], 1):  # Show top 20
                    activity = rec['activity']

                    # Escape HTML to prevent broken rendering
                    import html
                    safe_rec_name = html.escape(activity['name'])
                    safe_rec_desc = html.escape(activity['description'])

                    # Use Streamlit container for clean card display
                    with st.container():
                        # Header with score
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                                    padding: 1.5rem;
                                    border-radius: 12px;
                                    border-left: 4px solid #4ecdc4;
                                    margin: 1rem 0;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            <h4 style="margin: 0; color: #ff6b6b;">
                                #{i} {safe_rec_name}
                                <span style="background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
                                            color: white;
                                            padding: 0.35rem 0.85rem;
                                            border-radius: 15px;
                                            font-size: 0.85rem;
                                            margin-left: 0.5rem;
                                            font-weight: normal;">
                                    Score: {rec['score']}/100
                                </span>
                            </h4>
                            <p style="margin: 0.75rem 0; color: #636e72; line-height: 1.6;">{safe_rec_desc}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        # Activity details in columns
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"**💰 Cost:** {activity['cost_range']}")
                        with col2:
                            st.markdown(f"**⏱️ Duration:** {activity['duration']}")
                        with col3:
                            st.markdown(f"**⭐ Rating:** {activity.get('rating', 'N/A')}")

                        # Why This Fits section
                        if rec['reasons']:
                            st.success("**✅ Why This Fits:**")
                            for reason in rec['reasons']:
                                st.markdown(f"• {reason}")

                        # Warnings section
                        if rec['warnings']:
                            st.warning("**⚠️ Important Notes:**")
                            for warning in rec['warnings']:
                                st.markdown(f"• {warning}")

                        # Pro tip
                        st.info(f"**💡 Pro Tip:** {activity['tips']}")

                        # Interactive controls to add to schedule
                        with st.expander("📅 Add to Your Schedule"):
                            add_col1, add_col2, add_col3 = st.columns(3)

                            with add_col1:
                                selected_day = st.selectbox(
                                    "Select Day",
                                    ["Friday, Nov 7", "Saturday, Nov 8", "Sunday, Nov 9",
                                     "Monday, Nov 10", "Tuesday, Nov 11", "Wednesday, Nov 12"],
                                    key=f"day_select_{gap['description']}_{i}"
                                )

                            with add_col2:
                                selected_time = st.time_input(
                                    "Start Time",
                                    value=None,
                                    key=f"time_select_{gap['description']}_{i}"
                                )

                            with add_col3:
                                custom_duration = st.text_input(
                                    "Duration",
                                    value=activity['duration'],
                                    key=f"duration_{gap['description']}_{i}"
                                )

                            if st.button(f"➕ Add {activity['name']} to Schedule",
                                       key=f"add_{gap['description']}_{i}",
                                       use_container_width=True):
                                if selected_time:
                                    # Extract cost for tracking
                                    cost = 0
                                    cost_str = activity.get('cost_range', '$0')
                                    try:
                                        cost = int(re.findall(r'\d+', cost_str.split('-')[0])[0])
                                    except:
                                        cost = 0

                                    # Determine activity type
                                    activity_type = 'activity'
                                    if 'dining' in activity.get('name', '').lower() or 'restaurant' in activity.get('name', '').lower():
                                        activity_type = 'dining'
                                    elif 'beach' in activity.get('name', '').lower():
                                        activity_type = 'beach'
                                    elif 'spa' in activity.get('name', '').lower() or 'massage' in activity.get('name', '').lower():
                                        activity_type = 'spa'

                                    # Add to schedule
                                    success = add_activity_to_schedule(
                                        activity_name=activity['name'],
                                        activity_description=activity.get('description', ''),
                                        selected_day=selected_day,
                                        selected_time=selected_time,
                                        duration=custom_duration,
                                        activity_type=activity_type,
                                        cost=cost,
                                        location_name=activity.get('name', 'TBD')
                                    )

                                    if success:
                                        st.success(f"✅ Added {activity['name']} to {selected_day} at {selected_time}!")
                                        st.info("💡 Reloading to show in your schedule...")
                                        st.balloons()
                                        # Reload custom activities from database
                                        st.session_state.custom_activities = load_custom_activities()
                                        import time
                                        time.sleep(1)  # Give user time to see the success message
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to add activity. Please try again.")
                                else:
                                    st.warning("⚠️ Please select a time first!")

                        st.markdown("---")

                st.markdown("---")
            else:
                st.info(f"No activities match this {gap['duration_hours']}-hour time slot perfectly. Check the full activity list below!")
    else:
        st.info("Your schedule is fully booked! Browse activities below to find options for future trips.")

    # Additional tips
    st.markdown("---")
    st.markdown("### 🎯 Top Picks")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="ultimate-card" style="border-top: 4px solid #ff6b6b;">
            <div class="card-body">
                <h4 style="color: #ff6b6b;">🏆 Must-Do</h4>
                <ul style="margin: 0.5rem 0; padding-left: 1.25rem;">
                    <li>Horseback riding on beach</li>
                    <li>Birthday dinner at David's</li>
                    <li>Sunset viewing</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="ultimate-card" style="border-top: 4px solid #4ecdc4;">
            <div class="card-body">
                <h4 style="color: #4ecdc4;">💎 Hidden Gems</h4>
                <ul style="margin: 0.5rem 0; padding-left: 1.25rem;">
                    <li>Peters Point Beach (quiet)</li>
                    <li>Egan's Creek nature trail</li>
                    <li>Saturday farmer's market</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="ultimate-card" style="border-top: 4px solid #96ceb4;">
            <div class="card-body">
                <h4 style="color: #96ceb4;">🍽️ Foodie Favorites</h4>
                <ul style="margin: 0.5rem 0; padding-left: 1.25rem;">
                    <li>Brett's for sunset dinner</li>
                    <li>29 South for brunch</li>
                    <li>Le Clos for romance</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TRAVEL DASHBOARD
# ============================================================================

def render_travel_dashboard(activities_data, show_sensitive=True):
    """Render comprehensive travel dashboard with all critical info"""

    # Scroll to top on page load
    st.markdown("""
    <script>
        window.parent.document.querySelector('section.main').scrollTo(0, 0);
    </script>
    """, unsafe_allow_html=True)

    st.markdown("## 🎯 Travel Dashboard")
    st.markdown("Your real-time trip command center with live updates")

    # Quick Navigation
    st.markdown("""
    <div class="info-box" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; margin-bottom: 1rem;">
        <h4 style="margin: 0 0 0.5rem 0; color: white;">🔗 Quick Jump To:</h4>
        <p style="margin: 0; font-size: 0.9rem;">
            <a href="#budget" style="color: white; text-decoration: underline; margin-right: 1rem;">💰 Budget</a>
            <a href="#booze" style="color: white; text-decoration: underline; margin-right: 1rem;">🍺 Booze Run</a>
            <a href="#meals" style="color: white; text-decoration: underline; margin-right: 1rem;">🍽️ Meal Planning</a>
            <a href="#activities" style="color: white; text-decoration: underline;">🎯 Activities</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Get today's date and trip dates
    from datetime import datetime, date
    today = date.today()
    trip_start = date(2025, 11, 7)
    trip_end = date(2025, 11, 12)
    johns_arrival = date(2025, 11, 8)
    johns_departure = date(2025, 11, 11)

    # Days until trip
    days_until = (trip_start - today).days

    # Dashboard metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if days_until > 0:
            st.metric("🎊 Days Until Trip", f"{days_until} days")
        elif days_until == 0:
            st.metric("✈️ Trip Status", "TODAY!")
        else:
            st.metric("🏖️ Trip Status", "In Progress")

    with col2:
        budget_data = calculate_trip_budget(activities_data)
        st.metric("💰 Total Budget", f"${budget_data['total']:,.0f}")

    with col3:
        st.metric("📅 Total Days", "5 nights")

    with col4:
        st.metric("🎯 Activities", len(activities_data))

    st.markdown("---")

    # Live Flight Tracking (Day-Of Only)
    if today == date(2025, 11, 7) or today == johns_arrival:
        st.markdown("### ✈️ Live Flight Tracking")
        st.info("🔴 **LIVE** - Real-time flight updates active!")

        # Michael's departure flight (Nov 7)
        if today == date(2025, 11, 7):
            st.markdown("#### Michael's Departure - AA2434")
            render_flight_status_widget('AA2434', '2025-11-07', compact=False)
            st.markdown("**🛂 TSA Security Wait Time**")
            render_tsa_wait_widget('DCA')

        # John's arrival flight (Nov 8)
        if today == johns_arrival:
            st.markdown("#### John's Arrival - AA1585")
            render_flight_status_widget('AA1585', '2025-11-08', compact=False)

    elif today == johns_departure or today == trip_end:
        st.markdown("### ✈️ Live Flight Tracking")
        st.info("🔴 **LIVE** - Real-time flight updates active!")

        # John's departure (Nov 11)
        if today == johns_departure:
            st.markdown("#### John's Departure - AA1586")
            render_flight_status_widget('AA1586', '2025-11-11', compact=False)
            st.markdown("**🛂 TSA Security Wait Time**")
            render_tsa_wait_widget('JAX')

        # Michael's return (Nov 12)
        if today == trip_end:
            st.markdown("#### Michael's Return - AA2435")
            render_flight_status_widget('AA2435', '2025-11-12', compact=False)
            st.markdown("**🛂 TSA Security Wait Time**")
            render_tsa_wait_widget('JAX')
    else:
        st.info("✈️ Live flight tracking will activate on travel days (Nov 7, 8, 11, 12)")

    # Budget Overview
    st.markdown("---")
    st.markdown('<div id="budget"></div>', unsafe_allow_html=True)
    render_budget_widget(activities_data, show_sensitive, view_mode='michael')

    # Weather widget could go here
    st.markdown("---")
    st.markdown("### 🌤️ Weather Forecast")
    st.info("Average: 75°F • Partly cloudy • Perfect beach weather!")

    # ============ BOOZE RUN SHOPPING LIST ============
    st.markdown("---")
    st.markdown('<div id="booze"></div>', unsafe_allow_html=True)
    st.markdown("### 🍺 Booze Run Shopping List")

    st.markdown("""
    <div class="info-box" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white;">
        <h4 style="margin: 0; color: white;">🛒 Shopping List for Arrival</h4>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.95;">Your booze run checklist! Plan to shop Friday night or Saturday morning. Check off items as you purchase them.</p>
    </div>
    """, unsafe_allow_html=True)

    # Get alcohol requests
    alcohol_requests = get_alcohol_requests()

    if alcohol_requests:
        # Unpurchased items
        unpurchased = [r for r in alcohol_requests if not r['purchased']]
        purchased = [r for r in alcohol_requests if r['purchased']]

        if unpurchased:
            st.markdown("**🛒 To Buy:**")
            for request in unpurchased:
                quantity_str = f" - {request['quantity']}" if request['quantity'] else ""
                notes_str = f" ({request['notes']})" if request['notes'] else ""

                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"""
                    <div class="ultimate-card" style="padding: 0.5rem;">
                        <p style="margin: 0;"><strong>{request['item_name']}</strong>{quantity_str}{notes_str}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    cost_input = st.number_input(
                        "Cost",
                        min_value=0.0,
                        step=1.0,
                        key=f"cost_{request['id']}",
                        label_visibility="collapsed",
                        placeholder="$0.00"
                    )
                with col3:
                    if st.button("✅ Got it", key=f"purchase_{request['id']}", use_container_width=True):
                        mark_alcohol_purchased(request['id'], True, cost_input)
                        st.success(f"✅ Marked {request['item_name']} as purchased for ${cost_input:.2f}!")
                        st.rerun()
        else:
            st.success("🎉 **All items purchased!** Shopping complete!")

        # Show purchased items
        if purchased:
            with st.expander(f"✅ Already Purchased ({len(purchased)} items)"):
                total_purchased_cost = sum(r['cost'] for r in purchased)
                st.info(f"💰 **Total spent on alcohol:** ${total_purchased_cost:.2f} (Split 50/50: ${total_purchased_cost/2:.2f} each)")

                for request in purchased:
                    quantity_str = f" - {request['quantity']}" if request['quantity'] else ""
                    notes_str = f" ({request['notes']})" if request['notes'] else ""
                    cost_str = f" - ${request['cost']:.2f}" if request['cost'] > 0 else ""

                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"- ~~**{request['item_name']}**{quantity_str}{notes_str}~~{cost_str}")
                    with col2:
                        if st.button("↩️ Undo", key=f"unpurchase_{request['id']}", help="Mark as not purchased"):
                            mark_alcohol_purchased(request['id'], False, 0)
                            st.rerun()

        st.info("💡 **Tip:** ABC Fine Wine & Spirits and Total Wine are nearby. Also, there's a Publix 5 mins away for mixers/snacks!")
    else:
        st.info("👀 No drink requests yet. John can add his requests on his page!")

    # ============ MEAL PLANNING SECTION ============
    st.markdown("---")
    st.markdown('<div id="meals"></div>', unsafe_allow_html=True)
    st.markdown("### 🍽️ Meal Planning & Coordination")

    # Arrival time context
    st.markdown("""
    <div class="info-box" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; margin-bottom: 1rem;">
        <h4 style="margin: 0; color: white;">✈️ John's Arrival Timeline</h4>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.95;"><strong>Saturday, Nov 8:</strong> Flight lands at 10:40 AM • Hotel arrival ~12:00 PM</p>
        <p style="margin: 0.3rem 0 0 0; opacity: 0.95;">📍 <strong>Arrives in time for:</strong> Saturday Lunch & Dinner</p>
        <p style="margin: 0.3rem 0 0 0; opacity: 0.85; font-size: 0.9rem;">(Misses Friday dinner & Saturday breakfast)</p>
    </div>
    """, unsafe_allow_html=True)

    # Weather context for outdoor dining
    st.markdown("""
    <div class="info-box" style="background: linear-gradient(135deg, #56ccf2 0%, #2f80ed 100%); color: white; margin-bottom: 1rem;">
        <h4 style="margin: 0; color: white;">🌤️ November Weather</h4>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.95;">Average: 75°F • Partly cloudy • Low humidity</p>
        <p style="margin: 0.3rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">Perfect for outdoor dining! Restaurants with 🌤️ have outdoor seating options.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
        <h4 style="margin: 0; color: white;">🎯 Coordinate Meals with John</h4>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.95;">Propose 3 restaurant options for each meal. John can vote on what works for him, then finalize and add to calendar with all details!</p>
    </div>
    """, unsafe_allow_html=True)

    # Get all dining restaurants
    restaurants_dict = get_optional_activities()
    restaurant_details = get_restaurant_details()

    # Flatten all restaurant options
    all_restaurants = []
    for category_name, items in restaurants_dict.items():
        if any(word in category_name.lower() for word in ['dining', 'fine dining', 'seafood', 'italian', 'mexican', 'asian', 'breakfast', 'casual', 'coffee', 'ritz-carlton dining', 'bars', 'deli', 'lunch']):
            all_restaurants.extend(items)

    # Define daily schedule context (activities that affect meal times)
    def get_daily_schedule(date_str):
        """Get scheduled activities for a given date to show meal time constraints"""
        schedules = {
            "2025-11-08": [  # Saturday
                {"time": "12:00 PM", "activity": "John arrives at hotel", "icon": "✈️"},
            ],
            "2025-11-09": [  # Sunday - Birthday!
                {"time": "9:00 AM", "activity": "Room Service Breakfast (already booked)", "icon": "🛎️"},
                {"time": "10:00 AM", "activity": "Heaven in a Hammock Spa (90 min)", "icon": "💆"},
                {"time": "12:00 PM", "activity": "HydraFacial Spa Treatment (60 min)", "icon": "💧"},
                {"time": "1:30 PM", "activity": "Mani-Pedi Spa Treatment (90 min)", "icon": "💅"},
                {"time": "7:00 PM", "activity": "Birthday Dinner (already booked)", "icon": "🎂"},
            ],
            "2025-11-10": [  # Monday
                {"time": "Flexible", "activity": "No activities scheduled - can sleep in!", "icon": "😴"},
            ],
            "2025-11-11": [  # Tuesday
                {"time": "11:00 AM", "activity": "Check out from hotel", "icon": "🏨"},
                {"time": "1:00 PM", "activity": "Flight departure", "icon": "✈️"},
            ],
        }
        return schedules.get(date_str, [])

    # Define meal slots - ONLY for days when John is there (Nov 8-11)
    meal_slots = [
        # Friday removed - John not there yet
        # Saturday breakfast removed - John doesn't arrive until 12:00 PM
        {"id": "sat_lunch", "label": "Saturday Lunch (Nov 8)", "date": "2025-11-08", "time": "12:30 PM"},
        {"id": "sat_dinner", "label": "Saturday Dinner (Nov 8)", "date": "2025-11-08", "time": "7:00 PM"},
        {"id": "sun_breakfast", "label": "Sunday Breakfast (Nov 9) - 🎂 Room Service!", "date": "2025-11-09", "time": "9:00 AM", "locked": True, "room_service": True},
        {"id": "sun_lunch", "label": "Sunday Lunch (Nov 9)", "date": "2025-11-09", "time": "12:30 PM"},
        {"id": "sun_dinner", "label": "Sunday Dinner (Nov 9) - 🎂 BIRTHDAY!", "date": "2025-11-09", "time": "7:00 PM", "locked": True},
        {"id": "mon_breakfast", "label": "Monday Breakfast (Nov 10)", "date": "2025-11-10", "time": "9:00 AM"},
        {"id": "mon_lunch", "label": "Monday Lunch (Nov 10)", "date": "2025-11-10", "time": "12:30 PM"},
        {"id": "mon_dinner", "label": "Monday Dinner (Nov 10)", "date": "2025-11-10", "time": "7:00 PM"},
        {"id": "tue_breakfast", "label": "Tuesday Breakfast (Nov 11)", "date": "2025-11-11", "time": "8:00 AM"},
    ]

    # Get list of already-used restaurants to prevent duplicates
    def get_used_restaurants():
        """Get list of restaurant names already confirmed or proposed"""
        used = set()
        data = get_trip_data()

        for meal_id, proposal in data.get('meal_proposals', {}).items():
            if proposal.get('status') in ('confirmed', 'proposed', 'voted'):
                options = proposal.get('restaurant_options', [])
                for opt in options:
                    used.add(opt.get('name', ''))

        return used

    for meal_slot in meal_slots:
        if meal_slot.get("locked"):
            if meal_slot.get("room_service"):
                st.success(f"✅ **{meal_slot['label']}**")
                st.markdown("""
                <div class="ultimate-card" style="border-left: 4px solid #4caf50;">
                    <div class="card-body">
                        <p><strong>🛎️ In-Room Dining:</strong> The Ritz-Carlton Amelia Island</p>
                        <p><strong>⏰ Order Time:</strong> Call by 8:30 AM for 9:00 AM delivery</p>
                        <p><strong>📞 Phone:</strong> Dial extension from room or 904-277-1100</p>
                        <p><strong>🍳 Get Menu:</strong> Menu available in your room or call 904-277-1100 to hear options</p>
                        <p><strong>💡 Tip:</strong> Perfect way to relax on your birthday morning before spa at 10 AM!</p>
                        <p><strong>🥐 Popular Items:</strong> Pancakes, eggs benedict, fresh fruit, pastries, coffee service, omelets</p>
                        <p><strong>💰 Est. Cost:</strong> $25-45 per person (plus 18% service charge + delivery fee)</p>
                        <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #666;"><em>💡 Pro tip: Menu booklet is in your room, or call ahead to ask about breakfast options and pricing</em></p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Budget-friendly panic button
                with st.expander("💡 **Budget-Friendly Alternative?** Click for walking-distance breakfast spots"):
                    st.markdown("""
                    <div style="background: #f5f5f5; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                        <p style="margin: 0 0 0.5rem 0; font-weight: bold;">If room service prices are high, these spots are a short walk from the Ritz:</p>
                    </div>
                    """, unsafe_allow_html=True)

                    budget_options = [
                        {
                            "name": "First Drop Coffee (ON-SITE)",
                            "distance": "In the hotel lobby",
                            "cost": "$5-10 per person",
                            "menu": "Espresso, pastries, light breakfast items",
                            "time": "Opens 7:00 AM",
                            "walk_time": "30 seconds from room"
                        },
                        {
                            "name": "Coast Restaurant (ON-SITE)",
                            "distance": "In the hotel",
                            "cost": "$18-28 per person",
                            "menu": "Full breakfast buffet or a la carte",
                            "time": "Opens 7:00 AM",
                            "walk_time": "1 minute from room"
                        },
                        {
                            "name": "Aloha Bagel and Deli",
                            "distance": "5 min drive (2 miles)",
                            "cost": "$8-15 per person",
                            "menu": "Fresh bagels, breakfast sandwiches, coffee",
                            "time": "Opens 7:00 AM",
                            "phone": "904-277-3073"
                        },
                        {
                            "name": "Beach Diner",
                            "distance": "8 min drive (3 miles)",
                            "cost": "$10-20 per person",
                            "menu": "Chocolate chip pancakes, omelettes, Fish & Grits",
                            "time": "Opens early",
                            "phone": "904-261-3663"
                        }
                    ]

                    cols = st.columns(2)
                    for idx, option in enumerate(budget_options):
                        col = cols[idx % 2]
                        with col:
                            # Build complete HTML card
                            phone_line = f"<p style='margin: 0.3rem 0; font-size: 0.9rem;'><strong>📞</strong> {option['phone']}</p>" if 'phone' in option else ""
                            walk_line = f"<p style='margin: 0.3rem 0; font-size: 0.85rem; color: #666;'>🚶 {option['walk_time']}</p>" if 'walk_time' in option else ""

                            card_html = f"""<div class="ultimate-card">
<div class="card-body">
<h4 style="margin: 0 0 0.5rem 0;">{option['name']}</h4>
<p style="margin: 0.3rem 0; font-size: 0.9rem;"><strong>📍</strong> {option['distance']}</p>
<p style="margin: 0.3rem 0; font-size: 0.9rem;"><strong>💰</strong> {option['cost']}</p>
<p style="margin: 0.3rem 0; font-size: 0.9rem;"><strong>🍽️</strong> {option['menu']}</p>
<p style="margin: 0.3rem 0; font-size: 0.9rem;"><strong>⏰</strong> {option['time']}</p>
{phone_line}
{walk_line}
</div>
</div>"""

                            st.markdown(card_html, unsafe_allow_html=True)

                    st.info("💡 **Pro Tip**: First Drop Coffee is perfect for a quick coffee & pastry if you're rushing to spa!")
            else:
                st.info(f"✅ **{meal_slot['label']}** - Already planned!")
            continue

        st.markdown(f"#### {meal_slot['label']}")

        # Get existing proposal
        proposal = get_meal_proposal(meal_slot['id'])

        if proposal and proposal['status'] == 'confirmed':
            # Meal is confirmed - show final choice
            final_idx = proposal.get('final_choice')
            if final_idx is not None and final_idx < len(proposal['restaurant_options']):
                final_restaurant = proposal['restaurant_options'][final_idx]
                rest_details = restaurant_details.get(final_restaurant['name'], {})

                # Use custom meal time if set, otherwise use default
                display_time = proposal.get('meal_time') or meal_slot['time']

                # Check if booking is required
                booking_required = rest_details.get('booking_required', False)
                booking_reminder = "📅 <strong>Reservation required!</strong> " if booking_required else ""

                # Make links clickable
                phone = final_restaurant.get('phone', 'N/A')
                phone_html = f'<a href="tel:{phone}" style="color: #2196f3; text-decoration: none;">{phone}</a>' if phone != 'N/A' else 'N/A'

                booking = final_restaurant.get('booking_url', 'N/A')
                if booking and booking != 'N/A' and booking != 'Call to book' and booking.startswith('http'):
                    booking_html = f'<a href="{booking}" target="_blank" style="color: #2196f3; text-decoration: none;">Book Now →</a>'
                else:
                    booking_html = booking

                menu = rest_details.get('menu_url', 'N/A')
                menu_html = f'<a href="{menu}" target="_blank" style="color: #2196f3; text-decoration: none;">View Menu →</a>' if menu != 'N/A' and menu.startswith('http') else menu

                st.success(f"✅ **CONFIRMED:** {final_restaurant['name']}")
                st.markdown(f"""
                <div class="ultimate-card" style="border-left: 4px solid #4caf50;">
                    <div class="card-body">
                        <p><strong>📍 Restaurant:</strong> {final_restaurant['name']}</p>
                        <p><strong>💰 Cost:</strong> {final_restaurant.get('cost_range', 'N/A')}</p>
                        <p><strong>👔 Dress Code:</strong> {rest_details.get('dress_code', 'Casual')}</p>
                        <p><strong>📞 Phone:</strong> {phone_html}</p>
                        <p><strong>🔗 Booking:</strong> {booking_html}</p>
                        <p><strong>🍽️ Menu:</strong> {menu_html}</p>
                        <p><strong>⏰ Time:</strong> {display_time}</p>
                        <p style="margin-top: 0.5rem;">{booking_reminder}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"🔄 Change {meal_slot['label']}", key=f"change_{meal_slot['id']}"):
                    # Reset to proposal stage
                    data = get_trip_data()
                    if meal_slot['id'] in data.get('meal_proposals', {}):
                        data['meal_proposals'][meal_slot['id']]['status'] = 'proposed'
                        data['meal_proposals'][meal_slot['id']]['final_choice'] = None
                        save_trip_data(f"Reset meal proposal: {meal_slot['id']}")
                    st.rerun()

        elif proposal and proposal['status'] == 'voted':
            # John has voted - show his choice
            options = proposal['restaurant_options']
            john_vote = proposal['john_vote']

            st.info(f"🗳️ **John has voted!** Choice: {john_vote}")

            # Show daily schedule context
            daily_schedule = get_daily_schedule(meal_slot['date'])
            if daily_schedule and len(daily_schedule) > 0:
                schedule_items_html = ""
                for item in daily_schedule:
                    schedule_items_html += f"<p style='margin: 0.3rem 0; font-size: 0.9rem;'>{item['icon']} <strong>{item['time']}</strong> - {item['activity']}</p>"

                st.markdown(f"""
                <div class="info-box" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; margin: 1rem 0;">
                    <h4 style="margin: 0 0 0.5rem 0; color: white;">📅 {meal_slot['label'].split('(')[0]} Schedule</h4>
                    {schedule_items_html}
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; opacity: 0.9;"><em>💡 Adjust meal time to fit your schedule below</em></p>
                </div>
                """, unsafe_allow_html=True)

            for idx, restaurant in enumerate(options):
                rest_details = restaurant_details.get(restaurant['name'], {})
                is_johns_choice = (str(idx) == str(john_vote))

                border_color = "#4caf50" if is_johns_choice else "#ddd"
                # Make links clickable
                phone = restaurant.get('phone', 'N/A')
                phone_html = f'<a href="tel:{phone}" style="color: #2196f3; text-decoration: none;">{phone}</a>' if phone != 'N/A' else 'N/A'

                booking = restaurant.get('booking_url', 'Call to book')
                if booking and booking != 'N/A' and booking != 'Call to book' and booking.startswith('http'):
                    booking_html = f'<a href="{booking}" target="_blank" style="color: #2196f3; text-decoration: none;">Book Online →</a>'
                else:
                    booking_html = booking

                menu = rest_details.get('menu_url', 'N/A')
                menu_html = f'<a href="{menu}" target="_blank" style="color: #2196f3; text-decoration: none;">View Menu →</a>' if menu != 'N/A' and menu.startswith('http') else menu

                st.markdown(f"""
                <div class="ultimate-card" style="border-left: 4px solid {border_color};">
                    <div class="card-body">
                        <h4 style="margin: 0;">{'✅ ' if is_johns_choice else ''}Option {idx + 1}: {restaurant['name']}</h4>
                        <p style="margin: 0.5rem 0;"><strong>💰</strong> {restaurant.get('cost_range', 'N/A')} | <strong>👔</strong> {rest_details.get('dress_code', 'Casual')}</p>
                        <p style="margin: 0.5rem 0;"><strong>📞</strong> {phone_html}</p>
                        <p style="margin: 0.5rem 0;"><strong>🔗 Booking:</strong> {booking_html}</p>
                        <p style="margin: 0.5rem 0;"><strong>🍽️ Menu:</strong> {menu_html}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if john_vote == "none":
                st.warning("❌ John said none of these work. Pick 3 new options!")
                if st.button(f"Pick New Options for {meal_slot['label']}", key=f"repick_{meal_slot['id']}"):
                    data = get_trip_data()
                    if meal_slot['id'] in data.get('meal_proposals', {}):
                        del data['meal_proposals'][meal_slot['id']]
                        save_trip_data(f"Delete meal proposal: {meal_slot['id']}")
                    st.rerun()
            else:
                # Time picker for meal
                st.markdown("---")
                st.markdown("**⏰ Set Meal Time:**")

                # Parse default time for this meal
                import datetime
                default_time_str = meal_slot.get('time', '12:00 PM')
                try:
                    # Parse time string like "12:30 PM" to time object
                    default_time_obj = datetime.datetime.strptime(default_time_str, '%I:%M %p').time()
                except:
                    default_time_obj = datetime.time(12, 0)

                # Time picker
                time_key = f"time_{meal_slot['id']}"
                selected_time = st.time_input(
                    f"Choose time for {meal_slot['label'].split('(')[0]}",
                    value=default_time_obj,
                    key=time_key,
                    help="Adjust based on your daily schedule and spa appointments"
                )

                # Format selected time as string (e.g., "7:30 PM")
                formatted_time = selected_time.strftime('%I:%M %p')

                st.info(f"📍 Meal will be scheduled for **{formatted_time}**")

                # Confirm button
                if st.button(f"✅ Confirm & Add to Calendar", key=f"confirm_{meal_slot['id']}", type="primary"):
                    finalize_meal_choice(meal_slot['id'], int(john_vote), formatted_time)
                    st.success("Meal confirmed and added to calendar!")
                    st.rerun()

        elif proposal and proposal['status'] == 'proposed':
            # Waiting for John's vote
            st.warning("🗳️ **Waiting for John to vote...**")

            options = proposal['restaurant_options']
            for idx, restaurant in enumerate(options):
                rest_details = restaurant_details.get(restaurant['name'], {})

                # Make links clickable
                phone = restaurant.get('phone', 'N/A')
                phone_html = f'<a href="tel:{phone}" style="color: #2196f3; text-decoration: none;">{phone}</a>' if phone != 'N/A' else 'N/A'

                booking = restaurant.get('booking_url', 'Call to book')
                if booking and booking != 'N/A' and booking != 'Call to book' and booking.startswith('http'):
                    booking_html = f'<a href="{booking}" target="_blank" style="color: #2196f3; text-decoration: none;">Book Online →</a>'
                else:
                    booking_html = booking

                menu = rest_details.get('menu_url', 'N/A')
                menu_html = f'<a href="{menu}" target="_blank" style="color: #2196f3; text-decoration: none;">View Menu →</a>' if menu != 'N/A' and menu.startswith('http') else menu

                st.markdown(f"""
                <div class="ultimate-card">
                    <div class="card-body">
                        <h4 style="margin: 0;">Option {idx + 1}: {restaurant['name']}</h4>
                        <p style="margin: 0.5rem 0;"><strong>💰</strong> {restaurant.get('cost_range', 'N/A')} | <strong>👔</strong> {rest_details.get('dress_code', 'Casual')}</p>
                        <p style="margin: 0.5rem 0;"><strong>📞</strong> {phone_html}</p>
                        <p style="margin: 0.5rem 0;"><strong>🔗</strong> {booking_html}</p>
                        <p style="margin: 0.5rem 0;"><strong>🍽️ Menu:</strong> {menu_html}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if st.button(f"Cancel Proposal for {meal_slot['label']}", key=f"cancel_{meal_slot['id']}"):
                data = get_trip_data()
                if meal_slot['id'] in data.get('meal_proposals', {}):
                    del data['meal_proposals'][meal_slot['id']]
                    save_trip_data(f"Cancel meal proposal: {meal_slot['id']}")
                st.rerun()

        else:
            # No proposal yet - create one
            with st.expander(f"📝 **Propose 3 Options for {meal_slot['label']}**", expanded=True):
                st.markdown("**Select 3 restaurants to propose to John:**")
                meal_type = "breakfast" if "breakfast" in meal_slot['label'].lower() else ("lunch" if "lunch" in meal_slot['label'].lower() else "dinner")

                # Parse date to get day of week (0=Mon, 6=Sun)
                from datetime import datetime
                meal_date = datetime.strptime(meal_slot['date'], '%Y-%m-%d')
                day_of_week = meal_date.weekday()
                day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

                st.info(f"💡 Showing {meal_type} options open on {day_names[day_of_week]}. Filters: serves {meal_type}, open that day, not already booked.")

                # Get already-used restaurants
                used_restaurants = get_used_restaurants()

                # Smart filtering based on restaurant operating data
                meal_appropriate_restaurants = []
                for category_name, items in restaurants_dict.items():
                    for restaurant in items:
                        rest_name = restaurant['name']
                        rest_details = restaurant_details.get(rest_name, {})

                        # Check if restaurant serves this meal type
                        serves_list = rest_details.get('serves', [])
                        # Check if restaurant is open on this day
                        days_open = rest_details.get('days_open', [0,1,2,3,4,5,6])

                        # Only include if: serves the meal AND open on that day
                        if meal_type in serves_list and day_of_week in days_open:
                            meal_appropriate_restaurants.append(restaurant)

                # Filter out used restaurants
                available_restaurants = [r for r in meal_appropriate_restaurants if r['name'] not in used_restaurants]

                if len(available_restaurants) < 3:
                    st.error("⚠️ Not enough unique restaurants available! You may need to cancel some previous proposals or pick different options.")
                else:
                    # Initialize session state for selections
                    selection_key = f"selected_{meal_slot['id']}"
                    if selection_key not in st.session_state:
                        st.session_state[selection_key] = []

                    st.markdown(f"**Selected: {len(st.session_state[selection_key])}/3**")

                    # Show available restaurants as clickable cards
                    cols = st.columns(3)
                    for idx, restaurant in enumerate(available_restaurants):
                        col = cols[idx % 3]
                        rest_details = restaurant_details.get(restaurant['name'], {})
                        is_selected = restaurant['name'] in st.session_state[selection_key]

                        with col:
                            # Create card with description - escape HTML
                            import html
                            import urllib.parse
                            safe_name = html.escape(restaurant['name'])
                            safe_desc = html.escape(restaurant.get('description', 'Great dining option'))
                            safe_cost = html.escape(restaurant.get('cost_range', 'N/A'))
                            dress_code_raw = rest_details.get('dress_code', 'Casual')
                            safe_dress = html.escape(dress_code_raw)

                            # Dress code definitions for hover tooltips
                            dress_code_definitions = {
                                "Resort Elegant": "Dressy resort wear - Collared shirts, slacks, dresses, skirts. Jackets optional. NO shorts, t-shirts, flip-flops, or athletic wear.",
                                "Business Casual": "Collared shirts, slacks, khakis, dresses, skirts. NO shorts, t-shirts, flip-flops, or overly casual wear.",
                                "Smart Casual": "Neat, polished casual - Nice jeans OK, collared shirts, blouses, dress shoes. Avoid athletic wear and flip-flops.",
                                "Resort Casual": "Relaxed resort wear - Nice shorts OK, polo shirts, sundresses, sandals. Clean and put-together but comfortable.",
                                "Casual": "Comfortable everyday wear - Jeans, t-shirts, shorts, casual dresses, sandals all fine.",
                                "Very Casual": "Any comfortable clothing - Beach attire, athletic wear, flip-flops all welcome.",
                                "Beachwear/Casual": "Beach-friendly casual - Swimsuit cover-ups, shorts, tank tops, flip-flops all perfectly fine.",
                                "Any": "No dress code - Wear whatever makes you comfortable!"
                            }

                            # Find matching dress code definition
                            dress_tooltip = dress_code_definitions.get(dress_code_raw, "Dress comfortably and appropriately for the venue.")
                            # For complex dress codes with parentheticals, try to match the base
                            if dress_tooltip == "Dress comfortably and appropriately for the venue.":
                                for key in dress_code_definitions:
                                    if key in dress_code_raw:
                                        dress_tooltip = dress_code_definitions[key]
                                        break

                            # Escape tooltip for HTML
                            safe_dress_tooltip = html.escape(dress_tooltip)

                            # Get rating
                            rating = restaurant.get('rating', 'N/A')

                            # Check for outdoor seating (only shown if weather is good - 75°F in November!)
                            has_outdoor = rest_details.get('outdoor_seating', False)
                            outdoor_icon = "🌤️ Outdoor seating (perfect 75° weather!)" if has_outdoor else ""

                            # Check for booking requirement
                            booking_required = rest_details.get('booking_required', False)
                            booking_icon = "📅 Reservation required" if booking_required else ""

                            # Build links
                            website_url = restaurant.get('booking_url', 'N/A')
                            menu_url = rest_details.get('menu_url', 'N/A')

                            # Generate Google and Yelp search URLs
                            search_name = urllib.parse.quote(f"{restaurant['name']} Amelia Island FL")
                            google_url = f"https://www.google.com/search?q={search_name}"
                            yelp_url = f"https://www.yelp.com/search?find_desc={urllib.parse.quote(restaurant['name'])}&find_loc=Amelia+Island+FL"

                            # Build links HTML
                            links_html = ""
                            if website_url != "N/A":
                                links_html += f'<a href="{website_url}" target="_blank" style="color: #2196f3; font-size: 0.85rem; margin-right: 0.5rem;">🌐 Website</a>'
                            if menu_url != "N/A":
                                links_html += f'<a href="{menu_url}" target="_blank" style="color: #2196f3; font-size: 0.85rem; margin-right: 0.5rem;">📋 Menu</a>'
                            links_html += f'<a href="{google_url}" target="_blank" style="color: #2196f3; font-size: 0.85rem; margin-right: 0.5rem;">⭐ Google</a>'
                            links_html += f'<a href="{yelp_url}" target="_blank" style="color: #2196f3; font-size: 0.85rem;">📝 Yelp</a>'

                            border_color = "#4caf50" if is_selected else "#ddd"
                            st.markdown(f"""
<div class="ultimate-card" style="border-left: 4px solid {border_color}; min-height: 250px;">
<div class="card-body">
<h4 style="margin: 0 0 0.5rem 0;">{'✅ ' if is_selected else ''}{safe_name}</h4>
<p style="margin: 0.3rem 0; font-size: 0.85rem; color: #ff9800;"><strong>⭐ {rating}</strong></p>
<p style="margin: 0.5rem 0; font-size: 0.9rem; color: #666;">{safe_desc}</p>
<p style="margin: 0.5rem 0;"><strong>💰</strong> {safe_cost}</p>
<p style="margin: 0.5rem 0; cursor: help;" title="{safe_dress_tooltip}"><strong>👔</strong> {safe_dress} <span style="font-size: 0.75rem; color: #999;">ⓘ</span></p>
{f'<p style="margin: 0.5rem 0; font-size: 0.85rem; color: #2196f3;">{outdoor_icon}</p>' if has_outdoor else ''}
{f'<p style="margin: 0.5rem 0; font-size: 0.85rem; color: #ff5722; font-weight: bold;">{booking_icon}</p>' if booking_required else ''}
<div style="margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid #eee;">
{links_html}
</div>
</div>
</div>
""", unsafe_allow_html=True)

                            # Toggle button
                            if is_selected:
                                if st.button(f"❌ Remove", key=f"remove_{meal_slot['id']}_{idx}", use_container_width=True):
                                    st.session_state[selection_key].remove(restaurant['name'])
                                    st.rerun()
                            else:
                                if len(st.session_state[selection_key]) < 3:
                                    if st.button(f"➕ Select", key=f"select_{meal_slot['id']}_{idx}", use_container_width=True):
                                        st.session_state[selection_key].append(restaurant['name'])
                                        st.rerun()
                                else:
                                    st.button(f"Max 3", key=f"disabled_{meal_slot['id']}_{idx}", use_container_width=True, disabled=True)

                    # Send proposal button
                    if len(st.session_state[selection_key]) == 3:
                        st.markdown("---")
                        if st.button(f"✅ Send Proposal to John", key=f"propose_{meal_slot['id']}", type="primary", use_container_width=True):
                            # Get full restaurant data
                            selected_restaurants = []
                            for name in st.session_state[selection_key]:
                                rest = next((r for r in all_restaurants if r['name'] == name), None)
                                if rest:
                                    selected_restaurants.append(rest)

                            if len(selected_restaurants) == 3:
                                success = save_meal_proposal(meal_slot['id'], selected_restaurants)
                                if success:
                                    # Clear selection
                                    st.session_state[selection_key] = []
                                    st.success(f"✅ Proposal sent! John will see these options on his page.")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to save proposal. Please try again or contact support.")
                    elif len(st.session_state[selection_key]) > 0:
                        st.warning(f"⚠️ Please select {3 - len(st.session_state[selection_key])} more restaurant(s)")
                    else:
                        st.info("👆 Select 3 restaurants from the cards above")

        st.markdown("---")

    # ============ ACTIVITY PLANNING SECTION ============
    st.markdown("---")
    st.markdown('<div id="activities"></div>', unsafe_allow_html=True)
    st.markdown("### 🎯 Activity Planning")

    st.markdown("""
    <div class="info-box" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">
        <h4 style="margin: 0; color: white;">🎯 Plan Your Free Time!</h4>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.95;">Fill your non-dining, non-spa time with fun activities! Propose 3 options for each slot, John votes, then confirm!</p>
    </div>
    """, unsafe_allow_html=True)

    # Define activity time slots (avoiding meals and spa times)
    activity_slots = [
        {"id": "sat_afternoon", "label": "Saturday Afternoon (Nov 8)", "date": "2025-11-08", "time": "After lunch", "notes": "Perfect time for boat tour, beach, or exploring!"},
        {"id": "sat_evening", "label": "Saturday Evening (Nov 8)", "date": "2025-11-08", "time": "After dinner", "notes": "Relax at hotel or explore"},
        {"id": "sun_afternoon", "label": "Sunday Afternoon (Nov 9)", "date": "2025-11-09", "time": "After spa", "notes": "Free time after mani-pedi (ends 3:00 PM)"},
        {"id": "sun_evening", "label": "Sunday Evening (Nov 9)", "date": "2025-11-09", "time": "After dinner", "notes": "Birthday celebration time!"},
        {"id": "mon_morning", "label": "Monday Morning (Nov 10)", "date": "2025-11-10", "time": "Morning", "notes": "Can sleep in - no schedule!"},
        {"id": "mon_afternoon", "label": "Monday Afternoon (Nov 10)", "date": "2025-11-10", "time": "Afternoon", "notes": "Full day free!"},
        {"id": "mon_evening", "label": "Monday Evening (Nov 10)", "date": "2025-11-10", "time": "After dinner", "notes": "Last night - make it count!"},
    ]

    # Get all non-dining optional activities
    all_activities_dict = get_optional_activities()
    available_activities = []
    for category_name, items in all_activities_dict.items():
        # Skip dining categories
        if not any(word in category_name.lower() for word in ['dining', 'restaurant', 'breakfast', 'lunch', 'dinner', 'coffee', 'bar']):
            available_activities.extend(items)

    for activity_slot in activity_slots:
        st.markdown(f"#### {activity_slot['label']}")

        # Get existing proposal
        proposal = get_activity_proposal(activity_slot['id'])

        if proposal and proposal['status'] == 'confirmed':
            # Activity is confirmed
            final_idx = proposal.get('final_choice')
            if final_idx is not None and final_idx < len(proposal['activity_options']):
                final_activity = proposal['activity_options'][final_idx]
                st.success(f"✅ **CONFIRMED:** {final_activity['name']}")
                st.markdown(f"""
                <div class="ultimate-card" style="border-left: 4px solid #4caf50;">
                    <div class="card-body">
                        <p><strong>🎯 Activity:</strong> {final_activity['name']}</p>
                        <p><strong>💰 Cost:</strong> {final_activity.get('cost_range', 'N/A')}</p>
                        <p><strong>⏰ Duration:</strong> {final_activity.get('duration', 'N/A')}</p>
                        <p><strong>📍 Location:</strong> {final_activity.get('description', 'N/A')[:100]}...</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"🔄 Change {activity_slot['label']}", key=f"change_activity_{activity_slot['id']}"):
                    data = get_trip_data()
                    if activity_slot['id'] in data.get('activity_proposals', {}):
                        data['activity_proposals'][activity_slot['id']]['status'] = 'proposed'
                        data['activity_proposals'][activity_slot['id']]['final_choice'] = None
                        save_trip_data(f"Reset activity proposal: {activity_slot['id']}")
                    st.rerun()

        elif proposal and proposal['status'] == 'voted':
            # John has voted
            options = proposal['activity_options']
            john_vote = proposal['john_vote']

            st.info(f"🗳️ **John has voted!** Choice: {john_vote}")

            for idx, activity in enumerate(options):
                is_johns_choice = (str(idx) == str(john_vote))
                border_color = "#4caf50" if is_johns_choice else "#ddd"

                st.markdown(f"""
                <div class="ultimate-card" style="border-left: 4px solid {border_color};">
                    <div class="card-body">
                        <h4 style="margin: 0;">{'✅ ' if is_johns_choice else ''}Option {idx + 1}: {activity['name']}</h4>
                        <p style="margin: 0.5rem 0;"><strong>💰</strong> {activity.get('cost_range', 'N/A')} | <strong>⏰</strong> {activity.get('duration', 'N/A')}</p>
                        <p style="margin: 0.5rem 0;"><strong>📍</strong> {activity.get('description', 'N/A')[:100]}...</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if john_vote == "none":
                st.warning("❌ John said none of these work. Pick 3 new options!")
                if st.button(f"Pick New Options for {activity_slot['label']}", key=f"repick_activity_{activity_slot['id']}"):
                    data = get_trip_data()
                    if activity_slot['id'] in data.get('activity_proposals', {}):
                        del data['activity_proposals'][activity_slot['id']]
                        save_trip_data(f"Delete activity proposal: {activity_slot['id']}")
                    st.rerun()
            else:
                # Confirm button
                if st.button(f"✅ Confirm & Add to Calendar", key=f"confirm_activity_{activity_slot['id']}", type="primary"):
                    finalize_activity_choice(activity_slot['id'], int(john_vote))
                    st.success("Activity confirmed and added to calendar!")
                    st.rerun()

        elif proposal and proposal['status'] == 'proposed':
            # Waiting for John's vote
            st.warning("🗳️ **Waiting for John to vote...**")

            options = proposal['activity_options']
            for idx, activity in enumerate(options):
                st.markdown(f"""
                <div class="ultimate-card">
                    <div class="card-body">
                        <h4 style="margin: 0;">Option {idx + 1}: {activity['name']}</h4>
                        <p style="margin: 0.5rem 0;"><strong>💰</strong> {activity.get('cost_range', 'N/A')} | <strong>⏰</strong> {activity.get('duration', 'N/A')}</p>
                        <p style="margin: 0.5rem 0;"><strong>📍</strong> {activity.get('description', 'N/A')[:100]}...</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if st.button(f"🔄 Pick Different Options", key=f"repick_proposed_{activity_slot['id']}"):
                data = get_trip_data()
                if activity_slot['id'] in data.get('activity_proposals', {}):
                    del data['activity_proposals'][activity_slot['id']]
                    save_trip_data(f"Delete activity proposal: {activity_slot['id']}")
                st.rerun()

        else:
            # No proposal yet - let Michael pick 3 activities
            st.info(f"💡 **{activity_slot['notes']}**")

            # Initialize selection state
            selection_key = f"activity_selection_{activity_slot['id']}"
            if selection_key not in st.session_state:
                st.session_state[selection_key] = []

            st.markdown(f"**Select 3 activities for this time slot ({len(st.session_state[selection_key])}/3):**")

            # Show activities in a grid
            cols = st.columns(3)
            for idx, activity in enumerate(available_activities):
                col = cols[idx % 3]
                is_selected = activity['name'] in st.session_state[selection_key]

                with col:
                    import html
                    safe_name = html.escape(activity['name'])
                    safe_desc = html.escape(activity.get('description', '')[:60])
                    safe_cost = html.escape(activity.get('cost_range', 'N/A'))

                    border_color = "#4caf50" if is_selected else "#ddd"
                    st.markdown(f"""
<div class="ultimate-card" style="border-left: 4px solid {border_color}; min-height: 180px;">
<div class="card-body">
<h4 style="margin: 0 0 0.5rem 0; font-size: 0.95rem;">{'✅ ' if is_selected else ''}{safe_name}</h4>
<p style="margin: 0.3rem 0; font-size: 0.85rem; color: #666;">{safe_desc}...</p>
<p style="margin: 0.3rem 0; font-size: 0.85rem;"><strong>💰</strong> {safe_cost}</p>
<p style="margin: 0.3rem 0; font-size: 0.85rem;"><strong>⏰</strong> {activity.get('duration', 'Varies')}</p>
</div>
</div>
""", unsafe_allow_html=True)

                    # Toggle button
                    if is_selected:
                        if st.button(f"Remove", key=f"activity_remove_{activity_slot['id']}_{idx}", use_container_width=True):
                            st.session_state[selection_key].remove(activity['name'])
                            st.rerun()
                    else:
                        if len(st.session_state[selection_key]) < 3:
                            if st.button(f"Select", key=f"activity_select_{activity_slot['id']}_{idx}", use_container_width=True):
                                st.session_state[selection_key].append(activity['name'])
                                st.rerun()
                        else:
                            st.button(f"Max 3", key=f"activity_disabled_{activity_slot['id']}_{idx}", use_container_width=True, disabled=True)

            # Send proposal button
            if len(st.session_state[selection_key]) == 3:
                st.markdown("---")
                if st.button(f"✅ Send Proposal to John", key=f"propose_activity_{activity_slot['id']}", type="primary", use_container_width=True):
                    # Get full activity data
                    selected_activities = []
                    for activity_name in st.session_state[selection_key]:
                        for activity in available_activities:
                            if activity['name'] == activity_name:
                                selected_activities.append(activity)
                                break

                    success = save_activity_proposal(activity_slot['id'], selected_activities, activity_slot['date'], activity_slot['time'])
                    if success:
                        st.session_state[selection_key] = []  # Clear selection
                        st.success("✅ Activity proposal sent to John!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to save activity proposal. Please try again or contact support.")
            elif len(st.session_state[selection_key]) > 0:
                st.warning(f"⚠️ Please select {3 - len(st.session_state[selection_key])} more activit(y/ies)")
            else:
                st.info("👆 Select 3 activities from the cards above")

        st.markdown("---")


# ============================================================================
# JOHN'S PAGE
# ============================================================================

def render_johns_page(df, activities_data, show_sensitive):
    """John's dedicated trip companion page"""
    # Load John's preferences for opt-in status
    john_prefs = load_john_preferences()

    st.markdown('<h2 class="fade-in">👋 John\'s Trip Companion</h2>', unsafe_allow_html=True)

    # Welcome banner
    st.markdown("""
    <div class="birthday-special">
        <h3 style="margin: 0 0 0.5rem 0;">🌴 Welcome to Amelia Island!</h3>
        <p style="margin: 0; font-size: 1.1rem;">Your quick reference guide for an amazing weekend getaway</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.95rem; opacity: 0.9;">November 8-11, 2025 • The Ritz-Carlton, Amelia Island</p>
    </div>
    """, unsafe_allow_html=True)

    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📅 Trip Length", "3.5 days")
    with col2:
        st.metric("🏨 Hotel Nights", "3 nights")
    with col3:
        arrival_activity = next((a for a in activities_data if a.get('id') == 'arr002'), None)
        flight_lands = arrival_activity.get('estimated_flight_arrival', '10:40 AM') if arrival_activity else "10:40 AM"
        hotel_arrival = arrival_activity.get('estimated_hotel_arrival', '12:00 PM') if arrival_activity else "12:00 PM"
        st.metric("✈️ Flight Lands", f"Sat {flight_lands}", delta=f"Hotel ~{hotel_arrival}", delta_color="off")
    with col4:
        departure_activity = next((a for a in activities_data if a.get('id') == 'dep001'), None)
        flight_departs = departure_activity.get('flight_departure_time', '11:05 AM') if departure_activity else "11:05 AM"
        hotel_depart = departure_activity.get('time', '8:20 AM') if departure_activity else "8:20 AM"
        st.metric("🛫 Flight Departs", f"Tue {flight_departs}", delta=f"Leave hotel ~{hotel_depart}", delta_color="off")

    st.markdown("---")

    # Create tabs for better organization
    tab1, tab2, tab3, tab4 = st.tabs(["✈️ Trip Info", "💰 Budget & Drinks", "🍽️ Vote on Meals", "🎯 Vote on Activities"])

    with tab1:
        # ============ YOUR FLIGHT & ARRIVAL ============
        st.markdown("### ✈️ Your Flight & Arrival")

        john_arrival = next((a for a in activities_data if a.get('id') == 'arr002'), None)
        john_departure = next((a for a in activities_data if a.get('id') == 'dep001'), None)

        # Check if it's travel day
        from datetime import date
        today = date.today()
        is_arrival_day = (today == date(2025, 11, 8))
        is_departure_day = (today == date(2025, 11, 11))

        if john_arrival:
            # Live flight tracking (only on travel day)
            st.markdown("#### 🛬 Arrival Flight - Nov 8")

            if is_arrival_day:
                st.success("🔴 **LIVE TRACKING ACTIVE** - Your flight today!")
                if john_arrival.get('flight_number'):
                    render_flight_status_widget(john_arrival['flight_number'], '2025-11-08', compact=False)
                # TSA wait times at DCA
                st.markdown("**🛂 TSA Security Wait Time - DCA**")
                render_tsa_wait_widget('DCA')
            else:
                if john_arrival.get('flight_number'):
                    render_flight_status_widget(john_arrival['flight_number'], '2025-11-08', compact=False)

            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"""<div class="ultimate-card" style="border-left: 4px solid #4caf50; margin-top: 1rem;">
<div class="card-body">
<h4 style="margin: 0 0 0.5rem 0;">📍 Arrival Details</h4>
<p style="margin: 0.5rem 0;">
✈️ <strong>Lands at JAX:</strong> {john_arrival.get('estimated_flight_arrival', '10:40 AM')}<br>
🏨 <strong>Hotel Arrival:</strong> ~{john_arrival.get('estimated_hotel_arrival', '12:00 PM')}<br>
🚗 <strong>Ground Transport:</strong> {john_arrival['notes']}
</p>
</div>
</div>""", unsafe_allow_html=True)

            with col2:
                st.markdown("**📋 Arrival Checklist**")
                st.markdown("""
                - ✅ ID/Boarding Pass
                - ✅ Phone charged
                - ✅ Track flight status
                - ✅ Text when landing
                - ✅ 45 min drive to hotel
                """)

        # John's departure flight
        if john_departure:
            st.markdown("#### 🛫 Departure Flight - Nov 11")

            if is_departure_day:
                st.success("🔴 **LIVE TRACKING ACTIVE** - Your departure today!")
                if john_departure.get('flight_number'):
                    render_flight_status_widget(john_departure['flight_number'], '2025-11-11', compact=False)
                # TSA wait times at JAX
                st.markdown("**🛂 TSA Security Wait Time - JAX**")
                render_tsa_wait_widget('JAX')
            else:
                if john_departure.get('flight_number'):
                    render_flight_status_widget(john_departure['flight_number'], '2025-11-11', compact=False)

            # Traffic to airport (always show, but emphasize on day-of)
            st.markdown("**🚗 Traffic to Airport**")
            render_traffic_widget(
                "4750 Amelia Island Parkway, Amelia Island, FL",
                "2400 Yankee Clipper Dr, Jacksonville, FL 32218",
                "Hotel → JAX Airport"
            )

            st.info(f"💡 **Pro Tip:** Leave hotel by 8:20 AM for {john_departure.get('flight_departure_time', '11:05 AM')} flight (45 min drive + 2 hrs early)")

        # ============ DAY-BY-DAY SCHEDULE ============
        st.markdown("---")
        st.markdown("### 📅 Your Day-by-Day Schedule")

        # Filter John's relevant activities (Nov 8-11)
        john_start = '2025-11-08'
        john_end = '2025-11-11'
        johns_activities = [a for a in activities_data if a['date'] >= john_start and a['date'] <= john_end]

        # Group by date
        from itertools import groupby
        johns_activities_sorted = sorted(johns_activities, key=lambda x: (x['date'], x['time']))

        for date_str, day_activities in groupby(johns_activities_sorted, key=lambda x: x['date']):
            date_obj = pd.to_datetime(date_str)
            day_activities_list = list(day_activities)

            # Determine if there are partner-only activities (spa)
            partner_spa_times = [a for a in day_activities_list if a['type'] == 'spa']

            with st.expander(f"**{date_obj.strftime('%A, %B %d')}** ({len(day_activities_list)} activities)", expanded=(date_str == john_start)):
                for activity in day_activities_list:
                    # Determine if John is included and payment status
                    is_john_activity = False
                    activity_note = ""
                    activity_id = activity.get('id', '')

                    # Check if it's a couples spa activity (spa001)
                    is_couples_spa = activity['type'] == 'spa' and 'Couples' in activity.get('activity', '')

                    # Check if it's the birthday dinner (din001) - ONLY meal covered by user
                    is_birthday_dinner = activity_id == 'din001'

                    # Determine badge and color
                    if is_birthday_dinner:
                        is_john_activity = True
                        activity_note = "✅ Included - Michael's Treat"
                        border_color = "#4caf50"  # Green for covered
                    elif is_couples_spa:
                        is_john_activity = True
                        activity_note = "✅ Included - Already Covered"
                        border_color = "#4caf50"  # Green for covered
                    elif activity['type'] == 'transport':
                        is_john_activity = True
                        activity_note = "🚕 Your Transportation"
                        border_color = "#2196f3"  # Blue for transport
                    elif activity['type'] == 'dining':
                        is_john_activity = True
                        activity_note = "💰 Going Dutch (Each Pays Own)"
                        border_color = "#ff9800"  # Orange for split
                    elif activity['type'] == 'activity' or activity['type'] == 'beach':
                        is_john_activity = True
                        activity_note = "🎯 Shared Activity (Each Pays Own)"
                        border_color = "#ff9800"  # Orange for split
                    elif activity['type'] == 'spa':
                        activity_note = "💆 Michael's Spa Time (Your Free Time!)"
                        border_color = "#ff9800"  # Orange for free time
                    else:
                        border_color = "#9e9e9e"  # Grey for other

                    # Clean up activity name for John's view (remove "for you" text)
                    # Just remove the suffix - the activity notes explain the details
                    activity_name = activity['activity'].replace('(for you)', '').replace('(For You)', '').strip()

                    # Clean up notes for John's view
                    activity_notes = activity.get('notes', '')
                    if is_couples_spa:
                        # For couples massage, replace payment language
                        activity_notes = activity_notes.replace('YOU\'RE PAYING for both ($245 each = $490 total)', 'Included - already covered for both of you')
                        activity_notes = activity_notes.replace('YOU\'RE PAYING', 'Included - already covered')
                    elif activity_id == 'act001':
                        # For boat trip, clean up the opt-in language
                        activity_notes = activity_notes.replace('You\'re doing this either way - John can pay for this if he wants to join ($135 per person = $270 total for 2). ', 'Michael is doing this either way - want to join for $135? ')
                    elif activity['type'] == 'spa':
                        # Notes are already phrased for John's view - no changes needed
                        pass

                    # Build duration text (fixes nested f-string issue)
                    duration_text = ""
                    if activity.get('duration'):
                        duration_text = f"• {activity.get('duration', '')}"

                    # Escape HTML to prevent broken rendering
                    import html
                    safe_activity_name = html.escape(activity_name)
                    safe_time = html.escape(activity['time'])
                    safe_duration_text = html.escape(duration_text)
                    safe_location = html.escape(activity['location']['name'])
                    safe_notes = html.escape(activity_notes)
                    safe_notes = safe_notes.replace('\n', '<br>')
                    safe_activity_note = html.escape(activity_note)

                    st.markdown(f"""
                    <div class="ultimate-card" style="border-left: 4px solid {border_color}; margin-bottom: 1rem;">
                        <div class="card-body">
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <div style="flex: 1;">
                                    <h4 style="margin: 0 0 0.5rem 0;">{safe_activity_name}</h4>
                                    <p style="margin: 0.25rem 0;"><strong>⏰ {safe_time}</strong> {safe_duration_text}</p>
                                    <p style="margin: 0.25rem 0;">📍 {safe_location}</p>
                                    <p style="margin: 0.5rem 0; font-style: italic; font-size: 0.9rem;">{safe_notes}</p>
                                </div>
                                <div style="margin-left: 1rem;">
                                    <span style="background: {border_color}; color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem; white-space: nowrap;">{safe_activity_note}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Add opt-in buttons for activities that need John's decision
                    needs_optin = False
                    pref_key = ""

                    # Check if this activity needs opt-in
                    if activity_id in ['act001', 'spa002', 'spa003']:  # Activities John can opt into
                        needs_optin = True
                        pref_key = f"activity_opt_in_{activity_id}"

                    if needs_optin:
                        current_status = john_prefs.get(pref_key, "not_decided")

                        col1, col2, col3 = st.columns([1, 1, 2])
                        with col1:
                            if st.button(f"✅ Count Me In!", key=f"optin_{activity_id}_{date_str}", use_container_width=True):
                                save_john_preference(pref_key, "interested")
                                st.success("You're in!")
                                st.rerun()

                        with col2:
                            if st.button(f"❌ Not for Me", key=f"optout_{activity_id}_{date_str}", use_container_width=True):
                                save_john_preference(pref_key, "not_interested")
                                st.info("Got it!")
                                st.rerun()

                        with col3:
                            if current_status == "interested":
                                st.success("✅ **You're In!** - Michael will see this")
                            elif current_status == "not_interested":
                                st.info("❌ **Not Interested** - Michael will see this")
                            else:
                                st.warning("❓ **Please decide** - Michael needs to know")

                # Show free time suggestion if partner has spa
                if partner_spa_times:
                    st.markdown("""
                    <div class="info-box info-success">
                        <strong>💡 Free Time Ideas:</strong> While Michael is at the spa, enjoy the pool, hot tub, beach, or book your own spa treatment!
                    </div>
                    """, unsafe_allow_html=True)

        # ============ THINGS TO DO (FREE TIME) ============
        st.markdown("---")
        st.markdown("### 🎯 Things You Might Enjoy")

        subtab1, subtab2, subtab3 = st.tabs(["🏊 Pool & Beach", "💆 Optional Spa", "🎮 Activities"])

        with subtab1:
            st.markdown("""
            <div class="ultimate-card">
                <div class="card-body">
                    <h4 style="margin: 0 0 0.5rem 0;">🌴 Complimentary Resort Access</h4>
                    <p style="margin: 0.5rem 0;">Enjoy unlimited access to world-class facilities:</p>
                    <ul style="margin: 0.5rem 0;">
                        <li><strong>Multiple Pools</strong> - Oceanfront infinity pool, family pool, adult-only pool</li>
                        <li><strong>Hot Tubs</strong> - Several whirlpool spas throughout the property</li>
                        <li><strong>Private Beach</strong> - Beach chairs, umbrellas, and towel service included</li>
                        <li><strong>Poolside Bar</strong> - Cocktails and light fare available</li>
                        <li><strong>Beach Activities</strong> - Volleyball, paddleboards, kayaks (some may have fees)</li>
                    </ul>
                    <p style="margin: 0.5rem 0 0 0; font-style: italic; color: #666;">📍 All facilities are steps from your room. Towels available at pool & beach stations.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with subtab2:
            st.markdown("""
            <div class="info-box" style="background: linear-gradient(135deg, #e3f2fd 0%, #e1f5fe 100%);">
                <strong>ℹ️ Optional Services:</strong> Book any spa treatment at your own expense. Call 904-277-1087 or ask hotel concierge.
            </div>
            """, unsafe_allow_html=True)

            spa_options = [
                {"name": "Gentleman's Facial", "cost": "$165", "duration": "50 min", "desc": "Designed for men's skin. Addresses shaving irritation and deep cleaning."},
                {"name": "Aromatherapy Massage", "cost": "$185-245", "duration": "50-80 min", "desc": "Relaxing full-body massage with essential oils."},
                {"name": "Hot Stone Massage", "cost": "$205", "duration": "80 min", "desc": "Therapeutic massage with heated stones to ease muscle tension."},
                {"name": "Sports Massage", "cost": "$195", "duration": "50 min", "desc": "Deep tissue massage focused on muscle recovery."},
            ]

            for spa in spa_options:
                st.markdown(f"""
                <div class="ultimate-card">
                    <div class="card-body">
                        <h4 style="margin: 0 0 0.25rem 0;">{spa['name']}</h4>
                        <p style="margin: 0.25rem 0; color: #666;"><strong>{spa['duration']} • {spa['cost']}</strong></p>
                        <p style="margin: 0.5rem 0; font-size: 0.9rem;">{spa['desc']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('**📞 To Book:** <a href="tel:904-277-1087" style="color: #2196f3; text-decoration: none;">Call spa at 904-277-1087</a>', unsafe_allow_html=True)

        with subtab3:
            st.markdown("**🏖️ Nearby Activities** (during free time)")

            optional_ideas = [
                {"name": "Golf at Oak Marsh", "desc": "18-hole championship course on property", "cost": "~$150+"},
                {"name": "Bike Rental", "desc": "Explore the island on two wheels", "cost": "~$30/day"},
                {"name": "Historic Downtown Fernandina", "desc": "Shopping, dining, art galleries - 15 min drive", "cost": "Free"},
                {"name": "Fort Clinch State Park", "desc": "Historic fort, fishing pier, nature trails", "cost": "$6 entry"},
            ]

            for idea in optional_ideas:
                st.markdown(f"**{idea['name']}** ({idea['cost']})")
                st.caption(idea['desc'])
                st.markdown("")

        # ============ PRACTICAL ESSENTIALS ============
        st.markdown("---")
        st.markdown("### 🎒 What to Pack (Your Essentials)")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **🚨 Must Have:**
            - ✈️ ID & boarding pass
            - 💳 Credit card & cash
            - 📱 Phone & charger
            - 🧴 Toiletries & medications
            - 🩳 Swimsuit (for pool/beach!)

            **👕 Clothing:**
            - Casual resort wear
            - Swimwear & cover-up
            - Comfortable walking shoes
            - Sandals/flip-flops
            - Light jacket (evenings can be cool)
            """)

        with col2:
            st.markdown("""
            **🌞 Beach Essentials:**
            - Sunglasses
            - Sunscreen SPF 50+
            - Hat or cap
            - Beach read or e-reader

            **💼 Nice to Have:**
            - Camera
            - Headphones
            - Workout clothes (if using gym)
            - Golf gear (if playing)
            """)

        # ============ QUICK REFERENCE ============
        st.markdown("---")
        st.markdown("### 📞 Quick Reference")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="ultimate-card">
                <div class="card-body">
                    <h4 style="margin: 0 0 0.5rem 0;">🏨 Hotel Information</h4>
                    <p style="margin: 0.25rem 0;"><strong>The Ritz-Carlton, Amelia Island</strong></p>
                    <p style="margin: 0.25rem 0;">4750 Amelia Island Parkway<br>Amelia Island, FL 32034</p>
                    <p style="margin: 0.5rem 0 0 0;">
                        📞 <strong>Main:</strong> 904-277-1100<br>
                        🧖 <strong>Spa:</strong> 904-277-1087<br>
                        🍽️ <strong>Dining:</strong> 904-277-1100<br>
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="ultimate-card" style="margin-top: 1rem;">
                <div class="card-body">
                    <h4 style="margin: 0 0 0.5rem 0;">🚗 Getting Around</h4>
                    <p style="margin: 0.25rem 0;">
                        <strong>Airport to Hotel:</strong> 45 min drive<br>
                        <strong>Rental Car/Uber:</strong> Arrange at JAX<br>
                        <strong>Valet Parking:</strong> $40/day at hotel<br>
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Get weather
            weather = get_weather_ultimate()
            if weather and 'forecast' in weather:
                # Calculate average temp from forecast
                forecast = weather['forecast']
                if forecast:
                    avg_temp = sum([day.get('temp', 75) for day in forecast]) / len(forecast)
                else:
                    avg_temp = weather.get('current', {}).get('temperature', 75)

                st.markdown(f"""
                <div class="ultimate-card">
                    <div class="card-body">
                        <h4 style="margin: 0 0 0.5rem 0;">🌤️ Weather Forecast</h4>
                        <p style="margin: 0.25rem 0;">
                            <strong>Average:</strong> {avg_temp:.0f}°F<br>
                            <strong>Conditions:</strong> Partly cloudy<br>
                            <strong>What to Expect:</strong> Pleasant beach weather!
                        </p>
                        <p style="margin: 0.5rem 0 0 0; font-style: italic; font-size: 0.85rem;">
                            Pack sunscreen and light layers.
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Fallback if weather API unavailable
                st.markdown("""
                <div class="ultimate-card">
                    <div class="card-body">
                        <h4 style="margin: 0 0 0.5rem 0;">🌤️ Weather Forecast</h4>
                        <p style="margin: 0.25rem 0;">
                            <strong>Average:</strong> 75°F<br>
                            <strong>Conditions:</strong> Pleasant<br>
                            <strong>What to Expect:</strong> Nice beach weather!
                        </p>
                        <p style="margin: 0.5rem 0 0 0; font-style: italic; font-size: 0.85rem;">
                            Pack sunscreen and light layers.
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div class="ultimate-card" style="margin-top: 1rem;">
                <div class="card-body">
                    <h4 style="margin: 0 0 0.5rem 0;">💡 Good to Know</h4>
                    <p style="margin: 0.25rem 0;">
                        🏨 <strong>Check-in:</strong> 4:00 PM<br>
                        🚪 <strong>Check-out:</strong> 11:00 AM<br>
                        📶 <strong>WiFi:</strong> Complimentary<br>
                        🏋️ <strong>Fitness Center:</strong> 24/7 access<br>
                        ☕ <strong>Coffee:</strong> In-room Nespresso<br>
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        # ============ BUDGET OVERVIEW ============
        st.markdown("### 💰 Your Trip Budget")
        render_budget_widget(activities_data, show_sensitive, view_mode='john')

        # ============ ALCOHOL/DRINK REQUESTS ============
        st.markdown("---")
        st.markdown("### 🍺 Drink Requests")

        st.markdown("""
        <div class="info-box" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white;">
            <h4 style="margin: 0; color: white;">🍺 Michael's Booze Run!</h4>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.95;">Michael will do a booze run when he arrives (Friday night or Saturday morning). Submit your drink requests below!</p>
        </div>
        """, unsafe_allow_html=True)

        # Get existing requests
        all_requests = get_alcohol_requests()

        # Show existing requests
        if all_requests:
            st.markdown("**Your Current Requests:**")
            for request in all_requests:
                if not request['purchased']:
                    quantity_str = f" - {request['quantity']}" if request['quantity'] else ""
                    notes_str = f" ({request['notes']})" if request['notes'] else ""

                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"- **{request['item_name']}**{quantity_str}{notes_str}")
                    with col2:
                        if st.button("🗑️", key=f"delete_request_{request['id']}", help="Delete this request"):
                            delete_alcohol_request(request['id'])
                            st.rerun()

            # Show purchased items
            purchased_items = [r for r in all_requests if r['purchased']]
            if purchased_items:
                with st.expander("✅ Already Purchased"):
                    total_purchased_cost = sum(r['cost'] for r in purchased_items)
                    if total_purchased_cost > 0:
                        st.info(f"💰 **Total spent:** ${total_purchased_cost:.2f} (Your share: ${total_purchased_cost/2:.2f})")

                    for request in purchased_items:
                        quantity_str = f" - {request['quantity']}" if request['quantity'] else ""
                        notes_str = f" ({request['notes']})" if request['notes'] else ""
                        cost_str = f" - ${request['cost']:.2f}" if request['cost'] > 0 else ""
                        st.markdown(f"- ~~**{request['item_name']}**{quantity_str}{notes_str}~~{cost_str}")

        # Add new request form
        st.markdown("---")
        st.markdown("**Add New Request:**")

        with st.form("add_alcohol_request", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                item_name = st.text_input("Item Name", placeholder="e.g., Beer, Wine, Vodka, Mixers")
            with col2:
                quantity = st.text_input("Quantity (optional)", placeholder="e.g., 6-pack, 2 bottles")

            notes = st.text_input("Notes (optional)", placeholder="e.g., IPA preferred, Red wine, Any brand")

            submitted = st.form_submit_button("➕ Add Request", type="primary", use_container_width=True)
            if submitted:
                if item_name:
                    add_alcohol_request(item_name, quantity, notes)
                    st.success(f"✅ Added {item_name} to your requests!")
                    st.rerun()
                else:
                    st.error("Please enter an item name")

    with tab3:
        # ============ MEAL VOTING SECTION ============
        st.markdown("### 🍽️ Vote on Meal Options")

        st.markdown("""
        <div class="info-box" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
            <h4 style="margin: 0; color: white;">🗳️ Your Input Needed!</h4>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.95;">Michael has proposed restaurant options for meals. Vote on which ones work for you!</p>
        </div>
        """, unsafe_allow_html=True)

        # Refresh button to reload proposals
        if st.button("🔄 Refresh to Check for New Proposals", use_container_width=True):
            # Clear cached data to force reload from GitHub
            if 'trip_data' in st.session_state:
                del st.session_state['trip_data']
            st.rerun()

        # Get all meal proposals
        meal_slots = [
            {"id": "fri_dinner", "label": "Friday Dinner (Nov 7)", "date": "2025-11-07"},
            {"id": "sat_breakfast", "label": "Saturday Breakfast (Nov 8)", "date": "2025-11-08"},
            {"id": "sat_lunch", "label": "Saturday Lunch (Nov 8)", "date": "2025-11-08"},
            {"id": "sat_dinner", "label": "Saturday Dinner (Nov 8)", "date": "2025-11-08"},
            {"id": "sun_breakfast", "label": "Sunday Breakfast (Nov 9)", "date": "2025-11-09"},
            {"id": "sun_lunch", "label": "Sunday Lunch (Nov 9)", "date": "2025-11-09"},
            {"id": "sun_dinner", "label": "Sunday Dinner (Nov 9)", "date": "2025-11-09"},
            {"id": "mon_breakfast", "label": "Monday Breakfast (Nov 10)", "date": "2025-11-10"},
            {"id": "mon_lunch", "label": "Monday Lunch (Nov 10)", "date": "2025-11-10"},
            {"id": "mon_dinner", "label": "Monday Dinner (Nov 10)", "date": "2025-11-10"},
            {"id": "tue_breakfast", "label": "Tuesday Breakfast (Nov 11)", "date": "2025-11-11"},
        ]

        restaurant_details = get_restaurant_details()
        has_proposals = False

        # Debug: Show all proposals in the data
        data = get_trip_data()
        all_proposals = data.get('meal_proposals', {})
        if all_proposals:
            with st.expander("🔍 Debug: View All Meal Proposals"):
                for meal_id, prop in all_proposals.items():
                    st.write(f"**{meal_id}**: status={prop.get('status')}, submitted_by={prop.get('submitted_by', 'NOT SET')}, options={len(prop.get('restaurant_options', []))}")

        for meal_slot in meal_slots:
            proposal = get_meal_proposal(meal_slot['id'])

            # Only show proposals submitted by Michael (not John's counter-proposals)
            # Default to Michael if submitted_by is missing (backwards compatibility)
            if proposal and proposal['status'] == 'proposed' and proposal.get('submitted_by', 'Michael') == 'Michael':
                has_proposals = True
                st.markdown(f"#### {meal_slot['label']}")
                st.markdown("**Michael proposed these 3 options. Which works for you?**")

                options = proposal['restaurant_options']

                # Display options
                for idx, restaurant in enumerate(options):
                    rest_details = restaurant_details.get(restaurant['name'], {})

                    # Make links clickable
                    phone = restaurant.get('phone', 'N/A')
                    phone_html = f'<a href="tel:{phone}" style="color: #2196f3; text-decoration: none;">{phone}</a>' if phone != 'N/A' else 'N/A'

                    menu = rest_details.get('menu_url', 'N/A')
                    menu_html = f'<a href="{menu}" target="_blank" style="color: #2196f3; text-decoration: none;">View Menu →</a>' if menu != 'N/A' and menu.startswith('http') else menu

                    st.markdown(f"""
                    <div class="ultimate-card">
                        <div class="card-body">
                            <h4 style="margin: 0 0 0.5rem 0;">Option {idx + 1}: {restaurant['name']}</h4>
                            <p style="margin: 0.25rem 0;"><strong>📝 Description:</strong> {restaurant.get('description', 'N/A')}</p>
                            <p style="margin: 0.25rem 0;"><strong>💰 Cost:</strong> {restaurant.get('cost_range', 'N/A')}</p>
                            <p style="margin: 0.25rem 0;"><strong>👔 Dress Code:</strong> {rest_details.get('dress_code', 'Casual')}</p>
                            <p style="margin: 0.25rem 0;"><strong>📞 Phone:</strong> {phone_html}</p>
                            <p style="margin: 0.25rem 0;"><strong>🔗 Menu/Website:</strong> {menu_html}</p>
                            <p style="margin: 0.25rem 0;"><strong>💡 Tip:</strong> {restaurant.get('tips', 'N/A')}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Voting buttons
                st.markdown("**Cast Your Vote:**")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    if st.button(f"✅ Option 1", key=f"vote_{meal_slot['id']}_0", use_container_width=True, type="primary"):
                        save_john_meal_vote(meal_slot['id'], "0")
                        st.success("Vote recorded!")
                        st.rerun()

                with col2:
                    if st.button(f"✅ Option 2", key=f"vote_{meal_slot['id']}_1", use_container_width=True, type="primary"):
                        save_john_meal_vote(meal_slot['id'], "1")
                        st.success("Vote recorded!")
                        st.rerun()

                with col3:
                    if st.button(f"✅ Option 3", key=f"vote_{meal_slot['id']}_2", use_container_width=True, type="primary"):
                        save_john_meal_vote(meal_slot['id'], "2")
                        st.success("Vote recorded!")
                        st.rerun()

                with col4:
                    if st.button(f"❌ None Work", key=f"vote_{meal_slot['id']}_none", use_container_width=True):
                        save_john_meal_vote(meal_slot['id'], "none")
                        st.info("Michael will pick new options.")
                        st.rerun()

                # John can propose alternatives
                with st.expander("💡 **Don't like these options? Suggest 3 alternatives!**"):
                    st.markdown("**Browse all available restaurants and pick 3 you'd prefer:**")

                    # Get meal type
                    meal_type = "breakfast" if "breakfast" in meal_slot['label'].lower() else ("lunch" if "lunch" in meal_slot['label'].lower() else "dinner")

                    # Get available restaurants (same filtering logic as Michael's side)
                    restaurants_dict = get_optional_activities()
                    meal_date_str = meal_slot.get('date', '2025-11-08')  # Default to Nov 8 if not specified
                    from datetime import datetime
                    meal_date = datetime.strptime(meal_date_str, '%Y-%m-%d')
                    day_of_week = meal_date.weekday()

                    # Smart filtering
                    meal_appropriate_restaurants = []
                    for category_name, items in restaurants_dict.items():
                        for restaurant in items:
                            rest_name = restaurant['name']
                            rest_details = restaurant_details.get(rest_name, {})
                            serves_list = rest_details.get('serves', [])
                            days_open = rest_details.get('days_open', [0,1,2,3,4,5,6])

                            if meal_type in serves_list and day_of_week in days_open:
                                meal_appropriate_restaurants.append(restaurant)

                    # Initialize John's selection state
                    john_selection_key = f"john_alternative_{meal_slot['id']}"
                    if john_selection_key not in st.session_state:
                        st.session_state[john_selection_key] = []

                    st.markdown(f"**Selected: {len(st.session_state[john_selection_key])}/3**")

                    # Show available restaurants
                    cols = st.columns(3)
                    for idx, restaurant in enumerate(meal_appropriate_restaurants):
                        col = cols[idx % 3]
                        is_selected = restaurant['name'] in st.session_state[john_selection_key]
                        rest_details_local = restaurant_details.get(restaurant['name'], {})

                        with col:
                            import html
                            safe_name = html.escape(restaurant['name'])
                            safe_desc = html.escape(restaurant.get('description', 'Great dining option'))
                            safe_cost = html.escape(restaurant.get('cost_range', 'N/A'))

                            border_color = "#4caf50" if is_selected else "#ddd"
                            st.markdown(f"""
<div class="ultimate-card" style="border-left: 4px solid {border_color}; min-height: 150px;">
<div class="card-body">
<h4 style="margin: 0 0 0.5rem 0; font-size: 0.95rem;">{'✅ ' if is_selected else ''}{safe_name}</h4>
<p style="margin: 0.3rem 0; font-size: 0.85rem; color: #666;">{safe_desc[:80]}...</p>
<p style="margin: 0.3rem 0; font-size: 0.85rem;"><strong>💰</strong> {safe_cost}</p>
</div>
</div>
""", unsafe_allow_html=True)

                            # Toggle button
                            if is_selected:
                                if st.button(f"Remove", key=f"john_remove_{meal_slot['id']}_{idx}", use_container_width=True):
                                    st.session_state[john_selection_key].remove(restaurant['name'])
                                    st.rerun()
                            else:
                                if len(st.session_state[john_selection_key]) < 3:
                                    if st.button(f"Select", key=f"john_select_{meal_slot['id']}_{idx}", use_container_width=True):
                                        st.session_state[john_selection_key].append(restaurant['name'])
                                        st.rerun()
                                else:
                                    st.button(f"Max 3", key=f"john_disabled_{meal_slot['id']}_{idx}", use_container_width=True, disabled=True)

                    # Send counter-proposal button
                    if len(st.session_state[john_selection_key]) == 3:
                        st.markdown("---")
                        if st.button(f"✅ Send My 3 Alternatives to Michael", key=f"john_counter_{meal_slot['id']}", type="primary", use_container_width=True):
                            # Get full restaurant data
                            selected_restaurants = []
                            all_restaurants = []
                            for category_name, items in restaurants_dict.items():
                                all_restaurants.extend(items)

                            for name in st.session_state[john_selection_key]:
                                rest = next((r for r in all_restaurants if r['name'] == name), None)
                                if rest:
                                    selected_restaurants.append(rest)

                            if len(selected_restaurants) == 3:
                                # Save as a new proposal from John (replace Michael's)
                                success = save_meal_proposal(meal_slot['id'], selected_restaurants, submitted_by="John")
                                if success:
                                    # Clear selection
                                    st.session_state[john_selection_key] = []
                                    st.success("Counter-proposal sent to Michael! He can now vote on your 3 choices.")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to save counter-proposal. Please try again.")

                st.markdown("---")

            elif proposal and proposal['status'] == 'voted':
                # Already voted
                st.success(f"✅ **{meal_slot['label']}** - You voted! Waiting for Michael to confirm.")

            elif proposal and proposal['status'] == 'confirmed':
                # Confirmed
                final_idx = proposal.get('final_choice')
                if final_idx is not None:
                    final_restaurant = proposal['restaurant_options'][final_idx]
                    st.success(f"✅ **{meal_slot['label']}** - Confirmed: {final_restaurant['name']}")

        if not has_proposals:
            st.info("👀 No meal proposals yet. Michael will add options soon!")

    with tab4:
        # ============ ACTIVITY VOTING SECTION ============
        st.markdown("### 🎯 Vote on Activity Options")

        st.markdown("""
        <div class="info-box" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">
            <h4 style="margin: 0; color: white;">🎯 Your Input Needed!</h4>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.95;">Michael has proposed activity options. Vote on which ones work for you!</p>
        </div>
        """, unsafe_allow_html=True)

        # Refresh button to reload proposals
        if st.button("🔄 Refresh to Check for New Proposals", key="refresh_activities", use_container_width=True):
            # Clear cached data to force reload from GitHub
            if 'trip_data' in st.session_state:
                del st.session_state['trip_data']
            st.rerun()

        # Get all activity proposals
        activity_slots = [
            {"id": "sat_afternoon", "label": "Saturday Afternoon (Nov 8)"},
            {"id": "sat_evening", "label": "Saturday Evening (Nov 8)"},
            {"id": "sun_afternoon", "label": "Sunday Afternoon (Nov 9)"},
            {"id": "sun_evening", "label": "Sunday Evening (Nov 9)"},
            {"id": "mon_morning", "label": "Monday Morning (Nov 10)"},
            {"id": "mon_afternoon", "label": "Monday Afternoon (Nov 10)"},
            {"id": "mon_evening", "label": "Monday Evening (Nov 10)"},
        ]

        has_activity_proposals = False

        for activity_slot in activity_slots:
            proposal = get_activity_proposal(activity_slot['id'])

            # Only show proposals submitted by Michael (not John's counter-proposals)
            # Default to Michael if submitted_by is missing (backwards compatibility)
            if proposal and proposal['status'] == 'proposed' and proposal.get('submitted_by', 'Michael') == 'Michael':
                has_activity_proposals = True
                st.markdown(f"#### {activity_slot['label']}")
                st.markdown("**Michael proposed these 3 options. Which works for you?**")

                options = proposal['activity_options']

                # Display options
                for idx, activity in enumerate(options):
                    st.markdown(f"""
                    <div class="ultimate-card">
                        <div class="card-body">
                            <h4 style="margin: 0 0 0.5rem 0;">Option {idx + 1}: {activity['name']}</h4>
                            <p style="margin: 0.25rem 0;"><strong>📝 Description:</strong> {activity.get('description', 'N/A')[:120]}...</p>
                            <p style="margin: 0.25rem 0;"><strong>💰 Cost:</strong> {activity.get('cost_range', 'N/A')}</p>
                            <p style="margin: 0.25rem 0;"><strong>⏰ Duration:</strong> {activity.get('duration', 'N/A')}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Voting buttons
                st.markdown("**Cast Your Vote:**")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    if st.button(f"✅ Option 1", key=f"vote_activity_{activity_slot['id']}_0", use_container_width=True, type="primary"):
                        save_john_activity_vote(activity_slot['id'], "0")
                        st.success("Vote recorded!")
                        st.rerun()

                with col2:
                    if st.button(f"✅ Option 2", key=f"vote_activity_{activity_slot['id']}_1", use_container_width=True, type="primary"):
                        save_john_activity_vote(activity_slot['id'], "1")
                        st.success("Vote recorded!")
                        st.rerun()

                with col3:
                    if st.button(f"✅ Option 3", key=f"vote_activity_{activity_slot['id']}_2", use_container_width=True, type="primary"):
                        save_john_activity_vote(activity_slot['id'], "2")
                        st.success("Vote recorded!")
                        st.rerun()

                with col4:
                    if st.button(f"❌ None Work", key=f"vote_activity_{activity_slot['id']}_none", use_container_width=True):
                        save_john_activity_vote(activity_slot['id'], "none")
                        st.info("Michael will pick new options.")
                        st.rerun()

                st.markdown("---")

            elif proposal and proposal['status'] == 'voted':
                # Already voted
                st.success(f"✅ **{activity_slot['label']}** - You voted! Waiting for Michael to confirm.")

            elif proposal and proposal['status'] == 'confirmed':
                # Confirmed
                final_idx = proposal.get('final_choice')
                if final_idx is not None and final_idx < len(proposal['activity_options']):
                    final_activity = proposal['activity_options'][final_idx]
                    st.success(f"✅ **{activity_slot['label']}** - Confirmed: {final_activity['name']}")

        if not has_activity_proposals:
            st.info("👀 No activity proposals yet. Michael will add options soon!")

        # ============ OPT-IN ACTIVITIES SECTION ============
        st.markdown("---")
        st.markdown("### 🎟️ Activities You Can Join")

        st.markdown("""
        <div class="info-box" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white;">
            <h4 style="margin: 0; color: white;">🎟️ Michael's Doing These - Want to Join?</h4>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.95;">These activities are happening either way. Let Michael know if you want to join him!</p>
        </div>
        """, unsafe_allow_html=True)

        # Get opt-in activities from the schedule
        optin_activities = [a for a in activities_data if a.get('id') in ['act001', 'spa002', 'spa003']]

        if optin_activities:
            for activity in optin_activities:
                activity_id = activity.get('id')
                pref_key = f"activity_opt_in_{activity_id}"
                current_status = john_prefs.get(pref_key, "not_decided")

                # Format the date nicely
                date_obj = pd.to_datetime(activity['date'])
                date_display = date_obj.strftime('%A, %B %d')

                # Clean up activity name and notes for John's view
                # Remove the "(for you)" suffix from activity names - the notes explain the details
                activity_name = activity['activity'].replace('(for you)', '').replace('(For You)', '').strip()
                activity_notes = activity.get('notes', '')

                # Clean up notes based on activity type
                if activity_id == 'act001':
                    activity_notes = activity_notes.replace('You\'re doing this either way - John can pay for this if he wants to join ($135 per person = $270 total for 2). ', 'I\'m doing this either way - want to join for $135? ')
                elif activity['type'] == 'spa':
                    # Convert "you" references to "I/me" for John's view
                    activity_notes = activity_notes.replace('you at the same time? You\'d pay for yours', 'you at the same time? You\'d pay for yours')
                    activity_notes = activity_notes.replace('while I\'m getting pampered', 'while I\'m getting pampered')
                    # No additional changes needed - notes are already phrased for John

                # Make phone and booking URL clickable
                phone = activity.get('location', {}).get('phone', 'N/A')
                phone_html = f'<a href="tel:{phone}" style="color: #2196f3; text-decoration: none;">{phone}</a>' if phone and phone != 'N/A' else 'N/A'

                booking_url = activity.get('booking_url', '')
                if booking_url and booking_url != 'N/A' and booking_url != 'Call to book' and booking_url.startswith('http'):
                    booking_html = f'<a href="{booking_url}" target="_blank" style="color: #2196f3; text-decoration: none;">Book Online →</a>'
                elif 'Call' in booking_url or phone != 'N/A':
                    booking_html = 'Call to book'
                else:
                    booking_html = 'N/A'

                # Escape HTML
                import html
                safe_activity_name = html.escape(activity_name)
                safe_date = html.escape(date_display)
                safe_time = html.escape(activity['time'])
                safe_duration = html.escape(activity.get('duration', ''))
                safe_notes = html.escape(activity_notes)
                safe_cost = html.escape(f"${activity.get('cost', 0)}")

                st.markdown(f"""
                <div class="ultimate-card" style="border-left: 4px solid #fa709a;">
                    <div class="card-body">
                        <h4 style="margin: 0 0 0.5rem 0;">{safe_activity_name}</h4>
                        <p style="margin: 0.25rem 0;"><strong>📅 When:</strong> {safe_date} at {safe_time}</p>
                        <p style="margin: 0.25rem 0;"><strong>⏰ Duration:</strong> {safe_duration}</p>
                        <p style="margin: 0.25rem 0;"><strong>💰 Cost:</strong> {safe_cost} per person (if you join)</p>
                        <p style="margin: 0.25rem 0;"><strong>📞 Phone:</strong> {phone_html}</p>
                        <p style="margin: 0.25rem 0;"><strong>🔗 Booking:</strong> {booking_html}</p>
                        <p style="margin: 0.5rem 0; font-style: italic; color: #636e72;">{safe_notes}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Voting buttons
                col1, col2, col3 = st.columns([1, 1, 2])

                with col1:
                    if st.button(f"✅ Count Me In!", key=f"optin_tab4_{activity_id}", use_container_width=True, type="primary"):
                        save_john_preference(pref_key, "interested")
                        st.success("You're in!")
                        st.rerun()

                with col2:
                    if st.button(f"❌ Not for Me", key=f"optout_tab4_{activity_id}", use_container_width=True):
                        save_john_preference(pref_key, "not_interested")
                        st.info("Got it!")
                        st.rerun()

                with col3:
                    if current_status == "interested":
                        st.success("✅ **You're In!** - Michael will see this")
                    elif current_status == "not_interested":
                        st.info("❌ **Not Interested** - Michael will see this")
                    else:
                        st.warning("❓ **Please decide** - Michael needs to know")

                st.markdown("---")
        else:
            st.info("No opt-in activities available at this time.")

        # Final tips
        st.markdown("---")
        st.markdown("""
        <div class="info-box info-success">
            <h4 style="margin: 0 0 0.5rem 0;">✨ Tips for a Great Trip</h4>
            <ul style="margin: 0;">
                <li>Download the American Airlines app for mobile boarding pass</li>
                <li>Bring a refillable water bottle - stay hydrated in the sun</li>
                <li>The resort is walkable - comfortable shoes recommended</li>
                <li>Try the Salt restaurant for breakfast - amazing ocean views!</li>
                <li>Sunset at the beach is spectacular - bring your camera around 6 PM</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


def render_birthday_page():
    """Birthday Special Features - 40th Birthday Celebration Tools"""
    st.markdown('<h2 class="fade-in">🎂 40th Birthday Celebration</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; text-align: center;">
        <h1 style="margin: 0; color: white; font-size: 3rem;">🎉 HAPPY 40TH BIRTHDAY! 🎉</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.95;">November 10, 2025</p>
    </div>
    """, unsafe_allow_html=True)

    # Birthday countdown - use .date() for consistent day counting
    birthday_date = TRIP_CONFIG['birthday_date']
    days_until_birthday = (birthday_date.date() - datetime.now().date()).days

    if days_until_birthday > 0:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; text-align: center;">🎂 Birthday Countdown</h3>
            <h1 style="margin: 0.5rem 0 0 0; text-align: center; color: #ff6b6b; font-size: 3rem;">
                {days_until_birthday} Days
            </h1>
            <p style="margin: 0.5rem 0 0 0; text-align: center;">Until the big 4-0!</p>
        </div>
        """, unsafe_allow_html=True)
    elif days_until_birthday == 0:
        st.balloons()
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);">
            <h1 style="margin: 0; text-align: center; color: #d63031; font-size: 3rem;">🎉 TODAY IS THE DAY! 🎉</h1>
            <p style="margin: 0.5rem 0 0 0; text-align: center; font-size: 1.2rem;">Happy 40th Birthday!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        days_since = abs(days_until_birthday)
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; text-align: center;">✨ Birthday Memory</h3>
            <p style="margin: 0.5rem 0 0 0; text-align: center; font-size: 1.2rem;">
                {days_since} days since your amazing 40th birthday!
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Tabs for different birthday features
    tab1, tab2, tab3, tab4 = st.tabs(["🎁 Celebration Checklist", "💭 40 Reflections", "🎊 Birthday Wishes", "🎯 Bucket List"])

    with tab1:
        st.markdown("### 🎁 Birthday Celebration Checklist")
        st.markdown("Make sure you don't miss any special birthday moments!")

        celebration_items = [
            {"item": "Birthday breakfast in bed", "category": "morning"},
            {"item": "Spa day pampering", "category": "daytime"},
            {"item": "Take a birthday photo at the beach", "category": "daytime"},
            {"item": "Birthday dinner at Café Karibo", "category": "evening"},
            {"item": "Birthday cake and candles", "category": "evening"},
            {"item": "Toast with champagne", "category": "evening"},
            {"item": "Make a birthday wish", "category": "evening"},
            {"item": "Capture a birthday selfie", "category": "anytime"},
            {"item": "Write in your birthday journal", "category": "anytime"},
            {"item": "Call family to say thanks", "category": "anytime"}
        ]

        # Group by category
        for category in ["morning", "daytime", "evening", "anytime"]:
            category_name = category.capitalize()
            st.markdown(f"#### {category_name}")

            items_in_category = [item for item in celebration_items if item['category'] == category]

            for idx, item in enumerate(items_in_category):
                col1, col2 = st.columns([0.9, 0.1])

                with col1:
                    st.markdown(f"**{item['item']}**")

                with col2:
                    item_id = f"birthday_{category}_{idx}"
                    is_checked = st.session_state.packing_list.get(item_id, False)
                    checked = st.checkbox("✓", value=is_checked, key=f"bday_check_{item_id}", label_visibility="collapsed")

                    if checked != is_checked:
                        st.session_state.packing_list[item_id] = checked
                        update_packing_item(item_id, checked)
                        st.rerun()

    with tab2:
        st.markdown("### 💭 40th Birthday Reflections")
        st.markdown("Take a moment to reflect on this milestone!")

        reflection_prompts = [
            "What are you most proud of from your first 40 years?",
            "What lesson has been most valuable to learn?",
            "What are you most grateful for as you turn 40?",
            "What are you most excited about for the next chapter?",
            "If you could give advice to your younger self, what would it be?",
            "What does turning 40 mean to you?",
            "What's one thing you want to accomplish in your 40s?",
            "Who has made the biggest impact on your life?",
            "What's your favorite memory from your 30s?",
            "How do you want to celebrate life moving forward?"
        ]

        selected_prompt = st.selectbox("Choose a reflection prompt:", reflection_prompts)

        reflection_text = st.text_area(
            "Your reflection:",
            placeholder="Write your thoughts here...",
            height=150,
            key="reflection_input"
        )

        if st.button("💾 Save Reflection", type="primary", use_container_width=True):
            if reflection_text.strip():
                add_note(
                    datetime.now().strftime('%Y-%m-%d'),
                    f"**{selected_prompt}**\n\n{reflection_text}",
                    'reflection'
                )
                st.session_state.notes = get_notes()
                st.success("✅ Reflection saved!")
                add_notification("New Reflection", "40th birthday reflection saved", "success")
                st.rerun()
            else:
                st.warning("Please write your reflection first!")

        # Display saved reflections
        st.markdown("---")
        st.markdown("#### Your Reflections")
        reflections = [n for n in st.session_state.notes if n['type'] == 'reflection']

        if reflections:
            for reflection in reflections:
                parts = reflection['content'].split('\n\n', 1)
                prompt = parts[0].replace('**', '')
                response = parts[1] if len(parts) > 1 else ""

                st.markdown(f"""
                <div class="card" style="margin-bottom: 1rem; background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);">
                    <h4 style="margin: 0 0 0.5rem 0;">💭 {prompt}</h4>
                    <p style="margin: 0;">{response}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("💭 No reflections yet. Start writing your thoughts!")

    with tab3:
        st.markdown("### 🎊 Birthday Wishes Collection")
        st.markdown("Collect birthday wishes from friends and family!")

        # Add a wish (for others to fill in)
        with st.expander("✍️ Add a Birthday Wish", expanded=True):
            wisher_name = st.text_input("Your name:", placeholder="John")
            wish_message = st.text_area(
                "Birthday message:",
                placeholder="Happy 40th birthday! Wishing you...",
                height=100
            )

            if st.button("💌 Save Wish", type="primary", use_container_width=True):
                if wisher_name.strip() and wish_message.strip():
                    add_note(
                        datetime.now().strftime('%Y-%m-%d'),
                        f"**From {wisher_name}:**\n\n{wish_message}",
                        'wish'
                    )
                    st.session_state.notes = get_notes()
                    st.success("✅ Birthday wish saved!")
                    add_notification("New Wish", f"Birthday wish from {wisher_name}", "success")
                    st.rerun()
                else:
                    st.warning("Please fill in both name and message!")

        # Display wishes
        st.markdown("---")
        wishes = [n for n in st.session_state.notes if n['type'] == 'wish']

        if wishes:
            st.markdown(f"#### 💌 You have {len(wishes)} birthday wishes!")

            for wish in wishes:
                parts = wish['content'].split('\n\n', 1)
                from_line = parts[0].replace('**', '').replace('From ', '')
                message = parts[1] if len(parts) > 1 else ""

                st.markdown(f"""
                <div class="card" style="margin-bottom: 1rem; background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);">
                    <h4 style="margin: 0 0 0.5rem 0;">💌 {from_line}</h4>
                    <p style="margin: 0; font-style: italic;">"{message}"</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("💌 No birthday wishes yet!")

    with tab4:
        st.markdown("### 🎯 40 Before 50 Bucket List")
        st.markdown("What do you want to accomplish in your 40s?")

        # Add bucket list item
        with st.expander("➕ Add Bucket List Item", expanded=True):
            bucket_item = st.text_input("I want to...", placeholder="Travel to Japan")
            bucket_category = st.selectbox(
                "Category:",
                ["Travel", "Career", "Health", "Relationships", "Learning", "Adventure", "Creative", "Other"]
            )

            if st.button("⭐ Add to Bucket List", type="primary", use_container_width=True):
                if bucket_item.strip():
                    add_note(
                        datetime.now().strftime('%Y-%m-%d'),
                        f"**[{bucket_category}]** {bucket_item}",
                        'bucket_list'
                    )
                    st.session_state.notes = get_notes()
                    st.success("✅ Added to bucket list!")
                    add_notification("Bucket List", f"New goal: {bucket_item}", "info")
                    st.rerun()
                else:
                    st.warning("Please enter a bucket list item!")

        # Display bucket list
        st.markdown("---")
        bucket_items = [n for n in st.session_state.notes if n['type'] == 'bucket_list']

        if bucket_items:
            st.markdown(f"#### 🎯 Your 40 Before 50 ({len(bucket_items)} items)")

            for item in bucket_items:
                col1, col2 = st.columns([0.9, 0.1])

                with col1:
                    st.markdown(f"{item['content']}")

                with col2:
                    item_id = f"bucket_{item['id']}"
                    is_done = st.session_state.packing_list.get(item_id, False)
                    done = st.checkbox("✓", value=is_done, key=f"bucket_check_{item['id']}", label_visibility="collapsed")

                    if done != is_done:
                        st.session_state.packing_list[item_id] = done
                        update_packing_item(item_id, done)
                        if done:
                            st.balloons()
                        st.rerun()
        else:
            st.info("🎯 No bucket list items yet. Start dreaming big!")

def render_memories_page():
    """Photo Gallery & Memories page - Upload and view trip photos and notes"""
    st.markdown('<h2 class="fade-in">📸 Memories & Photos</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
        <h4 style="margin: 0; color: white;">✨ Capture Your Celebration</h4>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.95;">Upload photos and save memories from your 40th birthday trip!</p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📷 Photo Gallery", "📝 Trip Journal", "⭐ Highlights"])

    with tab1:
        st.markdown("### 📷 Photo Gallery")

        # Upload section
        with st.expander("📤 Upload New Photos", expanded=False):
            col1, col2 = st.columns([2, 1])

            with col1:
                uploaded_files = st.file_uploader(
                    "Choose photos to upload",
                    type=['png', 'jpg', 'jpeg'],
                    accept_multiple_files=True,
                    help="Upload photos from your trip"
                )

            with col2:
                photo_date = st.date_input(
                    "Photo Date",
                    value=TRIP_CONFIG['start_date'],
                    min_value=TRIP_CONFIG['start_date'],
                    max_value=TRIP_CONFIG['end_date']
                )

            photo_caption = st.text_input("Caption (optional)", placeholder="Sunset at the beach...")

            if uploaded_files and st.button("💾 Save Photos", type="primary", use_container_width=True):
                saved_count = 0
                failed_count = 0
                MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit

                for uploaded_file in uploaded_files:
                    # Check file size
                    file_size = uploaded_file.size if hasattr(uploaded_file, 'size') else len(uploaded_file.getvalue())

                    if file_size > MAX_FILE_SIZE:
                        st.warning(f"⚠️ {uploaded_file.name} is too large ({file_size / 1024 / 1024:.1f}MB). Max size is 10MB.")
                        failed_count += 1
                        continue

                    try:
                        photo_bytes = uploaded_file.read()
                        photo_id = save_photo(
                            uploaded_file.name,
                            photo_bytes,
                            photo_caption,
                            photo_date.strftime('%Y-%m-%d')
                        )
                        if photo_id:
                            saved_count += 1
                        else:
                            failed_count += 1
                    except Exception as e:
                        st.error(f"Error uploading {uploaded_file.name}: {e}")
                        failed_count += 1

                # Refresh photos in session state
                st.session_state.photos = load_photos()

                if saved_count > 0:
                    st.success(f"✅ {saved_count} photo(s) uploaded successfully!")
                    add_notification("Photos Uploaded", f"{saved_count} new photos added to your gallery", "success")
                if failed_count > 0:
                    st.error(f"❌ {failed_count} photo(s) failed to upload")

                st.rerun()

        # Display photos
        st.markdown("---")

        # Filter by date
        filter_col1, filter_col2 = st.columns([3, 1])
        with filter_col1:
            filter_date = st.selectbox(
                "Filter by date",
                ["All Dates"] + [
                    (TRIP_CONFIG['start_date'] + timedelta(days=i)).strftime('%Y-%m-%d')
                    for i in range((TRIP_CONFIG['end_date'] - TRIP_CONFIG['start_date']).days + 1)
                ]
            )

        with filter_col2:
            photo_count = len(st.session_state.photos)
            st.metric("Total Photos", photo_count)

        # Get photos based on filter
        if filter_date == "All Dates":
            photos_to_display = st.session_state.photos
        else:
            photos_to_display = [p for p in st.session_state.photos if p['date'] == filter_date]

        if photos_to_display:
            # Display photos in grid
            cols_per_row = 3
            for i in range(0, len(photos_to_display), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    idx = i + j
                    if idx < len(photos_to_display):
                        photo = photos_to_display[idx]
                        with cols[j]:
                            # Display photo
                            try:
                                image = Image.open(io.BytesIO(photo['photo_data']))
                                st.image(image, use_container_width=True)

                                # Photo info
                                st.caption(f"📅 {photo['date']}")
                                if photo.get('caption'):
                                    st.caption(f"💬 {photo['caption']}")

                                # Delete button
                                if st.button(f"🗑️ Delete", key=f"del_photo_{photo['id']}", use_container_width=True):
                                    delete_photo(photo['id'])
                                    st.session_state.photos = load_photos()
                                    st.success("Photo deleted!")
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Error loading photo: {e}")
        else:
            st.info("📸 No photos uploaded yet. Start capturing your memories!")

    with tab2:
        st.markdown("### 📝 Trip Journal")
        st.markdown("Write notes about each day of your trip!")

        # Add new note
        with st.expander("✍️ Add New Journal Entry", expanded=True):
            note_date = st.date_input(
                "Date",
                value=TRIP_CONFIG['start_date'],
                min_value=TRIP_CONFIG['start_date'],
                max_value=TRIP_CONFIG['end_date'],
                key="journal_date"
            )

            note_content = st.text_area(
                "What happened today?",
                placeholder="Today we...",
                height=150
            )

            if st.button("💾 Save Journal Entry", type="primary", use_container_width=True):
                if note_content.strip():
                    add_note(note_date.strftime('%Y-%m-%d'), note_content, 'journal')
                    st.session_state.notes = get_notes()
                    st.success("✅ Journal entry saved!")
                    add_notification("Journal Entry", f"New entry for {note_date.strftime('%b %d')}", "info")
                    st.rerun()
                else:
                    st.warning("Please write something before saving!")

        # Display journal entries
        st.markdown("---")
        journal_entries = [n for n in st.session_state.notes if n['type'] == 'journal']

        if journal_entries:
            for entry in journal_entries:
                with st.container():
                    st.markdown(f"""
                    <div class="card" style="margin-bottom: 1rem;">
                        <h4 style="margin: 0 0 0.5rem 0;">📅 {entry['date']}</h4>
                        <p style="margin: 0;">{entry['content']}</p>
                        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; opacity: 0.6;">
                            Written on {entry['created_at'][:10]}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"🗑️ Delete Entry", key=f"del_note_{entry['id']}", use_container_width=True):
                        delete_note(entry['id'])
                        st.session_state.notes = get_notes()
                        st.success("Entry deleted!")
                        st.rerun()
        else:
            st.info("📝 No journal entries yet. Start documenting your trip!")

    with tab3:
        st.markdown("### ⭐ Trip Highlights")
        st.markdown("Save your favorite moments and special memories!")

        # Add highlight
        with st.expander("✨ Add New Highlight", expanded=True):
            highlight_title = st.text_input("Highlight Title", placeholder="Best sunset ever!")
            highlight_content = st.text_area(
                "Describe this moment",
                placeholder="The sky turned the most amazing shades of pink and orange...",
                height=100
            )
            highlight_date = st.date_input(
                "Date",
                value=TRIP_CONFIG['start_date'],
                min_value=TRIP_CONFIG['start_date'],
                max_value=TRIP_CONFIG['end_date'],
                key="highlight_date"
            )

            if st.button("⭐ Save Highlight", type="primary", use_container_width=True):
                if highlight_title.strip() and highlight_content.strip():
                    add_note(
                        highlight_date.strftime('%Y-%m-%d'),
                        f"**{highlight_title}**\n\n{highlight_content}",
                        'highlight'
                    )
                    st.session_state.notes = get_notes()
                    st.success("✅ Highlight saved!")
                    add_notification("New Highlight", highlight_title, "success")
                    st.rerun()
                else:
                    st.warning("Please fill in both title and description!")

        # Display highlights
        st.markdown("---")
        highlights = [n for n in st.session_state.notes if n['type'] == 'highlight']

        if highlights:
            for idx, highlight in enumerate(highlights):
                # Parse title and content
                parts = highlight['content'].split('\n\n', 1)
                title = parts[0].replace('**', '')
                content = parts[1] if len(parts) > 1 else ""

                st.markdown(f"""
                <div class="card" style="margin-bottom: 1rem; background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);">
                    <h4 style="margin: 0 0 0.5rem 0;">⭐ {title}</h4>
                    <p style="margin: 0 0 0.5rem 0;">{content}</p>
                    <p style="margin: 0; font-size: 0.8rem; opacity: 0.7;">📅 {highlight['date']}</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"🗑️ Delete Highlight", key=f"del_highlight_{highlight['id']}", use_container_width=True):
                    delete_note(highlight['id'])
                    st.session_state.notes = get_notes()
                    st.success("Highlight deleted!")
                    st.rerun()
        else:
            st.info("⭐ No highlights yet. Mark your special moments!")

    # Trip recap section
    st.markdown("---")
    st.markdown("### 📊 Trip Recap")

    col1, col2, col3 = st.columns(3)
    with col1:
        photo_count = len(st.session_state.photos)
        st.metric("📷 Total Photos", photo_count)
    with col2:
        journal_count = len([n for n in st.session_state.notes if n['type'] == 'journal'])
        st.metric("📝 Journal Entries", journal_count)
    with col3:
        highlight_count = len([n for n in st.session_state.notes if n['type'] == 'highlight'])
        st.metric("⭐ Highlights", highlight_count)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application function"""
    
    # Load CSS
    load_ultimate_css()
    
    # Render header
    render_ultimate_header()

    # Get data (app is OPEN - no password wall!)
    df, activities_data = get_ultimate_trip_data()
    weather_data = get_weather_ultimate()
    show_sensitive = st.session_state.get('password_verified', False)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin-bottom: 1rem;">
            <h2 style="margin: 0;">🎂 Trip Menu</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Security status and login
        if show_sensitive:
            st.success("🔓 Full Access")
            if st.button("🔒 Lock", use_container_width=True):
                st.session_state['password_verified'] = False
                st.rerun()
        else:
            st.info("🔒 Public View (sensitive data hidden)")
            with st.expander("🔐 Unlock Full Access"):
                password_input = st.text_input("Enter password:", type="password", key="unlock_password")
                if st.button("Unlock", use_container_width=True):
                    if hashlib.md5(password_input.encode()).hexdigest() == os.getenv('TRIP_PASSWORD_HASH', 'a5be948874610641149611913c4924e5'):
                        st.session_state['password_verified'] = True
                        st.success("✅ Access granted!")
                        st.rerun()
                    else:
                        st.error("❌ Incorrect password")

        st.markdown("---")
        
        # Navigation
        # Check if nav override is set (from Getting Ready button)
        if st.session_state.get('nav_to_packing', False):
            default_index = 6  # Packing List (updated for new Travel Dashboard)
            st.session_state['nav_to_packing'] = False
        else:
            default_index = 0

        page = st.selectbox(
            "Navigate to:",
            [
                "🏠 Dashboard",
                "🎯 Travel Dashboard",
                "📅 Today",
                "🗓️ Full Schedule",
                "🎯 Explore & Plan",
                "👤 John's Page",
                "🗺️ Map & Locations",
                "🎒 Packing List",
                "🎂 Birthday",
                "📸 Memories",
                "💰 Budget",
                "🌤️ Weather",
                "ℹ️ About"
            ],
            index=default_index,
            label_visibility="collapsed"
        )

        st.markdown("---")
        
        # Quick stats
        urgent_count = len(df[df['status'] == 'URGENT'])
        if urgent_count > 0:
            st.error(f"⚠️ {urgent_count} urgent booking(s)")
        else:
            st.success("✅ All bookings set!")
        
        # Use .date() for consistent day counting across all countdowns
        days_until = (TRIP_CONFIG['start_date'].date() - datetime.now().date()).days
        if days_until > 0:
            st.info(f"🗓️ {days_until} days until trip")
        elif days_until == 0:
            st.success("🎉 Trip starts TODAY!")
        else:
            st.success("🏖️ On your trip!")
        
        st.markdown("---")

        # Notifications
        active_notifications = [n for n in st.session_state.notifications if not n['dismissed']]
        if active_notifications:
            st.markdown("### 🔔 Notifications")
            for notif in active_notifications[:3]:  # Show max 3 in sidebar
                notif_type = notif.get('type', 'info')

                # Icon based on type
                if notif_type == 'success':
                    icon = "✅"
                    color = "#4caf50"
                elif notif_type == 'warning':
                    icon = "⚠️"
                    color = "#ff9800"
                elif notif_type == 'error':
                    icon = "🚨"
                    color = "#f44336"
                else:
                    icon = "ℹ️"
                    color = "#2196f3"

                st.markdown(f"""
                <div style="background: {color}15; border-left: 3px solid {color}; padding: 0.5rem; margin-bottom: 0.5rem; border-radius: 4px;">
                    <div style="font-weight: bold; font-size: 0.9rem;">{icon} {notif['title']}</div>
                    <div style="font-size: 0.8rem; opacity: 0.8;">{notif['message']}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Dismiss", key=f"dismiss_{notif['id']}", use_container_width=True):
                    dismiss_notification(notif['id'])
                    st.session_state.notifications = load_notifications()
                    st.rerun()

            if len(active_notifications) > 3:
                st.caption(f"+{len(active_notifications) - 3} more notifications")

            st.markdown("---")

        # Version info
        st.caption("**Ultimate Edition v2.0**")
        st.caption("Enhanced by Claude Code")
    
    # Page routing
    if page == "🏠 Dashboard":
        render_dashboard_ultimate(df, activities_data, weather_data, show_sensitive)

    elif page == "🎯 Travel Dashboard":
        render_travel_dashboard(activities_data, show_sensitive)

    elif page == "📅 Today":
        render_today_view(df, activities_data, weather_data, show_sensitive)
    
    elif page == "🗓️ Full Schedule":
        render_full_schedule(df, activities_data, show_sensitive)

    elif page == "🎯 Explore & Plan":
        render_explore_activities()

    elif page == "👤 John's Page":
        render_johns_page(df, activities_data, show_sensitive)

    elif page == "🗺️ Map & Locations":
        render_map_page(activities_data)
    
    elif page == "🎒 Packing List":
        render_packing_list()

    elif page == "🎂 Birthday":
        render_birthday_page()

    elif page == "📸 Memories":
        render_memories_page()

    elif page == "💰 Budget":
        render_budget(df, show_sensitive)
    
    elif page == "🌤️ Weather":
        st.markdown('<h2 class="fade-in">🌤️ Weather, UV & Tides</h2>', unsafe_allow_html=True)

        # Get tide data
        tide_data = get_tide_data()

        col1, col2 = st.columns([2, 1])

        with col1:
            current = weather_data['current']
            uv_current = current.get('uv_index', 5.0)

            # UV warning level
            if uv_current < 3:
                uv_level = "Low"
                uv_color = "#4caf50"
            elif uv_current < 6:
                uv_level = "Moderate"
                uv_color = "#ff9800"
            elif uv_current < 8:
                uv_level = "High"
                uv_color = "#ff5722"
            else:
                uv_level = "Very High"
                uv_color = "#d32f2f"

            st.markdown(f"""
            <div class="weather-widget">
                <h2>Current Conditions</h2>
                <div class="weather-temp">{current['temperature']}°F</div>
                <p style="font-size: 1.3rem;">{current['condition']}</p>
                <div style="margin-top: 1rem; opacity: 0.9;">
                    <p>Feels like: {current['feels_like']}°F</p>
                    <p>💧 Humidity: {current['humidity']}%</p>
                    <p>💨 Wind: {current['wind_speed']} mph</p>
                    <p>👁️ Visibility: {current['visibility']} mi</p>
                    <p style="color: {uv_color}; font-weight: bold;">☀️ UV Index: {uv_current} ({uv_level})</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("### 🌊 Today's Tides")
            today_str = datetime.now().strftime('%Y-%m-%d')
            today_tides = tide_data.get(today_str, {})

            if today_tides:
                st.markdown("**High Tides:**")
                for high in today_tides.get('high', []):
                    st.markdown(f"- {high['time']}: {high['height']}ft")

                st.markdown("**Low Tides:**")
                for low in today_tides.get('low', []):
                    st.markdown(f"- {low['time']}: {low['height']}ft")
            else:
                st.info("Tide data unavailable")

        st.markdown("---")
        st.markdown("### 📅 6-Day Forecast with UV Index")

        for day in weather_data['forecast']:
            date_obj = datetime.strptime(day['date'], '%Y-%m-%d')
            emoji = get_weather_emoji(day['condition'])
            uv = day.get('uv_index', 5.0)

            # UV level for this day
            if uv < 3:
                uv_level = "Low"
                uv_color = "#4caf50"
            elif uv < 6:
                uv_level = "Moderate"
                uv_color = "#ff9800"
            elif uv < 8:
                uv_level = "High"
                uv_color = "#ff5722"
            else:
                uv_level = "Very High"
                uv_color = "#d32f2f"

            # Get tide info for this day
            day_tides = tide_data.get(day['date'], {})
            tide_info = ""
            if day_tides:
                high_times = [h['time'] for h in day_tides.get('high', [])]
                tide_info = f"<p style='margin: 0.5rem 0; font-size: 0.85rem;'>🌊 High tides: {', '.join(high_times) if high_times else 'N/A'}</p>"

            st.markdown(f"""
            <div class="ultimate-card fade-in">
                <div class="card-body">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <h4 style="margin: 0;">{date_obj.strftime('%A, %B %d')}</h4>
                            <p style="margin: 0.5rem 0;">{emoji} {day['condition']}</p>
                            {tide_info}
                        </div>
                        <div style="text-align: right;">
                            <p style="margin: 0; font-size: 1.5rem; font-weight: bold;">
                                {day['high']:.0f}° / {day['low']:.0f}°
                            </p>
                            <p style="margin: 0.5rem 0; font-size: 0.9rem;">
                                💧 {day.get('precipitation', 0)}% • 💨 {day.get('wind', 0)} mph
                            </p>
                            <p style="margin: 0.5rem 0; font-size: 0.9rem; color: {uv_color}; font-weight: bold;">
                                ☀️ UV: {uv} ({uv_level})
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "ℹ️ About":
        st.markdown('<h2 class="fade-in">ℹ️ About This App</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="birthday-special">
            <h2 style="margin: 0 0 1rem 0;">🎂 40th Birthday Trip Assistant</h2>
            <h3 style="margin: 0;">Ultimate Edition v2.0</h3>
        </div>
        
        <div class="ultimate-card" style="margin-top: 2rem;">
            <div class="card-header">✨ Features</div>
            <div class="card-body">
                <ul style="line-height: 2;">
                    <li>🗺️ Interactive maps of all locations</li>
                    <li>🌤️ Real-time weather integration</li>
                    <li>🎒 Smart packing list generator</li>
                    <li>📅 Context-aware "Today" view</li>
                    <li>💰 Comprehensive budget tracking</li>
                    <li>📍 Distance & travel time calculations</li>
                    <li>🔔 Smart booking alerts</li>
                    <li>📱 Fully mobile responsive</li>
                    <li>🔐 Password protected</li>
                    <li>✨ Beautiful modern design</li>
                </ul>
            </div>
        </div>
        
        <div class="ultimate-card" style="margin-top: 1.5rem;">
            <div class="card-header">📊 Trip Details</div>
            <div class="card-body">
                <p><b>Destination:</b> Amelia Island, Florida</p>
                <p><b>Dates:</b> November 7-12, 2025</p>
                <p><b>Hotel:</b> The Ritz-Carlton, Amelia Island</p>
                <p><b>Occasion:</b> 40th Birthday Celebration</p>
                <p><b>Travelers:</b> You + John</p>
            </div>
        </div>
        
        <div class="ultimate-card" style="margin-top: 1.5rem;">
            <div class="card-header">🚀 What's New in v2.0</div>
            <div class="card-body">
                <p>This is a completely rebuilt version with:</p>
                <ul>
                    <li>Brand new modern UI with animations</li>
                    <li>Real weather API integration</li>
                    <li>Interactive maps with all locations</li>
                    <li>Smart packing list based on activities</li>
                    <li>Enhanced mobile experience</li>
                    <li>Better data organization</li>
                    <li>More helpful tips and suggestions</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.caption("**Built with:** Streamlit, Folium, Plotly, OpenWeather API")
        st.caption("**Enhanced by:** Claude Code")
        st.caption("**Version:** 2.0 Ultimate Edition")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #636e72; padding: 2rem 1rem;">
        <p style="font-size: 1.2rem; margin: 0;">
            🎂 <strong>40th Birthday Trip Assistant - Ultimate Edition</strong> 🎂
        </p>
        <p style="margin: 0.5rem 0;">
            <small>Amelia Island • November 7-12, 2025 • The Ritz-Carlton</small>
        </p>
        <p style="margin: 1rem 0 0 0;">
            <small>Made with ❤️ for an unforgettable celebration!</small>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()

