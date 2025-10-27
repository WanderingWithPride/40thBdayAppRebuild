# Database Setup for Persistent Storage

## The Problem

Streamlit Cloud uses **ephemeral storage**, which means the SQLite database file (`trip_data.db`) gets wiped every time the app restarts or redeploys. This causes you to lose all your meal/activity proposals and other data.

## The Solution

The app now supports **PostgreSQL** for persistent cloud storage. When you add a PostgreSQL database connection, your data will persist across restarts.

---

## Quick Setup (5 minutes)

### Option 1: Supabase (Recommended - Free & Easy)

1. **Create Free Account**
   - Go to https://supabase.com/
   - Sign up for free (no credit card required)

2. **Create New Project**
   - Click "New Project"
   - Give it a name (e.g., "birthday-trip")
   - Set a database password (save this!)
   - Choose a region close to you
   - Click "Create new project" (takes ~2 minutes)

3. **Get Connection String**
   - Once created, go to **Project Settings** (gear icon)
   - Click **Database** in left sidebar
   - Under "Connection String", select **URI**
   - Copy the connection string (looks like: `postgresql://postgres:[YOUR-PASSWORD]@...`)
   - **Replace `[YOUR-PASSWORD]` with your actual database password**

4. **Add to Streamlit Cloud**
   - Go to your app on https://streamlit.io/cloud
   - Click the app menu (⋮) → **Settings**
   - Go to **Secrets** section
   - Add this line:
     ```toml
     DATABASE_URL = "postgresql://postgres:YOUR-PASSWORD@db.xxx.supabase.co:5432/postgres"
     ```
   - Replace with your actual connection string
   - Click **Save**

5. **Restart App**
   - Click **Reboot app**
   - Your app will now use PostgreSQL!
   - All data will persist across restarts

---

### Option 2: Railway (Alternative)

1. Go to https://railway.app/
2. Sign up and create new project
3. Add **PostgreSQL** service
4. Copy the `DATABASE_URL` from the service
5. Add to Streamlit Cloud secrets (same as step 4 above)

---

### Option 3: ElephantSQL (Alternative)

1. Go to https://www.elephantsql.com/
2. Sign up for free tier
3. Create new instance
4. Copy the connection URL
5. Add to Streamlit Cloud secrets (same as above)

---

## Verification

After setup:
1. Go to your live app
2. Log in (password: 28008985)
3. Create a meal or activity proposal
4. Wait for Streamlit Cloud to restart (or manually reboot)
5. Check if the proposal still shows up → ✅ Success!

---

## Local Development

For local development, the app will continue using SQLite (`trip_data.db`). No changes needed!

Only when `DATABASE_URL` environment variable is set (like on Streamlit Cloud), will it use PostgreSQL.

---

## Need Help?

If you run into issues:
1. Check that `DATABASE_URL` is correctly formatted
2. Make sure you replaced `[YOUR-PASSWORD]` with actual password
3. Verify the database is accessible (not paused/deleted)
4. Check Streamlit Cloud logs for connection errors
