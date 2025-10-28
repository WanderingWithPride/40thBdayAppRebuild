#!/usr/bin/env python3
"""
Air Quality & Pollen API Test Script
Tests Google Air Quality and Pollen APIs are working correctly
"""

import os
import sys
import requests
from typing import Optional

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Amelia Island coordinates
AMELIA_LAT = 30.6074
AMELIA_LON = -81.4493


def get_api_key() -> Optional[str]:
    """Get API key from environment or secrets"""
    # Try environment variable first
    api_key = os.getenv('GOOGLE_MAPS_API_KEY', '')
    if api_key:
        return api_key

    # Try streamlit secrets
    try:
        import streamlit as st
        return st.secrets.get("GOOGLE_MAPS_API_KEY", "")
    except:
        pass

    return None


def test_air_quality_api(api_key: str) -> bool:
    """Test Air Quality API"""
    print(f"\n{BLUE}━━━ Testing Air Quality API ━━━{RESET}")

    url = "https://airquality.googleapis.com/v1/currentConditions:lookup"

    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'key': api_key
    }

    data = {
        "location": {
            "latitude": AMELIA_LAT,
            "longitude": AMELIA_LON
        }
    }

    try:
        print(f"📡 Fetching air quality data for Amelia Island...")
        response = requests.post(url, headers=headers, params=params, json=data, timeout=10)

        if response.status_code == 200:
            result = response.json()

            # Extract AQI
            indexes = result.get('indexes', [])
            if indexes:
                universal_aqi = next((idx for idx in indexes if idx.get('code') == 'uaqi'), indexes[0])
                aqi = universal_aqi.get('aqi', 0)

                print(f"{GREEN}✓ Air Quality API is working!{RESET}")
                print(f"  📊 Current AQI: {aqi}")
                print(f"  📍 Location: Amelia Island, FL")

                # Show pollutants
                pollutants = result.get('pollutants', [])
                if pollutants:
                    print(f"  🧪 Pollutants detected: {len(pollutants)}")
                    for p in pollutants[:3]:  # Show first 3
                        name = p.get('displayName', p.get('code', 'Unknown'))
                        conc = p.get('concentration', {})
                        value = conc.get('value', 'N/A')
                        units = conc.get('units', '')
                        print(f"     • {name}: {value} {units}")

                return True
            else:
                print(f"{YELLOW}⚠ API responded but no AQI data available{RESET}")
                return False

        elif response.status_code == 403:
            print(f"{RED}✗ API Key issue - 403 Forbidden{RESET}")
            print(f"  Possible reasons:")
            print(f"  1. Air Quality API not enabled in Google Cloud Console")
            print(f"  2. API key doesn't have permission for Air Quality API")
            print(f"  3. Billing not enabled on your Google Cloud project")
            print(f"\n  Fix: Go to https://console.cloud.google.com/apis/library/airquality.googleapis.com")
            return False

        elif response.status_code == 400:
            print(f"{RED}✗ Bad Request - 400{RESET}")
            print(f"  Response: {response.text}")
            return False

        else:
            print(f"{RED}✗ API Error: {response.status_code}{RESET}")
            print(f"  Response: {response.text}")
            return False

    except Exception as e:
        print(f"{RED}✗ Request failed: {e}{RESET}")
        return False


