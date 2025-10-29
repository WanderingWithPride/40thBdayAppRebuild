#!/usr/bin/env python3
"""
Comprehensive Google Maps Platform API Testing
Tests all 8 APIs integrated into the Birthday Trip App
"""

import os
import requests
import json
from datetime import datetime

# Load API key from secrets
try:
    import toml
    secrets = toml.load('.streamlit/secrets.toml')
    API_KEY = secrets.get('GOOGLE_MAPS_API_KEY', '')
except:
    API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

print("=" * 80)
print("🗺️  COMPREHENSIVE GOOGLE MAPS PLATFORM API TESTING")
print("=" * 80)
print(f"Testing with API Key: {API_KEY[:20]}...{API_KEY[-10:] if len(API_KEY) > 30 else ''}")
print(f"Timestamp: {datetime.now().isoformat()}")
print("=" * 80)
print()

# Test coordinates for Amelia Island
AMELIA_ISLAND = (30.6687, -81.4618)
JAX_AIRPORT = (30.4941, -81.6879)

results = {
    "passed": [],
    "failed": [],
    "warnings": []
}

# ==============================================================================
# Test 1: Distance Matrix API (Traffic & Drive Times)
# ==============================================================================
print("1️⃣  Testing Distance Matrix API (Traffic & Drive Times)")
print("-" * 80)
try:
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        'origins': f'{JAX_AIRPORT[0]},{JAX_AIRPORT[1]}',
        'destinations': f'{AMELIA_ISLAND[0]},{AMELIA_ISLAND[1]}',
        'departure_time': 'now',
        'traffic_model': 'best_guess',
        'key': API_KEY
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    if data.get('status') == 'OK':
        element = data['rows'][0]['elements'][0]
        if element['status'] == 'OK':
            distance = element['distance']['text']
            duration = element['duration']['text']
            traffic_duration = element.get('duration_in_traffic', {}).get('text', 'N/A')
            print(f"   ✅ SUCCESS")
            print(f"   📍 JAX Airport → Amelia Island")
            print(f"   📏 Distance: {distance}")
            print(f"   ⏱️  Duration: {duration}")
            print(f"   🚗 With Traffic: {traffic_duration}")
            results["passed"].append("Distance Matrix API")
        else:
            print(f"   ❌ FAILED - Element Status: {element['status']}")
            results["failed"].append("Distance Matrix API")
    else:
        print(f"   ❌ FAILED - API Status: {data.get('status')}")
        print(f"   💡 Error: {data.get('error_message', 'Unknown error')}")
        results["failed"].append("Distance Matrix API")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    results["failed"].append("Distance Matrix API")
print()

# ==============================================================================
# Test 2: Places API (New) - Restaurant Search
# ==============================================================================
print("2️⃣  Testing Places API (New) - Restaurant Discovery")
print("-" * 80)
try:
    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'places.id,places.displayName,places.rating,places.userRatingCount'
    }
    data = {
        "includedTypes": ["restaurant"],
        "maxResultCount": 5,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": AMELIA_ISLAND[0],
                    "longitude": AMELIA_ISLAND[1]
                },
                "radius": 2000
            }
        }
    }
    response = requests.post(url, headers=headers, json=data, timeout=10)
    result = response.json()

    if 'places' in result and len(result['places']) > 0:
        print(f"   ✅ SUCCESS - Found {len(result['places'])} restaurants")
        for i, place in enumerate(result['places'][:3], 1):
            name = place.get('displayName', {}).get('text', 'Unknown')
            rating = place.get('rating', 'N/A')
            count = place.get('userRatingCount', 0)
            print(f"   {i}. {name} - ⭐ {rating} ({count} reviews)")
        results["passed"].append("Places API (New)")
    else:
        print(f"   ❌ FAILED - No places found")
        print(f"   Response: {result}")
        results["failed"].append("Places API (New)")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    results["failed"].append("Places API (New)")
print()

