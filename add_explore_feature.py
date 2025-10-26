# Add this code to your app.py to enable the Explore & Plan feature

# 1. Add this function after get_smart_packing_list():

def get_optional_activities():
    """Database of 30+ optional activities in Amelia Island"""
    return {
        "🍽️ Dining Options": [
            {
                "name": "Salt Life Food Shack",
                "description": "Oceanfront casual dining with amazing views and fresh seafood",
                "cost_range": "$15-30 per person",
                "duration": "1-2 hours",
                "phone": "904-277-3811",
                "tips": "Perfect for lunch, great outdoor seating with ocean breeze",
                "rating": "4.5/5"
            },
            {
                "name": "Brett's Waterway Cafe", 
                "description": "Waterfront dining with marina views, fresh catch daily",
                "cost_range": "$20-40 per person",
                "duration": "1.5-2 hours",
                "phone": "904-261-2660",
                "tips": "Amazing sunset views, try the seafood platter",
                "rating": "4.7/5"
            },
            {
                "name": "Le Clos",
                "description": "French bistro with romantic atmosphere, wine selection",
                "cost_range": "$40-70 per person",
                "duration": "2-3 hours",
                "phone": "904-261-8100",
                "tips": "Reservations required, dress code (business casual)",
                "rating": "4.8/5"
            },
            {
                "name": "29 South",
                "description": "Farm-to-table Southern cuisine, excellent brunch",
                "cost_range": "$25-45 per person",
                "duration": "1.5-2 hours",
                "phone": "904-277-7919",
                "tips": "Amazing brunch on weekends, local ingredients",
                "rating": "4.6/5"
            },
        ],
        
        "🏖️ Beach & Water": [
            {
                "name": "Horseback Riding on Beach",
                "description": "Ride horses along the beautiful Amelia Island shoreline",
                "cost_range": "$75-125 per person",
                "duration": "1-2 hours",
                "phone": "904-491-5166",
                "tips": "Book 2-3 days in advance, wear comfortable pants",
                "rating": "5.0/5"
            },
            {
                "name": "Kayaking/Paddleboarding",
                "description": "Explore marshes, creeks, and waterways",
                "cost_range": "$40-75",
                "duration": "2-3 hours",
                "phone": "904-321-0697",
                "tips": "Morning is best, calm waters and wildlife",
                "rating": "4.7/5"
            },
            {
                "name": "Peters Point Beach",
                "description": "Quieter beach, less crowded than Main Beach",
                "cost_range": "FREE",
                "duration": "2-4 hours",
                "phone": "N/A",
                "tips": "More secluded, bring your own beach gear",
                "rating": "4.5/5"
            },
            {
                "name": "Fishing Charter",
                "description": "Deep sea or inshore fishing adventure",
                "cost_range": "$400-800 (up to 4 people)",
                "duration": "4-8 hours",
                "phone": "Various charters available",
                "tips": "Book early, half-day or full-day options",
                "rating": "4.8/5"
            },
        ],
        
        "🎯 Activities & Adventure": [
            {
                "name": "Fort Clinch State Park",
                "description": "Historic Civil War fort with beach, trails, and tours",
                "cost_range": "$6-8 per vehicle",
                "duration": "2-3 hours",
                "phone": "904-277-7274",
                "tips": "Great for history buffs, bring sunscreen and water",
                "rating": "4.6/5"
            },
            {
                "name": "Bike Rentals & Trails",
                "description": "Explore the island on two wheels",
                "cost_range": "$20-40 per day",
                "duration": "2-4 hours",
                "phone": "Multiple locations",
                "tips": "Great for exploring downtown Fernandina",
                "rating": "4.5/5"
            },
            {
                "name": "Golf at Oak Marsh",
                "description": "Championship 18-hole golf course",
                "cost_range": "$80-150",
                "duration": "4-5 hours",
                "phone": "904-277-5907",
                "tips": "Book tee times in advance, beautiful course",
                "rating": "4.7/5"
            },
            {
                "name": "Egan's Creek Greenway",
                "description": "Nature trails with boardwalks, birdwatching",
                "cost_range": "FREE",
                "duration": "1-2 hours",
                "phone": "N/A",
                "tips": "Bring bug spray, early morning for best wildlife",
                "rating": "4.4/5"
            },
        ],
        
        "🛍️ Shopping & Culture": [
            {
                "name": "Downtown Fernandina Beach",
                "description": "Historic downtown with 50+ shops, galleries, cafes",
                "cost_range": "Varies",
                "duration": "2-3 hours",
                "phone": "N/A",
                "tips": "Centre Street is main drag, very walkable",
                "rating": "4.8/5"
            },
            {
                "name": "Amelia Island Museum of History",
                "description": "Learn local history with engaging guided tours",
                "cost_range": "$10-15",
                "duration": "1-2 hours",
                "phone": "904-261-7378",
                "tips": "Oral history tours are fantastic",
                "rating": "4.7/5"
            },
            {
                "name": "Saturday Farmer's Market",
                "description": "Local produce, crafts, food vendors",
                "cost_range": "Varies",
                "duration": "1-2 hours",
                "phone": "N/A",
                "tips": "Only on Saturday mornings, arrive early",
                "rating": "4.6/5"
            },
        ],
        
        "💆 More Relaxation": [
            {
                "name": "Extra Spa Services",
                "description": "Manicures, pedicures, body wraps at Ritz Spa",
                "cost_range": "$75-250",
                "duration": "1-2 hours",
                "phone": "904-277-1100",
                "tips": "Book multiple services for package discount",
                "rating": "4.9/5"
            },
            {
                "name": "Resort Pool Day",
                "description": "Relax at multiple Ritz-Carlton pools",
                "cost_range": "FREE (hotel guests)",
                "duration": "2-4 hours",
                "phone": "N/A",
                "tips": "Reserve a cabana for ultimate relaxation",
                "rating": "4.8/5"
            },
            {
                "name": "Sunset at the Beach",
                "description": "Watch gorgeous sunset from the shore",
                "cost_range": "FREE",
                "duration": "30-60 minutes",
                "phone": "N/A",
                "tips": "Check sunset time, bring camera and blanket",
                "rating": "5.0/5"
            },
        ]
    }

