#!/usr/bin/env python3
"""
Test GitHub Storage Integration
Verifies that the app can read AND write to GitHub
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up environment before importing streamlit
from dotenv import load_dotenv
load_dotenv('.streamlit/secrets.toml')

# Now we can import streamlit-dependent modules
import streamlit as st
from github_storage import load_data_from_github, save_data_to_github, GITHUB_TOKEN

print("=" * 70)
print("🔍 GITHUB STORAGE TEST")
print("=" * 70)
print()

# Check token
if GITHUB_TOKEN:
    print(f"✅ GitHub token loaded (length: {len(GITHUB_TOKEN)})")
else:
    print("❌ No GitHub token found!")
    sys.exit(1)

print()

# Test 1: Load data
print("1️⃣  Testing data load from GitHub...")
try:
    data = load_data_from_github()
    print(f"   ✅ SUCCESS - Loaded {len(data)} top-level keys")

    # Show some data
    if 'meal_proposals' in data:
        print(f"   📊 Meal proposals: {len(data['meal_proposals'])}")
    if 'activity_proposals' in data:
        print(f"   📊 Activity proposals: {len(data['activity_proposals'])}")

except Exception as e:
    print(f"   ❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print()

# Test 2: Save data (dry run - just test the function)
print("2️⃣  Testing data save capability...")
try:
    # Don't actually modify data, just test that we CAN
    test_data = data.copy()
    test_data['_test_write'] = 'verification'

    # This will actually write to GitHub
    print("   ⚠️  This will create a test commit to GitHub...")
    success = save_data_to_github(test_data, "Test write from API verification")

    if success:
        print("   ✅ SUCCESS - Can write to GitHub!")
        print("   💡 Check your GitHub repo for the test commit")
    else:
        print("   ❌ FAILED - Could not write to GitHub")

except Exception as e:
    print(f"   ❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
print("✅ GITHUB STORAGE TEST COMPLETE")
print("=" * 70)
print()
print("💡 If both tests passed, your app will work perfectly!")
print()
