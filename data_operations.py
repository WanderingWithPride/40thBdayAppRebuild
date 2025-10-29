"""
Data Operations - Wrapper functions that replace database operations
Uses GitHub JSON storage instead of SQLite
"""

import json
from datetime import datetime
from github_storage import get_trip_data, save_trip_data


# ============================================================================
# MEAL PROPOSALS
# ============================================================================

def save_meal_proposal(meal_id, restaurant_options, submitted_by="Michael", is_solo=False):
    """Save meal proposal (or auto-confirm if solo meal)"""
    try:
        data = get_trip_data()

        # For solo meals, auto-confirm the choice
        if is_solo:
            data['meal_proposals'][meal_id] = {
                'meal_id': meal_id,
                'restaurant_options': restaurant_options,
                'status': 'confirmed',  # Auto-confirm solo meals
                'john_vote': None,  # Not applicable for solo meals
                'final_choice': 0,  # Pick the only restaurant selected
                'meal_time': None,
                'submitted_by': submitted_by,
                'is_solo': True,  # Mark as solo meal
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
        else:
            # Regular meal proposal (requires John's vote)
            data['meal_proposals'][meal_id] = {
                'meal_id': meal_id,
                'restaurant_options': restaurant_options,
                'status': 'proposed',
                'john_vote': None,
                'final_choice': None,
                'meal_time': None,
                'submitted_by': submitted_by,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }

        return save_trip_data(f"Add meal proposal: {meal_id}")
    except Exception as e:
        print(f"Error saving meal proposal: {e}")
        return False


def get_meal_proposal(meal_id):
    """Get meal proposal"""
    try:
        data = get_trip_data()
        return data['meal_proposals'].get(meal_id)
    except Exception as e:
        print(f"Error getting meal proposal: {e}")
        return None


def save_john_meal_vote(meal_id, restaurant_choice):
    """Save John's vote on meal"""
    try:
        data = get_trip_data()
        if meal_id in data['meal_proposals']:
            data['meal_proposals'][meal_id]['john_vote'] = restaurant_choice
            data['meal_proposals'][meal_id]['status'] = 'voted'
            data['meal_proposals'][meal_id]['updated_at'] = datetime.now().isoformat()
            return save_trip_data(f"John voted on meal: {meal_id}")
        return False
    except Exception as e:
        print(f"Error saving vote: {e}")
        return False


def finalize_meal_choice(meal_id, final_choice_index, meal_time=None):
    """Finalize meal choice"""
    try:
        data = get_trip_data()
        if meal_id in data['meal_proposals']:
            data['meal_proposals'][meal_id]['final_choice'] = final_choice_index
            data['meal_proposals'][meal_id]['status'] = 'confirmed'
            if meal_time:
                data['meal_proposals'][meal_id]['meal_time'] = meal_time
            data['meal_proposals'][meal_id]['updated_at'] = datetime.now().isoformat()
            return save_trip_data(f"Confirmed meal: {meal_id}")
        return False
    except Exception as e:
        print(f"Error finalizing meal: {e}")
        return False


# ============================================================================
# ACTIVITY PROPOSALS
# ============================================================================

def save_activity_proposal(activity_slot_id, activity_options, activity_time=None, date=None, submitted_by="Michael"):
    """Save activity proposal"""
    try:
        data = get_trip_data()
        data['activity_proposals'][activity_slot_id] = {
            'activity_slot_id': activity_slot_id,
            'activity_options': activity_options,
            'status': 'proposed',
            'john_vote': None,
            'final_choice': None,
            'activity_time': activity_time,
            'date': date,
            'submitted_by': submitted_by,  # Track who submitted this proposal
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        return save_trip_data(f"Add activity proposal: {activity_slot_id}")
    except Exception as e:
        print(f"Error saving activity proposal: {e}")
        return False


def get_activity_proposal(activity_slot_id):
    """Get activity proposal"""
    try:
        data = get_trip_data()
        return data['activity_proposals'].get(activity_slot_id)
    except Exception as e:
        print(f"Error getting activity proposal: {e}")
        return None


def save_john_activity_vote(activity_slot_id, activity_choice):
    """Save John's vote on activity"""
    try:
        data = get_trip_data()
        if activity_slot_id in data['activity_proposals']:
            data['activity_proposals'][activity_slot_id]['john_vote'] = activity_choice
            data['activity_proposals'][activity_slot_id]['status'] = 'voted'
            data['activity_proposals'][activity_slot_id]['updated_at'] = datetime.now().isoformat()
            return save_trip_data(f"John voted on activity: {activity_slot_id}")
        return False
    except Exception as e:
        print(f"Error saving activity vote: {e}")
        return False


def finalize_activity_choice(activity_slot_id, final_choice_index, activity_time=None):
    """Finalize activity choice"""
    try:
        data = get_trip_data()
        if activity_slot_id in data['activity_proposals']:
            data['activity_proposals'][activity_slot_id]['final_choice'] = final_choice_index
            data['activity_proposals'][activity_slot_id]['status'] = 'confirmed'
            if activity_time:
                data['activity_proposals'][activity_slot_id]['activity_time'] = activity_time
            data['activity_proposals'][activity_slot_id]['updated_at'] = datetime.now().isoformat()
            return save_trip_data(f"Confirmed activity: {activity_slot_id}")
        return False
    except Exception as e:
        print(f"Error finalizing activity: {e}")
        return False


# ============================================================================
# JOHN'S PREFERENCES
# ============================================================================

def load_john_preferences():
    """Load John's preferences"""
    try:
        data = get_trip_data()
        return data.get('john_preferences', {})
    except Exception as e:
        print(f"Error loading preferences: {e}")
        return {}


def save_john_preference(key, value):
    """Save John's preference"""
    try:
        data = get_trip_data()
        data['john_preferences'][key] = value
        return save_trip_data(f"Update preference: {key}")
    except Exception as e:
        print(f"Error saving preference: {e}")
        return False


# ============================================================================
# ALCOHOL REQUESTS
# ============================================================================

def add_alcohol_request(item_name, quantity='', notes=''):
    """Add alcohol request"""
    try:
        data = get_trip_data()
        request = {
            'id': len(data['alcohol_requests']) + 1,
            'item_name': item_name,
            'quantity': quantity,
            'notes': notes,
            'purchased': False,
            'cost': 0.0,
            'created_at': datetime.now().isoformat()
        }
        data['alcohol_requests'].append(request)
        return save_trip_data(f"Add alcohol request: {item_name}")
    except Exception as e:
        print(f"Error adding alcohol request: {e}")
        return False


def get_alcohol_requests():
    """Get all alcohol requests"""
    try:
        data = get_trip_data()
        return data.get('alcohol_requests', [])
    except Exception as e:
        print(f"Error getting alcohol requests: {e}")
        return []


def delete_alcohol_request(request_id):
    """Delete alcohol request"""
    try:
        data = get_trip_data()
        data['alcohol_requests'] = [r for r in data['alcohol_requests'] if r['id'] != request_id]
        return save_trip_data(f"Delete alcohol request: {request_id}")
    except Exception as e:
        print(f"Error deleting alcohol request: {e}")
        return False


def mark_alcohol_purchased(request_id, cost=0.0):
    """Mark alcohol as purchased"""
    try:
        data = get_trip_data()
        for request in data['alcohol_requests']:
            if request['id'] == request_id:
                request['purchased'] = True
                request['cost'] = cost
                return save_trip_data(f"Mark purchased: {request['item_name']}")
        return False
    except Exception as e:
        print(f"Error marking purchased: {e}")
        return False


# ============================================================================
# CUSTOM ACTIVITIES
# ============================================================================

def save_custom_activity(activity_dict):
    """Save custom activity"""
    try:
        data = get_trip_data()
        activity_id = activity_dict.get('id', f"custom_{datetime.now().timestamp()}")
        activity_dict['id'] = activity_id
        # Remove existing if updating
        data['custom_activities'] = [a for a in data['custom_activities'] if a['id'] != activity_id]
        data['custom_activities'].append(activity_dict)
        save_trip_data(f"Add custom activity: {activity_dict.get('activity', 'Unknown')}")
        return activity_id
    except Exception as e:
        print(f"Error saving custom activity: {e}")
        return None


def load_custom_activities():
    """Load custom activities"""
    try:
        data = get_trip_data()
        return data.get('custom_activities', [])
    except Exception as e:
        print(f"Error loading custom activities: {e}")
        return []


def delete_custom_activity(activity_id):
    """Delete custom activity"""
    try:
        data = get_trip_data()
        data['custom_activities'] = [a for a in data['custom_activities'] if a['id'] != activity_id]
        return save_trip_data(f"Delete custom activity: {activity_id}")
    except Exception as e:
        print(f"Error deleting custom activity: {e}")
        return False


# ============================================================================
# COMPLETED ACTIVITIES
# ============================================================================

def mark_activity_completed(activity_id):
    """Mark activity as completed"""
    try:
        data = get_trip_data()
        if activity_id not in data['completed_activities']:
            data['completed_activities'].append(activity_id)
            return save_trip_data(f"Complete activity: {activity_id}")
        return True
    except Exception as e:
        print(f"Error marking completed: {e}")
        return False


def load_completed_activities():
    """Load completed activities"""
    try:
        data = get_trip_data()
        return data.get('completed_activities', [])
    except Exception as e:
        print(f"Error loading completed activities: {e}")
        return []


def mark_activity_done(activity_name):
    """Mark activity as done by name (for optional activities)"""
    try:
        data = get_trip_data()
        if 'done_activities' not in data:
            data['done_activities'] = []
        if activity_name not in data['done_activities']:
            data['done_activities'].append(activity_name)
            return save_trip_data(f"Mark done: {activity_name}")
        return True
    except Exception as e:
        print(f"Error marking activity done: {e}")
        return False


def unmark_activity_done(activity_name):
    """Remove activity from done list"""
    try:
        data = get_trip_data()
        if 'done_activities' not in data:
            data['done_activities'] = []
        if activity_name in data['done_activities']:
            data['done_activities'].remove(activity_name)
            return save_trip_data(f"Remove done: {activity_name}")
        return True
    except Exception as e:
        print(f"Error unmarking activity done: {e}")
        return False


def load_done_activities():
    """Load done activities"""
    try:
        data = get_trip_data()
        return data.get('done_activities', [])
    except Exception as e:
        print(f"Error loading done activities: {e}")
        return []


# ============================================================================
# INTERESTED ACTIVITIES
# ============================================================================

def mark_activity_interested(activity_name):
    """Mark activity as interested"""
    try:
        data = get_trip_data()
        if 'interested_activities' not in data:
            data['interested_activities'] = []
        if activity_name not in data['interested_activities']:
            data['interested_activities'].append(activity_name)
            return save_trip_data(f"Mark interested: {activity_name}")
        return True
    except Exception as e:
        print(f"Error marking activity interested: {e}")
        return False


def unmark_activity_interested(activity_name):
    """Remove activity from interested list"""
    try:
        data = get_trip_data()
        if 'interested_activities' not in data:
            data['interested_activities'] = []
        if activity_name in data['interested_activities']:
            data['interested_activities'].remove(activity_name)
            return save_trip_data(f"Remove interested: {activity_name}")
        return True
    except Exception as e:
        print(f"Error unmarking activity interested: {e}")
        return False


def load_interested_activities():
    """Load interested activities"""
    try:
        data = get_trip_data()
        return data.get('interested_activities', [])
    except Exception as e:
        print(f"Error loading interested activities: {e}")
        return []


# ============================================================================
# PACKING PROGRESS
# ============================================================================

def update_packing_item(item_id, packed):
    """Update packing item status"""
    try:
        data = get_trip_data()
        data['packing_progress'][item_id] = {
            'packed': packed,
            'updated_at': datetime.now().isoformat()
        }
        return save_trip_data("Update packing list")
    except Exception as e:
        print(f"Error updating packing: {e}")
        return False


def get_packing_progress():
    """Get packing progress"""
    try:
        data = get_trip_data()
        return data.get('packing_progress', {})
    except Exception as e:
        print(f"Error getting packing progress: {e}")
        return {}


# ============================================================================
# NOTES
# ============================================================================

def add_note(date, content, note_type='note'):
    """Add note"""
    try:
        data = get_trip_data()
        note = {
            'id': len(data['notes']) + 1,
            'date': date,
            'content': content,
            'type': note_type,
            'created_at': datetime.now().isoformat()
        }
        data['notes'].append(note)
        return save_trip_data("Add note")
    except Exception as e:
        print(f"Error adding note: {e}")
        return False


def get_notes():
    """Get all notes"""
    try:
        data = get_trip_data()
        return data.get('notes', [])
    except Exception as e:
        print(f"Error getting notes: {e}")
        return []


def delete_note(note_id):
    """Delete a note"""
    try:
        data = get_trip_data()
        data['notes'] = [n for n in data['notes'] if n['id'] != note_id]
        return save_trip_data(f"Delete note: {note_id}")
    except Exception as e:
        print(f"Error deleting note: {e}")
        return False


# ============================================================================
# PHOTOS (Stored in session state, not GitHub)
# ============================================================================

def save_photo(filename, photo_bytes, caption, date):
    """Save a photo (stored in session state only for now)"""
    # Photos are large binary data - store in session state instead of GitHub
    # In the future, could upload to image hosting service
    return None


def load_photos(date=None):
    """Load photos from session state"""
    # Photos are stored in session state, not GitHub storage
    return []


def delete_photo(photo_id):
    """Delete a photo"""
    # Photos are stored in session state, not GitHub storage
    pass


# ============================================================================
# NOTIFICATIONS (Stored in session state, not GitHub)
# ============================================================================

def add_notification(title, message, notif_type='info'):
    """Add a notification to session state"""
    # Notifications are transient - no need to persist to GitHub
    pass


def load_notifications(include_dismissed=False):
    """Load notifications from session state"""
    # Notifications are stored in session state, not GitHub storage
    return []


def dismiss_notification(notif_id):
    """Dismiss a notification"""
    # Notifications are stored in session state, not GitHub storage
    pass


# ============================================================================
# TSA UPDATES (Stored in GitHub)
# ============================================================================

def save_manual_tsa_update(airport_code, wait_minutes, reported_by="User", notes=""):
    """Save a manual TSA wait time update"""
    try:
        data = get_trip_data()
        update = {
            'airport_code': airport_code,
            'wait_minutes': wait_minutes,
            'reported_by': reported_by,
            'notes': notes,
            'created_at': datetime.now().isoformat()
        }
        if 'tsa_updates' not in data:
            data['tsa_updates'] = []
        data['tsa_updates'].append(update)
        return save_trip_data(f"TSA update: {airport_code}")
    except Exception as e:
        print(f"Error saving TSA update: {e}")
        return False


def get_latest_manual_tsa_update(airport_code, max_age_hours=2):
    """Get the most recent manual TSA wait time update for an airport"""
    try:
        from datetime import timedelta
        data = get_trip_data()
        updates = data.get('tsa_updates', [])

        # Filter by airport and time
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        recent_updates = [
            u for u in updates
            if u['airport_code'] == airport_code and
            datetime.fromisoformat(u['created_at']) > cutoff
        ]

        # Return most recent
        if recent_updates:
            return sorted(recent_updates, key=lambda x: x['created_at'], reverse=True)[0]
        return None
    except Exception as e:
        print(f"Error getting TSA update: {e}")
        return None
