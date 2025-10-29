#!/usr/bin/env python3
"""
Test Live API Connections
Verifies that all API keys work with actual API calls
"""

import os
import requests
from dotenv import load_dotenv

# Load from .streamlit/secrets.toml or .env
load_dotenv('.streamlit/secrets.toml')

print("=" * 70)
print("🔌 TESTING LIVE API CONNECTIONS")
print("=" * 70)
print()

# Test 1: GitHub API
print("1️⃣  Testing GitHub Token...")
github_token = os.getenv('GITHUB_TOKEN')
if github_token:
    try:
        response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'token {github_token}'},
            timeout=5
        )
        if response.status_code == 200:
            user = response.json()
            print(f"   ✅ SUCCESS - Connected as: {user.get('login', 'Unknown')}")
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            try:
                error_details = response.json()
                print(f"   ❌ Details: {error_details}")
            except:
                pass
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
else:
    print("   ⚠️  No token found")
print()

# Test 2: OpenWeather API
print("2️⃣  Testing OpenWeather API...")
weather_key = os.getenv('OPENWEATHER_API_KEY')
if weather_key:
    try:
        # Test with Amelia Island coordinates
        lat, lon = 30.6687, -81.4618
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_key}&units=imperial"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            condition = data['weather'][0]['description']
            print(f"   ✅ SUCCESS - Amelia Island: {temp}°F, {condition}")
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            if response.status_code == 401:
                print(f"   💡 Key may need activation (wait 10 mins after signup)")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
else:
    print("   ⚠️  No key found")
print()

# Test 3: Google Maps API
print("3️⃣  Testing Google Maps API...")
maps_key = os.getenv('GOOGLE_MAPS_API_KEY')
if maps_key:
    try:
        # Test with simple distance calculation
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            'origins': 'Jacksonville Airport',
            'destinations': 'Amelia Island',
            'key': maps_key
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK':
                distance = data['rows'][0]['elements'][0].get('distance', {}).get('text', 'N/A')
                duration = data['rows'][0]['elements'][0].get('duration', {}).get('text', 'N/A')
                print(f"   ✅ SUCCESS - JAX to Amelia: {distance}, {duration}")
            else:
                print(f"   ❌ FAILED - API Status: {data.get('status')}")
                print(f"   💡 Error: {data.get('error_message', 'Unknown error')}")
        else:
            print(f"   ❌ FAILED - HTTP Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
else:
    print("   ⚠️  No key found")
print()

# Test 4: AviationStack API
print("4️⃣  Testing AviationStack API...")
aviation_key = os.getenv('AVIATIONSTACK_API_KEY')
if aviation_key:
    try:
        # Test with simple flight query
        url = f"http://api.aviationstack.com/v1/flights"
        params = {
            'access_key': aviation_key,
            'limit': 1
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                print(f"   ✅ SUCCESS - API responding")
                print(f"   💡 Pagination: {data.get('pagination', {})}")
            else:
                print(f"   ⚠️  Response: {data}")
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
else:
    print("   ⚠️  No key found")
print()

print("=" * 70)
print("✅ API TESTING COMPLETE")
print("=" * 70)
print()
print("💡 Next Steps:")
print("   • If all tests passed: Run 'streamlit run app.py'")
print("   • If any failed: Check API key activation (may take 5-10 mins)")
print("   • For Google Maps: Ensure Distance Matrix API is enabled")
print()
