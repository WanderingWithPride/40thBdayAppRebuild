"""
Simple data validation script (no streamlit dependency)

Validates trip data directly from JSON file
"""

import json
from datetime import datetime


def validate_data():
    """Validate trip data from JSON file"""

    print("=" * 70)
    print("🔍 TRIP DATA VALIDATION REPORT")
    print("=" * 70)
    print()

    # Load data
    with open('data/trip_data.json', 'r') as f:
        data = json.load(f)

    print(f"✅ Successfully loaded trip data")
    print()

    # Validation results
    errors = []
    warnings = []
    info = []

    # Check meal proposals
    print("🍽️  MEAL PROPOSALS")
    print("-" * 70)

    meal_proposals = data.get('meal_proposals', {})
    print(f"Total meals: {len(meal_proposals)}")

    if not meal_proposals:
        errors.append("No meal proposals found")
    else:
        for meal_id, proposal in meal_proposals.items():
            # Check required fields
            if 'restaurant_options' not in proposal:
                errors.append(f"Meal {meal_id}: Missing restaurant_options")
            elif not proposal['restaurant_options']:
                warnings.append(f"Meal {meal_id}: Empty restaurant_options")
            else:
                print(f"   {meal_id}: {len(proposal['restaurant_options'])} options, status={proposal.get('status', 'N/A')}")

            # Check status
            status = proposal.get('status', '')
            if status not in ['proposed', 'voted', 'confirmed']:
                warnings.append(f"Meal {meal_id}: Invalid status '{status}'")

            # Check if confirmed but no final_choice
            if status == 'confirmed' and not proposal.get('final_choice'):
                warnings.append(f"Meal {meal_id}: Confirmed but no final_choice set")

            # Check if voted
            if 'john_vote' in proposal:
                info.append(f"Meal {meal_id}: John voted")

    print()

    # Check activity proposals
    print("🎯 ACTIVITY PROPOSALS")
    print("-" * 70)

    activity_proposals = data.get('activity_proposals', {})
    print(f"Total activities: {len(activity_proposals)}")

    if not activity_proposals:
        errors.append("No activity proposals found")
    else:
        for activity_id, proposal in activity_proposals.items():
            # Check required fields
            if 'activity_options' not in proposal:
                errors.append(f"Activity {activity_id}: Missing activity_options")
            elif not proposal['activity_options']:
                warnings.append(f"Activity {activity_id}: Empty activity_options")
            else:
                print(f"   {activity_id}: {len(proposal['activity_options'])} options, status={proposal.get('status', 'N/A')}")

            # Check status
            status = proposal.get('status', '')
            if status not in ['proposed', 'voted', 'confirmed']:
                warnings.append(f"Activity {activity_id}: Invalid status '{status}'")

            # Check if voted
            if 'john_vote' in proposal:
                info.append(f"Activity {activity_id}: John voted")

    print()

    # Check bookings
    print("📞 BOOKINGS")
    print("-" * 70)

    booking_keys = [k for k in data.keys() if k.startswith('booking_')]
    print(f"Total booking records: {len(booking_keys)}")

    if booking_keys:
        confirmed = sum(1 for k in booking_keys if data[k].get('status') == 'confirmed')
        not_booked = sum(1 for k in booking_keys if data[k].get('status') == 'not_booked')

        print(f"   Confirmed: {confirmed}")
        print(f"   Not booked: {not_booked}")

        if not_booked > 0:
            warnings.append(f"{not_booked} bookings still need to be made")

    print()

    # Check alcohol requests
    print("🍷 ALCOHOL REQUESTS")
    print("-" * 70)

    alcohol_requests = data.get('alcohol_requests', [])
    print(f"Total requests: {len(alcohol_requests)}")

    if alcohol_requests:
        purchased = sum(1 for a in alcohol_requests if a.get('purchased', False))
        pending = len(alcohol_requests) - purchased

        print(f"   Purchased: {purchased}")
        print(f"   Pending: {pending}")

        for request in alcohol_requests:
            item = request.get('item', 'Unknown')
            status = "✅" if request.get('purchased') else "❌"
            print(f"   {status} {item}")

    print()

    # Data size
    print("💾 DATA METRICS")
    print("-" * 70)

    data_str = json.dumps(data)
    data_size_kb = len(data_str) / 1024
    print(f"Data size: {data_size_kb:.2f} KB")
    print(f"Top-level keys: {len(data)}")

    # Check timestamps
    if 'created_at' in data:
        print(f"Created: {data['created_at']}")
    if 'last_updated' in data:
        print(f"Last updated: {data['last_updated']}")

    print()

    # Summary
    print("=" * 70)
    print("📊 VALIDATION SUMMARY")
    print("=" * 70)
    print()

    if errors:
        print(f"⛔ ERRORS: {len(errors)}")
        for error in errors:
            print(f"   - {error}")
        print()

    if warnings:
        print(f"⚠️  WARNINGS: {len(warnings)}")
        for warning in warnings:
            print(f"   - {warning}")
        print()

    if not errors and not warnings:
        print("✅ ALL CHECKS PASSED!")
        print("   Your trip data is valid and ready to go.")
    elif not errors:
        print("✅ DATA IS VALID (with some warnings)")
        print("   Consider addressing warnings for best experience.")
    else:
        print("❌ DATA HAS ERRORS")
        print("   Please fix errors before trip!")

    print()

    # Trip readiness check
    print("=" * 70)
    print("🎯 TRIP READINESS CHECKLIST")
    print("=" * 70)
    print()

    # Count finalized items
    meals_confirmed = sum(1 for m in meal_proposals.values() if m.get('status') == 'confirmed')
    meals_total = len(meal_proposals)

    activities_confirmed = sum(1 for a in activity_proposals.values() if a.get('status') == 'confirmed')
    activities_total = len(activity_proposals)

    bookings_confirmed = sum(1 for k in booking_keys if data[k].get('status') == 'confirmed')
    bookings_total = len(booking_keys)

    # Calculate readiness percentage
    total_items = meals_total + activities_total + bookings_total
    confirmed_items = meals_confirmed + activities_confirmed + bookings_confirmed

    if total_items > 0:
        readiness = (confirmed_items / total_items) * 100
    else:
        readiness = 0

    print(f"📊 Overall Readiness: {readiness:.1f}%")
    print()
    print(f"   Meals: {meals_confirmed}/{meals_total} confirmed")
    print(f"   Activities: {activities_confirmed}/{activities_total} confirmed")
    print(f"   Bookings: {bookings_confirmed}/{bookings_total} confirmed")
    print()

    if readiness >= 90:
        print("🎉 YOU'RE READY FOR YOUR TRIP!")
    elif readiness >= 70:
        print("✅ Almost ready! Just a few more things to finalize.")
    elif readiness >= 50:
        print("⚠️  Still some work to do. Keep going!")
    else:
        print("🚧 Trip planning in progress...")

    print()

    return len(errors) == 0


if __name__ == "__main__":
    success = validate_data()
    exit(0 if success else 1)
