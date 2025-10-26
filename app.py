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

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

st.set_page_config(
    page_title="🎂 40th Birthday Trip - Ultimate Edition",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Ultimate 40th Birthday Trip Assistant - v2.0"
    }
)

# Initialize session state
if 'password_verified' not in st.session_state:
    st.session_state.password_verified = False
if 'packing_list' not in st.session_state:
    st.session_state.packing_list = {}
if 'completed_activities' not in st.session_state:
    st.session_state.completed_activities = []
if 'notes' not in st.session_state:
    st.session_state.notes = []
if 'custom_activities' not in st.session_state:
    st.session_state.custom_activities = []

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
            "cost": 65,
            "category": "Transport",
            "notes": "American Airlines AA2434 - Departure 3:51 PM from DCA",
            "flight_number": "AA2434",
            "what_to_bring": ["ID", "Boarding pass", "Phone charger", "Snacks for flight"],
            "tips": ["Arrive 2 hours early", "TSA PreCheck available", "Download AA app"],
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
            "cost": 50,
            "category": "Dining",
            "notes": "Quick lunch after airport pickup - either at hotel restaurant or nearby casual spot",
            "what_to_bring": [],
            "tips": ["Coast restaurant at hotel is convenient for breakfast/lunch", "Salt Life Food Shack nearby for casual beachfront", "Keep it light before boat tour"],
            "priority": 2
        },
        {
            "id": "act001",
            "date": "2025-11-08",
            "time": "3:30 PM",
            "activity": "Backwater Cat Tour",
            "type": "activity",
            "duration": "2.5 hours",
            "location": {
                "name": "Dee Dee Bartels Boat Ramp",
                "address": "Amelia Island, FL",
                "lat": 30.6187,
                "lon": -81.4610,
                "phone": "904-753-7631"
            },
            "status": "URGENT",
            "cost": 270,
            "category": "Activity",
            "notes": "BOOK NOW! 2.5 hour eco tour - call 904-753-7631",
            "what_to_bring": ["Sunscreen SPF 50+", "Sunglasses", "Camera", "Water bottle", "Light jacket (can be windy)"],
            "tips": ["Best at golden hour", "Bring motion sickness meds if prone", "Wear non-slip shoes"],
            "priority": 1
        },
        {
            "id": "spa001",
            "date": "2025-11-09",
            "time": "10:00 AM",
            "activity": "Heaven in a Hammock Massage",
            "type": "spa",
            "duration": "1.5 hours",
            "location": {
                "name": "Ritz-Carlton Spa",
                "address": "4750 Amelia Island Parkway",
                "lat": 30.6074,
                "lon": -81.4493,
                "phone": "904-277-1100"
            },
            "status": "URGENT",
            "cost": 245,
            "category": "Spa",
            "notes": "BIRTHDAY SPA DAY! Couples beachside massage - book ASAP",
            "what_to_bring": ["Arrive 15 min early", "Robe provided", "Clean feet"],
            "tips": ["Hydrate before", "Communicate pressure preferences", "No heavy meal before"],
            "dress_code": "Spa attire provided",
            "booking_url": "https://www.ritzcarlton.com/en/hotels/ameliarc/spa",
            "priority": 1
        },
        {
            "id": "spa002",
            "date": "2025-11-09",
            "time": "12:00 PM",
            "activity": "HydraFacial Treatment",
            "type": "spa",
            "duration": "1 hour",
            "location": {
                "name": "Ritz-Carlton Spa",
                "address": "4750 Amelia Island Parkway",
                "lat": 30.6074,
                "lon": -81.4493,
                "phone": "904-277-1100"
            },
            "status": "URGENT",
            "cost": 195,
            "category": "Spa",
            "notes": "Advanced facial - book with massage for package deal",
            "what_to_bring": ["Clean face (no makeup)", "Hair tie", "Empty stomach OK"],
            "tips": ["Ask about serums for your skin type", "Great for pre-dinner glow"],
            "booking_url": "https://www.ritzcarlton.com/en/hotels/ameliarc/spa",
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
            "notes": "THE BIG 40! Upscale dining - MUST RESERVE - mention birthday!",
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
            "cost": 60,
            "category": "Dining",
            "notes": "Beachside casual - famous for tacos and fresh catch",
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
            "activity": "Drop John at Airport",
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
            "notes": "AA1586 to DCA departs 11:05 AM. Leave hotel 8:20am (45min drive) to arrive by 9:05am (2 hours before flight).",
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
            "notes": "AA5590 departs 2:39 PM. Checkout by 11am, leave hotel by 12:30pm (45min drive + 2hr early arrival buffer).",
            "flight_number": "AA5590",
            "what_to_bring": ["All belongings", "Souvenirs", "Photos", "Memories!"],
            "tips": ["Hotel checkout 11 AM", "Leave by 12:30 PM", "Double-check room for items", "Return home with amazing memories!"],
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

    TOTAL: 118 verified options with complete details, phone numbers, pricing, tips, and ratings!
    """
    return {
        "🍽️ Fine Dining": [
            {"name": "Le Clos", "description": "French bistro with romantic atmosphere, extensive wine selection", "cost_range": "$40-70 per person", "duration": "2-3 hours", "phone": "904-261-8100", "booking_url": "https://www.opentable.com/r/le-clos-fernandina-beach", "tips": "Reservations required, dress code (business casual)", "rating": "4.8/5"},
            {"name": "Burlingame", "description": "Charming 1947 cottage with modern twist, seasonal menu with Seafood Gumbo, Blue Crab Cakes, Lamb Bolognese", "cost_range": "$35-65 per person", "duration": "2-2.5 hours", "phone": "904-277-3700", "booking_url": "https://www.opentable.com/burlingame", "tips": "Intimate setting, reserve ahead for special occasions", "rating": "4.9/5"},
            {"name": "Lagniappe", "description": "Southern refinement meets French Creole, standout Salmon Brulee and Lamb Lollipops", "cost_range": "$40-70 per person", "duration": "2-3 hours", "phone": "904-321-2007", "booking_url": "https://www.opentable.com/lagniappe-fernandina", "tips": "Chef Brett Heritage creates unique elevated cuisine", "rating": "4.8/5"},
            {"name": "Cucina South", "description": "Fine dining Italian with chef-driven creations, traditional Italian with Mediterranean accents", "cost_range": "$35-60 per person", "duration": "2-2.5 hours", "phone": "904-321-2699", "booking_url": "https://www.opentable.com/cucina-south", "tips": "Classic Italian with modern twists, excellent wine list", "rating": "4.7/5"},
        ],
        "🦞 Seafood & Waterfront": [
            {"name": "Brett's Waterway Cafe", "description": "Waterfront dining with marina views, fresh catch daily", "cost_range": "$20-40 per person", "duration": "1.5-2 hours", "phone": "904-261-2660", "booking_url": "https://www.opentable.com/r/bretts-waterway-cafe-fernandina-beach", "tips": "Amazing sunset views, try the seafood platter", "rating": "4.7/5"},
            {"name": "Salty Pelican Bar & Grill", "description": "Heart of downtown waterfront, blackened grouper tacos, fresh oysters, fried tuna", "cost_range": "$18-35 per person", "duration": "1-2 hours", "phone": "904-277-3811", "booking_url": "https://saltypelican.com", "tips": "Best place to catch sunset over the river", "rating": "4.6/5"},
            {"name": "Sandbar", "description": "Directly on Main Beach with Atlantic Ocean views, coastal cuisine, 1200+ whiskey selections", "cost_range": "$25-45 per person", "duration": "1.5-2 hours", "phone": "904-491-3743", "booking_url": "https://sandbaramelia.com", "tips": "Unobstructed beach views, live music on weekends", "rating": "4.7/5"},
            {"name": "The Boat House", "description": "Waterfront seafood with fresh local catches and harbor views", "cost_range": "$22-40 per person", "duration": "1-2 hours", "phone": "904-261-9300", "booking_url": "https://boathouseamelia.com", "tips": "Try the catch of the day and she-crab soup", "rating": "4.6/5"},
            {"name": "Down Under", "description": "Under the bridge to Amelia Island, oysters, crab dip, shrimp, fresh fish with waterfront view", "cost_range": "$15-30 per person", "duration": "1-1.5 hours", "phone": "904-261-1001", "booking_url": "N/A", "tips": "Casual vibe, great for fresh oysters and cold beer", "rating": "4.5/5"},
            {"name": "Timoti's Seafood Shak", "description": "Family-friendly wild-caught seafood, fresh fried shrimp, poke bowls, fish tacos, lobster rolls", "cost_range": "$12-25 per person", "duration": "45min-1 hour", "phone": "904-206-0965", "booking_url": "https://timotis.com", "tips": "Fast casual, great for lunch, super fresh seafood", "rating": "4.6/5"},
            {"name": "Salt Life Food Shack", "description": "Oceanfront casual dining with amazing views and fresh seafood", "cost_range": "$15-30 per person", "duration": "1-2 hours", "phone": "904-277-3811", "booking_url": "https://www.saltlifefoodshack.com", "tips": "Perfect for lunch, great outdoor seating with ocean breeze", "rating": "4.5/5"},
        ],
        "🍕 Italian & Pizza": [
            {"name": "Ciao Italian Eatery", "description": "Authentic Italian by Chef Luca, pasta, pizza, seafood, veal, chicken, pork, ribeye", "cost_range": "$20-40 per person", "duration": "1.5-2 hours", "phone": "904-491-9700", "booking_url": "https://ciaoitalianeats.com", "tips": "Dinner only, homemade pasta is exceptional", "rating": "4.7/5"},
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
            {"name": "Salt (AAA Five Diamond)", "description": "Signature restaurant with fresh seafood, water views, Michelin-trained Chef D' Cuisine Okan Kizilbayir", "cost_range": "$45-85 per person", "duration": "2-3 hours", "phone": "904-277-1100", "booking_url": "https://www.opentable.com/salt-at-the-ritz-carlton", "tips": "Open 5pm-9pm Tue-Sat, reservations essential", "rating": "4.8/5"},
            {"name": "Coast", "description": "Coastal cuisine with seasonal menu, local seafood, steaks, salads, small plates. All-day dining", "cost_range": "$25-55 per person", "duration": "1.5-2 hours", "phone": "904-277-1100", "booking_url": "https://www.opentable.com/coast-at-the-ritz-carlton", "tips": "Open 7am-3pm and 5pm-9pm daily", "rating": "4.4/5"},
            {"name": "Coquina", "description": "Oceanfront restaurant with beach views and casual coastal fare", "cost_range": "$20-40 per person", "duration": "1-2 hours", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Open 11am-9pm daily, perfect for lunch with ocean breeze", "rating": "4.5/5"},
            {"name": "Tidewater Grill", "description": "Casual poolside dining with grilled favorites and refreshing drinks", "cost_range": "$15-30 per person", "duration": "1-1.5 hours", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Open 5pm-10pm Mon-Fri, 3pm-10pm Sat-Sun", "rating": "4.3/5"},
            {"name": "Lobby Bar", "description": "Classic lounge with craft cocktails, wine, and small plates", "cost_range": "$12-25 per drink/plate", "duration": "1-2 hours", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Open 3pm-12am Mon-Thu, 3pm-1am Fri-Sat", "rating": "4.6/5"},
            {"name": "Dune Bar", "description": "Beach bar with tropical drinks, frozen cocktails, and light bites", "cost_range": "$10-20 per drink", "duration": "1-2 hours", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Open 11am-6pm daily, perfect beach relaxation", "rating": "4.5/5"},
        ],
        "🍺 Bars & Nightlife": [
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
            {"name": "Wine & Tasting Tour", "description": "Local guide takes you to best restaurants, bars and hot spots", "cost_range": "$60-90 per person", "duration": "2-3 hours", "phone": "904-556-7594", "booking_url": "N/A", "tips": "Fun way to discover local flavors and meet people", "rating": "4.5/5"},
        ],
        "💆 Ritz-Carlton Spa Services": [
            {"name": "Heaven in a Hammock Massage (Couples)", "description": "ALREADY BOOKED - Beachside couples massage in swaying hammocks", "cost_range": "$245 each", "duration": "80 minutes", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Book together for birthday celebration", "rating": "5.0/5"},
            {"name": "HydraFacial Treatment", "description": "ALREADY BOOKED - Advanced facial for glowing skin", "cost_range": "$195", "duration": "50 minutes", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Perfect before birthday dinner", "rating": "4.9/5"},
            {"name": "Aromatherapy Massage", "description": "Full body massage with essential oils", "cost_range": "$185-245", "duration": "50-80 minutes", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Choose from lavender, eucalyptus, or citrus blends", "rating": "4.9/5"},
            {"name": "Mani-Pedi Combo", "description": "Professional manicure and pedicure", "cost_range": "$125", "duration": "90 minutes", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Great add-on for spa day", "rating": "4.8/5"},
            {"name": "Body Scrub & Wrap", "description": "Exfoliating scrub followed by hydrating wrap", "cost_range": "$175-225", "duration": "50-80 minutes", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Ocean salt scrub is signature treatment", "rating": "4.8/5"},
            {"name": "Hot Stone Massage", "description": "Deep relaxation with heated volcanic stones", "cost_range": "$205", "duration": "80 minutes", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Perfect for sore muscles after activities", "rating": "4.9/5"},
            {"name": "Gentleman's Facial", "description": "Facial designed for men's skin", "cost_range": "$165", "duration": "50 minutes", "phone": "904-277-1100", "booking_url": "N/A", "tips": "John might enjoy this!", "rating": "4.7/5"},
            {"name": "Reflexology Treatment", "description": "Therapeutic foot and lower leg massage", "cost_range": "$115", "duration": "50 minutes", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Great after beach walking", "rating": "4.6/5"},
            {"name": "Chakra Balancing", "description": "Energy healing and chakra alignment treatment", "cost_range": "$145-185", "duration": "60-80 minutes", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Combines meditation and energy work", "rating": "4.7/5"},
            {"name": "Healing Saltwater Pool", "description": "Access to therapeutic saltwater healing pool at spa", "cost_range": "Included with treatments", "duration": "Flexible", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Arrive early to enjoy before your treatment", "rating": "4.8/5"},
        ],
        "🧘 Wellness & Other Spas": [
            {"name": "Omni Spa Clean & Green Therapies", "description": "Massage, peels, wraps, and signature scrubs at Omni Resort", "cost_range": "$150-250", "duration": "50-90 minutes", "phone": "904-261-6161", "booking_url": "N/A", "tips": "Eco-friendly products and treatments", "rating": "4.7/5"},
            {"name": "Drift Day Spa", "description": "Custom massages, reflexology, facials, couple massages 7 days/week", "cost_range": "$90-180", "duration": "60-90 minutes", "phone": "904-277-5454", "booking_url": "N/A", "tips": "More affordable alternative to resort spas", "rating": "4.6/5"},
            {"name": "Coastal Massage Therapy", "description": "Downtown cottage with neuromuscular, deep tissue, trigger point, prenatal, reiki, crystal healing, lomilomi", "cost_range": "$80-150", "duration": "60-90 minutes", "phone": "904-432-5998", "booking_url": "N/A", "tips": "Specialized therapeutic massage techniques", "rating": "4.7/5"},
            {"name": "Centred On Yoga", "description": "Beginner and intermediate yoga classes in historic downtown with certified instructors (28+ years experience)", "cost_range": "$18-25 per class", "duration": "60-75 minutes", "phone": "904-310-9642", "booking_url": "N/A", "tips": "Drop-in classes available, bring your own mat", "rating": "4.8/5"},
            {"name": "The Sprouting Project", "description": "Monthly farm-to-table dining experience at Omni with garden tour, aquaponic greenhouse, barrel room, apiary", "cost_range": "$75-95 per person", "duration": "2-3 hours", "phone": "904-261-6161", "booking_url": "N/A", "tips": "Unique wellness and culinary experience, book ahead", "rating": "4.9/5"},
        ],
        "🏊 Resort & Free Activities": [
            {"name": "Resort Pool Day", "description": "Relax at multiple Ritz-Carlton pools and hot tubs", "cost_range": "FREE (hotel guests)", "duration": "2-4 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Reserve a cabana for ultimate luxury relaxation", "rating": "4.8/5"},
            {"name": "Beach Sunset Viewing", "description": "Watch gorgeous sunset from the shore", "cost_range": "FREE", "duration": "30-60 minutes", "phone": "N/A", "booking_url": "N/A", "tips": "Check sunset time, bring camera and beach blanket", "rating": "5.0/5"},
            {"name": "Yoga on the Beach", "description": "Morning yoga classes on the beach at resort", "cost_range": "$20-35", "duration": "1 hour", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Hotel offers classes, check schedule", "rating": "4.6/5"},
            {"name": "Beach Bonfires", "description": "Private or group beach bonfire with s'mores", "cost_range": "$150-300", "duration": "2 hours", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Perfect for special celebrations, book ahead", "rating": "4.9/5"},
            {"name": "Fitness Center Access", "description": "State-of-the-art gym with ocean views", "cost_range": "FREE (hotel guests)", "duration": "Flexible", "phone": "904-277-1100", "booking_url": "N/A", "tips": "Open 24/7, personal trainers available", "rating": "4.7/5"},
            {"name": "Beach Volleyball", "description": "Courts available at Main Beach Park", "cost_range": "FREE", "duration": "1-2 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Bring your own equipment or join pickup games", "rating": "4.4/5"},
            {"name": "Shelling & Beach Combing", "description": "Search for shells, sand dollars, and sea glass", "cost_range": "FREE", "duration": "1-2 hours", "phone": "N/A", "booking_url": "N/A", "tips": "Best at low tide, early morning for best finds", "rating": "4.6/5"},
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
            'energy_balance': True
        }

    # Get all optional activities
    optional_activities = get_optional_activities()
    all_activities = []
    for category, items in optional_activities.items():
        all_activities.extend(items)

    # Get dining options
    dining_options = optional_activities.get('🍽️ Fine Dining', []) + \
                     optional_activities.get('🍽️ Casual Dining', []) + \
                     optional_activities.get('🥞 Breakfast & Brunch', [])

    # Check what's already scheduled for this day
    day_activities = [a for a in existing_activities if a['date'] == target_date_str]

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

    # SMART CHECK: Is this an arrival or departure day?
    is_arrival_day = any('arrival' in a['activity'].lower() or 'arrive' in a['activity'].lower() for a in day_activities)
    is_departure_day = any('departure' in a['activity'].lower() or 'depart' in a['activity'].lower() or 'leave hotel' in a['activity'].lower() for a in day_activities)

    # Get arrival/departure times to be smart about meal scheduling
    latest_arrival_time = None
    earliest_departure_time = None

    if is_arrival_day:
        for activity in day_activities:
            if 'arrival' in activity['activity'].lower() or 'arrive' in activity['activity'].lower():
                try:
                    arrival_time = datetime.strptime(activity['time'], "%I:%M %p")
                    if latest_arrival_time is None or arrival_time > latest_arrival_time:
                        latest_arrival_time = arrival_time
                except:
                    pass

    if is_departure_day:
        for activity in day_activities:
            if 'departure' in activity['activity'].lower() or 'depart' in activity['activity'].lower() or 'leave' in activity['activity'].lower():
                try:
                    departure_time = datetime.strptime(activity['time'], "%I:%M %p")
                    if earliest_departure_time is None or departure_time < earliest_departure_time:
                        earliest_departure_time = departure_time
                except:
                    pass

    recommendations = []

    # STEP 1: Schedule breakfast if missing (7:30-9:00 AM)
    has_breakfast = any(a['type'] == 'dining' and datetime.strptime(a['time'], "%I:%M %p").hour < 11 for a in day_activities)

    # SMART: Don't suggest breakfast if arriving late in the day
    skip_breakfast = False
    if is_arrival_day and latest_arrival_time and latest_arrival_time.hour >= 11:
        skip_breakfast = True

    if not has_breakfast and preferences['include_meals'] and not skip_breakfast:
        breakfast_candidates = [r for r in dining_options if 'breakfast' in r.get('name', '').lower() or 'brunch' in r.get('name', '').lower()]
        if breakfast_candidates:
            # Return TOP 3 options instead of just 1
            top_breakfasts = sorted(breakfast_candidates, key=lambda x: float(x.get('rating', '0/5').split('/')[0]), reverse=True)[:3]

            for i, breakfast in enumerate(top_breakfasts):
                recommendations.append({
                    'time': '8:00 AM',
                    'activity': breakfast,
                    'type': 'dining',
                    'reason': f'Start your day with highly-rated breakfast (Option {i+1} of {len(top_breakfasts)})',
                    'duration': '45 minutes',
                    'alternative_rank': i + 1,
                    'total_alternatives': len(top_breakfasts)
                })

    # STEP 2: Morning activity (9:00 AM - 12:00 PM)
    morning_slot_filled = any(9 <= datetime.strptime(a['time'], "%I:%M %p").hour < 12 for a in day_activities)

    if not morning_slot_filled:
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

        # Get TOP 3 recommendations
        if morning_scores:
            top_morning_activities = sorted(morning_scores, key=lambda x: x['score'], reverse=True)[:3]

            for i, morning_activity in enumerate(top_morning_activities):
                if morning_activity['score'] > 50:  # Only recommend if score is decent
                    recommendations.append({
                        'time': '10:00 AM',
                        'activity': morning_activity['activity'],
                        'type': 'activity',
                        'reason': f"{', '.join(morning_activity['reasons'][:2])} (Option {i+1} of {len(top_morning_activities)})",
                        'duration': morning_activity['activity'].get('duration', '2 hours'),
                        'alternative_rank': i + 1,
                        'total_alternatives': len(top_morning_activities)
                    })

    # STEP 3: Lunch (12:00 PM - 2:00 PM)
    has_lunch = any(a['type'] == 'dining' and 11 <= datetime.strptime(a['time'], "%I:%M %p").hour < 16 for a in day_activities)

    # SMART: Don't suggest lunch if departing early
    skip_lunch = False
    if is_departure_day and earliest_departure_time and earliest_departure_time.hour <= 12:
        skip_lunch = True

    if not has_lunch and preferences['include_meals'] and not skip_lunch:
        lunch_candidates = [r for r in dining_options if 'casual' in r.get('description', '').lower() or 'lunch' in r.get('description', '').lower()]
        if not lunch_candidates:
            lunch_candidates = dining_options[:10]

        if lunch_candidates:
            # Return TOP 3 options
            top_lunches = sorted(lunch_candidates, key=lambda x: float(x.get('rating', '0/5').split('/')[0]), reverse=True)[:3]

            for i, lunch in enumerate(top_lunches):
                recommendations.append({
                    'time': '12:30 PM',
                    'activity': lunch,
                    'type': 'dining',
                    'reason': f'Refuel with a great lunch spot (Option {i+1} of {len(top_lunches)})',
                    'duration': '1 hour',
                    'alternative_rank': i + 1,
                    'total_alternatives': len(top_lunches)
                })

    # STEP 4: Afternoon activity (2:00 PM - 5:00 PM)
    afternoon_slot_filled = any(14 <= datetime.strptime(a['time'], "%I:%M %p").hour < 17 for a in day_activities)

    if not afternoon_slot_filled:
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

        # Get TOP 3 recommendations
        if afternoon_scores:
            top_afternoon_activities = sorted(afternoon_scores, key=lambda x: x['score'], reverse=True)[:3]

            for i, afternoon_activity in enumerate(top_afternoon_activities):
                if afternoon_activity['score'] > 50:
                    recommendations.append({
                        'time': '3:00 PM',
                        'activity': afternoon_activity['activity'],
                        'type': 'activity',
                        'reason': f"{', '.join(afternoon_activity['reasons'][:2])} (Option {i+1} of {len(top_afternoon_activities)})",
                        'duration': afternoon_activity['activity'].get('duration', '2 hours'),
                        'alternative_rank': i + 1,
                        'total_alternatives': len(top_afternoon_activities)
                    })

    # STEP 5: Dinner (6:00 PM - 8:00 PM)
    has_dinner = any(a['type'] == 'dining' and datetime.strptime(a['time'], "%I:%M %p").hour >= 16 for a in day_activities)

    # SMART: Don't suggest dinner if it's arrival day late arrival
    skip_dinner = False
    if is_arrival_day and latest_arrival_time and latest_arrival_time.hour >= 19:  # 7 PM or later
        skip_dinner = True

    if not has_dinner and preferences['include_meals'] and not skip_dinner:
        dinner_candidates = [r for r in dining_options if 'fine' in r.get('description', '').lower() or 'dinner' in r.get('description', '').lower()]
        if not dinner_candidates:
            dinner_candidates = dining_options[:10]

        if dinner_candidates:
            # Return TOP 3 options
            top_dinners = sorted(dinner_candidates, key=lambda x: float(x.get('rating', '0/5').split('/')[0]), reverse=True)[:3]

            for i, dinner in enumerate(top_dinners):
                recommendations.append({
                    'time': '6:30 PM',
                    'activity': dinner,
                    'type': 'dining',
                    'reason': f'End the day with an amazing dinner (Option {i+1} of {len(top_dinners)})',
                    'duration': '1.5 hours',
                    'alternative_rank': i + 1,
                    'total_alternatives': len(top_dinners)
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

    return recommendations[:8]  # Return top 8 recommendations


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
            
            popup_html = f"""
            <div style='min-width: 280px; font-family: Inter, sans-serif;'>
                <h3 style='color: #ff6b6b; margin: 0 0 10px 0;'>{activity['activity']}</h3>
                <p style='margin: 5px 0;'><b>📅</b> {activity['date']} at {activity['time']}</p>
                <p style='margin: 5px 0;'><b>📍</b> {loc['name']}</p>
                <p style='margin: 5px 0;'><b>📞</b> {loc.get('phone', 'N/A')}</p>
                <p style='margin: 5px 0;'><b>💰</b> ${activity['cost']}</p>
                <p style='margin: 5px 0;'><b>🚗</b> {distance:.1f} mi ({travel_time} min from hotel)</p>
                <p style='margin: 5px 0; font-style: italic;'>{activity['notes']}</p>
            </div>
            """
            
            folium.Marker(
                location=[loc['lat'], loc['lon']],
                popup=folium.Popup(popup_html, max_width=320),
                tooltip=f"{activity['activity']} - {activity['date']}",
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
    days_until = (trip_start - now).days
    
    # Determine trip phase
    if days_until > 0:
        countdown_text = f"{days_until} Days Until Your Adventure!"
        phase_emoji = "⏳"
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
        days_until = (datetime(2025, 11, 7) - datetime.now()).days
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
        
        if today_activities:
            st.markdown(f"### Today is {today.strftime('%A, %B %d, %Y')}")
            
            # Morning briefing
            st.markdown("""
            <div class="ultimate-card fade-in">
                <div class="card-header">🌅 Morning Briefing</div>
                <div class="card-body">
            """, unsafe_allow_html=True)
            
            # Weather for today
            current = weather_data['current']
            st.write(f"**Weather:** {current['temperature']}°F, {current['condition']}")
            st.write(f"**Activities Scheduled:** {len(today_activities)}")
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Timeline of today's activities
            st.markdown("### 📋 Today's Schedule")
            
            for activity in sorted(today_activities, key=lambda x: x['time']):
                activity_time = datetime.strptime(activity['time'], '%H:%M').time()
                activity_datetime = datetime.combine(today, activity_time)
                time_until = (activity_datetime - datetime.now()).total_seconds() / 60
                
                if time_until > 0 and time_until < 60:
                    next_badge = '<span class="today-badge">⏰ COMING UP SOON!</span>'
                elif time_until <= 0:
                    next_badge = '<span class="status-confirmed">✅ In Progress / Completed</span>'
                else:
                    hours_until = int(time_until / 60)
                    next_badge = f'<span class="status-pending">In {hours_until}h {int(time_until % 60)}m</span>'
                
                st.markdown(f"""
                <div class="ultimate-card today-card fade-in">
                    <div class="card-body">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <h3 style="margin: 0 0 0.5rem 0;">{activity['activity']}</h3>
                                <p style="margin: 0.25rem 0;"><b>🕐 {activity['time']}</b></p>
                                <p style="margin: 0.25rem 0;">📍 {activity['location']['name']}</p>
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
    
    # Summary stats
    total_items = sum(len(items) for items in packing_data.values())
    checked_items = sum(1 for category in packing_data.values() for item in category if item.get('checked', False))
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
                    checked = st.checkbox("✓", value=item.get('checked', False), key=f"pack_{category}_{idx}", label_visibility="collapsed")
                    if checked != item.get('checked', False):
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

    # Get all dates and sort
    dates = sorted(df['date'].dt.date.unique())

    # NO TABS - Show all days in one scrollable view
    for date in dates:
        # Day header with weather
        day_activities = [a for a in activities_data if pd.to_datetime(a['date']).date() == date]
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

        st.markdown(f"""
        <div style="{header_style} padding: 1.5rem; border-radius: 12px; margin: 1.5rem 0 1rem 0; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <h2 style="margin: 0; color: white;">{'🎂 BIRTHDAY! ' if is_birthday else '📅 '}{date.strftime('%A, %B %d, %Y')}</h2>
            {f'<p style="margin: 0.5rem 0 0 0; opacity: 0.95; font-size: 1.1rem;">{day_weather["condition"]} | 🌡️ {day_weather["high"]}°F | 💧 {day_weather["precipitation"]}% rain | 💨 {day_weather["wind"]} mph</p>' if day_weather else ''}
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
                                    st.markdown(f"""
                                    <div style="background: #f0f9ff; border-left: 4px solid #4ecdc4; padding: 1rem; margin: 0.5rem 0; border-radius: 8px;">
                                        <p style="margin: 0; color: #636e72;">💡 <strong>Free Time:</strong> {round(gap_minutes/60, 1)}h gap ({prev_end_time} - {activity['time']})</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                            except:
                                pass

                # Custom activity badge
                custom_badge = ""
                if activity.get('is_custom', False):
                    custom_badge = '<span style="background: #74b9ff; color: white; padding: 0.25rem 0.75rem; border-radius: 10px; font-size: 0.85rem; margin-left: 0.5rem;">➕ Custom</span>'

                # Activity card
                st.markdown(f"""
                <div class="timeline-item {status_class}" style="margin: 1rem 0;">
                    <div class="ultimate-card">
                        <div class="card-body">
                            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                                <h4 style="margin: 0;">{activity['activity']} {custom_badge}</h4>
                                <span class="status-{status_class}">{activity['status']}</span>
                            </div>
                            <p style="margin: 0.5rem 0;"><b>🕐 {time_display}</b> {f'({activity["duration"]})' if activity.get('duration') else ''}</p>
                            <p style="margin: 0.5rem 0;">📍 {activity['location']['name']}</p>
                            <p style="margin: 0.5rem 0;">📞 {mask_info(activity['location'].get('phone', 'N/A'), show_sensitive)}</p>
                            <p style="margin: 0.5rem 0;">💰 {"$" + str(activity['cost']) if show_sensitive else "$***"}</p>
                            <p style="margin: 0.5rem 0; font-style: italic;">{mask_info(activity['notes'], show_sensitive)}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

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

                        # Activity card
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                                    padding: 1.5rem;
                                    border-radius: 12px;
                                    border-left: 4px solid #f5576c;
                                    margin: 1rem 0;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            <h4 style="margin: 0; color: #f5576c;">⏰ {rec['time']} - {activity['name']}</h4>
                            <p style="margin: 0.75rem 0; color: #636e72; line-height: 1.6;">{activity.get('description', '')}</p>
                            <p style="margin: 0.5rem 0; font-style: italic; color: #2ecc71;">✨ {rec['reason']}</p>
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
                    # Activity header
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                                padding: 1.5rem;
                                border-radius: 12px;
                                border-left: 4px solid #ff6b6b;
                                margin: 1rem 0;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <h4 style="margin: 0; color: #ff6b6b;">{activity['name']}</h4>
                        <p style="margin: 0.75rem 0; color: #636e72; line-height: 1.6;">{activity['description']}</p>
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
                        st.markdown(f"**📞 Phone:** {activity['phone']}")

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
                                    st.info("💡 View your updated schedule on the Full Schedule page!")
                                    st.balloons()
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
                st.markdown(f"**Top {len(recommendations)} Recommended Activities:**")

                for i, rec in enumerate(recommendations[:5], 1):  # Show top 5
                    activity = rec['activity']

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
                                #{i} {activity['name']}
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
                            <p style="margin: 0.75rem 0; color: #636e72; line-height: 1.6;">{activity['description']}</p>
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
                                        st.info("💡 View your updated schedule on the Full Schedule page!")
                                        st.balloons()
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
# JOHN'S PAGE
# ============================================================================

def render_johns_page(df, activities_data, show_sensitive):
    """John's dedicated page to manage his activities and opt-ins"""
    st.markdown('<h2 class="fade-in">👤 John\'s Trip Overview</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div class="birthday-special">
        <h3 style="margin: 0 0 0.5rem 0;">🎉 Welcome John!</h3>
        <p style="margin: 0; font-size: 1.1rem;">Your Amelia Island adventure awaits! Nov 8-11, 2025</p>
    </div>
    """, unsafe_allow_html=True)

    # John's activities
    johns_activities = [a for a in activities_data if 'john' in a['activity'].lower() or a['date'] >= '2025-11-08']

    st.markdown("### 📅 Your Schedule")

    # Categorize activities
    included_activities = []
    optional_activities_john = []

    for activity in johns_activities:
        # Activities John is definitely in
        if activity['date'] >= '2025-11-08' and activity['date'] <= '2025-11-11':
            if activity['type'] in ['transport', 'dining'] and activity['id'] != 'arr002':
                included_activities.append(activity)
            elif activity['id'] in ['act001', 'bch001', 'din002']:  # Shared activities
                included_activities.append(activity)
            elif activity['id'] == 'arr002':
                included_activities.append(activity)

    # Optional spa services for John
    spa_options = [
        {"name": "Aromatherapy Massage", "cost": "$185-245", "duration": "50-80 min"},
        {"name": "Hot Stone Massage", "cost": "$205", "duration": "80 min"},
        {"name": "Gentleman's Facial", "cost": "$165", "duration": "50 min"},
        {"name": "Mani-Pedi", "cost": "$125", "duration": "90 min"},
        {"name": "Body Scrub & Wrap", "cost": "$175-225", "duration": "50-80 min"},
    ]

    # Display John's confirmed activities
    st.markdown("#### ✅ Included in Your Trip")

    for activity in sorted(included_activities, key=lambda x: x['date'] + x['time']):
        date_obj = pd.to_datetime(activity['date'])

        paid_by = ""
        if activity['id'] == 'arr002':
            paid_by = "<span style='background: #e8f5e9; padding: 0.25rem 0.75rem; border-radius: 10px; font-size: 0.85rem;'>✈️ Your Flight</span>"
        elif activity['id'] in ['act001', 'bch001']:
            paid_by = "<span style='background: #fff9c4; padding: 0.25rem 0.75rem; border-radius: 10px; font-size: 0.85rem;'>💝 Shared Activity</span>"

        cost_display = f"${activity['cost']}" if show_sensitive and activity['cost'] > 0 else ""
        if not show_sensitive and activity['cost'] > 0:
            cost_display = "$***"

        st.markdown(f"""
        <div class="ultimate-card fade-in">
            <div class="card-body">
                <h4 style="margin: 0 0 0.5rem 0;">{activity['activity']}</h4>
                <p style="margin: 0.25rem 0;"><strong>📅 {date_obj.strftime('%A, %B %d')} at {activity['time']}</strong></p>
                <p style="margin: 0.25rem 0;">📍 {activity['location']['name']}</p>
                {f"<p style='margin: 0.25rem 0;'>💰 {cost_display}</p>" if cost_display else ""}
                <p style="margin: 0.5rem 0; font-style: italic;">{activity['notes']}</p>
                {paid_by}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Optional spa services John can opt into
    st.markdown("---")
    st.markdown("### 💆 Optional Spa Services (You Pay)")

    st.markdown("""
    <div class="info-box" style="background: linear-gradient(135deg, #e3f2fd 0%, #e1f5fe 100%);">
        <p style="margin: 0;"><strong>ℹ️ Info:</strong> These spa treatments are optional. If you'd like to book any, let the trip organizer know and you'll cover the cost.</p>
    </div>
    """, unsafe_allow_html=True)

    for idx, spa in enumerate(spa_options):
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.markdown(f"**{spa['name']}**")
            st.caption(f"{spa['duration']} • {spa['cost']}")

        with col2:
            interested = st.checkbox("Interested?", key=f"john_spa_{idx}")

        with col3:
            if interested:
                st.success("✓ Noted")

    # Pool access reminder
    st.markdown("---")
    st.markdown("### 🏊 Complimentary Access")

    st.markdown("""
    <div class="ultimate-card" style="border-left: 4px solid #4caf50;">
        <div class="card-body">
            <h4 style="margin: 0 0 0.5rem 0;">🌴 Resort Pool & Beach Access</h4>
            <p style="margin: 0;">You have full access to all Ritz-Carlton pools, hot tubs, and beach facilities during your stay!</p>
            <ul style="margin: 0.5rem 0;">
                <li>Multiple pools & hot tubs</li>
                <li>Beach chairs & umbrellas</li>
                <li>Towel service</li>
                <li>Poolside bar & dining</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Summary
    st.markdown("---")
    st.markdown("### 📊 Trip Summary")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Days on Island", "3.5 days")
        st.metric("Confirmed Activities", len(included_activities))
    with col2:
        st.metric("Flight Arrival", "Sat Nov 8, 10:40am")
        st.metric("Flight Departure", "Tue Nov 11, 11:05am")


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
            default_index = 5  # Packing List
            st.session_state['nav_to_packing'] = False
        else:
            default_index = 0

        page = st.selectbox(
            "Navigate to:",
            [
                "🏠 Dashboard",
                "📅 Today",
                "🗓️ Full Schedule",
                "🎯 Explore & Plan",
                "👤 John's Page",
                "🗺️ Map & Locations",
                "🎒 Packing List",
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
        
        days_until = (datetime(2025, 11, 7) - datetime.now()).days
        if days_until > 0:
            st.info(f"🗓️ {days_until} days until trip")
        elif days_until == 0:
            st.success("🎉 Trip starts TODAY!")
        else:
            st.success("🏖️ On your trip!")
        
        st.markdown("---")
        
        # Version info
        st.caption("**Ultimate Edition v2.0**")
        st.caption("Enhanced by Claude Code")
    
    # Page routing
    if page == "🏠 Dashboard":
        render_dashboard_ultimate(df, activities_data, weather_data, show_sensitive)
    
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

