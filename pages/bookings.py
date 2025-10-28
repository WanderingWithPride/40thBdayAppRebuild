"""
Booking Dashboard - Complete booking management interface

Tracks all activities requiring bookings, their status, and confirmation details.
Provides urgency-based prioritization and quick actions.
"""

import streamlit as st
from datetime import datetime, timedelta
from github_storage import get_trip_data, save_trip_data


def show_booking_dashboard():
    """Complete booking management interface"""

    st.title("📞 Booking Dashboard")

    data = get_trip_data()

    # Get all activities from hardcoded schedule
    from app import get_activities_and_timeline
    df, activities_data = get_activities_and_timeline()

    # Categorize activities requiring bookings
    now = datetime.now()

    bookings = []
    for activity in activities_data:
        # Check if booking is required (URGENT status or specific categories)
        requires_booking = (
            activity.get('status') == 'URGENT' or
            activity.get('category') in ['Spa', 'Activity'] or
            'book' in activity.get('notes', '').lower()
        )

        if requires_booking:
            try:
                activity_dt = datetime.strptime(activity['date'], '%Y-%m-%d')
                days_until = (activity_dt - now).days

                # Determine urgency
                if days_until <= 3:
                    urgency = 'critical'
                elif days_until <= 7:
                    urgency = 'high'
                else:
                    urgency = 'normal'

                # Get or create booking status
                booking_key = f"booking_{activity.get('id', activity['activity'].replace(' ', '_'))}"
                if booking_key not in data:
                    data[booking_key] = {
                        'status': 'not_booked',
                        'confirmation_number': None,
                        'booked_date': None,
                        'notes': ''
                    }

                booking_info = data[booking_key]

                bookings.append({
                    'activity': activity,
                    'booking': booking_info,
                    'days_until': days_until,
                    'urgency': urgency,
                    'booking_key': booking_key
                })
            except Exception as e:
                print(f"Error processing booking for {activity.get('activity')}: {e}")

    # Sort by urgency and days until
    bookings.sort(key=lambda x: (0 if x['urgency'] == 'critical' else 1 if x['urgency'] == 'high' else 2, x['days_until']))

    # Separate by status
    not_booked = [b for b in bookings if b['booking']['status'] == 'not_booked']
    confirmed = [b for b in bookings if b['booking']['status'] == 'confirmed']

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🚨 Need Booking", len(not_booked))
    with col2:
        st.metric("✅ Confirmed", len(confirmed))
    with col3:
        critical_count = sum(1 for b in not_booked if b['urgency'] == 'critical')
        st.metric("🔴 Critical", critical_count)

    st.divider()

    # URGENT BOOKINGS SECTION
    if not_booked:
        st.error(f"🚨 {len(not_booked)} BOOKINGS NEEDED")

        for booking in not_booked:
            activity = booking['activity']
            urgency_icons = {
                'critical': '🔴',
                'high': '🟠',
                'normal': '🟡'
            }

            with st.expander(
                f"{urgency_icons[booking['urgency']]} {activity['activity']} - {booking['days_until']} days away",
                expanded=(booking['urgency'] == 'critical')
            ):
                col1, col2, col3 = st.columns([2, 2, 1])

                with col1:
                    st.write(f"**📅 When:** {activity['date']} at {activity.get('time', 'TBD')}")

                    location = activity.get('location', {})
                    if isinstance(location, dict):
                        st.write(f"**📍 Where:** {location.get('name', 'TBD')}")
                        phone = location.get('phone', 'N/A')
                    else:
                        st.write(f"**📍 Where:** {location}")
                        phone = 'N/A'

                    if phone and phone != 'N/A':
                        st.write(f"**📞 Phone:** {phone}")
                        st.markdown(f"[📱 Call Now](tel:{phone})")

                with col2:
                    cost = activity.get('cost', 'TBD')
                    st.write(f"**💰 Cost:** ${cost}" if isinstance(cost, (int, float)) else f"**💰 Cost:** {cost}")
                    st.write(f"**⏱️ Duration:** {activity.get('duration', 'TBD')}")

                    notes = activity.get('notes', '')
                    if notes:
                        st.info(f"💡 {notes[:100]}...")

                with col3:
                    # Booking form
                    if st.button("✅ Mark Booked", key=f"btn_book_{booking['booking_key']}"):
                        st.session_state[f"show_form_{booking['booking_key']}"] = True

                    # Show confirmation form
                    if st.session_state.get(f"show_form_{booking['booking_key']}"):
                        with st.form(key=f"form_{booking['booking_key']}"):
                            conf_num = st.text_input("Confirmation #:", key=f"conf_{booking['booking_key']}")
                            notes_input = st.text_area("Notes:", key=f"notes_{booking['booking_key']}")

                            if st.form_submit_button("💾 Save"):
                                data[booking['booking_key']]['status'] = 'confirmed'
                                data[booking['booking_key']]['confirmation_number'] = conf_num
                                data[booking['booking_key']]['booked_date'] = datetime.now().isoformat()
                                data[booking['booking_key']]['notes'] = notes_input

                                save_trip_data(f"Booked: {activity['activity']}")
                                st.success("✅ Saved!")
                                st.session_state[f"show_form_{booking['booking_key']}"] = False
                                st.rerun()

    else:
        st.success("✅ All bookings complete!")

    # CONFIRMED BOOKINGS SECTION
    if confirmed:
        st.divider()
        st.success(f"✅ {len(confirmed)} CONFIRMED BOOKINGS")

        for booking in confirmed:
            activity = booking['activity']
            booking_info = booking['booking']

            with st.expander(f"✅ {activity['activity']} - {activity['date']}"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(f"**Confirmation:** {booking_info['confirmation_number']}")
                    if booking_info['booked_date']:
                        booked_date = booking_info['booked_date'][:10]
                        st.write(f"**Booked:** {booked_date}")

                    location = activity.get('location', {})
                    if isinstance(location, dict) and location.get('phone'):
                        st.write(f"**Phone:** {location['phone']}")

                    if booking_info.get('notes'):
                        st.info(booking_info['notes'])

                with col2:
                    if st.button("✏️ Edit", key=f"edit_{booking['booking_key']}"):
                        st.session_state[f"edit_mode_{booking['booking_key']}"] = True

                    if st.button("❌ Cancel", key=f"cancel_{booking['booking_key']}"):
                        data[booking['booking_key']]['status'] = 'cancelled'
                        save_trip_data(f"Cancelled: {activity['activity']}")
                        st.rerun()

                # Edit mode
                if st.session_state.get(f"edit_mode_{booking['booking_key']}"):
                    with st.form(key=f"edit_form_{booking['booking_key']}"):
                        new_conf = st.text_input("Confirmation #:", value=booking_info['confirmation_number'])
                        new_notes = st.text_area("Notes:", value=booking_info.get('notes', ''))

                        if st.form_submit_button("💾 Update"):
                            data[booking['booking_key']]['confirmation_number'] = new_conf
                            data[booking['booking_key']]['notes'] = new_notes
                            save_trip_data(f"Updated: {activity['activity']}")
                            st.success("✅ Updated!")
                            st.session_state[f"edit_mode_{booking['booking_key']}"] = False
                            st.rerun()

    # QUICK ACTIONS SIDEBAR
    st.sidebar.title("Quick Actions")

    if not_booked:
        if st.sidebar.button("📋 Copy All Phone Numbers"):
            phones = []
            for b in not_booked:
                loc = b['activity'].get('location', {})
                if isinstance(loc, dict) and loc.get('phone'):
                    phones.append(f"{b['activity']['activity']}: {loc['phone']}")

            if phones:
                phone_list = "\n".join(phones)
                st.sidebar.code(phone_list)
                st.sidebar.info("☝️ Copy these and start calling!")

        if st.sidebar.button("📧 Email Booking List"):
            email_body = generate_booking_email(not_booked)
            st.sidebar.text_area("Copy and email to John:", email_body, height=300)


def generate_booking_email(bookings):
    """Generate email-friendly booking list"""
    email = "Hi John,\n\n"
    email += "Here's what we still need to book for the trip:\n\n"

    for booking in bookings:
        activity = booking['activity']
        email += f"❌ {activity['activity']}\n"

        location = activity.get('location', {})
        if isinstance(location, dict) and location.get('phone'):
            email += f"   📞 {location['phone']}\n"

        email += f"   📅 {activity['date']} at {activity.get('time', 'TBD')}\n"
        email += f"   Days away: {booking['days_until']}\n\n"

    email += "Let me know if you want to help call any of these!\n\n"
    email += "Michael"

    return email


if __name__ == "__main__":
    show_booking_dashboard()
