#!/usr/bin/env python3
"""
Quick API Status Checker
Run this to see what's configured and what's missing
"""

import os
from dotenv import load_dotenv

# Load .env if it exists
load_dotenv()

print("=" * 70)
print("🔍 API CONFIGURATION STATUS")
print("=" * 70)
print()

apis = {
    "GITHUB_TOKEN": {
        "name": "GitHub Token",
        "purpose": "Data persistence (votes, preferences)",
        "priority": "⭐ RECOMMENDED",
        "free": True
    },
    "OPENWEATHER_API_KEY": {
        "name": "OpenWeather API",
        "purpose": "Real weather forecasts",
        "priority": "⭐ RECOMMENDED",
        "free": True
    },
    "GOOGLE_MAPS_API_KEY": {
        "name": "Google Maps API",
        "purpose": "Live traffic updates",
        "priority": "Optional",
        "free": True
    },
    "AVIATIONSTACK_API_KEY": {
        "name": "AviationStack API",
        "purpose": "Flight tracking",
        "priority": "Optional",
        "free": True
    }
}

# Check Streamlit secrets
secrets_configured = []
try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        for key in apis.keys():
            if key in st.secrets:
                secrets_configured.append(key)
except:
    pass

configured = []
missing = []

for key, info in apis.items():
    env_value = os.getenv(key)
    in_secrets = key in secrets_configured

    status = "✅ Configured" if (env_value or in_secrets) else "❌ Missing"
    configured.append(key) if (env_value or in_secrets) else missing.append(key)

    source = ""
    if env_value:
        source = f"(in .env, length: {len(env_value)})"
    elif in_secrets:
        source = "(in secrets.toml)"

    print(f"{status} {info['priority']}")
    print(f"   {info['name']}: {info['purpose']}")
    if env_value or in_secrets:
        print(f"   {source}")
    print()

print("=" * 70)
print("📊 SUMMARY")
print("=" * 70)
print(f"✅ Configured: {len(configured)}/{len(apis)}")
print(f"❌ Missing: {len(missing)}/{len(apis)}")
print()

if missing:
    print("🔧 To configure missing APIs:")
    print("   1. See API_SETUP_GUIDE.md for detailed instructions")
    print("   2. Create .streamlit/secrets.toml with your API keys")
    print("   3. Run this script again to verify")
else:
    print("🎉 All APIs configured! Your app is fully functional!")

print()
print("💡 Quick Start:")
print("   • Minimal setup: GITHUB_TOKEN + OPENWEATHER_API_KEY")
print("   • Full experience: All 4 APIs")
print("   • Cost: $0.00 (all have free tiers)")
print()
