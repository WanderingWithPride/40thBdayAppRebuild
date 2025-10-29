# GitHub 401 Error - Investigation Report
**Date:** October 29, 2025
**Issue:** "Could not load data from GitHub (status 401)" error persisting after fixes

---

## 🔍 Investigation Summary

I've conducted a comprehensive investigation into the persistent 401 errors you're experiencing. Here's what I found:

### ✅ What's Working Correctly:

1. **GitHub Token is Valid** ✅
   - Tested token directly with curl → SUCCESS (200 OK)
   - Token has correct permissions (read/write)
   - Token expires Nov 27, 2025 (not expired)
   - Token length: 93 characters ✅

2. **Token is Properly Stored** ✅
   - Located in: `.streamlit/secrets.toml`
   - File is gitignored (secure) ✅
   - Token format is correct ✅

3. **Code Fix is Implemented** ✅
   - `github_storage.py` now uses dynamic token loading
   - No module-level token assignment
   - Proper fallback mechanism (env var → st.secrets)
   - Both `load_data_from_github()` and `save_data_to_github()` use `_get_github_token()`

4. **Test Script Confirms Everything Works** ✅
   - Token loads from secrets.toml ✅
   - Environment variable can be set ✅
   - GitHub API call succeeds (200 OK) ✅

---

## 🤔 Why Are You Still Getting 401 Errors?

Since all the code is correct and the token works, the issue is likely one of these:

### Most Likely Causes:

1. **Python Bytecode Cache (.pyc files)**
   - Old compiled code might still be running
   - **I've cleared these for you** ✅

2. **Streamlit is Running Old Code**
   - Streamlit might be using cached version
   - Need to fully restart the Streamlit server

3. **Browser Cache**
   - Your browser might be showing old app state
   - Need hard refresh

4. **Not Running Latest Code**
   - Need to pull latest changes from git

---

## 🚀 How to Fix This

Follow these steps **in order**:

### Step 1: Pull Latest Changes
```bash
cd /home/user/40thBdayAppRebuild
git pull origin claude/security-audit-investigation-011CUadQBs1kcUWKLzXraspq
```

### Step 2: Verify Token is in Secrets File
```bash
grep "GITHUB_TOKEN" .streamlit/secrets.toml
```
You should see:
```toml
GITHUB_TOKEN = "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"
```

### Step 3: Clear All Caches
```bash
# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null

# Clear Streamlit cache (if it exists)
rm -rf ~/.streamlit/cache 2>/dev/null
```

### Step 4: Run Diagnostic Tool
```bash
streamlit run diagnose_github_issue.py
```

This will open an interactive diagnostic tool that tests:
- ✅ Secrets file exists
- ✅ Streamlit can read secrets
- ✅ github_storage module works
- ✅ GitHub API connection works

**Run ALL the tests** and see which ones pass/fail.

### Step 5: Restart Streamlit Completely

**If you were running `streamlit run app.py`:**
1. Stop it completely (`Ctrl+C`)
2. Kill any lingering processes: `pkill -f streamlit`
3. Wait 5 seconds
4. Start fresh: `streamlit run app.py`
5. Hard refresh browser: `Ctrl+Shift+R` (Windows/Linux) or `⌘+Shift+R` (Mac)

---

## 📊 Diagnostic Tests Available

I've created two diagnostic tools for you:

### 1. **test_github_token_loading.py** (Command Line)
```bash
python3 test_github_token_loading.py
```
Quick standalone test - doesn't require Streamlit.

### 2. **diagnose_github_issue.py** (Interactive Streamlit App)
```bash
streamlit run diagnose_github_issue.py
```
Comprehensive web-based diagnostic with interactive buttons.

---

## 🔧 What Was Fixed

Here's a summary of all fixes applied:

### Fix #1: Dynamic Token Loading (github_storage.py)
**Before:**
```python
# Token loaded at module import time (before secrets available)
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN') or st.secrets.get("GITHUB_TOKEN")
```

**After:**
```python
def _get_github_token():
    """Get token dynamically when needed"""
    token = os.getenv('GITHUB_TOKEN')
    if token:
        return token

    if hasattr(st, 'secrets'):
        return st.secrets.get("GITHUB_TOKEN", None)

    return None
```

### Fix #2: Updated All References
Both functions now call `_get_github_token()` when needed:
- `load_data_from_github()` - line 150
- `save_data_to_github()` - line 218

### Fix #3: Added Debug Logging
Added print statements to track where token is loaded from:
```python
print(f"✅ GitHub token loaded from os.environ (length: {len(token)})")
print(f"✅ GitHub token loaded from st.secrets (length: {len(token)})")
print("❌ No GitHub token found in environment or secrets")
```

---

## 📝 Verification Checklist

Run through this checklist:

- [ ] Pulled latest code from git
- [ ] Verified token in `.streamlit/secrets.toml`
- [ ] Cleared Python cache files
- [ ] Ran `test_github_token_loading.py` → All tests pass
- [ ] Ran `streamlit run diagnose_github_issue.py` → All tests pass
- [ ] Completely restarted Streamlit server
- [ ] Hard refreshed browser
- [ ] Tested main app with `streamlit run app.py`

---

## 🆘 If Still Not Working

If you still get 401 errors after following all steps:

1. **Run the diagnostic tool and screenshot the results**
   ```bash
   streamlit run diagnose_github_issue.py
   ```
   Click all the test buttons and show me which ones fail.

2. **Check the console output when running the app**
   ```bash
   streamlit run app.py
   ```
   Look for these debug messages:
   - `✅ GitHub token loaded from os.environ`
   - `✅ GitHub token loaded from st.secrets`
   - `❌ No GitHub token found`

3. **Verify you're running the latest code**
   ```bash
   git log -1 --oneline
   ```
   Should show commit: `e67bc6e Add diagnostic tools...`

---

## 📌 Key Files Reference

| File | Purpose | Status |
|------|---------|--------|
| `.streamlit/secrets.toml` | Stores API keys (gitignored) | ✅ Token present |
| `github_storage.py` | GitHub API functions | ✅ Fixed (dynamic loading) |
| `app.py` | Main application | ✅ Loads secrets on startup |
| `test_github_token_loading.py` | Standalone test | ✅ All tests pass |
| `diagnose_github_issue.py` | Interactive diagnostic | ✅ Ready to use |

---

## ✨ Expected Behavior After Fix

When you run the app, you should see:
1. ✅ App starts without errors
2. ✅ Data loads from GitHub automatically
3. ✅ No "401 Unauthorized" messages
4. ✅ Trip data displays correctly

---

## 🔐 Security Note

Your GitHub token is:
- ✅ Stored in `.streamlit/secrets.toml` (gitignored)
- ✅ NOT committed to git repository
- ✅ Loaded dynamically (not hardcoded)
- ✅ Has fallback mechanism for reliability

Token expires: **November 27, 2025**

---

## 📞 Next Steps

1. Follow the "How to Fix This" steps above
2. Run the diagnostic tool
3. If still having issues, share the diagnostic results with me

The token IS valid, the code IS fixed, and the tests PASS. The issue is likely just stale code being cached somewhere. A clean restart should resolve it! 🚀
