"""
Optional Activities Database for Amelia Island
Add this to the main app for activity discovery
"""

def get_optional_activities():
    """Database of optional activities in Amelia Island"""
    return {
        "Dining": [
            {
                "name": "Salt Life Food Shack",
                "description": "Oceanfront casual dining with great views",
                "type": "Casual Dining",
                "cost_range": "$15-30",
                "duration": "1-2 hours",
                "location": {"lat": 30.6502, "lon": -81.4525, "address": "Amelia Island"},
                "phone": "904-277-3811",
                "tips": "Great for lunch, outdoor seating",
                "best_time": "Lunch or dinner"
            },
            {
                "name": "Brett's Waterway Cafe",
                "description": "Waterfront dining with marina views",
                "type": "Seafood",
                "cost_range": "$20-40",
                "duration": "1.5-2 hours",
                "location": {"lat": 30.6692, "lon": -81.4651, "address": "Fernandina Beach"},
                "phone": "904-261-2660",
                "tips": "Sunset views, fresh catch daily",
                "best_time": "Dinner"
            },
            {
                "name": "Le Clos",
                "description": "French bistro, romantic atmosphere",
                "type": "Fine Dining",
                "cost_range": "$40-70",
                "duration": "2-3 hours",
                "location": {"lat": 30.6692, "lon": -81.4651, "address": "Fernandina Beach"},
                "phone": "904-261-8100",
                "tips": "Make reservations, dress code",
                "best_time": "Dinner"
            },
            {
                "name": "29 South",
                "description": "Farm-to-table Southern cuisine",
                "type": "Upscale Casual",
                "cost_range": "$25-45",
                "duration": "1.5-2 hours",
                "location": {"lat": 30.6692, "lon": -81.4651, "address": "Fernandina Beach"},
                "phone": "904-277-7919",
                "tips": "Great brunch, local ingredients",
                "best_time": "Brunch or dinner"
            },
            {
                "name": "The Surf Restaurant & Bar",
                "description": "Beachfront dining at Ritz-Carlton",
                "type": "Resort Dining",
                "cost_range": "$30-60",
                "duration": "1.5-2 hours",
                "location": {"lat": 30.6074, "lon": -81.4493, "address": "Ritz-Carlton"},
                "phone": "904-277-1100",
                "tips": "No reservation needed, great views",
                "best_time": "Any"
            }
        ],
        "Activities": [
            {
                "name": "Horseback Riding on Beach",
                "description": "Ride horses along the beautiful beach",
                "type": "Adventure",
                "cost_range": "$75-125",
                "duration": "1-2 hours",
                "location": {"lat": 30.6502, "lon": -81.4525, "address": "Amelia Island"},
                "phone": "904-491-5166",
                "tips": "Book in advance, wear comfortable clothes",
                "best_time": "Morning or late afternoon"
            },
            {
                "name": "Fort Clinch State Park",
                "description": "Historic fort with beach access and trails",
                "type": "Historical/Nature",
                "cost_range": "$6-8",
                "duration": "2-3 hours",
                "location": {"lat": 30.7152, "lon": -81.4467, "address": "Fernandina Beach"},
                "phone": "904-277-7274",
                "tips": "Bring sunscreen, great for photos",
                "best_time": "Morning"
            },
            {
                "name": "Kayaking/Paddleboarding",
                "description": "Explore marshes and waterways",
                "type": "Water Sports",
                "cost_range": "$40-75",
                "duration": "2-3 hours",
                "location": {"lat": 30.6187, "lon": -81.4610, "address": "Various locations"},
                "phone": "904-321-0697",
                "tips": "Multiple rental companies available",
                "best_time": "Morning"
            },
            {
                "name": "Bike Rentals",
                "description": "Explore island by bike",
                "type": "Recreation",
                "cost_range": "$20-40",
                "duration": "2-4 hours",
                "location": {"lat": 30.6074, "lon": -81.4493, "address": "Multiple locations"},
                "phone": "Various",
                "tips": "Great way to explore downtown",
                "best_time": "Morning or afternoon"
            },
            {
                "name": "Fishing Charter",
                "description": "Deep sea or inshore fishing",
                "type": "Water Sports",
                "cost_range": "$400-800",
                "duration": "4-8 hours",
                "location": {"lat": 30.6692, "lon": -81.4651, "address": "Fernandina Harbor"},
                "phone": "Various charters",
                "tips": "Book early, full or half day",
                "best_time": "Morning"
            },
            {
                "name": "Golf at Oak Marsh",
                "description": "Championship golf course",
                "type": "Golf",
                "cost_range": "$80-150",
                "duration": "4-5 hours",
                "location": {"lat": 30.5950, "lon": -81.4520, "address": "Amelia Island"},
                "phone": "904-277-5907",
                "tips": "Tee time reservations recommended",
                "best_time": "Morning"
            }
        ],
        "Beaches & Nature": [
            {
                "name": "Main Beach Park",
                "description": "Popular beach with facilities",
                "type": "Beach",
                "cost_range": "Free",
                "duration": "2-4 hours",
                "location": {"lat": 30.6502, "lon": -81.4525, "address": "Fernandina Beach"},
                "phone": "N/A",
                "tips": "Arrive early for parking, rentals available",
                "best_time": "Morning"
            },
            {
                "name": "Peters Point Beach",
                "description": "Quieter beach, less crowded",
                "type": "Beach",
                "cost_range": "Free",
                "duration": "2-4 hours",
                "location": {"lat": 30.6300, "lon": -81.4500, "address": "Amelia Island"},
                "phone": "N/A",
                "tips": "More secluded, bring your own chairs",
                "best_time": "Any"
            },
            {
                "name": "Egan's Creek Greenway",
                "description": "Nature trails and boardwalks",
                "type": "Nature Walk",
                "cost_range": "Free",
                "duration": "1-2 hours",
                "location": {"lat": 30.6400, "lon": -81.5000, "address": "Fernandina Beach"},
                "phone": "N/A",
                "tips": "Bring bug spray, great for birdwatching",
                "best_time": "Morning"
            }
        ],
        "Shopping & Culture": [
            {
                "name": "Downtown Fernandina Beach",
                "description": "Historic downtown with shops and galleries",
                "type": "Shopping/Sightseeing",
                "cost_range": "Varies",
                "duration": "2-3 hours",
                "location": {"lat": 30.6692, "lon": -81.4651, "address": "Centre Street"},
                "phone": "N/A",
                "tips": "Walkable, lots of boutiques and antiques",
                "best_time": "Afternoon"
            },
            {
                "name": "Amelia Island Museum of History",
                "description": "Local history and guided tours",
                "type": "Museum",
                "cost_range": "$10-15",
                "duration": "1-2 hours",
                "location": {"lat": 30.6692, "lon": -81.4651, "address": "Fernandina Beach"},
                "phone": "904-261-7378",
                "tips": "Oral history tours are excellent",
                "best_time": "Afternoon"
            },
            {
                "name": "Farmer's Market",
                "description": "Local produce and crafts (Saturdays)",
                "type": "Market",
                "cost_range": "Varies",
                "duration": "1-2 hours",
                "location": {"lat": 30.6692, "lon": -81.4651, "address": "Downtown"},
                "phone": "N/A",
                "tips": "Only on Saturday mornings",
                "best_time": "Saturday morning"
            }
        ],
        "Relaxation": [
            {
                "name": "Additional Spa Services",
                "description": "More spa treatments at Ritz",
                "type": "Spa",
                "cost_range": "$150-300",
                "duration": "1-2 hours",
                "location": {"lat": 30.6074, "lon": -81.4493, "address": "Ritz-Carlton"},
                "phone": "904-277-1100",
                "tips": "Book multiple treatments for discount",
                "best_time": "Morning or afternoon"
            },
            {
                "name": "Pool Time at Ritz",
                "description": "Relax by the resort pools",
                "type": "Pool",
                "cost_range": "Free (guest)",
                "duration": "2-4 hours",
                "location": {"lat": 30.6074, "lon": -81.4493, "address": "Ritz-Carlton"},
                "phone": "N/A",
                "tips": "Multiple pools, get cabana",
                "best_time": "Afternoon"
            },
            {
                "name": "Sunset Viewing",
                "description": "Watch sunset from beach or pier",
                "type": "Experience",
                "cost_range": "Free",
                "duration": "30-60 min",
                "location": {"lat": 30.6502, "lon": -81.4525, "address": "Beach"},
                "phone": "N/A",
                "tips": "Check sunset time, bring camera",
                "best_time": "Evening"
            }
        ]
    }

def get_schedule_gaps(scheduled_activities):
    """Find free time in schedule"""
    # Implementation to find gaps between activities
    pass