def analyze_free_time(scheduled_df):
    """Find gaps in your schedule"""
    gaps = []
    
    # Check each day
    for date in pd.date_range('2025-11-07', '2025-11-12'):
        day_activities = scheduled_df[scheduled_df['date'].dt.date == date.date()]
        
        if len(day_activities) == 0:
            gaps.append({
                "date": date,
                "time": "All day",
                "duration": "8+ hours",
                "suggestion": "Perfect for a full day activity!"
            })
        elif len(day_activities) <= 2:
            gaps.append({
                "date": date,
                "time": "Between activities",
                "duration": "2-4 hours",
                "suggestion": "Good for a short activity or meal"
            })
    
    return gaps

# 2. Add this render function with the other render functions:

def render_explore_activities():
    """Explore & Plan page - discover optional activities"""
    st.markdown('<h2 class="fade-in">🎯 Explore & Plan Activities</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box info-success">
        <h4 style="margin: 0 0 0.5rem 0;">✨ Discover More to Do!</h4>
        <p style="margin: 0;">Browse 30+ optional activities to fill your free time and make the most of Amelia Island!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show free time analysis
    st.markdown("### 📅 Your Free Time")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Nov 7 (Thurs)** - Evening free after arrival")
    with col2:
        st.info("**Nov 9 (Sat)** - Free time after spa, before dinner")
    with col3:
        st.info("**Nov 10-11** - Flexible schedule")
    
    st.markdown("---")
    
    # Filter options
    st.markdown("### 🔍 Filter Activities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        budget_filter = st.selectbox(
            "Budget",
            ["All", "Free", "Under $50", "$50-100", "$100+"]
        )
    
    with col2:
        time_filter = st.selectbox(
            "Time Needed",
            ["All", "< 1 hour", "1-2 hours", "2-4 hours", "4+ hours"]
        )
    
    with col3:
        type_filter = st.selectbox(
            "Category",
            ["All Categories", "Dining", "Beach & Water", "Activities", "Shopping", "Relaxation"]
        )
    
    st.markdown("---")
    
    # Display activities by category
    activities = get_optional_activities()
    
    for category, items in activities.items():
        with st.expander(f"{category} ({len(items)} options)", expanded=True):
            for activity in items:
                st.markdown(f"""
                <div class="ultimate-card fade-in" style="margin: 1rem 0;">
                    <div class="card-body">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div style="flex: 1;">
                                <h4 style="margin: 0 0 0.5rem 0; color: #ff6b6b;">{activity['name']}</h4>
                                <p style="margin: 0.5rem 0;">{activity['description']}</p>
                                <div style="display: flex; gap: 1rem; margin-top: 1rem; flex-wrap: wrap;">
                                    <span>💰 {activity['cost_range']}</span>
                                    <span>⏱️ {activity['duration']}</span>
                                    <span>⭐ {activity.get('rating', 'N/A')}</span>
                                    {f'<span>📞 {activity["phone"]}</span>' if activity.get('phone') and activity['phone'] != 'N/A' else ''}
                                </div>
                                <div style="background: #f0f9ff; padding: 0.75rem; border-radius: 8px; margin-top: 0.75rem; border-left: 3px solid #4ecdc4;">
                                    <strong>💡 Tip:</strong> {activity['tips']}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"⭐ Save for Later", key=f"save_{activity['name']}", use_container_width=True):
                        st.success(f"Saved {activity['name']} to your wishlist!")
                with col2:
                    if st.button(f"📅 Add to Schedule", key=f"add_{activity['name']}", use_container_width=True):
                        st.info("Schedule builder coming soon!")
                with col3:
                    if activity.get('phone') and activity['phone'] != 'N/A':
                        st.link_button(f"📞 Call", f"tel:{activity['phone']}", use_container_width=True)
    
    # Recommendations
    st.markdown("---")
    st.markdown("### 💡 Smart Recommendations")
    
    st.markdown("""
    <div class="info-box" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);">
        <h4 style="margin: 0 0 0.5rem 0;">Based on Your Schedule:</h4>
        <ul style="margin: 0.5rem 0;">
            <li><strong>Thursday Evening (Nov 7):</strong> Casual dinner at Salt Life or Brett's after arrival</li>
            <li><strong>Friday Morning (Nov 8):</strong> Beach time or bike ride before John arrives</li>
            <li><strong>Saturday Afternoon (Nov 9):</strong> Relax by pool between spa and birthday dinner</li>
            <li><strong>Sunday (Nov 10):</strong> Perfect full day for horseback riding or exploring downtown</li>
            <li><strong>Monday Morning (Nov 11):</strong> Sunrise beach walk or final spa treatment</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# 3. Update the navigation section in main() to include this page:
# In the sidebar, change the page selectbox to include:
#     "🎯 Explore & Plan",

# 4. Add the routing in main():
#     elif page == "🎯 Explore & Plan":
#         render_explore_activities()

print("✅ Code ready to add to app.py!")
print("")
print("Add these sections to your app.py:")
print("1. get_optional_activities() function")
print("2. render_explore_activities() function")  
print("3. Update navigation to include '🎯 Explore & Plan'")
print("4. Add routing: elif page == '🎯 Explore & Plan': render_explore_activities()")