def test_pollen_api(api_key: str) -> bool:
    """Test Pollen API"""
    print(f"\n{BLUE}━━━ Testing Pollen API ━━━{RESET}")

    url = "https://pollen.googleapis.com/v1/forecast:lookup"

    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'key': api_key,
        'days': 5
    }

    data = {
        "location": {
            "latitude": AMELIA_LAT,
            "longitude": AMELIA_LON
        }
    }

    try:
        print(f"📡 Fetching pollen forecast for Amelia Island...")
        response = requests.post(url, headers=headers, params=params, json=data, timeout=10)

        if response.status_code == 200:
            result = response.json()

            # Extract pollen data
            daily_info = result.get('dailyInfo', [])
            if daily_info:
                print(f"{GREEN}✓ Pollen API is working!{RESET}")
                print(f"  📊 Forecast days available: {len(daily_info)}")
                print(f"  📍 Location: Amelia Island, FL")

                # Show today's pollen
                today = daily_info[0]
                plant_info = today.get('plantInfo', [])

                if plant_info:
                    tree_idx = plant_info[0].get('indexInfo', {}).get('value', 0) if len(plant_info) > 0 else 0
                    grass_idx = plant_info[1].get('indexInfo', {}).get('value', 0) if len(plant_info) > 1 else 0
                    weed_idx = plant_info[2].get('indexInfo', {}).get('value', 0) if len(plant_info) > 2 else 0

                    print(f"  🌳 Tree Pollen: Level {tree_idx}/5")
                    print(f"  🌾 Grass Pollen: Level {grass_idx}/5")
                    print(f"  🌿 Weed Pollen: Level {weed_idx}/5")

                return True
            else:
                print(f"{YELLOW}⚠ API responded but no pollen data available{RESET}")
                return False

        elif response.status_code == 403:
            print(f"{RED}✗ API Key issue - 403 Forbidden{RESET}")
            print(f"  Possible reasons:")
            print(f"  1. Pollen API not enabled in Google Cloud Console")
            print(f"  2. API key doesn't have permission for Pollen API")
            print(f"  3. Billing not enabled on your Google Cloud project")
            print(f"\n  Fix: Go to https://console.cloud.google.com/apis/library/pollen.googleapis.com")
            return False

        elif response.status_code == 400:
            print(f"{RED}✗ Bad Request - 400{RESET}")
            print(f"  Response: {response.text}")
            return False

        else:
            print(f"{RED}✗ API Error: {response.status_code}{RESET}")
            print(f"  Response: {response.text}")
            return False

    except Exception as e:
        print(f"{RED}✗ Request failed: {e}{RESET}")
        return False


def main():
    """Main test runner"""
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  Air Quality & Pollen API Test Suite{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

    # Get API key
    api_key = get_api_key()

    if not api_key:
        print(f"\n{RED}✗ No Google Maps API key found!{RESET}")
        print(f"\nPlease set your API key:")
        print(f"  1. Create .streamlit/secrets.toml")
        print(f"  2. Add: GOOGLE_MAPS_API_KEY = \"your_key_here\"")
        print(f"  OR")
        print(f"  export GOOGLE_MAPS_API_KEY=\"your_key_here\"")
        sys.exit(1)

    print(f"\n{GREEN}✓ API key found{RESET}")
    print(f"  Key: {api_key[:10]}...{api_key[-4:]}")

    # Run tests
    air_quality_ok = test_air_quality_api(api_key)
    pollen_ok = test_pollen_api(api_key)

    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  Test Summary{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

    print(f"\n  Air Quality API: {GREEN + '✓ PASS' + RESET if air_quality_ok else RED + '✗ FAIL' + RESET}")
    print(f"  Pollen API:      {GREEN + '✓ PASS' + RESET if pollen_ok else RED + '✗ FAIL' + RESET}")

    if air_quality_ok and pollen_ok:
        print(f"\n{GREEN}🎉 All tests passed! Your APIs are ready to use.{RESET}")
        sys.exit(0)
    else:
        print(f"\n{YELLOW}⚠ Some tests failed. Check the errors above.{RESET}")
        print(f"\n{BLUE}Common fixes:{RESET}")
        print(f"  1. Enable APIs in Google Cloud Console")
        print(f"  2. Enable billing (you get $200/month free credit)")
        print(f"  3. Wait 5-10 minutes after enabling for APIs to activate")
        print(f"  4. Check your API key has correct permissions")
        sys.exit(1)


if __name__ == "__main__":
    main()
