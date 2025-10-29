#!/usr/bin/env python3
"""
Test script to verify GitHub token loading mechanism
"""
import os
import sys
import json

print("=" * 60)
print("GITHUB TOKEN LOADING TEST")
print("=" * 60)

# Test 1: Load secrets from file directly
print("\n1. Testing direct file read of secrets.toml...")
try:
    import toml
    secrets = toml.load('.streamlit/secrets.toml')
    if 'GITHUB_TOKEN' in secrets:
        token = secrets['GITHUB_TOKEN']
        print(f"   ✅ Token found in secrets.toml (length: {len(token)})")
        print(f"   Token starts with: {token[:20]}...")
        print(f"   Token ends with: ...{token[-20:]}")
    else:
        print("   ❌ GITHUB_TOKEN not found in secrets.toml")
except Exception as e:
    print(f"   ❌ Error reading secrets.toml: {e}")

# Test 2: Load environment variable
print("\n2. Testing environment variable...")
env_token = os.getenv('GITHUB_TOKEN')
if env_token:
    print(f"   ✅ Token found in environment (length: {len(env_token)})")
else:
    print("   ❌ GITHUB_TOKEN not found in environment variables")

# Test 3: Simulate what app.py does
print("\n3. Simulating app.py load_secrets_to_env()...")
try:
    secrets = toml.load('.streamlit/secrets.toml')
    for key in ['GITHUB_TOKEN']:
        if key in secrets:
            os.environ[key] = secrets[key]
            print(f"   ✅ Set {key} in os.environ (length: {len(secrets[key])})")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Simulate what github_storage.py does
print("\n4. Simulating github_storage.py _get_github_token()...")
token = os.getenv('GITHUB_TOKEN')
if token:
    print(f"   ✅ Token loaded from os.environ (length: {len(token)})")
else:
    print("   ❌ No token found in os.environ")

# Test 5: Make actual GitHub API call
print("\n5. Testing actual GitHub API call...")
if token:
    import requests
    url = "https://api.github.com/repos/WanderingWithPride/40thBdayAppRebuild/contents/data/trip_data.json"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ SUCCESS! GitHub API call worked!")
            data = response.json()
            print(f"   File: {data['name']} ({data['size']} bytes)")
        elif response.status_code == 401:
            print(f"   ❌ FAILED! 401 Unauthorized")
            print(f"   Response: {response.text}")
        else:
            print(f"   ⚠️ Unexpected status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error making API call: {e}")
else:
    print("   ⚠️ Skipping - no token available")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