# ==============================================================================
# Test 3: Geocoding API - Address Validation
# ==============================================================================
print("3️⃣  Testing Geocoding API - Address Validation")
print("-" * 80)
try:
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': '4750 Amelia Island Parkway, Fernandina Beach, FL',
        'key': API_KEY
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    if data.get('status') == 'OK' and len(data['results']) > 0:
        result = data['results'][0]
        formatted_address = result['formatted_address']
        location = result['geometry']['location']
        print(f"   ✅ SUCCESS")
        print(f"   📍 Address: {formatted_address}")
        print(f"   🌐 Coordinates: {location['lat']:.4f}, {location['lng']:.4f}")
        results["passed"].append("Geocoding API")
    else:
        print(f"   ❌ FAILED - Status: {data.get('status')}")
        results["failed"].append("Geocoding API")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    results["failed"].append("Geocoding API")
print()

# ==============================================================================
# Test 4: Directions API - Turn-by-Turn Navigation
# ==============================================================================
print("4️⃣  Testing Directions API - Turn-by-Turn Navigation")
print("-" * 80)
try:
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        'origin': f'{JAX_AIRPORT[0]},{JAX_AIRPORT[1]}',
        'destination': f'{AMELIA_ISLAND[0]},{AMELIA_ISLAND[1]}',
        'mode': 'driving',
        'departure_time': 'now',
        'key': API_KEY
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    if data.get('status') == 'OK':
        route = data['routes'][0]
        leg = route['legs'][0]
        print(f"   ✅ SUCCESS")
        print(f"   🗺️  Route: {leg['start_address']} → {leg['end_address']}")
        print(f"   📏 Distance: {leg['distance']['text']}")
        print(f"   ⏱️  Duration: {leg['duration']['text']}")
        print(f"   🔄 Steps: {len(leg['steps'])} navigation steps")
        results["passed"].append("Directions API")
    else:
        print(f"   ❌ FAILED - Status: {data.get('status')}")
        results["failed"].append("Directions API")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    results["failed"].append("Directions API")
print()

# ==============================================================================
# Test 5: Static Maps API - Map Image Generation
# ==============================================================================
print("5️⃣  Testing Static Maps API - Map Image Generation")
print("-" * 80)
try:
    url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        'center': f'{AMELIA_ISLAND[0]},{AMELIA_ISLAND[1]}',
        'zoom': 13,
        'size': '400x400',
        'markers': f'color:red|{AMELIA_ISLAND[0]},{AMELIA_ISLAND[1]}',
        'key': API_KEY
    }
    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 200 and 'image' in response.headers.get('content-type', ''):
        size_kb = len(response.content) / 1024
        print(f"   ✅ SUCCESS")
        print(f"   🖼️  Generated map image: {size_kb:.1f} KB")
        print(f"   📐 Size: 400x400 pixels")
        results["passed"].append("Static Maps API")
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type')}")
        results["failed"].append("Static Maps API")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    results["failed"].append("Static Maps API")
print()

# ==============================================================================
# Test 6: Air Quality API - Outdoor Activity Safety
# ==============================================================================
print("6️⃣  Testing Air Quality API - Outdoor Activity Safety")
print("-" * 80)
try:
    url = "https://airquality.googleapis.com/v1/currentConditions:lookup"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "location": {
            "latitude": AMELIA_ISLAND[0],
            "longitude": AMELIA_ISLAND[1]
        }
    }
    params = {'key': API_KEY}
    response = requests.post(url, headers=headers, json=data, params=params, timeout=10)

    if response.status_code == 200:
        result = response.json()
        if 'indexes' in result:
            aqi = result['indexes'][0]
            print(f"   ✅ SUCCESS")
            print(f"   🌬️  AQI: {aqi.get('aqi', 'N/A')} - {aqi.get('category', 'Unknown')}")
            print(f"   📊 Dominant Pollutant: {aqi.get('dominantPollutant', 'N/A')}")
            results["passed"].append("Air Quality API")
        else:
            print(f"   ⚠️  WARNING - No air quality data available")
            print(f"   Response: {result}")
            results["warnings"].append("Air Quality API - No data")
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        results["failed"].append("Air Quality API")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    results["failed"].append("Air Quality API")
print()

