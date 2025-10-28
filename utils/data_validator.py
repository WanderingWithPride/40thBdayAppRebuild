"""
Data Validation Module

Ensures data integrity for trip activities, meals, and proposals.
Validates schema, detects issues, and provides actionable fix suggestions.
"""

from datetime import datetime
import re


def validate_trip_data(activities_data, trip_data):
    """Validate complete trip data structure

    Args:
        activities_data (list): List of activity dictionaries
        trip_data (dict): Full trip data including proposals

    Returns:
        tuple: (is_valid, errors, warnings)
    """

    errors = []
    warnings = []

    # Validate activities
    activity_errors, activity_warnings = validate_activities(activities_data)
    errors.extend(activity_errors)
    warnings.extend(activity_warnings)

    # Validate meal proposals
    meal_errors, meal_warnings = validate_meal_proposals(trip_data.get('meal_proposals', {}))
    errors.extend(meal_errors)
    warnings.extend(meal_warnings)

    # Validate activity proposals
    activity_proposal_errors, activity_proposal_warnings = validate_activity_proposals(
        trip_data.get('activity_proposals', {})
    )
    errors.extend(activity_proposal_errors)
    warnings.extend(activity_proposal_warnings)

    is_valid = len(errors) == 0

    return is_valid, errors, warnings


def validate_activities(activities):
    """Validate activity data structure

    Args:
        activities (list): List of activity dictionaries

    Returns:
        tuple: (errors, warnings)
    """

    errors = []
    warnings = []

    required_fields = ['activity', 'date', 'time', 'duration', 'location', 'category', 'status']

    for idx, activity in enumerate(activities):
        activity_name = activity.get('activity', f'Activity #{idx+1}')

        # Check required fields
        missing_fields = [field for field in required_fields if field not in activity or not activity[field]]
        if missing_fields:
            errors.append({
                'type': 'missing_field',
                'activity': activity_name,
                'fields': missing_fields,
                'message': f"⛔ {activity_name}: Missing required fields: {', '.join(missing_fields)}",
                'fix': f"Add the following fields to this activity: {', '.join(missing_fields)}"
            })

        # Validate date format
        if 'date' in activity:
            try:
                datetime.strptime(activity['date'], '%Y-%m-%d')
            except (ValueError, TypeError):
                errors.append({
                    'type': 'invalid_date',
                    'activity': activity_name,
                    'value': activity['date'],
                    'message': f"⛔ {activity_name}: Invalid date format '{activity['date']}'",
                    'fix': "Use YYYY-MM-DD format (e.g., 2025-11-07)"
                })

        # Validate time format
        if 'time' in activity:
            try:
                datetime.strptime(activity['time'], '%I:%M %p')
            except (ValueError, TypeError):
                errors.append({
                    'type': 'invalid_time',
                    'activity': activity_name,
                    'value': activity['time'],
                    'message': f"⛔ {activity_name}: Invalid time format '{activity['time']}'",
                    'fix': "Use HH:MM AM/PM format (e.g., 02:30 PM)"
                })

        # Validate location structure
        if 'location' in activity:
            if isinstance(activity['location'], dict):
                if not activity['location'].get('name'):
                    warnings.append({
                        'type': 'incomplete_location',
                        'activity': activity_name,
                        'message': f"⚠️ {activity_name}: Location missing 'name' field",
                        'fix': "Add 'name' field to location dictionary"
                    })
            elif not isinstance(activity['location'], str):
                errors.append({
                    'type': 'invalid_location',
                    'activity': activity_name,
                    'message': f"⛔ {activity_name}: Location must be string or dict",
                    'fix': "Change location to string or dict with 'name' field"
                })

        # Validate cost
        if 'cost' in activity:
            cost = activity['cost']
            if not isinstance(cost, (int, float, str)) or (isinstance(cost, str) and cost.lower() not in ['free', 'tbd', 'n/a']):
                warnings.append({
                    'type': 'invalid_cost',
                    'activity': activity_name,
                    'value': cost,
                    'message': f"⚠️ {activity_name}: Cost '{cost}' should be number or 'Free'/'TBD'",
                    'fix': "Use number for cost or 'Free'/'TBD'"
                })

        # Validate status
        if 'status' in activity:
            valid_statuses = ['Confirmed', 'URGENT', 'Pending', 'Optional', 'Proposed']
            if activity['status'] not in valid_statuses:
                warnings.append({
                    'type': 'invalid_status',
                    'activity': activity_name,
                    'value': activity['status'],
                    'message': f"⚠️ {activity_name}: Status '{activity['status']}' not recognized",
                    'fix': f"Use one of: {', '.join(valid_statuses)}"
                })

        # Validate category
        if 'category' in activity:
            valid_categories = ['Transport', 'Meal', 'Spa', 'Activity', 'Accommodation', 'Event', 'Free Time']
            if activity['category'] not in valid_categories:
                warnings.append({
                    'type': 'invalid_category',
                    'activity': activity_name,
                    'value': activity['category'],
                    'message': f"⚠️ {activity_name}: Category '{activity['category']}' not standard",
                    'fix': f"Consider using: {', '.join(valid_categories)}"
                })

    return errors, warnings


