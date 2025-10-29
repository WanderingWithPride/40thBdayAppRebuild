#!/usr/bin/env python3
"""
Minimal test to reproduce the exact GitHub 401 issue
Run with: streamlit run test_minimal.py
"""
import streamlit as st
import os
import requests
import sys

st.set_page_config(page_title="Minimal GitHub Test", page_icon="🔬")

st.title("🔬 Minimal GitHub 401 Test")
st.markdown("---")

# Step 1: Check secrets
st.header("Step 1: Check Secrets")
token_from_secrets = None
try:
    if hasattr(st, 'secrets') and 'GITHUB_TOKEN' in st.secrets:
        token_from_secrets = st.secrets['GITHUB_TOKEN']
        st.success(f"✅ Token found in st.secrets (length: {len(token_from_secrets)})")
        st.code(f"{token_from_secrets[:25]}...{token_from_secrets[-15:]}")
    else:
        st.error("❌ No token in st.secrets")
        if hasattr(st, 'secrets'):
            st.info(f"Available keys: {list(st.secrets.keys())}")
except Exception as e:
    st.error(f"❌ Error accessing st.secrets: {e}")

# Step 2: Check environment
st.header("Step 2: Check Environment Variables")
token_from_env = os.getenv('GITHUB_TOKEN')
if token_from_env:
    st.success(f"✅ Token found in environment (length: {len(token_from_env)})")
else:
    st.warning("⚠️ No token in environment")

# Step 3: Mimic what github_storage.py does
st.header("Step 3: Simulate github_storage.py _get_github_token()")

def _get_github_token():
    """Exact copy of function from github_storage.py"""
    # Try environment variable first
    token = os.getenv('GITHUB_TOKEN')
    if token:
        st.info(f"✅ Token loaded from os.environ (length: {len(token)})")
        return token

    # Fallback to Streamlit secrets
    try:
        if hasattr(st, 'secrets'):
            token = st.secrets.get("GITHUB_TOKEN", None)
            if token:
                st.info(f"✅ Token loaded from st.secrets (length: {len(token)})")
                return token
    except Exception as e:
        st.error(f"⚠️ Could not load from st.secrets: {e}")

    st.error("❌ No GitHub token found in environment or secrets")
    return None

token = _get_github_token()

if token:
    st.success(f"✅ Got token! Length: {len(token)}")

    # Step 4: Test API call with exact same code
    st.header("Step 4: Test GitHub API Call")

    GITHUB_OWNER = "WanderingWithPride"
    GITHUB_REPO = "40thBdayAppRebuild"
    GITHUB_DATA_PATH = "data/trip_data.json"

    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{GITHUB_DATA_PATH}"

    st.text(f"URL: {url}")
    st.text(f"Token preview: {token[:25]}...{token[-15:]}")

    if st.button("🚀 Make API Call"):
        with st.spinner("Calling GitHub API..."):
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }

            try:
                response = requests.get(url, headers=headers, timeout=10)

                st.markdown("### Response:")
                st.text(f"Status Code: {response.status_code}")

                if response.status_code == 200:
                    st.success("✅ SUCCESS! API call worked!")
                    data = response.json()
                    st.json({
                        "name": data['name'],
                        "size": data['size'],
                        "sha": data['sha'][:10]
                    })
                elif response.status_code == 401:
                    st.error("❌ 401 UNAUTHORIZED")
                    st.code(response.text)
                    st.markdown("### Response Headers:")
                    st.json(dict(response.headers))
                else:
                    st.warning(f"⚠️ Status {response.status_code}")
                    st.code(response.text)

            except Exception as e:
                st.error(f"❌ Exception: {e}")
                import traceback
                st.code(traceback.format_exc())
else:
    st.error("❌ Cannot proceed - no token available")

# Step 5: Test actual function
st.header("Step 5: Test Actual github_storage.py Function")

if st.button("🎯 Test load_data_from_github()"):
    with st.spinner("Loading from GitHub..."):
        try:
            # Capture stdout
            from io import StringIO
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()

            from github_storage import load_data_from_github
            data = load_data_from_github()

            # Restore stdout
            sys.stdout = old_stdout
            output = mystdout.getvalue()

            if output:
                st.text_area("Console Output:", output, height=200)

            if data and "meal_proposals" in data:
                st.success("✅ Successfully loaded data!")
                st.json({"keys": list(data.keys())})
            else:
                st.error("❌ Failed or got empty data")

        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"❌ Exception: {e}")
            import traceback
            st.code(traceback.format_exc())