# ==============================================================================
# Test 7: Routes API (New) - Optimized Routing
# ==============================================================================
print("7️⃣  Testing Routes API (New) - Optimized Routing")
print("-" * 80)
try:
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters,routes.polyline'
    }
    data = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": JAX_AIRPORT[0],
                    "longitude": JAX_AIRPORT[1]
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": AMELIA_ISLAND[0],
                    "longitude": AMELIA_ISLAND[1]
                }
            }
        },
        "travelMode": "DRIVE"
    }
    response = requests.post(url, headers=headers, json=data, timeout=10)

    if response.status_code == 200:
        result = response.json()
        if 'routes' in result and len(result['routes']) > 0:
            route = result['routes'][0]
            duration = route.get('duration', '0s')
            distance = route.get('distanceMeters', 0)
            print(f"   ✅ SUCCESS")
            print(f"   🛣️  Distance: {distance / 1609:.1f} miles ({distance}m)")
            print(f"   ⏱️  Duration: {duration}")
            results["passed"].append("Routes API (New)")
        else:
            print(f"   ❌ FAILED - No routes found")
            results["failed"].append("Routes API (New)")
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        results["failed"].append("Routes API (New)")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    results["failed"].append("Routes API (New)")
print()

# ==============================================================================
# Test 8: Street View Static API - Location Previews
# ==============================================================================
print("8️⃣  Testing Street View Static API - Location Previews")
print("-" * 80)
try:
    url = "https://maps.googleapis.com/maps/api/streetview"
    params = {
        'size': '400x400',
        'location': f'{AMELIA_ISLAND[0]},{AMELIA_ISLAND[1]}',
        'heading': '90',
        'pitch': '0',
        'fov': '90',
        'key': API_KEY
    }
    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 200 and 'image' in response.headers.get('content-type', ''):
        size_kb = len(response.content) / 1024
        print(f"   ✅ SUCCESS")
        print(f"   📸 Generated Street View image: {size_kb:.1f} KB")
        print(f"   📐 Size: 400x400 pixels")
        results["passed"].append("Street View Static API")
    else:
        print(f"   ⚠️  WARNING - May not have Street View coverage at this location")
        print(f"   Status: {response.status_code}")
        results["warnings"].append("Street View - No coverage at test location")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    results["failed"].append("Street View Static API")
print()

# ==============================================================================
# SUMMARY
# ==============================================================================
print("=" * 80)
print("📊 TEST SUMMARY")
print("=" * 80)
print(f"✅ Passed: {len(results['passed'])}/8")
print(f"❌ Failed: {len(results['failed'])}/8")
print(f"⚠️  Warnings: {len(results['warnings'])}")
print()

if results['passed']:
    print("✅ PASSED APIs:")
    for api in results['passed']:
        print(f"   • {api}")
    print()

if results['failed']:
    print("❌ FAILED APIs:")
    for api in results['failed']:
        print(f"   • {api}")
    print()
    print("💡 Common fixes:")
    print("   1. Verify API key is correct in .streamlit/secrets.toml")
    print("   2. Enable missing APIs in Google Cloud Console:")
    print("      https://console.cloud.google.com/google/maps-apis")
    print("   3. Check API key restrictions (IP, referrer, API limits)")
    print("   4. Ensure billing is enabled (free tier is sufficient)")
    print()

if results['warnings']:
    print("⚠️  WARNINGS:")
    for warning in results['warnings']:
        print(f"   • {warning}")
    print()

# Overall status
if len(results['passed']) == 8:
    print("🎉 ALL TESTS PASSED! Your Google Maps Platform integration is fully operational!")
elif len(results['passed']) >= 6:
    print("✅ MOSTLY WORKING! Core APIs are functional. Check warnings above.")
elif len(results['passed']) >= 3:
    print("⚠️  PARTIAL SUCCESS. Some APIs working but configuration needed.")
else:
    print("❌ CRITICAL: Most APIs failing. Check your API key and Cloud Console setup.")

print("=" * 80)
