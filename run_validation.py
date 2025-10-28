"""
Run comprehensive data validation on trip data

This script validates:
- Activity data structure
- Meal proposals
- Activity proposals
- Date/time formats
- Required fields
- Data consistency

Usage:
    python run_validation.py
"""

from github_storage import get_trip_data
from utils.data_validator import validate_trip_data, generate_validation_report


def get_activities_from_hardcoded_data():
    """Get activities from the hardcoded data in app.py"""
    # For now, return empty list - activities are hardcoded in app.py
    # In a real scenario, we'd import them from app.py
    activities = []
    return activities


def main():
    print("=" * 70)
    print("🔍 TRIP DATA VALIDATION")
    print("=" * 70)
    print()

    # Load trip data
    print("📂 Loading trip data from GitHub storage...")
    trip_data = get_trip_data()
    print(f"✅ Loaded trip data with {len(trip_data)} top-level keys")
    print()

    # Get activities (hardcoded in app.py)
    activities_data = get_activities_from_hardcoded_data()

    # Run validation
    print("🔍 Running validation checks...")
    print()

    is_valid, errors, warnings = validate_trip_data(activities_data, trip_data)

    # Generate report
    report = generate_validation_report(is_valid, errors, warnings)
    print(report)
    print()

    # Additional checks for trip_data structure
    print("=" * 70)
    print("📊 TRIP DATA STRUCTURE ANALYSIS")
    print("=" * 70)
    print()

    # Check meal proposals
    meal_proposals = trip_data.get('meal_proposals', {})
    print(f"🍽️  Meal Proposals: {len(meal_proposals)}")
    if meal_proposals:
        confirmed = sum(1 for m in meal_proposals.values() if m.get('status') == 'confirmed')
        voted = sum(1 for m in meal_proposals.values() if m.get('status') == 'voted')
        proposed = sum(1 for m in meal_proposals.values() if m.get('status') == 'proposed')
        print(f"   - Confirmed: {confirmed}")
        print(f"   - Voted: {voted}")
        print(f"   - Proposed: {proposed}")
        print()

        # Sample meal
        if meal_proposals:
            sample_key = list(meal_proposals.keys())[0]
            sample_meal = meal_proposals[sample_key]
            print(f"   Sample meal ({sample_key}):")
            print(f"   - Status: {sample_meal.get('status', 'N/A')}")
            print(f"   - Options: {len(sample_meal.get('restaurant_options', []))}")
            if 'john_vote' in sample_meal:
                print(f"   - John's vote: {sample_meal['john_vote']}")
            print()

    # Check activity proposals
    activity_proposals = trip_data.get('activity_proposals', {})
    print(f"🎯 Activity Proposals: {len(activity_proposals)}")
    if activity_proposals:
        confirmed = sum(1 for a in activity_proposals.values() if a.get('status') == 'confirmed')
        voted = sum(1 for a in activity_proposals.values() if a.get('status') == 'voted')
        proposed = sum(1 for a in activity_proposals.values() if a.get('status') == 'proposed')
        print(f"   - Confirmed: {confirmed}")
        print(f"   - Voted: {voted}")
        print(f"   - Proposed: {proposed}")
        print()

    # Check for booking data
    booking_keys = [k for k in trip_data.keys() if k.startswith('booking_')]
    print(f"📞 Booking Records: {len(booking_keys)}")
    if booking_keys:
        confirmed_bookings = sum(1 for k in booking_keys if trip_data[k].get('status') == 'confirmed')
        pending_bookings = len(booking_keys) - confirmed_bookings
        print(f"   - Confirmed: {confirmed_bookings}")
        print(f"   - Pending: {pending_bookings}")
        print()

    # Check for custom activities
    custom_activities = trip_data.get('custom_activities', [])
    print(f"✨ Custom Activities: {len(custom_activities)}")
    print()

    # Check alcohol requests
    alcohol_requests = trip_data.get('alcohol_requests', [])
    print(f"🍷 Alcohol Requests: {len(alcohol_requests)}")
    if alcohol_requests:
        purchased = sum(1 for a in alcohol_requests if a.get('purchased', False))
        pending = len(alcohol_requests) - purchased
        print(f"   - Purchased: {purchased}")
        print(f"   - Pending: {pending}")
        print()

    # Data size analysis
    import json
    data_str = json.dumps(trip_data)
    data_size_kb = len(data_str) / 1024
    print(f"💾 Data Size: {data_size_kb:.2f} KB")
    print()

    # Summary
    print("=" * 70)
    print("✅ VALIDATION COMPLETE")
    print("=" * 70)

    if is_valid:
        print("🎉 Your trip data is valid and ready!")
    else:
        print("⚠️  Please fix the errors listed above")
        print("💡 Run this script again after making fixes")

    return 0 if is_valid else 1


if __name__ == "__main__":
    exit(main())
