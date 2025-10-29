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

## 3️⃣ Google Maps API (OPTIONAL - for live traffic)

### Why?
Get real-time traffic updates and drive times.

### Steps:
1. Go to https://console.cloud.google.com/
2. Create a new project: "40th-birthday-trip"
3. Enable "Distance Matrix API"
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy your API key

**Cost:** FREE ($200/month credit - more than enough!)

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

Once you have your API keys, create a file called `secrets.toml` in the `.streamlit` folder:

### Option A: For Streamlit Cloud (when deployed)

In your Streamlit Cloud dashboard:
1. Go to your app settings
2. Click "Secrets"
3. Add:

```toml
# GitHub Token (for data persistence)
GITHUB_TOKEN = "your_github_token_here"

# Password hash (set your own password, then generate MD5 hash)
TRIP_PASSWORD_HASH = "a5be948874610641149611913c4924e5"

# Weather API (RECOMMENDED)
OPENWEATHER_API_KEY = "your_openweather_key_here"

# Traffic API (OPTIONAL)
GOOGLE_MAPS_API_KEY = "your_google_maps_key_here"

# Flight API (OPTIONAL)
AVIATIONSTACK_API_KEY = "your_aviationstack_key_here"
```

### Option B: For Local Testing

Create `.streamlit/secrets.toml`:

```bash
# Create the file
touch .streamlit/secrets.toml
```

Then add the same content as above.

---

## ✅ Test Your Setup

After adding API keys, restart your app:

```bash
streamlit run app.py
```

### What to Check:

✅ **Weather Page**: Should show real Amelia Island forecast (not sample data)
✅ **Dashboard**: Weather widget should say "OpenWeather" instead of "Sample Data"
✅ **Meals/Activities**: Votes should persist after page refresh
✅ **Travel Intelligence**: Should show "Connected to AviationStack" if configured

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
