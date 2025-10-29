#!/usr/bin/env python3
"""
Streamlit Diagnostic Tool for GitHub 401 Issues
Run this with: streamlit run diagnose_github_issue.py
"""
import streamlit as st
import os
import sys

st.set_page_config(page_title="GitHub Token Diagnostic", page_icon="🔍")

st.title("🔍 GitHub Token Diagnostic Tool")
st.markdown("---")

# Test 1: Check if secrets file exists
st.header("1. Secrets File Check")
import os.path
if os.path.exists('.streamlit/secrets.toml'):
    st.success("✅ secrets.toml file exists")
    try:
        with open('.streamlit/secrets.toml', 'r') as f:
            content = f.read()
            if 'GITHUB_TOKEN' in content:
                st.success("✅ GITHUB_TOKEN found in secrets.toml")
                # Count token length without exposing it
                lines = content.split('\n')
                for line in lines:
                    if line.strip().startswith('GITHUB_TOKEN'):
                        token_value = line.split('=')[1].strip().strip('"')
                        st.info(f"Token length: {len(token_value)} characters")
            else:
                st.error("❌ GITHUB_TOKEN not found in secrets.toml")
    except Exception as e:
        st.error(f"❌ Error reading secrets.toml: {e}")
else:
    st.error("❌ secrets.toml file not found")

# Test 2: Check Streamlit secrets
st.header("2. Streamlit Secrets Check")
try:
    if hasattr(st, 'secrets'):
        st.success("✅ st.secrets is available")
        if 'GITHUB_TOKEN' in st.secrets:
            token = st.secrets['GITHUB_TOKEN']
            st.success(f"✅ GITHUB_TOKEN loaded from st.secrets (length: {len(token)})")
            st.code(f"Token preview: {token[:20]}...{token[-10:]}")
        else:
            st.error("❌ GITHUB_TOKEN not in st.secrets")
            st.info(f"Available keys: {list(st.secrets.keys())}")
    else:
        st.error("❌ st.secrets not available")
except Exception as e:
    st.error(f"❌ Error accessing st.secrets: {e}")

# Test 3: Check environment variables
st.header("3. Environment Variable Check")
env_token = os.getenv('GITHUB_TOKEN')
if env_token:
    st.success(f"✅ GITHUB_TOKEN in environment (length: {len(env_token)})")
else:
    st.warning("⚠️ GITHUB_TOKEN not in environment variables")
    st.info("This is OK if st.secrets works (fallback mechanism)")

# Test 4: Test github_storage module
st.header("4. GitHub Storage Module Test")
try:
    from github_storage import _get_github_token
    st.success("✅ github_storage module imported successfully")

    token = _get_github_token()
    if token:
        st.success(f"✅ _get_github_token() returned token (length: {len(token)})")
    else:
        st.error("❌ _get_github_token() returned None")
except Exception as e:
    st.error(f"❌ Error importing github_storage: {e}")
    st.exception(e)

# Test 5: Test actual GitHub API call
st.header("5. GitHub API Call Test")
if st.button("Test GitHub API Connection"):
    with st.spinner("Testing GitHub API..."):
        try:
            from github_storage import load_data_from_github
            import sys
            from io import StringIO

            # Capture print output
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()

            # Try to load data
            data = load_data_from_github()

            # Get captured output
            sys.stdout = old_stdout
            debug_output = mystdout.getvalue()

            if data and "meal_proposals" in data:
                st.success("✅ Successfully loaded data from GitHub!")
                st.json({"keys": list(data.keys())[:5]})

                if debug_output:
                    st.text_area("Debug Output:", debug_output, height=150)
            else:
                st.error("❌ Failed to load data or data is empty")
                if debug_output:
                    st.error("Debug output:")
                    st.code(debug_output)
        except Exception as e:
            st.error(f"❌ Error during API call: {e}")
            st.exception(e)

# Test 6: Direct API test
st.header("6. Direct API Test (Manual)")
if st.button("Test Direct GitHub API"):
    with st.spinner("Making direct API call..."):
        try:
            import requests

            # Get token
            if 'GITHUB_TOKEN' in st.secrets:
                token = st.secrets['GITHUB_TOKEN']
            else:
                token = os.getenv('GITHUB_TOKEN')

            if not token:
                st.error("❌ No token available for testing")
            else:
                url = "https://api.github.com/repos/WanderingWithPride/40thBdayAppRebuild/contents/data/trip_data.json"
                headers = {
                    "Authorization": f"token {token}",
                    "Accept": "application/vnd.github.v3+json"
                }

                response = requests.get(url, headers=headers, timeout=10)

                st.info(f"Status Code: {response.status_code}")

                if response.status_code == 200:
                    st.success("✅ GitHub API call successful!")
                    data = response.json()
                    st.json({"name": data['name'], "size": data['size'], "sha": data['sha'][:10]})
                elif response.status_code == 401:
                    st.error("❌ 401 Unauthorized - Token is invalid or expired")
                    st.code(response.text)
                else:
                    st.warning(f"⚠️ Unexpected status code: {response.status_code}")
                    st.code(response.text)
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.exception(e)

st.markdown("---")
st.markdown("""
### 📋 Summary

This diagnostic tool tests:
1. ✅ Secrets file exists and contains token
2. ✅ Streamlit can access the token via st.secrets
3. ⚠️ Environment variables (optional - fallback works)
4. ✅ github_storage module loads correctly
5. ✅ load_data_from_github() function works
6. ✅ Direct GitHub API access works

**If all tests pass**, the 401 error might be due to:
- Cached Python bytecode (.pyc files) - try restarting Streamlit
- Streamlit caching - clear with `Ctrl+Shift+R` or `⌘+Shift+R`
- Running old code - ensure latest changes are pulled from git

**Next steps if tests fail:**
- Check which specific test fails
- Review error messages above
- Verify token hasn't expired (expires Nov 27, 2025)
""")
