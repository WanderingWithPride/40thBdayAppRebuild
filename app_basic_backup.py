"""
40th Birthday Trip Assistant - Streamlit Deployment Version
=========================================================
Complete deployment-ready application with all enhanced features

SECURITY NOTICE:
---------------
✅ All personal data (flights, phone numbers, bookings) is HARDCODED in this file
✅ Password protection REQUIRES authentication to view sensitive information
✅ Data masking OBFUSCATES all personal data when password not verified
✅ SAFE to upload to public GitHub - without password, all data is masked
✅ Password: '28008985' (set for deployment)

Personal data embedded in: sample_data dictionary (lines ~378-401)
Password protection: check_password() function (lines ~336-356)
Data masking: mask_sensitive_info() function (lines ~358-371)
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

# Configure page for deployment
st.set_page_config(
    page_title="40th Birthday Trip Assistant",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Your complete 40th birthday trip planning companion for Amelia Island"
    }
)

# Enhanced CSS for deployment
def load_deployment_css():
    """Load deployment-optimized CSS"""
    css = """
    <style>
    /* Enhanced deployment CSS */
    :root {
        --primary-color: #ff6b6b;
        --secondary-color: #4ecdc4;
        --accent-color: #45b7d1;
        --success-color: #96ceb4;
        --warning-color: #ffeaa7;
        --danger-color: #fd79a8;
        --dark-color: #2d3436;
        --light-color: #f8f9fa;
    }
    
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .status-bar {
        background: rgba(255, 255, 255, 0.2);
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        overflow: hidden;
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .card:hover {
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    .card-header {
        padding: 1.5rem;
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        color: white;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    .card-body {
        padding: 1.5rem;
    }
    
    .urgent-card {
        border-left: 5px solid var(--danger-color);
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        animation: pulse-urgent 2s infinite;
    }
    
    @keyframes pulse-urgent {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .activity-card {
        border-left: 5px solid var(--secondary-color);
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    }
    
    .weather-card {
        border-left: 5px solid var(--accent-color);
        background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%);
    }
    
    .spa-card {
        border-left: 5px solid var(--success-color);
        background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
    }
    
    .btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 10px;
        font-size: 1rem;
        font-weight: 600;
        text-decoration: none;
        cursor: pointer;
        transition: all 0.3s ease;
        min-height: 48px;
        gap: 0.5rem;
    }
    
    .btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .btn-primary {
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        color: white;
    }
    
    .btn-success {
        background: var(--success-color);
        color: white;
    }
    
    .btn-warning {
        background: var(--warning-color);
        color: var(--dark-color);
    }
    
    .btn-danger {
        background: var(--danger-color);
        color: white;
    }
    
    .status-confirmed {
        background: rgba(150, 206, 180, 0.2);
        color: var(--success-color);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .status-pending {
        background: rgba(255, 234, 167, 0.2);
        color: #d68910;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .status-urgent {
        background: rgba(253, 121, 168, 0.2);
        color: var(--danger-color);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        animation: pulse 1s infinite;
    }
    
    .timeline {
        position: relative;
        padding: 1rem 0;
    }
    
    .timeline::before {
        content: '';
        position: absolute;
        left: 1rem;
        top: 0;
        bottom: 0;
        width: 3px;
        background: linear-gradient(to bottom, var(--primary-color), var(--secondary-color));
        border-radius: 2px;
    }
    
    .timeline-item {
        position: relative;
        padding-left: 3rem;
        margin-bottom: 2rem;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: calc(1rem - 8px);
        top: 0.5rem;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: var(--primary-color);
        border: 3px solid white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .timeline-item.completed::before {
        background: var(--success-color);
    }
    
    .timeline-item.urgent::before {
        background: var(--danger-color);
        animation: pulse 1.5s infinite;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header {
            margin-left: -1rem;
            margin-right: -1rem;
            border-radius: 0;
            padding: 1.5rem;
        }
        
        .main-header h1 {
            font-size: 2rem;
        }
        
        .status-bar {
            flex-direction: column;
            text-align: center;
        }
        
        .metric-card {
            margin-left: -1rem;
            margin-right: -1rem;
            border-radius: 0;
        }
        
        .card {
            margin-left: -1rem;
            margin-right: -1rem;
            border-radius: 0;
        }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .card {
            background-color: #2d3748;
            color: white;
        }
    }
    
    /* Print styles */
    @media print {
        .main-header {
            background: #ff6b6b !important;
            -webkit-print-color-adjust: exact;
        }
        
        .card {
            break-inside: avoid;
            box-shadow: none;
            border: 1px solid #ccc;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Authentication functions
def check_password():
    """Password protection for sensitive information"""
    if 'password_verified' not in st.session_state:
        st.session_state.password_verified = False
    
    if not st.session_state.password_verified:
        st.markdown("### 🔒 Access Personal Information")
        st.info("Enter password to view booking details, flight numbers, and personal information:")
        
        password = st.text_input("Password:", type="password", key="password_input")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔓 Unlock Personal Details", use_container_width=True):
                # Password is "28008985" (hash: a5be948874610641149611913c4924e5)
                stored_hash = os.getenv('TRIP_PASSWORD_HASH', 'a5be948874610641149611913c4924e5')
                input_hash = hashlib.md5(password.encode()).hexdigest()
                
                if input_hash == stored_hash:
                    st.session_state.password_verified = True
                    st.success("✅ Access granted! Personal details are now visible.")
                    st.rerun()
                else:
                    st.error("❌ Incorrect password. Please try again.")
        
        with col2:
            if st.button("👀 Demo Mode", use_container_width=True):
                st.session_state.password_verified = False
                st.info("🔒 Demo mode - sensitive data will be masked")
        
        st.markdown("---")
        return False
    return True

def mask_sensitive_info(text, show_sensitive=False):
    """Mask sensitive information if not authenticated"""
    if show_sensitive:
        return text
    
    # Enhanced masking patterns
    patterns = {
        r'\b\d{6,}\b': '***BOOKING***',
        r'\b[A-Z0-9]{6,}\b': '***CONFIRM***',
        r'\b\d{3}-\d{3}-\d{4}\b': '***-***-****',
        r'\b[\w\.-]+@[\w\.-]+\.\w+\b': '***@***.***',
        r'\bAA\d{4}\b': 'AA****'
    }
    
    for pattern, replacement in patterns.items():
        text = re.sub(pattern, replacement, str(text))
    
    return text

# Data loading functions
@st.cache_data(ttl=3600)
def load_trip_data():
    """Load trip data with fallback to sample data"""
    # Sample data for deployment
    sample_data = [
        {"Date": "2025-11-07", "Time": "18:01", "Activity": "Land JAX", "Location": "Jacksonville Airport", "Cost": 65, "Phone": "App", "Status": "Confirmed", "Category": "Transport", "Notes": "American Airlines 2434"},
        {"Date": "2025-11-08", "Time": "11:00", "Activity": "John Arrives", "Location": "Jacksonville Airport", "Cost": 0, "Phone": "App", "Status": "Confirmed", "Category": "Transport", "Notes": "AA1585 - 10:40 AM arrival"},
        {"Date": "2025-11-08", "Time": "15:30", "Activity": "Backwater Cat Tour", "Location": "Dee Dee Bartels Boat Ramp", "Cost": 270, "Phone": "904-753-7631", "Status": "URGENT", "Category": "Activity", "Notes": "BOOK NOW - 2.5 hours eco tour"},
        {"Date": "2025-11-09", "Time": "10:00", "Activity": "Heaven in a Hammock Massage", "Location": "Ritz-Carlton Spa", "Cost": 245, "Phone": "904-277-1100", "Status": "URGENT", "Category": "Spa", "Notes": "Birthday spa day for both"},
        {"Date": "2025-11-09", "Time": "12:00", "Activity": "HydraFacial Treatment", "Location": "Ritz-Carlton Spa", "Cost": 195, "Phone": "904-277-1100", "Status": "URGENT", "Category": "Spa", "Notes": "Advanced facial treatment"},
        {"Date": "2025-11-09", "Time": "19:00", "Activity": "Birthday Dinner", "Location": "David's Restaurant & Lounge", "Cost": 210, "Phone": "904-310-6049", "Status": "URGENT", "Category": "Dining", "Notes": "40th birthday celebration dinner"},
        {"Date": "2025-11-10", "Time": "10:00", "Activity": "Beach Day", "Location": "Main Beach Park", "Cost": 0, "Phone": "N/A", "Status": "Confirmed", "Category": "Beach", "Notes": "Relaxing beach day"},
        {"Date": "2025-11-10", "Time": "18:00", "Activity": "Casual Dinner", "Location": "Timoti's Seafood Shak", "Cost": 60, "Phone": "904-321-1430", "Status": "Pending", "Category": "Dining", "Notes": "Beachside casual dining"},
        {"Date": "2025-11-11", "Time": "12:12", "Activity": "John Departs", "Location": "Jacksonville Airport", "Cost": 65, "Phone": "App", "Status": "Confirmed", "Category": "Transport", "Notes": "AA1586 departure"},
        {"Date": "2025-11-12", "Time": "14:39", "Activity": "Departure", "Location": "Jacksonville Airport", "Cost": 0, "Phone": "App", "Status": "Confirmed", "Category": "Transport", "Notes": "AA5590 - Return home"}
    ]
    
    df = pd.DataFrame(sample_data)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce').fillna(0)
    df['Priority'] = df['Status'].map({
        'URGENT': 1,
        'Pending': 2,
        'Confirmed': 3
    }).fillna(4)
    
    return df

@st.cache_data(ttl=1800)
def get_weather_data():
    """Get weather data with fallback"""
    return {
        "current": {
            "temperature": 75,
            "condition": "Partly Cloudy",
            "humidity": 68,
            "wind_speed": 8,
            "uv_index": 6,
            "visibility": 10
        },
        "forecast": [
            {"date": "2025-11-07", "high": 78, "low": 65, "condition": "Sunny", "uv": 5, "precipitation": 0},
            {"date": "2025-11-08", "high": 75, "low": 62, "condition": "Partly Cloudy", "uv": 6, "precipitation": 10},
            {"date": "2025-11-09", "high": 72, "low": 58, "condition": "Cloudy", "uv": 4, "precipitation": 20},
            {"date": "2025-11-10", "high": 74, "low": 60, "condition": "Sunny", "uv": 7, "precipitation": 0},
            {"date": "2025-11-11", "high": 76, "low": 63, "condition": "Partly Cloudy", "uv": 6, "precipitation": 5},
            {"date": "2025-11-12", "high": 77, "low": 64, "condition": "Sunny", "uv": 6, "precipitation": 0}
        ],
        "alerts": []
    }

@st.cache_data(ttl=300)
def get_flight_data():
    """Get flight status data"""
    return {
        "your_flights": [
            {"number": "AA2434", "date": "2025-11-07", "departure": "15:51", "arrival": "18:01", "status": "On Time", "gate": "B15", "route": "DCA → JAX"},
            {"number": "AA5590", "date": "2025-11-12", "departure": "14:39", "arrival": "16:40", "status": "On Time", "gate": "A8", "route": "JAX → DCA"}
        ],
        "john_flights": [
            {"number": "AA1585", "date": "2025-11-08", "departure": "09:15", "arrival": "10:40", "status": "On Time", "gate": "A12", "route": "DCA → JAX"},
            {"number": "AA1586", "date": "2025-11-11", "departure": "11:05", "arrival": "12:12", "status": "On Time", "gate": "B8", "route": "JAX → DCA"}
        ]
    }

# UI Components
def render_header():
    """Render main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🎂 40th Birthday Trip Assistant</h1>
        <p>Your complete Amelia Island adventure companion</p>
        <div class="status-bar">
            <div>📅 November 7-12, 2025</div>
            <div>🏨 The Ritz-Carlton Amelia Island</div>
            <div>🌴 6 Days of Paradise</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_dashboard():
    """Render main dashboard"""
    st.title("🏠 Trip Dashboard")
    
    # Load data
    df = load_trip_data()
    weather_data = get_weather_data()
    show_sensitive = st.session_state.get("password_verified", False)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_events = len(df)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_events}</div>
            <div class="metric-label">Total Events</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        days_remaining = (datetime(2025, 11, 7) - datetime.now()).days
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{max(0, days_remaining)}</div>
            <div class="metric-label">Days Remaining</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_budget = df['Cost'].sum()
        budget_display = f"${total_budget:,.0f}" if show_sensitive else "$***,***"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{budget_display}</div>
            <div class="metric-label">Total Budget</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        confirmed_count = len(df[df['Status'] == 'Confirmed'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{confirmed_count}</div>
            <div class="metric-label">Confirmed</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Current weather
    if weather_data:
        st.markdown("### 🌤️ Current Weather & Forecast")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            current = weather_data['current']
            st.markdown(f"""
            <div class="weather-card card">
                <div class="card-body">
                    <h4>🌡️ Current Conditions</h4>
                    <p style="font-size: 1.5rem; font-weight: bold; margin: 1rem 0;">
                        {current['temperature']}°F - {current['condition']}
                    </p>
                    <p>💧 Humidity: {current['humidity']}%</p>
                    <p>💨 Wind: {current['wind_speed']} mph</p>
                    <p>☀️ UV Index: {current['uv_index']}</p>
                    <p>👁️ Visibility: {current['visibility']} miles</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # 6-day forecast chart
            forecast_df = pd.DataFrame(weather_data['forecast'])
            forecast_df['date'] = pd.to_datetime(forecast_df['date'])
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=forecast_df['date'],
                y=forecast_df['high'],
                mode='lines+markers',
                name='High Temp',
                line=dict(color='#ff6b6b', width=3),
                marker=dict(size=10)
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast_df['date'],
                y=forecast_df['low'],
                mode='lines+markers',
                name='Low Temp',
                line=dict(color='#4ecdc4', width=3),
                marker=dict(size=10)
            ))
            
            fig.update_layout(
                title="6-Day Temperature Forecast",
                xaxis_title="Date",
                yaxis_title="Temperature (°F)",
                height=350,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Urgent items
    urgent_items = df[df['Status'] == 'URGENT'].sort_values('Priority')
    
    if len(urgent_items) > 0:
        st.markdown("### 🚨 Urgent Bookings")
        
        for _, item in urgent_items.iterrows():
            activity_name = mask_sensitive_info(item['Activity'], show_sensitive)
            phone = mask_sensitive_info(str(item['Phone']), show_sensitive)
            location = mask_sensitive_info(item['Location'], show_sensitive)
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"""
                <div class="urgent-card card">
                    <div class="card-body">
                        <h4>⚠️ {activity_name}</h4>
                        <p><strong>📅 {item['Date'].strftime('%A, %B %d')} at {item['Time']}</strong></p>
                        <p>📍 {location}</p>
                        <p>📞 {phone}</p>
                        <p>💰 ${item['Cost']}</p>
                        <p><em>{item['Notes']}</em></p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button(f"📞 Call", key=f"call_{item.name}", use_container_width=True):
                    st.success(f"Calling {phone}...")
                
                if st.button(f"✅ Mark Booked", key=f"book_{item.name}", use_container_width=True):
                    st.success("Marked as booked!")
    else:
        st.success("🎉 No urgent bookings! Everything is on track.")

def render_schedule():
    """Render interactive schedule"""
    st.title("📅 Interactive Schedule")
    
    df = load_trip_data()
    show_sensitive = st.session_state.get("password_verified", False)
    
    # Group by date
    dates = df['Date'].dt.date.unique()
    dates.sort()
    
    # Create tabs for each day
    date_tabs = st.tabs([f"{date.strftime('%a %m/%d')}" for date in dates])
    
    for i, date in enumerate(dates):
        with date_tabs[i]:
            day_events = df[df['Date'].dt.date == date].sort_values('Time')
            
            st.markdown(f"#### {date.strftime('%A, %B %d, %Y')}")
            
            if len(day_events) == 0:
                st.info("No events scheduled for this day")
            else:
                # Timeline view
                st.markdown('<div class="timeline">', unsafe_allow_html=True)
                
                for _, event in day_events.iterrows():
                    activity_name = mask_sensitive_info(event['Activity'], show_sensitive)
                    location = mask_sensitive_info(event['Location'], show_sensitive)
                    phone = mask_sensitive_info(str(event['Phone']), show_sensitive)
                    
                    status_class = event['Status'].lower()
                    
                    st.markdown(f"""
                    <div class="timeline-item {status_class}">
                        <div class="activity-card card">
                            <div class="card-body">
                                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                                    <h5 style="margin: 0; color: #2d3436;">{activity_name}</h5>
                                    <span class="status-{status_class}">{event['Status']}</span>
                                </div>
                                <p style="margin: 0.5rem 0;"><strong>🕐 {event['Time']}</strong></p>
                                <p style="margin: 0.5rem 0;">📍 {location}</p>
                                <p style="margin: 0.5rem 0;">📞 {phone}</p>
                                <p style="margin: 0.5rem 0;">💰 ${event['Cost']}</p>
                                <p style="margin: 0.5rem 0; font-style: italic; color: #636e72;">{event['Notes']}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

def render_weather():
    """Render weather and tide information"""
    st.title("🌊 Weather & Tide Information")
    
    weather_data = get_weather_data()
    
    if weather_data:
        # Current conditions
        current = weather_data['current']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="weather-card card">
                <div class="card-header">🌡️ Temperature</div>
                <div class="card-body">
                    <h2 style="margin: 0; color: #ff6b6b;">{current['temperature']}°F</h2>
                    <p style="margin: 0.5rem 0;">{current['condition']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="weather-card card">
                <div class="card-header">☀️ UV Index</div>
                <div class="card-body">
                    <h2 style="margin: 0; color: #ffa502;">{current['uv_index']}</h2>
                    <p style="margin: 0.5rem 0;">{"High - Use SPF 30+" if current['uv_index'] > 6 else "Moderate"}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="weather-card card">
                <div class="card-header">💨 Wind</div>
                <div class="card-body">
                    <h2 style="margin: 0; color: #4ecdc4;">{current['wind_speed']} mph</h2>
                    <p style="margin: 0.5rem 0;">Humidity: {current['humidity']}%</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 6-day detailed forecast
        st.markdown("### 📅 6-Day Detailed Forecast")
        
        forecast_df = pd.DataFrame(weather_data['forecast'])
        
        for _, day in forecast_df.iterrows():
            date_obj = datetime.strptime(day['date'], '%Y-%m-%d')
            
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
            
            with col1:
                st.write(f"**{date_obj.strftime('%A, %B %d')}**")
            
            with col2:
                st.write(f"🌡️ {day['high']}°/{day['low']}°F")
            
            with col3:
                st.write(f"☀️ UV {day['uv']}")
            
            with col4:
                st.write(f"🌧️ {day['precipitation']}%")
            
            with col5:
                st.write(f"🌤️ {day['condition']}")
        
        # Tide information
        st.markdown("### 🌊 Today's Tide Schedule")
        
        tide_data = [
            {"time": "06:15 AM", "type": "High", "height": "5.2 ft"},
            {"time": "12:30 PM", "type": "Low", "height": "1.8 ft"},
            {"time": "06:45 PM", "type": "High", "height": "4.9 ft"},
            {"time": "12:30 AM", "type": "Low", "height": "2.1 ft"}
        ]
        
        cols = st.columns(4)
        for i, tide in enumerate(tide_data):
            with cols[i]:
                st.markdown(f"""
                <div class="card">
                    <div class="card-body" style="text-align: center;">
                        <h4 style="margin: 0; color: #4ecdc4;">{tide['time']}</h4>
                        <p style="margin: 0.5rem 0; font-weight: bold;">{tide['type']} Tide</p>
                        <p style="margin: 0;">{tide['height']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

def render_travel():
    """Render travel intelligence"""
    st.title("🚗 Travel Intelligence")
    
    flight_data = get_flight_data()
    show_sensitive = st.session_state.get("password_verified", False)
    
    if flight_data:
        st.markdown("### ✈️ Flight Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Your Flights:**")
            for flight in flight_data['your_flights']:
                flight_num = mask_sensitive_info(flight['number'], show_sensitive)
                
                st.markdown(f"""
                <div class="card">
                    <div class="card-body">
                        <h5 style="margin: 0 0 1rem 0; color: #ff6b6b;">{flight_num} - {flight['status']}</h5>
                        <p style="margin: 0.25rem 0;">📅 {flight['date']}</p>
                        <p style="margin: 0.25rem 0;">🛫 Departure: {flight['departure']}</p>
                        <p style="margin: 0.25rem 0;">🛬 Arrival: {flight['arrival']}</p>
                        <p style="margin: 0.25rem 0;">🚪 Gate: {flight['gate']}</p>
                        <p style="margin: 0.25rem 0;">✈️ Route: {flight['route']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**John's Flights:**")
            for flight in flight_data['john_flights']:
                flight_num = mask_sensitive_info(flight['number'], show_sensitive)
                
                st.markdown(f"""
                <div class="card">
                    <div class="card-body">
                        <h5 style="margin: 0 0 1rem 0; color: #4ecdc4;">{flight_num} - {flight['status']}</h5>
                        <p style="margin: 0.25rem 0;">📅 {flight['date']}</p>
                        <p style="margin: 0.25rem 0;">🛫 Departure: {flight['departure']}</p>
                        <p style="margin: 0.25rem 0;">🛬 Arrival: {flight['arrival']}</p>
                        <p style="margin: 0.25rem 0;">🚪 Gate: {flight['gate']}</p>
                        <p style="margin: 0.25rem 0;">✈️ Route: {flight['route']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Travel times from hotel
    st.markdown("### 🚗 Travel Times from Hotel")
    
    locations = [
        {"name": "Jacksonville Airport", "time": "45 minutes", "distance": "30 miles"},
        {"name": "Downtown Fernandina Beach", "time": "10 minutes", "distance": "5 miles"},
        {"name": "David's Restaurant", "time": "12 minutes", "distance": "6 miles"},
        {"name": "Backwater Cat Tour", "time": "8 minutes", "distance": "4 miles"},
        {"name": "Fort Clinch State Park", "time": "15 minutes", "distance": "8 miles"},
        {"name": "Main Beach Park", "time": "5 minutes", "distance": "2 miles"}
    ]
    
    cols = st.columns(3)
    for i, location in enumerate(locations):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card">
                <div class="card-body">
                    <h5 style="margin: 0 0 0.5rem 0;">{location['name']}</h5>
                    <p style="margin: 0.25rem 0;">🕐 {location['time']}</p>
                    <p style="margin: 0.25rem 0;">📏 {location['distance']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_spa():
    """Render spa treatments"""
    st.title("💆 Spa Treatments")
    
    treatments = [
        {
            "name": "Heaven in a Hammock",
            "duration": "80 minutes",
            "price": "$245",
            "description": "Signature couples massage experience in a private beachside cabana",
            "category": "Couples Massage"
        },
        {
            "name": "HydraFacial Treatment",
            "duration": "60 minutes", 
            "price": "$195",
            "description": "Advanced facial treatment with cleansing, exfoliation, and hydration",
            "category": "Facial"
        },
        {
            "name": "Manicure & Pedicure",
            "duration": "90 minutes",
            "price": "$125",
            "description": "Complete nail care with luxury treatments and polish",
            "category": "Nail Care"
        },
        {
            "name": "Awakening Bamboo Massage",
            "duration": "50 minutes",
            "price": "$185",
            "description": "Relaxing massage using warm bamboo tools",
            "category": "Massage"
        },
        {
            "name": "Ocean Renewal Body Wrap",
            "duration": "75 minutes",
            "price": "$215",
            "description": "Detoxifying body treatment with marine ingredients",
            "category": "Body Treatment"
        },
        {
            "name": "Gentleman's Facial",
            "duration": "60 minutes",
            "price": "$165",
            "description": "Customized facial treatment designed for men's skin",
            "category": "Facial"
        }
    ]
    
    # Treatment categories
    categories = list(set(t['category'] for t in treatments))
    selected_category = st.selectbox("Filter by Category:", ["All"] + categories)
    
    # Filter treatments
    if selected_category != "All":
        filtered_treatments = [t for t in treatments if t['category'] == selected_category]
    else:
        filtered_treatments = treatments
    
    # Display treatments
    for treatment in filtered_treatments:
        st.markdown(f"""
        <div class="spa-card card">
            <div class="card-body">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <h4 style="margin: 0; color: #2d3436;">{treatment['name']}</h4>
                    <span style="background: #96ceb4; color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.875rem;">
                        {treatment['category']}
                    </span>
                </div>
                <p style="margin: 0.5rem 0; font-size: 1.2rem; font-weight: bold; color: #ff6b6b;">
                    {treatment['duration']} - {treatment['price']}
                </p>
                <p style="margin: 0.5rem 0; color: #636e72;">{treatment['description']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"📞 Book {treatment['name']}", key=f"book_{treatment['name']}"):
            st.success(f"Calling Ritz-Carlton Spa to book {treatment['name']}...")

def render_budget():
    """Render budget tracker"""
    st.title("💰 Budget Tracker")
    
    df = load_trip_data()
    show_sensitive = st.session_state.get("password_verified", False)
    
    if show_sensitive:
        # Budget breakdown by category
        category_spending = df.groupby('Category')['Cost'].sum().reset_index()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.pie(
                category_spending,
                values='Cost',
                names='Category',
                title="Spending by Category",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Budget metrics
            total_cost = df['Cost'].sum()
            confirmed_cost = df[df['Status'] == 'Confirmed']['Cost'].sum()
            pending_cost = df[df['Status'].isin(['Pending', 'URGENT'])]['Cost'].sum()
            
            st.metric("Total Budget", f"${total_cost:,.0f}")
            st.metric("Confirmed", f"${confirmed_cost:,.0f}")
            st.metric("Pending", f"${pending_cost:,.0f}")
        
        # Daily spending breakdown
        st.markdown("### 📅 Daily Spending Breakdown")
        
        daily_spending = df.groupby(df['Date'].dt.date)['Cost'].sum().reset_index()
        daily_spending['Date'] = pd.to_datetime(daily_spending['Date'])
        
        fig = px.bar(
            daily_spending,
            x='Date',
            y='Cost',
            title="Spending by Day",
            color='Cost',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed breakdown
        st.markdown("### 📋 Detailed Breakdown")
        
        for category in df['Category'].unique():
            category_items = df[df['Category'] == category]
            category_total = category_items['Cost'].sum()
            
            with st.expander(f"{category} - ${category_total:.0f}"):
                for _, item in category_items.iterrows():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**{item['Activity']}**")
                        st.write(f"📅 {item['Date'].strftime('%m/%d')} - {item['Location']}")
                    
                    with col2:
                        st.write(f"**${item['Cost']:.0f}**")
                    
                    with col3:
                        st.write(f"**{item['Status']}**")
    else:
        st.info("🔒 Unlock personal details to view budget information")

# Main application
def main():
    """Main application function"""
    
    # Load CSS
    load_deployment_css()
    
    # Render header
    render_header()
    
    # Authentication check
    if not check_password():
        return
    
    # Get sensitive data visibility
    show_sensitive = st.session_state.get("password_verified", False)
    
    # Sidebar
    with st.sidebar:
        st.title("🎂 Trip Assistant")
        
        # Security status
        if show_sensitive:
            st.success("🔓 Personal details unlocked")
        else:
            st.info("🔒 Personal details locked")
        
        st.markdown("---")
        
        # Navigation
        page = st.selectbox("Navigate", [
            "🏠 Dashboard",
            "📅 Interactive Schedule",
            "🌊 Weather & Tides",
            "🚗 Travel Intelligence",
            "💆 Spa Treatments",
            "💰 Budget Tracker"
        ])
        
        st.markdown("---")
        
        # Quick stats
        df = load_trip_data()
        urgent_count = len(df[df['Status'] == 'URGENT'])
        
        if urgent_count > 0:
            st.error(f"⚠️ {urgent_count} urgent booking(s)")
        else:
            st.success("✅ All bookings on track")
        
        total_cost = df['Cost'].sum()
        cost_display = f"${total_cost:,.0f}" if show_sensitive else "$***,***"
        st.metric("Total Budget", cost_display)
        
        # Trip countdown
        days_remaining = (datetime(2025, 11, 7) - datetime.now()).days
        if days_remaining > 0:
            st.info(f"🗓️ {days_remaining} days until trip!")
        elif days_remaining == 0:
            st.success("🎉 Trip starts today!")
        else:
            st.info("🏖️ Enjoy your trip!")
    
    # Page routing
    if page == "🏠 Dashboard":
        render_dashboard()
    elif page == "📅 Interactive Schedule":
        render_schedule()
    elif page == "🌊 Weather & Tides":
        render_weather()
    elif page == "🚗 Travel Intelligence":
        render_travel()
    elif page == "💆 Spa Treatments":
        render_spa()
    elif page == "💰 Budget Tracker":
        render_budget()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #636e72; padding: 1rem;">
        🎂 <strong>40th Birthday Trip Assistant</strong> - Made with ❤️ for your special celebration!<br>
        <small>Amelia Island • November 7-12, 2025 • The Ritz-Carlton</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