def validate_meal_proposals(meal_proposals):
    """Validate meal proposal data

    Args:
        meal_proposals (dict): Dictionary of meal proposals

    Returns:
        tuple: (errors, warnings)
    """

    errors = []
    warnings = []

    required_fields = ['restaurant_options', 'meal_time', 'status']

    for meal_id, proposal in meal_proposals.items():
        # Check required fields
        missing_fields = [field for field in required_fields if field not in proposal]
        if missing_fields:
            errors.append({
                'type': 'missing_proposal_field',
                'meal_id': meal_id,
                'fields': missing_fields,
                'message': f"⛔ Meal {meal_id}: Missing fields: {', '.join(missing_fields)}",
                'fix': f"Add: {', '.join(missing_fields)}"
            })

        # Validate restaurant_options
        if 'restaurant_options' in proposal:
            if not isinstance(proposal['restaurant_options'], list):
                errors.append({
                    'type': 'invalid_restaurant_options',
                    'meal_id': meal_id,
                    'message': f"⛔ Meal {meal_id}: restaurant_options must be a list",
                    'fix': "Change restaurant_options to list of dicts"
                })
            elif len(proposal['restaurant_options']) == 0:
                warnings.append({
                    'type': 'empty_options',
                    'meal_id': meal_id,
                    'message': f"⚠️ Meal {meal_id}: No restaurant options provided",
                    'fix': "Add at least 2-3 restaurant options"
                })

        # Validate voting
        if 'john_vote' in proposal:
            john_vote = proposal['john_vote']
            num_options = len(proposal.get('restaurant_options', []))

            if isinstance(john_vote, int) and john_vote >= num_options:
                errors.append({
                    'type': 'invalid_vote',
                    'meal_id': meal_id,
                    'value': john_vote,
                    'message': f"⛔ Meal {meal_id}: john_vote ({john_vote}) exceeds options count ({num_options})",
                    'fix': f"Vote must be 0-{num_options-1}"
                })

        # Validate status
        if 'status' in proposal:
            valid_statuses = ['proposed', 'voted', 'confirmed']
            if proposal['status'] not in valid_statuses:
                warnings.append({
                    'type': 'invalid_status',
                    'meal_id': meal_id,
                    'value': proposal['status'],
                    'message': f"⚠️ Meal {meal_id}: Status '{proposal['status']}' not standard",
                    'fix': f"Use: {', '.join(valid_statuses)}"
                })

        # Check for confirmed meals without final_choice
        if proposal.get('status') == 'confirmed' and 'final_choice' not in proposal:
            warnings.append({
                'type': 'missing_final_choice',
                'meal_id': meal_id,
                'message': f"⚠️ Meal {meal_id}: Confirmed but no final_choice set",
                'fix': "Add 'final_choice' field with restaurant index or name"
            })

    return errors, warnings


