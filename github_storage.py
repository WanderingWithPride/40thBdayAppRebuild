"""
GitHub File Storage for Trip Data
Stores all trip data in a JSON file on GitHub for persistence across Streamlit Cloud restarts
"""

import os
import json
import base64
import requests
import streamlit as st
from datetime import datetime

# GitHub configuration
GITHUB_OWNER = "WanderingWithPride"
GITHUB_REPO = "40thBdayAppRebuild"
GITHUB_DATA_PATH = "data/trip_data.json"

# Get GitHub token from Streamlit secrets (cloud) or environment variable (local)
try:
    GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", None)
except:
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Local fallback
LOCAL_DATA_FILE = "trip_data_local.json"


def init_empty_data():
    """Initialize empty data structure"""
    return {
        "meal_proposals": {},
        "activity_proposals": {},
        "john_preferences": {
            "avoid_seafood_focused": "false",
            "avoid_mexican": "false"
        },
        "alcohol_requests": [],
        "packing_progress": {},
        "notes": [],
        "custom_activities": [],
        "completed_activities": [],
        "notifications": [],
        "tsa_updates": [],
        "last_updated": datetime.now().isoformat()
    }


def load_data_from_github():
    """Load data from GitHub"""
    if not GITHUB_TOKEN:
        # Local development - use local file
        try:
            if os.path.exists(LOCAL_DATA_FILE):
                with open(LOCAL_DATA_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading local data: {e}")
        return init_empty_data()

    try:
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{GITHUB_DATA_PATH}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            content = response.json()
            file_content = base64.b64decode(content['content']).decode('utf-8')
            data = json.loads(file_content)
            # Ensure all required keys exist
            default_data = init_empty_data()
            for key in default_data:
                if key not in data:
                    data[key] = default_data[key]
            return data
        elif response.status_code == 404:
            # File doesn't exist - initialize
            return init_empty_data()
        else:
            st.warning(f"Could not load data from GitHub (status {response.status_code}). Using default data.")
            return init_empty_data()
    except Exception as e:
        st.warning(f"Error loading data from GitHub: {e}")
        return init_empty_data()


def save_data_to_github(data, commit_message="Update trip data"):
    """Save data to GitHub"""
    # Update timestamp
    data["last_updated"] = datetime.now().isoformat()

    if not GITHUB_TOKEN:
        # Local development - save to local file
        try:
            with open(LOCAL_DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving local data: {e}")
            return False

    try:
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{GITHUB_DATA_PATH}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Get current file SHA (needed for update)
        response = requests.get(url, headers=headers, timeout=10)
        sha = response.json()['sha'] if response.status_code == 200 else None

        # Encode content
        content_encoded = base64.b64encode(json.dumps(data, indent=2).encode('utf-8')).decode('utf-8')

        # Prepare commit
        payload = {
            "message": f"{commit_message} 🤖",
            "content": content_encoded,
            "branch": "main"
        }
        if sha:
            payload["sha"] = sha

        # Commit to GitHub
        response = requests.put(url, headers=headers, json=payload, timeout=15)

        if response.status_code in [200, 201]:
            return True
        else:
            st.error(f"Failed to save to GitHub: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        st.error(f"Error saving to GitHub: {e}")
        return False


def get_trip_data():
    """Get trip data from session state (loads from GitHub if not cached)"""
    if 'trip_data' not in st.session_state:
        st.session_state.trip_data = load_data_from_github()
    return st.session_state.trip_data


def save_trip_data(commit_message="Update trip data"):
    """Save current trip data to GitHub"""
    return save_data_to_github(st.session_state.trip_data, commit_message)
