"""
Weather Alerts System

Automatically monitors weather conditions for scheduled outdoor activities
and generates actionable alerts for:
- Rain during outdoor activities
- High UV index for extended outdoor time
- Strong winds for water activities
- Temperature extremes
"""

from datetime import datetime, timedelta


def check_weather_alerts(activities_data, weather_data):
    """Check weather conditions against activities and generate alerts

    Args:
        activities_data (list): List of activity dictionaries
        weather_data (dict): Weather data with forecast

    Returns:
        list: List of alert dictionaries
    """

    alerts = []

    # Create weather lookup by date
    weather_by_date = {}
    for day in weather_data.get('forecast', []):
        weather_by_date[day['date']] = day

    # Check each activity
    for activity in activities_data:
        date = activity.get('date')
        if not date:
            continue

        # Get weather for this day
        day_weather = weather_by_date.get(date)
        if not day_weather:
            continue

        # Identify outdoor activities
        is_outdoor = _is_outdoor_activity(activity)
        if not is_outdoor:
            continue

        # Check for rain
        if day_weather.get('rain_chance', 0) > 30:
            alerts.append({
                'severity': 'warning' if day_weather['rain_chance'] > 60 else 'info',
                'type': 'rain',
                'activity': activity['activity'],
                'date': date,
                'time': activity.get('time', 'TBD'),
                'rain_chance': day_weather['rain_chance'],
                'message': f"⛈️ {day_weather['rain_chance']}% chance of rain during {activity['activity']}",
                'suggestion': _get_rain_suggestion(activity, day_weather['rain_chance'])
            })

        # Check for high UV
        uv_index = day_weather.get('uv_index', 5)
        if uv_index >= 8 and _is_extended_outdoor(activity):
            alerts.append({
                'severity': 'warning',
                'type': 'uv',
                'activity': activity['activity'],
                'date': date,
                'time': activity.get('time', 'TBD'),
                'uv_index': uv_index,
                'message': f"☀️ Very high UV index ({uv_index}) during {activity['activity']}",
                'suggestion': "Bring high SPF sunscreen, sunglasses, and consider a hat. Reapply sunscreen every 2 hours."
            })

        # Check for strong winds (water activities)
        if _is_water_activity(activity) and day_weather.get('wind_speed', 0) > 15:
            alerts.append({
                'severity': 'warning',
                'type': 'wind',
                'activity': activity['activity'],
                'date': date,
                'time': activity.get('time', 'TBD'),
                'wind_speed': day_weather['wind_speed'],
                'message': f"💨 Strong winds ({day_weather['wind_speed']} mph) during {activity['activity']}",
                'suggestion': "Check with activity provider about conditions. May need to reschedule if winds are too strong."
            })

        # Check for temperature extremes
        high_temp = day_weather.get('high', 75)
        if high_temp > 85 and _is_extended_outdoor(activity):
            alerts.append({
                'severity': 'info',
                'type': 'heat',
                'activity': activity['activity'],
                'date': date,
                'time': activity.get('time', 'TBD'),
                'temperature': high_temp,
                'message': f"🌡️ Hot day ({high_temp}°F) during {activity['activity']}",
                'suggestion': "Stay hydrated! Bring water bottles and take breaks in shade."
            })

    # Sort by severity and date
    severity_order = {'warning': 0, 'info': 1}
    alerts.sort(key=lambda x: (severity_order.get(x['severity'], 2), x['date']))

    return alerts


def _is_outdoor_activity(activity):
    """Determine if activity is outdoors

    Args:
        activity (dict): Activity dictionary

    Returns:
        bool: True if outdoor activity
    """

    outdoor_keywords = [
        'boat', 'tour', 'beach', 'pool', 'outdoor', 'kayak',
        'fishing', 'park', 'golf', 'hiking', 'walk', 'photography'
    ]

    activity_name = activity.get('activity', '').lower()
    category = activity.get('category', '').lower()
    notes = activity.get('notes', '').lower()

    # Check for outdoor keywords
    for keyword in outdoor_keywords:
        if keyword in activity_name or keyword in category or keyword in notes:
            return True

    # Check location type
    location = activity.get('location', {})
    if isinstance(location, dict):
        location_type = location.get('type', '').lower()
        if location_type in ['outdoor', 'beach', 'park', 'water']:
            return True

    return False


