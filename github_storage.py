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
GITHUB_TOKEN = None
try:
    # Try Streamlit secrets first (for Streamlit Cloud)
    if hasattr(st, 'secrets'):
        GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", None)
        if GITHUB_TOKEN:
            print(f"✅ GitHub token loaded from st.secrets (length: {len(GITHUB_TOKEN)})")
except Exception as e:
    print(f"⚠️ Could not load from st.secrets: {e}")

# Fallback to environment variable (for local development)
if not GITHUB_TOKEN:
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    if GITHUB_TOKEN:
        print(f"✅ GitHub token loaded from environment variable")
    else:
        print(f"❌ No GitHub token found in secrets or environment")

# Local fallback
LOCAL_DATA_FILE = "trip_data_local.json"
LOCAL_BACKUP_DIR = "data/backups"
MAX_BACKUPS = 20


def _create_backup(data_file):
    """Create backup of current data file before writing

    Args:
        data_file (str): Path to data file to backup

    Returns:
        str: Path to created backup file, or None if no backup needed
    """
    import shutil
    from pathlib import Path

    if not os.path.exists(data_file):
        return None

    # Ensure backup directory exists
    Path(LOCAL_BACKUP_DIR).mkdir(parents=True, exist_ok=True)

    # Create timestamped backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f'{LOCAL_BACKUP_DIR}/trip_data_local_{timestamp}.json'
    shutil.copy2(data_file, backup_path)
    print(f"💾 Local backup created: {backup_path}")

    # Cleanup old backups
    _cleanup_old_backups()

    return backup_path


def _cleanup_old_backups():
    """Keep only last N backups, delete older ones"""
    from pathlib import Path

    backups = sorted(Path(LOCAL_BACKUP_DIR).glob('trip_data_local_*.json'))

    if len(backups) > MAX_BACKUPS:
        for old_backup in backups[:-MAX_BACKUPS]:
            old_backup.unlink()
            print(f"🗑️ Deleted old local backup: {old_backup.name}")


def _atomic_write_local(data, data_file):
    """Write data to local file atomically (prevents corruption)

    Args:
        data (dict): Data to write
        data_file (str): Path to target file

    Returns:
        bool: True if successful
    """
    import tempfile
    import shutil

    try:
        # Create backup before writing
        _create_backup(data_file)

        # Write to temporary file first
        temp_fd, temp_path = tempfile.mkstemp(
            suffix='.json',
            prefix='trip_data_tmp_',
            dir='.',
            text=True
        )

        with os.fdopen(temp_fd, 'w') as temp_file:
            json.dump(data, temp_file, indent=2)
            temp_file.flush()
            os.fsync(temp_file.fileno())  # Force write to disk

        # Atomic rename
        shutil.move(temp_path, data_file)
        return True

    except Exception as e:
        print(f"Error in atomic write: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False


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
        except json.JSONDecodeError as e:
            print(f"❌ ERROR: Local data file is corrupted!")
            print(f"JSON Error: {e}")

            # Try to recover from most recent backup
            from pathlib import Path
            backups = sorted(Path(LOCAL_BACKUP_DIR).glob('trip_data_local_*.json'))
            if backups:
                most_recent = backups[-1]
                print(f"🔄 Attempting recovery from backup: {most_recent}")
                try:
                    with open(most_recent, 'r') as f:
                        recovered_data = json.load(f)
                    print(f"✅ Successfully recovered from backup!")
                    # Save recovered data
                    _atomic_write_local(recovered_data, LOCAL_DATA_FILE)
                    return recovered_data
                except Exception as recovery_error:
                    print(f"❌ Recovery failed: {recovery_error}")

            print("⚠️ No backups available. Starting with empty data.")
            return init_empty_data()
        except Exception as e:
            print(f"Error loading local data: {e}")
            return init_empty_data()
        return init_empty_data()

    try:
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{GITHUB_DATA_PATH}"

        # Debug: Show token info (safely)
        token_prefix = GITHUB_TOKEN[:7] if GITHUB_TOKEN and len(GITHUB_TOKEN) > 7 else "INVALID"
        print(f"🔍 Attempting to load from GitHub with token prefix: {token_prefix}...")
        print(f"🔍 URL: {url}")

        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.get(url, headers=headers, timeout=10)

        print(f"🔍 Response status: {response.status_code}")

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
        elif response.status_code == 401:
            error_msg = "GitHub authentication failed (401)"
            try:
                error_details = response.json()
                print(f"❌ {error_msg}")
                print(f"❌ API Response: {error_details}")
                print(f"❌ Token type: {token_prefix}")

                # Check if it's a fine-grained token issue
                if 'message' in error_details:
                    msg = error_details['message']
                    if 'fine-grained' in msg.lower() or 'permissions' in msg.lower():
                        error_msg += " - Token may need additional permissions or be of wrong type."

                st.warning(f"{error_msg} Please check your GITHUB_TOKEN permissions. Using default data.")
            except:
                print(f"❌ {error_msg}")
                st.warning(f"{error_msg} Using default data.")
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
        # Local development - save to local file with atomic write + backups
        return _atomic_write_local(data, LOCAL_DATA_FILE)

    try:
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{GITHUB_DATA_PATH}"

        # Debug: Show token info (safely)
        token_prefix = GITHUB_TOKEN[:7] if GITHUB_TOKEN and len(GITHUB_TOKEN) > 7 else "INVALID"
        print(f"🔍 Attempting to save to GitHub with token prefix: {token_prefix}...")

        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Get current file SHA (needed for update)
        response = requests.get(url, headers=headers, timeout=10)

        print(f"🔍 GET response status (for SHA): {response.status_code}")

        if response.status_code == 401:
            error_msg = "GitHub authentication failed (401). Cannot save data."
            try:
                error_details = response.json()
                print(f"❌ {error_msg} Details: {error_details}")
                st.error(f"{error_msg} Please check your GITHUB_TOKEN permissions.")
            except:
                print(f"❌ {error_msg}")
                st.error(error_msg)
            return False

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

        print(f"🔍 PUT response status (for commit): {response.status_code}")

        if response.status_code in [200, 201]:
            print(f"✅ Successfully saved to GitHub")
            return True
        elif response.status_code == 401:
            error_msg = "GitHub authentication failed (401). Cannot save data."
            try:
                error_details = response.json()
                print(f"❌ {error_msg} Details: {error_details}")
                st.error(f"{error_msg} Please check your GITHUB_TOKEN permissions.")
            except:
                print(f"❌ {error_msg}")
                st.error(error_msg)
            return False
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
    # Defensive check for trip_data existence
    trip_data = st.session_state.get('trip_data')
    if trip_data is None:
        print("❌ ERROR: trip_data not loaded in session state")
        st.error("Trip data not loaded. Please refresh the page.")
        return False
    return save_data_to_github(trip_data, commit_message)
