# 🚀 Google APIs Integration Guide

## Overview

This guide explains how to integrate all the new Google API utilities into app.py.

**New Utilities Created:**
- ✅ `utils/google_places.py` - Restaurant/activity discovery
- ✅ `utils/air_quality.py` - Air quality & pollen monitoring
- ✅ `utils/google_routes.py` - Directions & route optimization
- ✅ `utils/street_view.py` - Street View previews
- ✅ `utils/geocoding.py` - Geocoding & address validation
- ✅ `utils/static_maps.py` - Static map generation

---

## Step 1: Add Imports to app.py

Add these imports at the top of app.py (around line 50, after existing imports):

```python
# Google API Integrations
from utils.google_places import (
    render_places_search_widget,
    search_nearby_places,
    get_place_details
)
from utils.air_quality import (
    render_air_quality_widget,
    check_outdoor_activity_safety
)
from utils.google_routes import (
    get_directions,
    render_directions_card,
    render_route_optimizer
)
from utils.street_view import (
    render_street_view_preview,
    get_street_view_url
)
from utils.geocoding import (
    geocode_address,
    get_coordinates,
    validate_address
)
from utils.static_maps import (
    generate_trip_map,
    generate_static_map_url
)
```

---

## Step 2: Add New Page - "Discover"

Add to sidebar navigation (around line 10118):

```python
page = st.selectbox(
    "📍 Navigate",
    [
        "🏠 Dashboard",
        "🎯 Travel Dashboard",
        "📅 Today",
        "🗓️ Full Schedule",
        "📞 Bookings",
        "👤 John's Page",
        "🗺️ Map & Locations",
        "🔍 Discover",  # <-- NEW PAGE
        "🎒 Packing List",
        "🎂 Birthday",
        "📸 Memories",
        "💰 Budget",
        "🌤️ Weather",
        "ℹ️ About"
    ],
    index=0
)
```

Add page handler (around line 10240, before "About" page):

```python
elif page == "🔍 Discover":
    st.markdown('<h2 class="fade-in">🔍 Discover Nearby</h2>', unsafe_allow_html=True)
    st.write("Find restaurants, activities, and attractions near Amelia Island!")

    # Render Places search widget
    render_places_search_widget(
        location_name="Amelia Island",
        lat=30.6074,
        lon=-81.4493
    )
```

---

## Step 3: Add Air Quality to Weather Page

In the Weather page (around line 10295, after tide data):

```python
elif page == "🌤️ Weather":
    st.markdown('<h2 class="fade-in">🌤️ Weather, UV & Tides</h2>', unsafe_allow_html=True)

    # Get tide data
    tide_data = get_tide_data()

    # NEW: Add Air Quality & Pollen section at top
    st.markdown("---")
    render_air_quality_widget(
        location_name="Amelia Island",
        lat=30.6074,
        lon=-81.4493
    )
    st.markdown("---")

    # ... existing weather code continues ...
```

---

## Step 4: Add Street View to Restaurants

In meal/restaurant display sections, add Street View previews. Find where restaurants are displayed (search for "restaurant_options") and add:

```python
# After displaying restaurant details
if restaurant.get('address') or restaurant.get('location'):
    location = restaurant.get('address') or f"{restaurant['location']['lat']},{restaurant['location']['lon']}"
    render_street_view_preview(location, title=restaurant['name'], size="600x300")
```

---

## Step 5: Add Route Optimizer to Travel Dashboard

In Travel Dashboard (around line 7200), add route optimization section:

```python
# In render_travel_dashboard() function
st.markdown("### 🗺️ Route Optimizer")

# Get today's activities
today_activities = [a for a in df.itertuples() if a.Date == datetime.now().strftime('%Y-%m-%d')]

if today_activities:
    # Convert to list of dicts
    activities_list = [
        {
            'name': a.Activity,
            'location': a.Location if hasattr(a, 'Location') else None
        }
        for a in today_activities
    ]

    hotel_location = (30.6074, -81.4493)  # Ritz-Carlton coordinates
    render_route_optimizer(activities_list, hotel_location)
else:
    st.info("No activities scheduled for today")
```

---

## Step 6: Add Trip Map Generator

Add a button to generate shareable trip map (add to Dashboard or Map page):

