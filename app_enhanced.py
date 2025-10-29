"""
⚠️ DEPRECATED BACKUP FILE - DO NOT USE ⚠️
This is an old backup version. Use app.py for current version.
Passwords and sensitive data in this file are outdated.
===============================================================

🎂 40th Birthday Trip Assistant - ENHANCED VERSION 2.0
=====================================================
Complete trip companion with real-time data, interactive maps, smart features!

Password: 28008985
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
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
import qrcode
from PIL import Image
import io

# Page Configuration
st.set_page_config(
    page_title="40th Birthday Trip - Enhanced",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple test to make sure it works
st.title("🎂 Enhanced 40th Birthday Trip Assistant")
st.success("✅ Enhanced version loading successfully!")
st.info("This is the new enhanced version with maps, real weather, and more!")

# Show what's new
st.markdown("""
### 🚀 What's New in Version 2.0:
- ✨ Interactive maps showing all locations
- 🌤️ Real-time weather integration (when API key provided)
- 🎒 Smart packing list generator
- 📍 Distance and travel time calculations
- 🗺️ Visual trip planning
- 💎 Enhanced UI with modern design
- 📱 Better mobile experience
- 🔔 Smart suggestions and alerts
""")

# Quick demo of a feature
if st.button("🗺️ Show Demo Map"):
    m = folium.Map(location=[30.6074, -81.4493], zoom_start=12)
    folium.Marker(
        [30.6074, -81.4493],
        popup="The Ritz-Carlton, Amelia Island",
        tooltip="Your Hotel",
        icon=folium.Icon(color='red', icon='home', prefix='fa')
    ).add_to(m)
    st_folium(m, width=700, height=500)

