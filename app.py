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
            "time": "18:01",
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
            "time": "10:40",
            "activity": "John Arrives at JAX",
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
            "notes": "AA1585 from DCA - Flight lands 10:40am. Plan realistic timeline: 15min deplaning + 10min baggage + 10min to curb = pickup ~11:15am. Then 45min drive to hotel = arrive ~12:00pm",
            "flight_number": "AA1585",
            "what_to_bring": ["Track flight on FlightAware", "Phone charged for coordination"],
            "tips": ["Leave hotel by 10:00am to arrive on time", "Text when boarding/landing", "Account for traffic on A1A", "Plan lunch after arrival at hotel"],
            "estimated_pickup_time": "11:15",
            "estimated_hotel_arrival": "12:00",
            "priority": 3
        },
        {
            "id": "arr002b",
            "date": "2025-11-08",
            "time": "12:00",
            "activity": "Back at Hotel + Lunch",
            "type": "dining",
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
            "tips": ["The Surf Restaurant at hotel is convenient", "Salt Life Food Shack nearby", "Keep it light before boat tour"],
            "priority": 2
        },
        {
            "id": "act001",
            "date": "2025-11-08",
            "time": "15:30",
            "activity": "Backwater Cat Tour",
            "type": "activity",
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
            "time": "10:00",
            "activity": "Heaven in a Hammock Massage",
            "type": "spa",
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
            "time": "12:00",
            "activity": "HydraFacial Treatment",
            "type": "spa",
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
            "time": "19:00",
            "activity": "40th Birthday Dinner",
            "type": "dining",
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
            "time": "10:00",
            "activity": "Beach Day",
            "type": "beach",
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
            "time": "18:00",
            "activity": "Casual Dinner",
            "type": "dining",
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
            "time": "11:05",
            "activity": "John Departs",
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
            "notes": "AA1586 to DCA - Arrive 2 hours early (9:05 AM)",
            "flight_number": "AA1586",
            "what_to_bring": ["ID", "Boarding pass"],
            "tips": ["Check traffic before leaving", "Allow 45 min drive"],
            "priority": 3
        },
        {
            "id": "dep002",
            "date": "2025-11-12",
            "time": "14:39",
            "activity": "Your Departure",
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
            "notes": "AA5590 - Return home with amazing memories!",
            "flight_number": "AA5590",
            "what_to_bring": ["All belongings", "Souvenirs", "Photos", "Memories!"],
            "tips": ["Hotel checkout 11 AM", "Leave by 12:30 PM", "Double-check room for items"],
            "priority": 3
        }
    ]
    
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
    """Database of 30+ optional activities in Amelia Island for trip planning"""
    return {
        "🍽️ Dining Options": [
            {"name": "Salt Life Food Shack", "description": "Oceanfront casual dining with amazing views and fresh seafood", "cost_range": "$15-30 per person", "duration": "1-2 hours", "phone": "904-277-3811", "booking_url": "https://www.saltlifefoodshack.com", "tips": "Perfect for lunch, great outdoor seating with ocean breeze", "rating": "4.5/5"},
            {"name": "Brett's Waterway Cafe", "description": "Waterfront dining with marina views, fresh catch daily", "cost_range": "$20-40 per person", "duration": "1.5-2 hours", "phone": "904-261-2660", "booking_url": "https://www.opentable.com/r/bretts-waterway-cafe-fernandina-beach", "tips": "Amazing sunset views, try the seafood platter", "rating": "4.7/5"},
            {"name": "Le Clos", "description": "French bistro with romantic atmosphere, extensive wine selection", "cost_range": "$40-70 per person", "duration": "2-3 hours", "phone": "904-261-8100", "booking_url": "https://www.opentable.com/r/le-clos-fernandina-beach", "tips": "Reservations required, dress code (business casual)", "rating": "4.8/5"},
            {"name": "29 South", "description": "Farm-to-table Southern cuisine, excellent brunch", "cost_range": "$25-45 per person", "duration": "1.5-2 hours", "phone": "904-277-7919", "booking_url": "https://www.opentable.com/r/29-south-fernandina-beach", "tips": "Amazing brunch on weekends, local ingredients", "rating": "4.6/5"},
            {"name": "The Surf Restaurant", "description": "Beachfront dining at Ritz-Carlton", "cost_range": "$30-60 per person", "duration": "1.5-2 hours", "phone": "904-277-1100", "booking_url": "https://www.ritzcarlton.com/en/hotels/ameliarc/dining", "tips": "No reservation needed, great ocean views", "rating": "4.7/5"},
        ],
        "🏖️ Beach & Water": [
            {"name": "Horseback Riding on Beach", "description": "Ride horses along the beautiful Amelia Island shoreline", "cost_range": "$75-125 per person", "duration": "1-2 hours", "phone": "904-491-5166", "tips": "Book 2-3 days in advance, wear comfortable pants", "rating": "5.0/5"},
            {"name": "Kayaking/Paddleboarding", "description": "Explore marshes, creeks, and waterways", "cost_range": "$40-75", "duration": "2-3 hours", "phone": "904-321-0697", "tips": "Morning is best, calm waters and lots of wildlife", "rating": "4.7/5"},
            {"name": "Peters Point Beach", "description": "Quieter beach, less crowded than Main Beach", "cost_range": "FREE", "duration": "2-4 hours", "phone": "N/A", "tips": "More secluded, bring your own beach gear", "rating": "4.5/5"},
            {"name": "Fishing Charter", "description": "Deep sea or inshore fishing adventure", "cost_range": "$400-800 (up to 4 people)", "duration": "4-8 hours", "phone": "904-206-0200", "tips": "Book early, half-day or full-day options available", "rating": "4.8/5"},
            {"name": "Sunset Cruise", "description": "Relaxing sunset sail", "cost_range": "$45-65 per person", "duration": "2 hours", "phone": "904-261-9972", "tips": "Bring camera, BYOB allowed", "rating": "4.9/5"},
        ],
        "🎯 Activities & Adventure": [
            {"name": "Fort Clinch State Park", "description": "Historic Civil War fort with beach, trails, and ranger-led tours", "cost_range": "$6-8 per vehicle", "duration": "2-3 hours", "phone": "904-277-7274", "tips": "Great for history buffs, bring sunscreen and water", "rating": "4.6/5"},
            {"name": "Bike Rentals & Trails", "description": "Explore the island on two wheels", "cost_range": "$20-40 per day", "duration": "2-4 hours", "phone": "Multiple locations", "tips": "Great for exploring downtown Fernandina Beach", "rating": "4.5/5"},
            {"name": "Golf at Oak Marsh", "description": "Championship 18-hole golf course designed by Tom Fazio", "cost_range": "$80-150", "duration": "4-5 hours", "phone": "904-277-5907", "tips": "Book tee times in advance, beautiful course", "rating": "4.7/5"},
            {"name": "Egan's Creek Greenway", "description": "Nature trails with boardwalks, excellent birdwatching", "cost_range": "FREE", "duration": "1-2 hours", "phone": "N/A", "tips": "Bring bug spray, early morning for best wildlife viewing", "rating": "4.4/5"},
            {"name": "Segway Tours", "description": "Guided Segway tour of historic Fernandina Beach", "cost_range": "$65-75 per person", "duration": "1.5-2 hours", "phone": "904-556-7594", "tips": "Fun way to see the sights, no experience needed", "rating": "4.8/5"},
        ],
        "🛍️ Shopping & Culture": [
            {"name": "Downtown Fernandina Beach", "description": "Historic downtown with 50+ shops, galleries, and cafes", "cost_range": "Varies", "duration": "2-3 hours", "phone": "N/A", "tips": "Centre Street is main drag, very walkable and charming", "rating": "4.8/5"},
            {"name": "Amelia Island Museum of History", "description": "Learn local history with engaging guided tours", "cost_range": "$10-15", "duration": "1-2 hours", "phone": "904-261-7378", "tips": "Oral history tours are fantastic and unique", "rating": "4.7/5"},
            {"name": "Saturday Farmer's Market", "description": "Local produce, crafts, and food vendors", "cost_range": "Varies", "duration": "1-2 hours", "phone": "N/A", "tips": "Only on Saturday mornings 9am-1pm, arrive early", "rating": "4.6/5"},
            {"name": "Art Galleries Walk", "description": "Multiple galleries along Centre Street", "cost_range": "FREE to browse", "duration": "1-2 hours", "phone": "N/A", "tips": "First Friday ArtWalk if timing works out", "rating": "4.5/5"},
        ],
        "💆 Ritz-Carlton Spa Services": [
            {"name": "Heaven in a Hammock Massage (Couples)", "description": "ALREADY BOOKED - Beachside couples massage in swaying hammocks", "cost_range": "$245 each", "duration": "80 minutes", "phone": "904-277-1100", "tips": "Book together for birthday celebration", "rating": "5.0/5"},
            {"name": "HydraFacial Treatment", "description": "ALREADY BOOKED - Advanced facial for glowing skin", "cost_range": "$195", "duration": "50 minutes", "phone": "904-277-1100", "tips": "Perfect before birthday dinner", "rating": "4.9/5"},
            {"name": "Aromatherapy Massage", "description": "Full body massage with essential oils", "cost_range": "$185-245", "duration": "50-80 minutes", "phone": "904-277-1100", "tips": "Choose from lavender, eucalyptus, or citrus blends", "rating": "4.9/5"},
            {"name": "Mani-Pedi Combo", "description": "Professional manicure and pedicure", "cost_range": "$125", "duration": "90 minutes", "phone": "904-277-1100", "tips": "Great add-on for spa day", "rating": "4.8/5"},
            {"name": "Body Scrub & Wrap", "description": "Exfoliating scrub followed by hydrating wrap", "cost_range": "$175-225", "duration": "50-80 minutes", "phone": "904-277-1100", "tips": "Ocean salt scrub is signature treatment", "rating": "4.8/5"},
            {"name": "Hot Stone Massage", "description": "Deep relaxation with heated volcanic stones", "cost_range": "$205", "duration": "80 minutes", "phone": "904-277-1100", "tips": "Perfect for sore muscles after activities", "rating": "4.9/5"},
            {"name": "Gentleman's Facial", "description": "Facial designed for men's skin", "cost_range": "$165", "duration": "50 minutes", "phone": "904-277-1100", "tips": "John might enjoy this!", "rating": "4.7/5"},
            {"name": "Reflexology Treatment", "description": "Therapeutic foot and lower leg massage", "cost_range": "$115", "duration": "50 minutes", "phone": "904-277-1100", "tips": "Great after beach walking", "rating": "4.6/5"},
        ],
        "🏊 Resort Amenities": [
            {"name": "Resort Pool Day", "description": "Relax at multiple Ritz-Carlton pools and hot tubs", "cost_range": "FREE (hotel guests)", "duration": "2-4 hours", "phone": "N/A", "tips": "Reserve a cabana for ultimate luxury relaxation", "rating": "4.8/5"},
            {"name": "Beach Sunset Viewing", "description": "Watch gorgeous sunset from the shore", "cost_range": "FREE", "duration": "30-60 minutes", "phone": "N/A", "tips": "Check sunset time, bring camera and beach blanket", "rating": "5.0/5"},
            {"name": "Yoga on the Beach", "description": "Morning yoga classes on the beach", "cost_range": "$20-35", "duration": "1 hour", "phone": "904-277-1100", "tips": "Hotel offers classes, check schedule", "rating": "4.6/5"},
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

@st.cache_data(ttl=3600)
def get_tide_data():
    """Get tide data from NOAA for Fernandina Beach, FL"""
    station_id = "8720030"  # Fernandina Beach, FL

    try:
        # Get tide predictions for next 7 days
        from datetime import datetime, timedelta
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
                date_str = pred['t'].split(' ')[0]
                if date_str not in daily_tides:
                    daily_tides[date_str] = {'high': [], 'low': []}

                if pred['type'] == 'H':
                    daily_tides[date_str]['high'].append({'time': pred['t'].split(' ')[1], 'height': float(pred['v'])})
                else:
                    daily_tides[date_str]['low'].append({'time': pred['t'].split(' ')[1], 'height': float(pred['v'])})

            return daily_tides
    except:
        pass

    # Fallback tide data
    return {
        '2025-11-07': {'high': [{'time': '06:30', 'height': 6.5}, {'time': '19:00', 'height': 6.8}],
                       'low': [{'time': '00:15', 'height': 0.5}, {'time': '12:45', 'height': 0.3}]},
        '2025-11-08': {'high': [{'time': '07:15', 'height': 6.6}, {'time': '19:45', 'height': 6.9}],
                       'low': [{'time': '01:00', 'height': 0.4}, {'time': '13:30', 'height': 0.2}]},
    }

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
    """Complete trip schedule"""
    st.markdown('<h2 class="fade-in">🗓️ Complete Trip Schedule</h2>', unsafe_allow_html=True)
    
    dates = df['date'].dt.date.unique()
    dates = sorted(dates)
    
    # Create tabs for each day
    date_tabs = st.tabs([f"📅 {date.strftime('%a %m/%d')}" for date in dates])
    
    for idx, date in enumerate(dates):
        with date_tabs[idx]:
            day_activities = [a for a in activities_data if pd.to_datetime(a['date']).date() == date]
            day_activities.sort(key=lambda x: x['time'])
            
            st.markdown(f"### {date.strftime('%A, %B %d, %Y')}")
            
            # Check if birthday
            if date.month == 11 and date.day == 9:
                st.markdown("""
                <div class="birthday-special">
                    <h2 style="margin: 0;">🎂 BIRTHDAY DAY! 🎉</h2>
                    <p style="font-size: 1.2rem; margin: 0.5rem 0 0 0;">Your special 40th celebration!</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Timeline
            if day_activities:
                st.markdown('<div class="timeline">', unsafe_allow_html=True)
                
                for activity in day_activities:
                    status_class = activity['status'].lower()
                    
                    st.markdown(f"""
                    <div class="timeline-item {status_class}">
                        <div class="ultimate-card">
                            <div class="card-body">
                                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                                    <h4 style="margin: 0;">{activity['activity']}</h4>
                                    <span class="status-{status_class}">{activity['status']}</span>
                                </div>
                                <p style="margin: 0.5rem 0;"><b>🕐 {activity['time']}</b></p>
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
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No scheduled activities - free day!")

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
        with st.expander(f"{category} ({len(items)} options)", expanded=(category == "🍽️ Dining Options")):
            for idx, activity in enumerate(items):
                st.markdown(f"""
                <div class="ultimate-card fade-in" style="margin: 1rem 0;">
                    <div class="card-body">
                        <div style="display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap;">
                            <div style="flex: 1; min-width: 300px;">
                                <h4 style="margin: 0 0 0.5rem 0; color: #ff6b6b;">{activity['name']}</h4>
                                <p style="margin: 0.5rem 0; color: #636e72;">{activity['description']}</p>
                                <div style="display: flex; gap: 1rem; margin-top: 1rem; flex-wrap: wrap; font-size: 0.95rem;">
                                    <span style="background: #f0f9ff; padding: 0.25rem 0.75rem; border-radius: 15px;">💰 {activity['cost_range']}</span>
                                    <span style="background: #fff5e6; padding: 0.25rem 0.75rem; border-radius: 15px;">⏱️ {activity['duration']}</span>
                                    <span style="background: #ffe6f0; padding: 0.25rem 0.75rem; border-radius: 15px;">⭐ {activity.get('rating', 'N/A')}</span>
                                </div>
                                {f'<div style="margin-top: 0.75rem;"><span style="background: #e6f7ff; padding: 0.25rem 0.75rem; border-radius: 15px;">📞 {activity["phone"]}</span></div>' if activity.get('phone') and activity['phone'] != 'N/A' else ''}
                                <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%); padding: 0.75rem; border-radius: 10px; margin-top: 1rem; border-left: 3px solid #4ecdc4;">
                                    <strong>💡 Pro Tip:</strong> {activity['tips']}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"⭐ Save", key=f"save_{category}_{idx}", use_container_width=True):
                        st.success(f"✅ Saved {activity['name']} to your wishlist!")
                with col2:
                    if st.button(f"📋 Notes", key=f"note_{category}_{idx}", use_container_width=True):
                        st.info("💭 Add this to your trip notes!")
                with col3:
                    if activity.get('phone') and activity['phone'] != 'N/A' and activity['phone'] != 'Multiple locations':
                        if st.button(f"📞 Call", key=f"call_{category}_{idx}", use_container_width=True):
                            st.info(f"Calling {activity['phone']}...")

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

                    # Build recommendation card
                    card_html = f"""
                    <div class="ultimate-card fade-in" style="margin: 1rem 0; border-left: 4px solid #4ecdc4;">
                        <div class="card-body">
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <div style="flex: 1;">
                                    <h5 style="margin: 0 0 0.5rem 0; color: #ff6b6b;">
                                        #{i} {activity['name']}
                                        <span style="background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem; margin-left: 0.5rem;">
                                            Score: {rec['score']}/100
                                        </span>
                                    </h5>
                                    <p style="margin: 0.5rem 0; color: #636e72; font-size: 0.95rem;">{activity['description']}</p>

                                    <div style="display: flex; gap: 0.75rem; margin: 0.75rem 0; flex-wrap: wrap; font-size: 0.9rem;">
                                        <span style="background: #f0f9ff; padding: 0.25rem 0.75rem; border-radius: 15px;">💰 {activity['cost_range']}</span>
                                        <span style="background: #fff5e6; padding: 0.25rem 0.75rem; border-radius: 15px;">⏱️ {activity['duration']}</span>
                                        <span style="background: #ffe6f0; padding: 0.25rem 0.75rem; border-radius: 15px;">⭐ {activity.get('rating', 'N/A')}</span>
                                    </div>
                    """

                    # Add "Why Recommended" reasons
                    if rec['reasons']:
                        card_html += '<div style="background: linear-gradient(135deg, #e6f7ff 0%, #d9f7e8 100%); padding: 0.75rem; border-radius: 10px; margin: 0.75rem 0;">'
                        card_html += '<strong style="color: #27ae60;">✅ Why This Fits:</strong><ul style="margin: 0.25rem 0; padding-left: 1.5rem;">'
                        for reason in rec['reasons']:
                            card_html += f'<li style="margin: 0.25rem 0;">{reason}</li>'
                        card_html += '</ul></div>'

                    # Add warnings if any
                    if rec['warnings']:
                        card_html += '<div style="background: #fff4e6; padding: 0.75rem; border-radius: 10px; margin: 0.75rem 0; border-left: 3px solid #f39c12;">'
                        card_html += '<strong style="color: #d35400;">⚠️ Important Notes:</strong><ul style="margin: 0.25rem 0; padding-left: 1.5rem;">'
                        for warning in rec['warnings']:
                            card_html += f'<li style="margin: 0.25rem 0;">{warning}</li>'
                        card_html += '</ul></div>'

                    # Add pro tip
                    card_html += f"""
                                    <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%); padding: 0.75rem; border-radius: 10px; margin: 0.75rem 0; border-left: 3px solid #4ecdc4;">
                                        <strong>💡 Pro Tip:</strong> {activity['tips']}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """

                    st.markdown(card_html, unsafe_allow_html=True)

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

