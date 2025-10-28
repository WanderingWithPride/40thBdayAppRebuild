"""
Export utilities for trip schedule

Provides calendar (iCal) and PDF exports for offline access to schedule.
Critical for trip when app may not be accessible.
"""

from icalendar import Calendar, Event, Alarm
from datetime import datetime, timedelta
import pytz


def export_to_ical(activities_data, meal_proposals, filename='trip_schedule.ics'):
    """Export confirmed schedule to iCalendar format

    Args:
        activities_data (list): List of activity dictionaries
        meal_proposals (dict): Dict of meal proposals
        filename (str): Output filename

    Returns:
        str: Path to created iCal file
    """

    cal = Calendar()
    cal.add('prodid', '-//40th Birthday Trip//EN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', '🎂 Florida Birthday Trip')
    cal.add('x-wr-timezone', 'America/New_York')

    # Get timezone
    eastern = pytz.timezone('America/New_York')

    # Add hardcoded activities
    for activity in activities_data:
        # Only add confirmed activities or transport/arrivals
        status = activity.get('status', '').lower()
        if status not in ['confirmed', 'urgent']:
            continue

        try:
            event = Event()

            # Parse date and time
            date_str = activity['date']
            time_str = activity.get('time', '12:00 PM')

            # Combine date and time
            dt_str = f"{date_str} {time_str}"
            dt = datetime.strptime(dt_str, '%Y-%m-%d %I:%M %p')
            dt = eastern.localize(dt)

            # Parse duration (handle different formats)
            duration_str = activity.get('duration', '2 hours')
            duration_hours = _parse_duration(duration_str)
            end_dt = dt + timedelta(hours=duration_hours)

            # Add event details
            event.add('summary', activity['activity'])
            event.add('dtstart', dt)
            event.add('dtend', end_dt)

            # Add location if available
            if 'location' in activity:
                loc = activity['location']
                location_str = f"{loc.get('name', '')}"
                if loc.get('address'):
                    location_str += f", {loc['address']}"
                event.add('location', location_str)

            # Add description with notes, phone, etc.
            description_parts = []
            if 'notes' in activity:
                description_parts.append(activity['notes'])
            if 'phone' in activity.get('location', {}):
                description_parts.append(f"\nPhone: {activity['location']['phone']}")
            if 'confirmation_code' in activity:
                description_parts.append(f"\nConfirmation: {activity['confirmation_code']}")

            if description_parts:
                event.add('description', '\n'.join(description_parts))

            # Add alarm (reminder 2 hours before for urgent, 1 day for transport)
            alarm = Alarm()
            alarm.add('action', 'DISPLAY')
            alarm.add('description', f"Reminder: {activity['activity']}")

            if activity.get('type') == 'transport':
                alarm.add('trigger', timedelta(days=-1))
            elif status == 'urgent':
                alarm.add('trigger', timedelta(hours=-2))
            else:
                alarm.add('trigger', timedelta(hours=-1))

            event.add_component(alarm)

            cal.add_component(event)

        except Exception as e:
            print(f"Warning: Could not add activity to calendar: {activity.get('activity', 'Unknown')}: {e}")

    # Add confirmed meal proposals
    day_map = {
        'fri': '2025-11-07',
        'sat': '2025-11-08',
        'sun': '2025-11-09',
        'mon': '2025-11-10',
        'tue': '2025-11-11'
    }

    meal_time_map = {
        'breakfast': '8:00 AM',
        'lunch': '12:30 PM',
        'dinner': '7:00 PM'
    }

    for meal_id, proposal in meal_proposals.items():
        if proposal.get('status') != 'confirmed':
            continue

        try:
            # Parse meal slot to get date/time
            parts = meal_id.split('_')
            if len(parts) != 2:
                continue

            day = parts[0]
            meal_type = parts[1]

            date_str = day_map.get(day)
            time_str = proposal.get('meal_time') or meal_time_map.get(meal_type)

            if not date_str or not time_str:
                continue

            dt_str = f"{date_str} {time_str}"
            dt = datetime.strptime(dt_str, '%Y-%m-%d %I:%M %p')
            dt = eastern.localize(dt)

            # Get final choice
            final_choice_idx = proposal.get('final_choice')
            restaurant_options = proposal.get('restaurant_options', [])

            if isinstance(final_choice_idx, int) and final_choice_idx < len(restaurant_options):
                restaurant = restaurant_options[final_choice_idx]
            elif isinstance(final_choice_idx, str):
                # final_choice is restaurant name
                restaurant = {'name': final_choice_idx}
            else:
                continue

            event = Event()
            event.add('summary', f"🍽️ {meal_type.title()}: {restaurant['name']}")
            event.add('dtstart', dt)
            event.add('dtend', dt + timedelta(hours=1.5))

            # Add location and details if available
            if 'phone' in restaurant:
                event.add('description', f"Phone: {restaurant['phone']}")

            # Add reminder 3 hours before meals
            alarm = Alarm()
            alarm.add('action', 'DISPLAY')
            alarm.add('description', f"Meal reminder: {restaurant['name']}")
            alarm.add('trigger', timedelta(hours=-3))
            event.add_component(alarm)

            cal.add_component(event)

        except Exception as e:
            print(f"Warning: Could not add meal to calendar: {meal_id}: {e}")

    # Write to file
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())

    print(f"✅ Calendar exported to {filename}")
    print(f"   Import this into Google Calendar, Apple Calendar, or Outlook!")
    return filename


