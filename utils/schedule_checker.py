"""
Schedule Conflict Detection and Visualization

Automatically detects:
- Hard conflicts (overlapping activities)
- Tight transitions (not enough time between locations)
- Good buffers (optimal spacing)
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd


def check_schedule_conflicts(activities):
    """Comprehensive conflict detection

    Args:
        activities (list): List of activity dictionaries

    Returns:
        tuple: (conflicts, warnings, suggestions)
    """

    conflicts = []
    warnings = []
    suggestions = []

    # Filter out activities without dates/times
    valid_activities = [
        a for a in activities
        if a.get('date') and a.get('time')
    ]

    # Sort chronologically
    sorted_acts = sorted(
        valid_activities,
        key=lambda x: datetime.strptime(f"{x['date']} {x.get('time', '12:00 PM')}", '%Y-%m-%d %I:%M %p')
    )

    for i in range(len(sorted_acts) - 1):
        current = sorted_acts[i]
        next_act = sorted_acts[i + 1]

        try:
            current_start = datetime.strptime(f"{current['date']} {current.get('time', '12:00 PM')}", '%Y-%m-%d %I:%M %p')

            # Parse duration
            duration = current.get('duration', '2 hours')
            duration_hours = _parse_duration_to_hours(duration)
            current_end = current_start + timedelta(hours=duration_hours)

            next_start = datetime.strptime(f"{next_act['date']} {next_act.get('time', '12:00 PM')}", '%Y-%m-%d %I:%M %p')

            # HARD CONFLICT (overlap)
            if current_end > next_start:
                conflicts.append({
                    'severity': 'critical',
                    'activity1': current['activity'],
                    'activity2': next_act['activity'],
                    'current_end': current_end.strftime('%I:%M %p'),
                    'next_start': next_start.strftime('%I:%M %p'),
                    'overlap_minutes': int((current_end - next_start).total_seconds() / 60),
                    'message': f"⛔ OVERLAP: {current['activity']} runs until {current_end.strftime('%I:%M %p')} but {next_act['activity']} starts at {next_start.strftime('%I:%M %p')}"
                })

            # TIGHT TRANSITION (< 30 min, different locations)
            elif (next_start - current_end) < timedelta(minutes=30):
                loc1 = _get_location_name(current)
                loc2 = _get_location_name(next_act)

                gap_minutes = int((next_start - current_end).total_seconds() / 60)

                if loc1 != loc2 and loc1 and loc2:
                    warnings.append({
                        'severity': 'warning',
                        'activity1': current['activity'],
                        'activity2': next_act['activity'],
                        'gap_minutes': gap_minutes,
                        'location1': loc1,
                        'location2': loc2,
                        'message': f"⚠️ TIGHT: Only {gap_minutes} min to get from {loc1} to {loc2}"
                    })

            # GOOD BUFFER (30min-2hrs)
            elif timedelta(minutes=30) <= (next_start - current_end) <= timedelta(hours=2):
                gap_minutes = int((next_start - current_end).total_seconds() / 60)
                suggestions.append({
                    'severity': 'info',
                    'gap_minutes': gap_minutes,
                    'message': f"✅ Good buffer: {gap_minutes} min between {current['activity']} and {next_act['activity']}"
                })

        except Exception as e:
            print(f"Error checking conflict between {current.get('activity')} and {next_act.get('activity')}: {e}")

    return conflicts, warnings, suggestions


def _parse_duration_to_hours(duration_str):
    """Parse duration string to hours

    Examples:
        "2 hours" -> 2.0
        "1.5 hours" -> 1.5
        "2h 10m" -> 2.17
        "90 minutes" -> 1.5

    Args:
        duration_str (str): Duration string

    Returns:
        float: Duration in hours
    """
    if not duration_str:
        return 2.0

    duration_str = str(duration_str).lower()

    # Handle "2 hours", "1.5 hours"
    if 'hour' in duration_str:
        try:
            numbers = duration_str.replace('hours', '').replace('hour', '').strip()
            return float(numbers.split()[0])
        except:
            pass

    # Handle "90 minutes", "30 min"
    if 'min' in duration_str:
        try:
            numbers = duration_str.replace('minutes', '').replace('minute', '').replace('min', '').strip()
            return float(numbers.split()[0]) / 60
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

    # Default
    return 2.0


def _get_location_name(activity):
    """Extract location name from activity

    Args:
        activity (dict): Activity dictionary

    Returns:
        str: Location name or empty string
    """
    location = activity.get('location', {})

    if isinstance(location, dict):
        return location.get('name', '')
    elif isinstance(location, str):
        return location
    else:
        return ''


def visualize_schedule_timeline(activities):
    """Create visual timeline of schedule

    Args:
        activities (list): List of activity dictionaries
    """

    st.subheader("📊 Schedule Timeline")

    # Prepare data for visualization
    schedule_data = []

    for activity in activities:
        if not activity.get('date') or not activity.get('time'):
            continue

        try:
            start = datetime.strptime(f"{activity['date']} {activity.get('time', '12:00 PM')}", '%Y-%m-%d %I:%M %p')

            duration_hours = _parse_duration_to_hours(activity.get('duration', '2 hours'))
            end = start + timedelta(hours=duration_hours)

            schedule_data.append({
                'Activity': activity['activity'],
                'Start': start,
                'End': end,
                'Duration (hrs)': duration_hours,
                'Day': start.strftime('%A, %b %d')
            })
        except Exception as e:
            print(f"Error visualizing {activity.get('activity')}: {e}")

    if not schedule_data:
        st.warning("No activities with valid dates/times to visualize")
        return

    df = pd.DataFrame(schedule_data)

    # Group by day
    days = df['Day'].unique()

    for day in sorted(days):
        day_activities = df[df['Day'] == day].sort_values('Start')

        st.markdown(f"### {day}")

        # Create simple timeline visualization
        for idx, row in day_activities.iterrows():
            start_time = row['Start'].strftime('%I:%M %p')
            end_time = row['End'].strftime('%I:%M %p')
            duration = row['Duration (hrs)']

            # Visual bar (scaled by duration)
            bar_width = int(min(duration * 50, 400))  # Max 400px

            st.markdown(f"""
            <div style="margin: 10px 0;">
                <div style="font-weight: bold;">{start_time} - {end_time}</div>
                <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                            height: 30px;
                            width: {bar_width}px;
                            border-radius: 5px;
                            display: flex;
                            align-items: center;
                            padding: 0 10px;
                            color: white;
                            font-size: 14px;">
                    {row['Activity'][:40]}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()


