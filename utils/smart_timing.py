"""
Smart Timing System for Trip Planning
======================================
Calculates intelligent timing for all event types including:
- Travel times between locations
- Preparation and buffer times
- Optimal timing windows (spa glow, golden hour)
- Complete arrival/departure timelines
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, List, Tuple
import streamlit as st

# Import Google Routes API for travel time calculations
try:
    from utils.google_routes import get_directions, format_duration
    GOOGLE_ROUTES_AVAILABLE = True
except ImportError:
    GOOGLE_ROUTES_AVAILABLE = False


# =============================================================================
# TIMING CONSTANTS (all in minutes)
# =============================================================================

# Flight-related timings
FLIGHT_BAGGAGE_CLAIM = 30
FLIGHT_AIRPORT_TO_HOTEL = 45  # Default if no Google API
FLIGHT_HOTEL_CHECKIN = 15
FLIGHT_FRESHEN_UP = 30
FLIGHT_CHECKOUT = 15
FLIGHT_HOTEL_TO_AIRPORT = 45  # Default if no Google API
FLIGHT_TSA_PRECHECK = 30
FLIGHT_TSA_REGULAR = 60
FLIGHT_SECURITY_BUFFER = 30
FLIGHT_RECOMMENDED_EARLY = 120  # Arrive 2 hours before departure

# Spa treatment timings
SPA_EARLY_ARRIVAL = 30  # Enjoy amenities before treatment
SPA_POST_TREATMENT_REST = 15
SPA_FACIAL_GLOW_START = 120  # 2 hours after facial - glow begins
SPA_FACIAL_GLOW_PEAK = 180  # 3 hours after facial - peak glow
SPA_FACIAL_GLOW_END = 300  # 5 hours after facial - glow window ends

# Meal timings
MEAL_ARRIVAL_BUFFER = 10  # Arrive before reservation
MEAL_CASUAL_DURATION = 60  # 1 hour for casual meals
MEAL_STANDARD_DURATION = 90  # 1.5 hours for standard dining
MEAL_UPSCALE_DURATION = 120  # 2 hours for upscale dining
MEAL_FINE_DINING_DURATION = 150  # 2.5 hours for fine dining
MEAL_POST_BUFFER = 10  # Time to settle check, leave

# Activity timings
ACTIVITY_EARLY_ARRIVAL = 15  # Arrive early for activities
ACTIVITY_POST_CLEANUP = 15  # Transition time after activity

# Photography timings
PHOTO_SETUP_TIME = 10
PHOTO_PRE_BUFFER = 15  # Time to get to location, compose self

# General travel and prep
GENERAL_PREP_TIME = 30  # Default preparation time
GENERAL_TRAVEL_BUFFER = 10  # Extra buffer for finding parking, etc.


# =============================================================================
# LOCATION DATA
# =============================================================================

HOTEL_LOCATION = {
    "name": "The Ritz-Carlton, Amelia Island",
    "address": "4750 Amelia Island Parkway, Fernandina Beach, FL 32034",
    "lat": 30.6074,
    "lon": -81.4493
}

AIRPORT_LOCATION = {
    "name": "Jacksonville International Airport (JAX)",
    "address": "2400 Yankee Clipper Dr, Jacksonville, FL 32218",
    "lat": 30.4941,
    "lon": -81.6879
}


# =============================================================================
# TRAVEL TIME CALCULATIONS
# =============================================================================

def get_travel_time(origin: Dict, destination: Dict, mode: str = "driving") -> Tuple[int, str]:
    """
    Get travel time between two locations using Google Routes API

    Args:
        origin: Dict with 'lat', 'lon', or 'address'
        destination: Dict with 'lat', 'lon', or 'address'
        mode: Travel mode (driving, walking, etc.)

    Returns:
        Tuple of (travel_minutes, formatted_display_string)
    """
    # Default fallback times
    default_times = {
        'airport_to_hotel': 45,
        'hotel_to_airport': 45,
        'local': 15  # Default for local destinations
    }

    if not GOOGLE_ROUTES_AVAILABLE:
        return default_times['local'], f"~{default_times['local']} min"

    # Format location strings
    origin_str = _format_location(origin)
    dest_str = _format_location(destination)

    if not origin_str or not dest_str:
        return default_times['local'], f"~{default_times['local']} min"

    # Get directions from Google
    try:
        directions = get_directions(origin_str, dest_str, mode=mode)

        if directions and directions.get('status') == 'OK':
            routes = directions.get('routes', [])
            if routes:
                leg = routes[0]['legs'][0]
                # Use traffic-adjusted duration if available
                duration_seconds = leg.get('duration_in_traffic', leg.get('duration', {})).get('value', 0)
                duration_minutes = (duration_seconds + 59) // 60  # Round up

                # Format display string
                if duration_minutes < 60:
                    display = f"~{duration_minutes} min"
                else:
                    hours = duration_minutes // 60
                    mins = duration_minutes % 60
                    display = f"~{hours}h {mins}m" if mins else f"~{hours}h"

                return duration_minutes, display
    except Exception as e:
        print(f"Travel time calculation error: {e}")

    # Fallback to default
    return default_times['local'], f"~{default_times['local']} min"


def _format_location(location: Dict) -> Optional[str]:
    """Format location dict into string for Google API"""
    if not location:
        return None

    # Prefer coordinates for accuracy
    if 'lat' in location and 'lon' in location:
        return f"{location['lat']},{location['lon']}"

    # Fall back to address
    if 'address' in location:
        return location['address']

    if 'name' in location:
        return location['name']

    return None


# =============================================================================
# ARRIVAL FLIGHT TIMELINE
# =============================================================================

def calculate_arrival_flight_timeline(arrival_time: str,
                                      destination: Dict = None) -> Optional[Dict]:
    """
    Calculate complete arrival timeline from flight landing to ready for dinner

    Args:
        arrival_time: Flight arrival time (e.g., "6:01 PM")
        destination: Destination location (defaults to hotel)

    Returns:
        Dict with complete timeline information
    """
    if not arrival_time or arrival_time == 'TBD':
        return None

    try:
        arrival_dt = datetime.strptime(arrival_time, '%I:%M %p')
    except:
        return None

    destination = destination or HOTEL_LOCATION

    # Get travel time from airport to destination
    travel_minutes, travel_display = get_travel_time(AIRPORT_LOCATION, destination)

    # Calculate timeline stages
    after_baggage = arrival_dt + timedelta(minutes=FLIGHT_BAGGAGE_CLAIM)
    at_destination = after_baggage + timedelta(minutes=travel_minutes)
    checked_in = at_destination + timedelta(minutes=FLIGHT_HOTEL_CHECKIN)
    ready_time = checked_in + timedelta(minutes=FLIGHT_FRESHEN_UP)

    total_minutes = FLIGHT_BAGGAGE_CLAIM + travel_minutes + FLIGHT_HOTEL_CHECKIN + FLIGHT_FRESHEN_UP

    return {
        'type': 'arrival_flight',
        'flight_lands': arrival_time,
        'stages': [
            {
                'icon': '🛬',
                'label': 'Flight lands',
                'time': arrival_time,
                'duration': None
            },
            {
                'icon': '🛄',
                'label': 'Baggage claim',
                'time': after_baggage.strftime('%I:%M %p'),
                'duration': f'~{FLIGHT_BAGGAGE_CLAIM} min'
            },
            {
                'icon': '🚗',
                'label': 'Drive to hotel',
                'time': at_destination.strftime('%I:%M %p'),
                'duration': travel_display
            },
            {
                'icon': '🏨',
                'label': 'Check-in',
                'time': checked_in.strftime('%I:%M %p'),
                'duration': f'~{FLIGHT_HOTEL_CHECKIN} min'
            },
            {
                'icon': '🚿',
                'label': 'Freshen up & change',
                'time': ready_time.strftime('%I:%M %p'),
                'duration': f'~{FLIGHT_FRESHEN_UP} min'
            }
        ],
        'at_hotel_by': at_destination.strftime('%I:%M %p'),
        'ready_for_dinner_by': ready_time.strftime('%I:%M %p'),
        'total_time': f'~{total_minutes} min',
        'total_minutes': total_minutes
    }


# =============================================================================
# DEPARTURE FLIGHT TIMELINE
# =============================================================================

def calculate_departure_flight_timeline(departure_time: str,
                                        has_tsa_precheck: bool = True,
                                        origin: Dict = None) -> Optional[Dict]:
    """
    Calculate when to leave hotel for departure flight

    Args:
        departure_time: Flight departure time (e.g., "11:05 AM")
        has_tsa_precheck: Whether traveler has TSA PreCheck
        origin: Origin location (defaults to hotel)

    Returns:
        Dict with departure timeline information
    """
    if not departure_time or departure_time == 'TBD':
        return None

    try:
        departure_dt = datetime.strptime(departure_time, '%I:%M %p')
    except:
        return None

    origin = origin or HOTEL_LOCATION

    # Get travel time from origin to airport
    travel_minutes, travel_display = get_travel_time(origin, AIRPORT_LOCATION)

    # Calculate TSA security time
    tsa_minutes = FLIGHT_TSA_PRECHECK if has_tsa_precheck else FLIGHT_TSA_REGULAR
    tsa_label = "TSA PreCheck" if has_tsa_precheck else "TSA Security"

    # Work backwards from departure time
    # Recommended: Arrive 2 hours before departure
    arrive_airport = departure_dt - timedelta(minutes=FLIGHT_RECOMMENDED_EARLY)

    # Account for travel time
    leave_hotel = arrive_airport - timedelta(minutes=travel_minutes)

    # Account for checkout
    start_checkout = leave_hotel - timedelta(minutes=FLIGHT_CHECKOUT)

    # Calculate time breakdown
    total_prep_minutes = FLIGHT_CHECKOUT + travel_minutes

    return {
        'type': 'departure_flight',
        'flight_departs': departure_time,
        'stages': [
            {
                'icon': '🧳',
                'label': 'Start checkout & load car',
                'time': start_checkout.strftime('%I:%M %p'),
                'duration': f'~{FLIGHT_CHECKOUT} min'
            },
            {
                'icon': '🚗',
                'label': 'Drive to airport',
                'time': arrive_airport.strftime('%I:%M %p'),
                'duration': travel_display
            },
            {
                'icon': '🛂',
                'label': tsa_label,
                'time': (arrive_airport + timedelta(minutes=tsa_minutes)).strftime('%I:%M %p'),
                'duration': f'~{tsa_minutes} min'
            },
            {
                'icon': '⏱️',
                'label': 'Buffer time at gate',
                'time': (departure_dt - timedelta(minutes=FLIGHT_SECURITY_BUFFER)).strftime('%I:%M %p'),
                'duration': f'~{FLIGHT_SECURITY_BUFFER} min'
            },
            {
                'icon': '✈️',
                'label': 'Flight departs',
                'time': departure_time,
                'duration': None
            }
        ],
        'start_checkout_by': start_checkout.strftime('%I:%M %p'),
        'leave_hotel_by': leave_hotel.strftime('%I:%M %p'),
        'arrive_airport_by': arrive_airport.strftime('%I:%M %p'),
        'total_prep_time': f'~{total_prep_minutes} min',
        'total_prep_minutes': total_prep_minutes
    }


# =============================================================================
# SPA TREATMENT TIMING
# =============================================================================

def calculate_spa_timeline(treatment_time: str,
                           treatment_duration_minutes: int,
                           is_facial: bool = False) -> Optional[Dict]:
    """
    Calculate spa treatment timeline with glow windows for facials

    Args:
        treatment_time: Treatment start time (e.g., "12:00 PM")
        treatment_duration_minutes: Duration of treatment
        is_facial: Whether this is a facial treatment (affects glow calculation)

    Returns:
        Dict with spa timeline information
    """
    if not treatment_time or treatment_time == 'TBD':
        return None

    try:
        treatment_dt = datetime.strptime(treatment_time, '%I:%M %p')
    except:
        return None

    # Calculate key times
    arrive_by = treatment_dt - timedelta(minutes=SPA_EARLY_ARRIVAL)
    treatment_ends = treatment_dt + timedelta(minutes=treatment_duration_minutes)
    ready_to_leave = treatment_ends + timedelta(minutes=SPA_POST_TREATMENT_REST)

    timeline = {
        'type': 'spa_treatment',
        'treatment_starts': treatment_time,
        'is_facial': is_facial,
        'stages': [
            {
                'icon': '🧖',
                'label': 'Arrive & enjoy spa amenities',
                'time': arrive_by.strftime('%I:%M %p'),
                'duration': f'~{SPA_EARLY_ARRIVAL} min',
                'tip': 'Enjoy saltwater pool, steam rooms, relaxation lounges'
            },
            {
                'icon': '💆',
                'label': 'Treatment begins',
                'time': treatment_time,
                'duration': f'{treatment_duration_minutes} min'
            },
            {
                'icon': '☕',
                'label': 'Rest & hydrate',
                'time': treatment_ends.strftime('%I:%M %p'),
                'duration': f'~{SPA_POST_TREATMENT_REST} min',
                'tip': 'Relax in lounge, drink water/tea'
            }
        ],
        'arrive_by': arrive_by.strftime('%I:%M %p'),
        'treatment_ends': treatment_ends.strftime('%I:%M %p'),
        'ready_to_leave': ready_to_leave.strftime('%I:%M %p')
    }

    # Add glow window for facials
    if is_facial:
        glow_start = treatment_ends + timedelta(minutes=SPA_FACIAL_GLOW_START)
        glow_peak = treatment_ends + timedelta(minutes=SPA_FACIAL_GLOW_PEAK)
        glow_end = treatment_ends + timedelta(minutes=SPA_FACIAL_GLOW_END)

        timeline['glow_window'] = {
            'start_time': glow_start.strftime('%I:%M %p'),
            'peak_time': glow_peak.strftime('%I:%M %p'),
            'end_time': glow_end.strftime('%I:%M %p'),
            'start_minutes': SPA_FACIAL_GLOW_START,
            'peak_minutes': SPA_FACIAL_GLOW_PEAK,
            'end_minutes': SPA_FACIAL_GLOW_END,
            'tip': '✨ PEAK GLOW for photos! Your skin will look absolutely radiant.'
        }

        timeline['stages'].append({
            'icon': '✨',
            'label': 'PEAK SKIN GLOW begins',
            'time': glow_start.strftime('%I:%M %p'),
            'duration': f'{(SPA_FACIAL_GLOW_END - SPA_FACIAL_GLOW_START) // 60}h window',
            'tip': '✨ Perfect time for photography! Skin looks incredible.'
        })

    return timeline


# =============================================================================
# MEAL TIMING
# =============================================================================

def calculate_meal_timeline(reservation_time: str,
                            meal_type: str,
                            restaurant_location: Dict = None,
                            previous_location: Dict = None) -> Optional[Dict]:
    """
    Calculate meal timeline with travel and arrival buffer

    Args:
        reservation_time: Reservation time (e.g., "7:00 PM")
        meal_type: Type of meal (casual, standard, upscale, fine_dining)
        restaurant_location: Restaurant location dict
        previous_location: Previous event location (defaults to hotel)

    Returns:
        Dict with meal timeline information
    """
    if not reservation_time or reservation_time == 'TBD':
        return None

    try:
        reservation_dt = datetime.strptime(reservation_time, '%I:%M %p')
    except:
        return None

    # Determine meal duration
    duration_map = {
        'casual': MEAL_CASUAL_DURATION,
        'standard': MEAL_STANDARD_DURATION,
        'upscale': MEAL_UPSCALE_DURATION,
        'fine_dining': MEAL_FINE_DINING_DURATION,
        'breakfast': MEAL_CASUAL_DURATION,
        'lunch': MEAL_STANDARD_DURATION,
        'dinner': MEAL_UPSCALE_DURATION
    }
    meal_duration = duration_map.get(meal_type.lower(), MEAL_STANDARD_DURATION)

    # Calculate travel time
    previous_location = previous_location or HOTEL_LOCATION
    if restaurant_location:
        travel_minutes, travel_display = get_travel_time(previous_location, restaurant_location)
    else:
        travel_minutes, travel_display = 15, "~15 min"

    # Calculate timeline
    leave_time = reservation_dt - timedelta(minutes=travel_minutes + MEAL_ARRIVAL_BUFFER)
    meal_ends = reservation_dt + timedelta(minutes=meal_duration)
    ready_to_leave = meal_ends + timedelta(minutes=MEAL_POST_BUFFER)

    return {
        'type': 'meal',
        'reservation_time': reservation_time,
        'meal_type': meal_type,
        'stages': [
            {
                'icon': '🚗',
                'label': 'Leave for restaurant',
                'time': leave_time.strftime('%I:%M %p'),
                'duration': travel_display
            },
            {
                'icon': '🍽️',
                'label': 'Arrive at restaurant',
                'time': (reservation_dt - timedelta(minutes=MEAL_ARRIVAL_BUFFER)).strftime('%I:%M %p'),
                'duration': f'{MEAL_ARRIVAL_BUFFER} min buffer',
                'tip': 'Arrive a few minutes early to check in'
            },
            {
                'icon': '🍷',
                'label': 'Dinner begins',
                'time': reservation_time,
                'duration': f'~{meal_duration} min'
            },
            {
                'icon': '💳',
                'label': 'Ready to leave',
                'time': ready_to_leave.strftime('%I:%M %p'),
                'duration': f'{MEAL_POST_BUFFER} min'
            }
        ],
        'leave_by': leave_time.strftime('%I:%M %p'),
        'arrive_by': (reservation_dt - timedelta(minutes=MEAL_ARRIVAL_BUFFER)).strftime('%I:%M %p'),
        'meal_ends': meal_ends.strftime('%I:%M %p'),
        'ready_to_leave': ready_to_leave.strftime('%I:%M %p'),
        'total_duration': meal_duration + MEAL_POST_BUFFER
    }


# =============================================================================
# ACTIVITY TIMING
# =============================================================================

def calculate_activity_timeline(activity_time: str,
                                activity_duration_minutes: int,
                                activity_location: Dict = None,
                                previous_location: Dict = None) -> Optional[Dict]:
    """
    Calculate activity timeline with travel and buffer times

    Args:
        activity_time: Activity start time (e.g., "9:00 AM")
        activity_duration_minutes: Duration of activity
        activity_location: Activity location dict
        previous_location: Previous event location (defaults to hotel)

    Returns:
        Dict with activity timeline information
    """
    if not activity_time or activity_time == 'TBD':
        return None

    try:
        activity_dt = datetime.strptime(activity_time, '%I:%M %p')
    except:
        return None

    # Calculate travel time
    previous_location = previous_location or HOTEL_LOCATION
    if activity_location:
        travel_minutes, travel_display = get_travel_time(previous_location, activity_location)
    else:
        travel_minutes, travel_display = 15, "~15 min"

    # Calculate timeline
    leave_time = activity_dt - timedelta(minutes=travel_minutes + ACTIVITY_EARLY_ARRIVAL)
    activity_ends = activity_dt + timedelta(minutes=activity_duration_minutes)
    ready_to_leave = activity_ends + timedelta(minutes=ACTIVITY_POST_CLEANUP)

    return {
        'type': 'activity',
        'activity_starts': activity_time,
        'stages': [
            {
                'icon': '🚗',
                'label': 'Leave for activity',
                'time': leave_time.strftime('%I:%M %p'),
                'duration': travel_display
            },
            {
                'icon': '📍',
                'label': 'Arrive early',
                'time': (activity_dt - timedelta(minutes=ACTIVITY_EARLY_ARRIVAL)).strftime('%I:%M %p'),
                'duration': f'{ACTIVITY_EARLY_ARRIVAL} min',
                'tip': 'Check in, get oriented'
            },
            {
                'icon': '🎯',
                'label': 'Activity begins',
                'time': activity_time,
                'duration': f'~{activity_duration_minutes} min'
            },
            {
                'icon': '✅',
                'label': 'Ready to leave',
                'time': ready_to_leave.strftime('%I:%M %p'),
                'duration': f'{ACTIVITY_POST_CLEANUP} min'
            }
        ],
        'leave_by': leave_time.strftime('%I:%M %p'),
        'arrive_by': (activity_dt - timedelta(minutes=ACTIVITY_EARLY_ARRIVAL)).strftime('%I:%M %p'),
        'activity_ends': activity_ends.strftime('%I:%M %p'),
        'ready_to_leave': ready_to_leave.strftime('%I:%M %p'),
        'total_duration': activity_duration_minutes + ACTIVITY_POST_CLEANUP
    }


# =============================================================================
# PHOTOGRAPHY TIMING
# =============================================================================

def calculate_photography_timeline(session_time: str,
                                   session_duration_minutes: int,
                                   location: Dict = None,
                                   previous_location: Dict = None,
                                   after_facial: bool = False,
                                   facial_end_time: str = None) -> Optional[Dict]:
    """
    Calculate photography session timeline with optimal timing notes

    Args:
        session_time: Session start time (e.g., "5:00 PM")
        session_duration_minutes: Duration of photo session
        location: Photo location dict
        previous_location: Previous event location (defaults to hotel)
        after_facial: Whether this follows a facial treatment
        facial_end_time: End time of facial (for glow calculation)

    Returns:
        Dict with photography timeline information
    """
    if not session_time or session_time == 'TBD':
        return None

    try:
        session_dt = datetime.strptime(session_time, '%I:%M %p')
    except:
        return None

    # Calculate travel time
    previous_location = previous_location or HOTEL_LOCATION
    if location:
        travel_minutes, travel_display = get_travel_time(previous_location, location)
    else:
        travel_minutes, travel_display = 5, "~5 min"  # Assume on-property

    # Calculate timeline
    leave_time = session_dt - timedelta(minutes=travel_minutes + PHOTO_PRE_BUFFER)
    session_ends = session_dt + timedelta(minutes=session_duration_minutes)

    timeline = {
        'type': 'photography',
        'session_starts': session_time,
        'stages': [
            {
                'icon': '🚶',
                'label': 'Head to photo location',
                'time': leave_time.strftime('%I:%M %p'),
                'duration': travel_display
            },
            {
                'icon': '💄',
                'label': 'Final touch-ups',
                'time': (session_dt - timedelta(minutes=PHOTO_PRE_BUFFER)).strftime('%I:%M %p'),
                'duration': f'{PHOTO_PRE_BUFFER} min',
                'tip': 'Check hair, makeup, outfit'
            },
            {
                'icon': '📸',
                'label': 'Photo session begins',
                'time': session_time,
                'duration': f'{session_duration_minutes} min'
            },
            {
                'icon': '✅',
                'label': 'Session complete',
                'time': session_ends.strftime('%I:%M %p'),
                'duration': None
            }
        ],
        'leave_by': leave_time.strftime('%I:%M %p'),
        'session_ends': session_ends.strftime('%I:%M %p')
    }

    # Add glow timing if after facial
    if after_facial and facial_end_time:
        try:
            facial_dt = datetime.strptime(facial_end_time, '%I:%M %p')
            time_after_facial = (session_dt - facial_dt).total_seconds() / 60

            timeline['after_facial'] = {
                'facial_ended': facial_end_time,
                'time_after_facial_minutes': int(time_after_facial),
                'glow_status': _get_glow_status(time_after_facial)
            }
        except:
            pass

    return timeline


def _get_glow_status(minutes_after_facial: float) -> Dict:
    """Determine glow status based on time after facial"""
    if minutes_after_facial < SPA_FACIAL_GLOW_START:
        return {
            'level': 'building',
            'emoji': '⏳',
            'message': 'Skin glow is building...'
        }
    elif minutes_after_facial < SPA_FACIAL_GLOW_PEAK:
        return {
            'level': 'good',
            'emoji': '✨',
            'message': 'Great glow! Skin looks fantastic.'
        }
    elif minutes_after_facial <= SPA_FACIAL_GLOW_END:
        return {
            'level': 'peak',
            'emoji': '🌟',
            'message': 'PEAK GLOW! Absolutely radiant - perfect timing!'
        }
    else:
        return {
            'level': 'fading',
            'emoji': '💫',
            'message': 'Still glowing! Skin looks great.'
        }


# =============================================================================
# UNIVERSAL SMART TIMING
# =============================================================================

def calculate_smart_timing(event: Dict, previous_event: Dict = None) -> Optional[Dict]:
    """
    Universal function to calculate smart timing for any event type

    Args:
        event: Event dict with 'type', 'time', 'duration', 'location', etc.
        previous_event: Previous event dict (for travel time calculation)

    Returns:
        Dict with complete smart timing information
    """
    event_type = event.get('type', '').lower()
    event_time = event.get('time', '')

    # Get locations
    event_location = event.get('location')
    previous_location = previous_event.get('location') if previous_event else None

    # Route to appropriate calculator
    if 'arrival' in event_type or event.get('is_arrival'):
        return calculate_arrival_flight_timeline(event_time)

    elif 'departure' in event_type or event.get('is_departure'):
        has_precheck = event.get('has_tsa_precheck', True)
        return calculate_departure_flight_timeline(event_time, has_precheck)

    elif event_type == 'spa' or 'spa' in event.get('category', '').lower():
        duration = _parse_duration(event.get('duration', '60 min'))
        is_facial = 'facial' in event.get('activity', '').lower()
        return calculate_spa_timeline(event_time, duration, is_facial)

    elif 'meal' in event_type or event.get('is_meal') or event.get('category', '').lower() == 'dining':
        meal_type = _determine_meal_type(event)
        # Only calculate if we have location data or fallback to defaults
        return calculate_meal_timeline(event_time, meal_type, event_location, previous_location)

    elif 'photo' in event_type or 'photography' in event.get('activity', '').lower():
        duration = _parse_duration(event.get('duration', '60 min'))
        return calculate_photography_timeline(event_time, duration, event_location, previous_location)

    elif event_type == 'activity':
        duration = _parse_duration(event.get('duration', '60 min'))
        return calculate_activity_timeline(event_time, duration, event_location, previous_location)

    return None


def _parse_duration(duration_str: str) -> int:
    """Parse duration string into minutes"""
    if isinstance(duration_str, int):
        return duration_str

    if not isinstance(duration_str, str):
        return 60  # Default

    duration_str = duration_str.lower()

    # Handle various formats
    import re

    # "2 hours" or "2h"
    hours = re.search(r'(\d+\.?\d*)\s*h', duration_str)
    # "30 minutes" or "30 min"
    minutes = re.search(r'(\d+)\s*m', duration_str)

    total_minutes = 0
    if hours:
        total_minutes += int(float(hours.group(1)) * 60)
    if minutes:
        total_minutes += int(minutes.group(1))

    return total_minutes if total_minutes > 0 else 60


def _determine_meal_type(event: Dict) -> str:
    """Determine meal type from event data"""
    activity = event.get('activity', '').lower()
    notes = event.get('notes', '').lower()
    cost = event.get('cost_range', event.get('cost', '')).lower() if isinstance(event.get('cost_range', event.get('cost', '')), str) else ''

    # Check for fine dining indicators
    if any(word in activity or word in notes for word in ['fine dining', 'tasting menu', 'michelin']):
        return 'fine_dining'

    # Check for upscale indicators
    if any(word in activity or word in notes for word in ['upscale', 'birthday dinner', 'celebration', 'dress code']):
        return 'upscale'

    # Check for casual indicators
    if any(word in activity or word in notes for word in ['casual', 'quick', 'beach', 'food truck', 'counter']):
        return 'casual'

    # Check cost range
    if '$' in cost:
        if '40' in cost or '50' in cost or '60' in cost or '70' in cost:
            return 'upscale'
        elif '15' in cost or '20' in cost or '25' in cost:
            return 'standard'
        elif '10' in cost or '12' in cost:
            return 'casual'

    # Default to standard
    return 'standard'