def _parse_duration(duration_str):
    """Parse duration string to hours

    Args:
        duration_str (str): Duration like "2 hours", "1.5 hours", "2h 10m"

    Returns:
        float: Duration in hours
    """
    if not duration_str:
        return 2.0

    duration_str = duration_str.lower()

    # Handle "2 hours", "1.5 hours"
    if 'hour' in duration_str:
        try:
            return float(duration_str.split('hour')[0].strip().split()[0])
        except:
            pass

    # Handle "2h 10m"
    if 'h' in duration_str and 'm' in duration_str:
        try:
            parts = duration_str.replace('h', ' ').replace('m', '').split()
            hours = float(parts[0])
            minutes = float(parts[1]) if len(parts) > 1 else 0
            return hours + (minutes / 60)
        except:
            pass

    # Handle just "2h"
    if 'h' in duration_str:
        try:
            return float(duration_str.replace('h', '').strip())
        except:
            pass

    # Handle "90 minutes", "30 min", etc.
    if 'min' in duration_str:
        try:
            minutes = float(duration_str.split('min')[0].strip().split()[0])
            return minutes / 60.0  # Convert minutes to hours
        except:
            pass

    # Default
    return 2.0


def create_simple_text_schedule(activities_data, meal_proposals):
    """Create simple text version of schedule for printing or emailing

    Args:
        activities_data (list): List of activity dictionaries
        meal_proposals (dict): Dict of meal proposals

    Returns:
        str: Formatted text schedule
    """
    schedule_text = "🎂 40TH BIRTHDAY TRIP SCHEDULE\n"
    schedule_text += "Florida • November 7-12, 2025\n"
    schedule_text += "=" * 60 + "\n\n"

    # Emergency contacts
    schedule_text += "📞 EMERGENCY CONTACTS:\n"
    schedule_text += "-" * 60 + "\n"
    schedule_text += "Hotel: The Ritz-Carlton, Amelia Island\n"
    schedule_text += "  Phone: 904-277-1100\n"
    schedule_text += "Spa: 904-277-1087\n"
    schedule_text += "Boat Tour: 904-753-7631\n"
    schedule_text += "\n\n"

    # Group activities by date
    from collections import defaultdict
    by_date = defaultdict(list)

    for activity in activities_data:
        by_date[activity['date']].append(activity)

    # Add meals to by_date
    day_map = {
        'fri': '2025-11-07',
        'sat': '2025-11-08',
        'sun': '2025-11-09',
        'mon': '2025-11-10',
        'tue': '2025-11-11'
    }

    for meal_id, proposal in meal_proposals.items():
        if proposal.get('status') != 'confirmed':
            continue

        parts = meal_id.split('_')
        if len(parts) == 2:
            day = parts[0]
            meal_type = parts[1]
            date_str = day_map.get(day)

            if date_str:
                final_choice = proposal.get('final_choice')
                if isinstance(final_choice, str):
                    restaurant_name = final_choice
                elif isinstance(final_choice, int):
                    options = proposal.get('restaurant_options', [])
                    restaurant_name = options[final_choice]['name'] if final_choice < len(options) else "TBD"
                else:
                    restaurant_name = "TBD"

                meal_activity = {
                    'time': proposal.get('meal_time', '12:00 PM'),
                    'activity': f"🍽️ {meal_type.title()}: {restaurant_name}",
                    'type': 'meal'
                }
                by_date[date_str].append(meal_activity)

    # Sort by date
    sorted_dates = sorted(by_date.keys())

    days = {
        '2025-11-07': 'FRIDAY, NOV 7',
        '2025-11-08': 'SATURDAY, NOV 8',
        '2025-11-09': 'SUNDAY, NOV 9 🎂 BIRTHDAY!',
        '2025-11-10': 'MONDAY, NOV 10',
        '2025-11-11': 'TUESDAY, NOV 11',
        '2025-11-12': 'WEDNESDAY, NOV 12'
    }

    for date in sorted_dates:
        schedule_text += f"\n{days.get(date, date)}\n"
        schedule_text += "=" * 60 + "\n"

        # Sort activities by time
        day_activities = sorted(by_date[date], key=lambda x: x.get('time', '00:00 AM'))

        for activity in day_activities:
            time = activity.get('time', 'TBD')
            name = activity['activity']
            schedule_text += f"{time:15} {name}\n"

            # Add location if available
            if 'location' in activity:
                loc = activity['location']
                # Handle both dict and string location data
                if isinstance(loc, dict):
                    if loc.get('name'):
                        schedule_text += f"{'':15} 📍 {loc['name']}\n"
                    if loc.get('phone'):
                        schedule_text += f"{'':15} 📞 {loc['phone']}\n"
                elif isinstance(loc, str) and loc:
                    # Location is a simple string
                    schedule_text += f"{'':15} 📍 {loc}\n"

        schedule_text += "\n"

    return schedule_text