def _is_water_activity(activity):
    """Determine if activity is on/near water

    Args:
        activity (dict): Activity dictionary

    Returns:
        bool: True if water activity
    """

    water_keywords = ['boat', 'kayak', 'fishing', 'cruise', 'sail', 'swim', 'beach']

    activity_name = activity.get('activity', '').lower()

    for keyword in water_keywords:
        if keyword in activity_name:
            return True

    return False


def _is_extended_outdoor(activity):
    """Determine if activity involves extended time outdoors (>2 hours)

    Args:
        activity (dict): Activity dictionary

    Returns:
        bool: True if extended outdoor activity
    """

    duration_str = activity.get('duration', '1 hour').lower()

    # Parse duration
    try:
        if 'hour' in duration_str:
            hours = float(duration_str.split('hour')[0].strip().split()[-1])
            return hours >= 2
        elif 'h' in duration_str:
            hours = float(duration_str.split('h')[0].strip())
            return hours >= 2
    except:
        pass

    # Assume extended for certain activities
    extended_activities = ['boat tour', 'beach', 'all day', 'full day', 'photography']
    activity_name = activity.get('activity', '').lower()

    for extended in extended_activities:
        if extended in activity_name:
            return True

    return False


def _get_rain_suggestion(activity, rain_chance):
    """Get appropriate suggestion based on activity type and rain chance

    Args:
        activity (dict): Activity dictionary
        rain_chance (int): Percentage chance of rain

    Returns:
        str: Suggestion text
    """

    if rain_chance > 70:
        return "High chance of rain. Consider rescheduling or having a backup indoor plan."
    elif rain_chance > 50:
        return "Moderate rain chance. Bring umbrellas/rain jackets and monitor forecast closely."
    else:
        return "Light rain possible. Pack a light rain jacket just in case."


def generate_weather_briefing(activities_data, weather_data, target_date=None):
    """Generate daily weather briefing for activities

    Args:
        activities_data (list): List of activity dictionaries
        weather_data (dict): Weather data with forecast
        target_date (str, optional): Date to generate briefing for (YYYY-MM-DD)

    Returns:
        dict: Briefing with summary, alerts, and recommendations
    """

    if not target_date:
        target_date = datetime.now().strftime('%Y-%m-%d')

    # Get activities for target date
    day_activities = [a for a in activities_data if a.get('date') == target_date]

    # Get weather for target date
    day_weather = None
    for day in weather_data.get('forecast', []):
        if day['date'] == target_date:
            day_weather = day
            break

    if not day_weather:
        return {
            'date': target_date,
            'summary': "No weather data available",
            'alerts': [],
            'recommendations': []
        }

    # Count outdoor activities
    outdoor_activities = [a for a in day_activities if _is_outdoor_activity(a)]

    # Generate summary
    summary = f"{day_weather['condition']}, {day_weather['high']}°F / {day_weather['low']}°F"
    if day_weather.get('rain_chance', 0) > 30:
        summary += f" ({day_weather['rain_chance']}% chance of rain)"

    # Get alerts for this day
    all_alerts = check_weather_alerts(activities_data, weather_data)
    day_alerts = [a for a in all_alerts if a['date'] == target_date]

    # Generate recommendations
    recommendations = []

    if len(outdoor_activities) > 0:
        recommendations.append(f"📍 {len(outdoor_activities)} outdoor activity(ies) scheduled")

        if day_weather.get('uv_index', 0) >= 6:
            recommendations.append("☀️ Apply sunscreen before heading out")

        if day_weather.get('rain_chance', 0) > 30:
            recommendations.append("☂️ Pack umbrella or rain jacket")

        if day_weather['high'] > 85:
            recommendations.append("💧 Bring water bottles - hot day ahead")

    return {
        'date': target_date,
        'summary': summary,
        'outdoor_count': len(outdoor_activities),
        'alerts': day_alerts,
        'recommendations': recommendations
    }
