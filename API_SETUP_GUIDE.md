# 🔧 API Setup Guide - Get Everything Working!

## 🎯 What You Need

Your app is working, but using sample data. Follow these steps to enable real APIs:

---

## 1️⃣ GitHub Token (RECOMMENDED - for data persistence)

### Why?
Saves all your votes, preferences, and bookings to GitHub so they survive app restarts.

### Steps:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: `40th-birthday-app`
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
5. Click "Generate token"
6. **COPY THE TOKEN NOW** (you won't see it again!)

---

## 2️⃣ OpenWeather API (RECOMMENDED - for real weather)

### Why?
Get actual weather forecasts for Amelia Island during your trip.

### Steps:
1. Go to https://openweathermap.org/api
2. Click "Sign Up" (it's FREE!)
3. Verify your email
4. Go to https://home.openweathermap.org/api_keys
5. Copy your API key

**Cost:** FREE (1,000 calls/day)

---

## 3️⃣ Google Maps Platform APIs (RECOMMENDED - for enhanced features)

### Why?
Get real-time traffic, air quality monitoring, pollen forecasts, place search, directions, and more!

### Steps:

1. **Go to Google Cloud Console**
   - Visit https://console.cloud.google.com/

2. **Create a New Project**
   - Click "Select a project" → "New Project"
   - Name: "40th-birthday-trip"
   - Click "Create"

3. **Enable Required APIs**
   - Go to "APIs & Services" → "Library"
   - Search for and enable each of these APIs:
     - ✅ **Air Quality API** (for air quality monitoring)
     - ✅ **Pollen API** (for pollen forecasts)
     - ✅ **Distance Matrix API** (for travel times and traffic)
     - ✅ **Geocoding API** (for address validation)
     - ✅ **Places API (New)** (for restaurant/activity search)
     - ✅ **Directions API** (for route planning)
     - ✅ **Maps Static API** (for shareable map images)
     - ✅ **Street View Static API** (for location previews)

4. **Create API Key**
   - Go to "Credentials" → "Create Credentials" → "API Key"
   - Copy your API key
   - (Optional) Click "Restrict Key" to limit usage:
     - Application restrictions: None (or IP addresses if you know them)
     - API restrictions: Select only the APIs listed above

5. **Important Notes**
   - ⚠️ **All APIs use the SAME API key** - you only need one key!
   - 🔒 **Secure your key**: Never commit it to GitHub
   - 💰 **Billing**: You must enable billing, but you get $200/month free credit
   - 📊 **Usage**: This trip will use far less than the free tier

**Cost:** FREE ($200/month credit - your trip will use ~$5-10 max!)

### What Each API Does:

| API | Feature | Where Used |
|-----|---------|-----------|
| Air Quality API | Real-time air quality index (AQI) and pollutant levels | Dashboard, Today page |
| Pollen API | 5-day pollen forecast (tree, grass, weed) | Dashboard, Weather page |
| Distance Matrix API | Drive times with live traffic | Travel Intelligence |
| Geocoding API | Validate addresses and convert to coordinates | Location management |
| Places API | Find restaurants, activities, nearby attractions | Activity planning |
| Directions API | Turn-by-turn directions between locations | Route planning |
| Maps Static API | Generate shareable map images | Trip maps |
| Street View Static API | Preview images of locations | Location details |

---

## 4️⃣ AviationStack API (OPTIONAL - for flight tracking)

### Why?
Track your flights in real-time with gate info.

### Steps:
1. Go to https://aviationstack.com/
2. Click "Sign Up Free"
3. Verify your email
4. Go to your dashboard and copy your API key

**Cost:** FREE (100 calls/month)

---

## 📝 Configure Your App

Once you have your API keys, you need to add them to your app configuration.

### Option A: For Local Testing

1. **Copy the template file**
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. **Edit `.streamlit/secrets.toml`** with your actual API keys
   ```bash
   nano .streamlit/secrets.toml
   # or use your preferred text editor
   ```

3. **Fill in your keys** (remove the "your_" placeholders):
   ```toml
   # GitHub Token (for data persistence)
   GITHUB_TOKEN = "ghp_your_actual_token_here"

   # GitHub Repository
   GITHUB_REPO = "WanderingWithPride/40thBdayAppRebuild"

   # Password hash (current password is "28008985")
   TRIP_PASSWORD_HASH = "a5be948874610641149611913c4924e5"

   # Weather API (RECOMMENDED)
   OPENWEATHER_API_KEY = "your_actual_openweather_key"

   # Google Maps Platform API (RECOMMENDED - all features use this ONE key)
   GOOGLE_MAPS_API_KEY = "your_actual_google_maps_key"

   # Flight API (OPTIONAL)
   AVIATIONSTACK_API_KEY = "your_actual_aviationstack_key"
   ```

4. **Save and close** the file

5. **Verify the file is ignored by git**
   ```bash
   # This should already be in .gitignore, but double-check:
   echo ".streamlit/secrets.toml" >> .gitignore
   ```

### Option B: For Streamlit Cloud (when deployed)

In your Streamlit Cloud dashboard:
1. Go to your app settings
2. Click "Secrets"
3. Paste the entire contents of your local `secrets.toml` file

---

## ✅ Test Your Setup

After adding API keys, restart your app:

```bash
streamlit run app.py
```

### What to Check:

✅ **Weather Page**: Should show real Amelia Island forecast (not sample data)
✅ **Dashboard**:
   - Weather widget should say "OpenWeather" instead of "Sample Data"
   - Air Quality widget should show actual AQI value (not "data unavailable")
   - Pollen widget should show Tree/Grass/Weed levels (not "data unavailable")
✅ **Meals/Activities**: Votes should persist after page refresh
✅ **Travel Intelligence**: Should show "Connected to AviationStack" if configured
✅ **Maps**: Should show interactive maps with location markers

### Quick API Test

You can also run the test script to verify all APIs:

```bash
python test_apis_live.py
```

This will check:
- ✅ OpenWeather API connection
- ✅ Google Maps APIs (all 8 APIs)
- ✅ Air Quality API
- ✅ Pollen API
- ✅ GitHub connection

---

## 🎯 Minimal Setup (Just to Get Started)

If you want to start quickly, just set up these two:

1. **GitHub Token** → Data persistence
2. **OpenWeather API** → Real weather

The others can wait!

---

## 🆘 Troubleshooting

### "No GitHub token found"
- Check that `GITHUB_TOKEN` is in secrets.toml
- Make sure the file is in `.streamlit/secrets.toml`
- Restart the app

### "Sample Data" showing in weather
- Check that `OPENWEATHER_API_KEY` is in secrets.toml
- Verify the API key is active (may take a few minutes after signup)
- Try in a private/incognito browser window

### API not working after adding key
- Wait 5-10 minutes (APIs need activation time)
- Restart the Streamlit app
- Check API key has no extra spaces

---

## 💰 Cost Summary

| Service | Free Tier | Enough for Trip? |
|---------|-----------|------------------|
| GitHub Token | Unlimited | ✅ Yes |
| OpenWeather | 1,000 calls/day | ✅ Yes |
| Google Maps | $200/month credit | ✅ Yes |
| AviationStack | 100 calls/month | ✅ Yes |

**Total Cost: $0.00** for your trip! 🎉

---

## 🚀 Ready to Deploy?

Once you have your APIs set up:

1. **Test locally** with `streamlit run app.py`
2. **Deploy to Streamlit Cloud** (see DEPLOYMENT_GUIDE.md)
3. **Add secrets** in Streamlit Cloud dashboard
4. **Enjoy your trip!** 🎂