```python
# In render_dashboard_ultimate() or render_map_page()
st.markdown("### 📸 Trip Map")

if st.button("🗺️ Generate Shareable Map", type="primary"):
    with st.spinner("Generating map..."):
        # Get all activities
        activities = []
        for idx, row in df.iterrows():
            activities.append({
                'name': row['Activity'],
                'location': row.get('Location', '')
            })

        # Generate static map
        hotel = "30.6074,-81.4493"
        map_url = generate_trip_map(hotel, activities, size="800x600")

        if map_url:
            st.image(map_url, caption="Your Trip Map - Right-click to save!", use_container_width=True)
            st.success("✅ Map generated! Right-click the image to save and share.")
        else:
            st.error("Could not generate map - check API key")
```

---

## Step 7: Add Directions to Activities

When displaying an activity, add "Get Directions" button:

```python
# In activity display section
col1, col2 = st.columns([3, 1])

with col1:
    st.write(f"**Activity:** {activity_name}")
    st.write(f"**Location:** {location}")

with col2:
    if st.button("🚗 Get Directions", key=f"dir_{activity_name}"):
        hotel = "The Ritz-Carlton, Amelia Island"
        directions = get_directions(hotel, location)

        if directions:
            render_directions_card(directions)
        else:
            st.error("Could not get directions")
```

---

## Step 8: Add Outdoor Safety Check to Dashboard

In Dashboard (around line 4720), add safety widget:

```python
# In render_dashboard_ultimate()
st.markdown("### 🌬️ Outdoor Activity Safety")

safety = check_outdoor_activity_safety(30.6074, -81.4493)

if safety['safe']:
    st.success(safety['recommendation'])
else:
    st.warning(safety['recommendation'])

if safety['issues']:
    for issue in safety['issues']:
        st.write(f"  {issue}")
```

---

## Step 9: Add Geocoding for New Activities

When users add custom activities, use geocoding to auto-fill coordinates:

```python
# In add custom activity section
address = st.text_input("Address/Location")

if address:
    coords = get_coordinates(address)
    if coords:
        st.success(f"✅ Found: {coords}")
        # Auto-fill lat/lon fields
    else:
        st.warning("⚠️ Could not find location")
```

---

## Quick Integration Checklist

- [x] Weather page HTML fix (DONE)
- [ ] Import all new utilities
- [ ] Add "Discover" page
- [ ] Add Air Quality to Weather page
- [ ] Add Street View to restaurants
- [ ] Add Route Optimizer to Travel Dashboard
- [ ] Add Trip Map generator
- [ ] Add Directions buttons
- [ ] Add Outdoor Safety widget
- [ ] Add Geocoding to activity creation

---

## Testing Checklist

After integration:

1. **Test Places Search:**
   - Go to Discover page
   - Search for "restaurant"
   - Verify results appear with photos
   - Check ratings display correctly

2. **Test Air Quality:**
   - Go to Weather page
   - Verify AQI displays with color coding
   - Check pollen forecast shows

3. **Test Street View:**
   - Find any restaurant
   - Verify Street View image loads
   - Check it shows correct location

4. **Test Route Optimizer:**
   - Go to Travel Dashboard
   - Select multiple activities
   - Click "Optimize Route"
   - Verify optimized order displays

5. **Test Directions:**
   - Click "Get Directions" on any activity
   - Verify turn-by-turn instructions show
   - Check duration and distance display

6. **Test Trip Map:**
   - Click "Generate Shareable Map"
   - Verify static map shows all locations
   - Try right-click save

---

## Cost Monitoring

Monitor usage at: https://console.cloud.google.com/apis/dashboard

**Expected costs for 5-day trip:**
- Places API: ~$2
- Directions: ~$0.50
- Air Quality: ~$0.75
- Pollen: ~$0.15
- Street View: ~$0.50
- Geocoding: ~$0.30
- Static Maps: ~$0.05

**Total: ~$4.25** (well under $200 free tier!)

---

## Troubleshooting

**"No results found"**
- Check GOOGLE_MAPS_API_KEY is set in .streamlit/secrets.toml
- Verify API is enabled in Google Cloud Console
- Check API key restrictions

**"API quota exceeded"**
- Check usage dashboard
- Verify you're under daily limits
- Consider caching more aggressively

**Street View not loading**
- Location may not have Street View coverage
- Check metadata first with get_street_view_metadata()

**Route optimization fails**
- Try with fewer waypoints (max ~10)
- Verify locations are valid addresses or coordinates
- Check network connectivity

---

## Next Steps

1. Import utilities into app.py
2. Add new Discover page
3. Integrate Air Quality into Weather
4. Test each feature individually
5. Monitor API usage
6. Adjust caching as needed

**Ready to integrate? Start with Step 1!**