def show_schedule_conflicts_panel(activities):
    """Display conflicts panel with all checks and visualizations

    Args:
        activities (list): List of activity dictionaries
    """

    st.markdown("### 🔍 Schedule Conflict Detection")

    # Run conflict check
    conflicts, warnings, suggestions = check_schedule_conflicts(activities)

    # Display alerts
    if conflicts:
        st.error(f"⛔ {len(conflicts)} CRITICAL CONFLICTS DETECTED")
        for conflict in conflicts:
            with st.expander(conflict['message'], expanded=True):
                st.write(f"**Problem:** {conflict['activity1']} and {conflict['activity2']} overlap by {abs(conflict['overlap_minutes'])} minutes")
                st.write(f"**Fix Options:**")
                st.write(f"- Reschedule {conflict['activity2']} to after {conflict['current_end']}")
                st.write(f"- Shorten {conflict['activity1']} duration")
                st.write(f"- Cancel one of the activities")

    if warnings:
        st.warning(f"⚠️ {len(warnings)} POTENTIAL ISSUES")
        for warning in warnings:
            with st.expander(warning['message']):
                st.write(f"**Gap:** {warning['gap_minutes']} minutes")
                st.write(f"**From:** {warning['location1']}")
                st.write(f"**To:** {warning['location2']}")

                st.info("💡 Suggestions:")
                st.write(f"- Check Google Maps for actual drive time")
                st.write(f"- Add 15-30 min buffer if needed")
                st.write(f"- Consider Uber/Lyft vs driving")

    if suggestions and not conflicts and not warnings:
        with st.expander(f"✅ {len(suggestions)} Good Transitions"):
            for suggestion in suggestions[:5]:  # Show first 5
                st.success(suggestion['message'])

    if not conflicts and not warnings:
        st.success("✅ No schedule conflicts detected! Your timeline looks good.")

    # Visualize
    st.divider()
    visualize_schedule_timeline(activities)
