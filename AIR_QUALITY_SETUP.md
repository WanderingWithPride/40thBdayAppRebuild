# 🌿 Air Quality & Pollen Setup Guide

Quick guide to enable Air Quality and Pollen monitoring features in your 40th Birthday Trip Assistant.

---

## 🎯 What You'll Get

Once set up, your app will display:

### Air Quality Widget
- **Real-time AQI** (Air Quality Index) for Amelia Island
- **Color-coded status** (Good, Moderate, Unhealthy, etc.)
- **Health recommendations** based on current air quality
- **Pollutant details** (PM2.5, PM10, O3, NO2, CO, SO2)

### Pollen Forecast Widget
- **5-day pollen forecast** for Amelia Island
- **Three pollen types**: Tree, Grass, and Weed
- **Level indicators** (Very Low to Very High)
- **Allergy recommendations** for outdoor activities

---

## 📋 Prerequisites

You need **one Google Maps API key** that works for all Google services.

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Get Your Google Maps API Key

If you already have one, skip to Step 2.

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/

2. **Create or Select a Project**
   - Click "Select a project" → "New Project"
   - Name it: `40th-birthday-trip`
   - Click "Create"

3. **Enable Billing** (Required, but you get $200/month FREE credit!)
   - Go to "Billing" → "Link a billing account"
   - Add a credit card (you won't be charged if you stay under $200/month)
   - Your trip will use ~$5-10 total

4. **Enable Required APIs**
   - Go to "APIs & Services" → "Library"
   - Search and enable these APIs (click "Enable" for each):
     - ✅ **Air Quality API**
     - ✅ **Pollen API**
     - ✅ **Distance Matrix API** (optional, for traffic)
     - ✅ **Geocoding API** (optional, for address validation)
     - ✅ **Places API (New)** (optional, for restaurant search)

5. **Create API Key**
   - Go to "Credentials" → "Create Credentials" → "API Key"
   - Copy your API key (starts with `AIza...`)
   - (Optional) Click "Restrict Key" to limit to specific APIs

### Step 2: Add API Key to Your App

1. **Copy the template file**
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. **Edit the secrets file**
   ```bash
   nano .streamlit/secrets.toml
   # or use your preferred text editor
   ```

3. **Add your API key**
   Find this line:
   ```toml
   GOOGLE_MAPS_API_KEY = "your_google_maps_key_here"
   ```

   Replace with your actual key:
   ```toml
   GOOGLE_MAPS_API_KEY = "AIzaSyD-9tSr..."
   ```

4. **Save and close** the file (Ctrl+X, then Y, then Enter in nano)

### Step 3: Test the APIs

Run the test script to verify everything works:

```bash
python test_air_quality_pollen.py
```

You should see:
```
✓ API key found
━━━ Testing Air Quality API ━━━
✓ Air Quality API is working!
  📊 Current AQI: 42

━━━ Testing Pollen API ━━━
✓ Pollen API is working!
  🌳 Tree Pollen: Level 2/5

🎉 All tests passed! Your APIs are ready to use.
```

### Step 4: Run Your App

```bash
streamlit run app.py
```

Navigate to the **Dashboard** and scroll down to see:
- 🌬️ **Air Quality & Pollen - Amelia Island** widget with real data!

---

## ✅ Verification Checklist

Make sure these all work:

- [ ] Air Quality widget shows actual AQI (not "data unavailable")
- [ ] AQI has a color-coded display (green/yellow/red background)
- [ ] Pollen widget shows Tree/Grass/Weed levels (not "data unavailable")
- [ ] 5-day pollen forecast is available in the expander
- [ ] Health recommendations appear based on conditions

---

## 🆘 Troubleshooting

### "Air quality data unavailable"

**Causes:**
1. API key not set correctly in `secrets.toml`
2. Air Quality API not enabled in Google Cloud Console
3. Billing not enabled on your Google Cloud project

**Fixes:**
```bash
# Check if API key is set
cat .streamlit/secrets.toml | grep GOOGLE_MAPS_API_KEY

# Run test script
python test_air_quality_pollen.py

# Check for specific error messages
```

### "403 Forbidden" Error

This means the API is not enabled.

**Fix:**
1. Go to: https://console.cloud.google.com/apis/library
2. Search for "Air Quality API"
3. Click "Enable"
4. Search for "Pollen API"
5. Click "Enable"
6. Wait 5-10 minutes for activation
7. Restart your app

### "Billing not enabled" Error

You need to enable billing to use these APIs (but you get $200/month free).

**Fix:**
1. Go to: https://console.cloud.google.com/billing
2. Click "Link a billing account"
3. Add a payment method
4. Your trip usage will be under the free tier

### API Key Not Found

**Fix:**
```bash
# Make sure the file exists
ls -la .streamlit/secrets.toml

# If not, copy the template
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit and add your key
nano .streamlit/secrets.toml
```

### Test Script Shows Old Data

If you just enabled the APIs, they might take a few minutes to activate.

**Fix:**
1. Wait 5-10 minutes
2. Run the test again:
   ```bash
   python test_air_quality_pollen.py
   ```

---

## 💡 How It Works

### Air Quality API
- **Endpoint**: `https://airquality.googleapis.com/v1/currentConditions:lookup`
- **Data**: Real-time air quality measurements from monitoring stations
- **Update frequency**: Hourly
- **Cache**: Data cached for 1 hour to reduce API calls

### Pollen API
- **Endpoint**: `https://pollen.googleapis.com/v1/forecast:lookup`
- **Data**: 5-day pollen forecasts (tree, grass, weed)
- **Update frequency**: Daily
- **Cache**: Data cached for 1 hour to reduce API calls

### Cost Estimate

For your 4-day trip with 2 users:
- **Air Quality API**: ~$0.01 per request
- **Pollen API**: ~$0.01 per request
- **Estimated total**: $5-10 for the entire trip
- **Your free credit**: $200/month

**You won't pay anything!** 🎉

---

## 🔧 Advanced Configuration

### Cache Settings

Air Quality and Pollen data is cached for 1 hour. To change:

Edit `utils/air_quality.py`:
```python
@st.cache_data(ttl=3600)  # Change 3600 to desired seconds
```

### Custom Locations

To add other locations, edit `app.py` around line 10530:

```python
render_air_quality_widget(
    location_name="Your Location",
    lat=YOUR_LATITUDE,
    lon=YOUR_LONGITUDE
)
```

---

## 📊 What the Data Means

### Air Quality Index (AQI)

| AQI | Category | Color | Meaning |
|-----|----------|-------|---------|
| 0-50 | Good | 🟢 Green | Ideal for outdoor activities |
| 51-100 | Moderate | 🟡 Yellow | Acceptable quality |
| 101-150 | Unhealthy for Sensitive Groups | 🟠 Orange | Limit prolonged exertion |
| 151-200 | Unhealthy | 🔴 Red | Avoid prolonged exertion |
| 201-300 | Very Unhealthy | 🟣 Purple | Avoid all outdoor activity |
| 301+ | Hazardous | 🟤 Maroon | Stay indoors |

### Pollen Levels

| Level | Icon | Meaning |
|-------|------|---------|
| 0 | None | No pollen |
| 1 | 🟢 Very Low | Safe for allergy sufferers |
| 2 | 🟡 Low | Minimal symptoms |
| 3 | 🟠 Moderate | Take allergy medication if sensitive |
| 4 | 🔴 High | Expect symptoms, take medication |
| 5 | 🔴🔴 Very High | Stay indoors if very sensitive |

---

## 🎉 You're Done!

Your Air Quality and Pollen monitoring is now fully operational!

**Next steps:**
- Check the dashboard to see current conditions
- Plan outdoor activities based on air quality
- Take allergy medication on high pollen days
- Enjoy your trip! 🎂

---

## 📞 Support

If you run into issues:

1. **Run the test script**: `python test_air_quality_pollen.py`
2. **Check the logs**: Look at terminal output when running the app
3. **Verify APIs are enabled**: https://console.cloud.google.com/apis/dashboard
4. **Check API_SETUP_GUIDE.md** for general Google API setup

---

**Last Updated**: October 28, 2025
**Status**: Production Ready ✅