def validate_activity_proposals(activity_proposals):
    """Validate activity proposal data

    Args:
        activity_proposals (dict): Dictionary of activity proposals

    Returns:
        tuple: (errors, warnings)
    """

    errors = []
    warnings = []

    required_fields = ['activity_options', 'time_slot', 'status']

    for activity_id, proposal in activity_proposals.items():
        # Check required fields
        missing_fields = [field for field in required_fields if field not in proposal]
        if missing_fields:
            errors.append({
                'type': 'missing_proposal_field',
                'activity_id': activity_id,
                'fields': missing_fields,
                'message': f"⛔ Activity {activity_id}: Missing fields: {', '.join(missing_fields)}",
                'fix': f"Add: {', '.join(missing_fields)}"
            })

        # Validate activity_options
        if 'activity_options' in proposal:
            if not isinstance(proposal['activity_options'], list):
                errors.append({
                    'type': 'invalid_activity_options',
                    'activity_id': activity_id,
                    'message': f"⛔ Activity {activity_id}: activity_options must be a list",
                    'fix': "Change activity_options to list of dicts"
                })
            elif len(proposal['activity_options']) == 0:
                warnings.append({
                    'type': 'empty_options',
                    'activity_id': activity_id,
                    'message': f"⚠️ Activity {activity_id}: No activity options provided",
                    'fix': "Add at least 2-3 activity options"
                })

        # Validate voting
        if 'john_vote' in proposal:
            john_vote = proposal['john_vote']
            num_options = len(proposal.get('activity_options', []))

            if isinstance(john_vote, int) and john_vote >= num_options:
                errors.append({
                    'type': 'invalid_vote',
                    'activity_id': activity_id,
                    'value': john_vote,
                    'message': f"⛔ Activity {activity_id}: john_vote ({john_vote}) exceeds options count ({num_options})",
                    'fix': f"Vote must be 0-{num_options-1}"
                })

    return errors, warnings


def generate_validation_report(is_valid, errors, warnings):
    """Generate formatted validation report

    Args:
        is_valid (bool): Whether data is valid
        errors (list): List of error dicts
        warnings (list): List of warning dicts

    Returns:
        str: Formatted report
    """

    report = []
    report.append("=" * 60)
    report.append("🔍 TRIP DATA VALIDATION REPORT")
    report.append("=" * 60)
    report.append("")

    if is_valid and len(warnings) == 0:
        report.append("✅ ALL CHECKS PASSED!")
        report.append("   Your trip data is valid and ready to go.")
        return "\n".join(report)

    # Errors section
    if errors:
        report.append(f"⛔ ERRORS: {len(errors)}")
        report.append("-" * 60)
        for idx, error in enumerate(errors, 1):
            report.append(f"\n{idx}. {error['message']}")
            report.append(f"   💡 Fix: {error['fix']}")
        report.append("")

    # Warnings section
    if warnings:
        report.append(f"⚠️  WARNINGS: {len(warnings)}")
        report.append("-" * 60)
        for idx, warning in enumerate(warnings, 1):
            report.append(f"\n{idx}. {warning['message']}")
            report.append(f"   💡 Suggestion: {warning['fix']}")
        report.append("")

    # Summary
    report.append("=" * 60)
    report.append("📊 SUMMARY")
    report.append("=" * 60)
    report.append(f"Status: {'❌ INVALID' if errors else '✅ VALID with warnings'}")
    report.append(f"Errors: {len(errors)}")
    report.append(f"Warnings: {len(warnings)}")

    if errors:
        report.append("\n🚨 FIX ERRORS BEFORE TRIP!")
        report.append("   Data integrity issues must be resolved.")
    elif warnings:
        report.append("\n💡 Consider addressing warnings for best experience.")

    return "\n".join(report)
