# GitHub Storage Setup Guide

## What This Does

Your app now stores all data (meal proposals, activity votes, preferences, etc.) in a **JSON file in your GitHub repo** instead of a database. This means:

✅ **Data persists** across Streamlit Cloud restarts
✅ **No external database** needed
✅ **Free forever** - no costs
✅ **You own your data** - it's in your repo
✅ **Version controlled** - you can see all changes
✅ **Easy to edit** - just edit the JSON file if needed

---

## Quick Setup (2 minutes)

### Step 1: Create a GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `Streamlit Trip App`
4. Set expiration: **No expiration** (or 1 year if you prefer)
5. Select scopes:
   - ✅ **repo** (Full control of private repositories)
   - That's it! Just check "repo"
6. Click **"Generate token"** at the bottom
7. **COPY THE TOKEN** - you won't see it again!
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 2: Add Token to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Find your app → Click **⋮** menu → **Settings**
3. Click **"Secrets"** tab
4. Add this line:
   ```toml
   GITHUB_TOKEN = "ghp_your_actual_token_here"
   ```
5. Replace `ghp_your_actual_token_here` with the token you copied
6. Click **"Save"**
7. Click **"Reboot app"**

### Step 3: Test It!

1. Open your live app
2. Log in (password: 28008985)
3. Go to **Travel Dashboard**
4. Create a meal or activity proposal
5. Go to your GitHub repo → Check `data/trip_data.json`
6. You should see your proposal saved! 🎉

---

## How It Works

### Data Storage
- All data is stored in `data/trip_data.json` in your GitHub repo
- When you create/update proposals, the app commits changes to GitHub
- When the app starts/restarts, it loads data from GitHub

### Local Development
- When developing locally (no GITHUB_TOKEN), it uses a local file: `trip_data_local.json`
- This way you can test without affecting the live data

### What Gets Stored
- Meal proposals and votes
- Activity proposals and votes
- John's preferences
- Alcohol/drink requests
- Packing list progress
- Custom activities
- Notes and memories
- Completed activities

---

## Troubleshooting

### "Failed to save to GitHub"
- Check that your token has `repo` scope
- Make sure the token hasn't expired
- Verify the token is correctly pasted in Streamlit secrets

### "Could not load data from GitHub"
- Check that `data/trip_data.json` exists in your repo
- Verify the GITHUB_TOKEN is set
- Check Streamlit Cloud logs for error details

### Data Not Persisting
- Make sure you clicked "Save" in Streamlit secrets
- Reboot the app after adding the token
- Check that commits are appearing in your GitHub repo

### Want to Reset All Data?
- Go to your repo → `data/trip_data.json`
- Click Edit → Delete all content
- Paste the initial structure:
```json
{
  "meal_proposals": {},
  "activity_proposals": {},
  "john_preferences": {
    "avoid_seafood_focused": "false",
    "avoid_mexican": "false"
  },
  "alcohol_requests": [],
  "packing_progress": {},
  "notes": [],
  "custom_activities": [],
  "completed_activities": [],
  "notifications": [],
  "tsa_updates": [],
  "last_updated": "2025-01-27T00:00:00"
}
```
- Commit the changes

---

## Security Notes

✅ **Safe:** The token is stored in Streamlit secrets (encrypted)
✅ **Safe:** The token only has access to your own repos
✅ **Safe:** No one can see your token in the app
❗ **Important:** Don't share your token with anyone
❗ **Important:** Don't commit the token to your repo

---

## Benefits Over Database

| Feature | GitHub Storage | PostgreSQL/Database |
|---------|---------------|---------------------|
| **Cost** | FREE forever | Free tier limits |
| **Setup Time** | 2 minutes | 10-15 minutes |
| **Persistence** | ✅ Always | ✅ Yes |
| **Your Data** | ✅ In your repo | ❌ External service |
| **Version History** | ✅ Git commits | ❌ No |
| **Easy to Edit** | ✅ Edit JSON file | ❌ Need SQL |
| **Backup** | ✅ Auto (Git) | ⚠️ Need to configure |

---

## Need Help?

If you run into issues:
1. Check Streamlit Cloud logs
2. Verify the token has `repo` scope
3. Make sure `data/trip_data.json` exists in your repo
4. Try regenerating the token if it's not working

That's it! Your data will now persist forever. 🎉
