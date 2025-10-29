# GitHub Authentication Troubleshooting Guide

## Error: "Could not load data from GitHub (status 401)"

This means your GitHub token is being rejected by the API. Here's how to fix it:

## Step 1: Check Token Type

GitHub now has TWO types of tokens:

### Classic Personal Access Token (starts with `ghp_`)
- ✅ Works with simple scope selection
- ✅ Easy to set up
- ⚠️ Has broad access to all repos you have access to

### Fine-Grained Personal Access Token (starts with `github_pat_`)
- ✅ More secure, granular permissions
- ❌ Requires specific repository selection
- ❌ More complex to configure

**Most likely issue: You're using a fine-grained token without proper repository permissions!**

## Step 2: Token Requirements

### For Classic Tokens:
Your token needs the **`repo`** scope (for private repos) or **`public_repo`** (for public repos).

### For Fine-Grained Tokens:
1. **Repository access**: Must select `WanderingWithPride/40thBdayAppRebuild` specifically
2. **Repository permissions**:
   - Contents: **Read and write** access
   - Metadata: **Read** access (usually automatic)

## Step 3: Create/Update Your Token

### Option A: Classic Token (Recommended - Easier)

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: `40thBdayApp - Streamlit Cloud`
4. Set expiration (recommend 90 days or No expiration for testing)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories) - this includes Contents access
6. Click "Generate token"
7. **COPY THE TOKEN IMMEDIATELY** (you can't see it again!)

### Option B: Fine-Grained Token (More Secure)

1. Go to https://github.com/settings/tokens?type=beta
2. Click "Generate new token"
3. Give it a name: `40thBdayApp - Streamlit Cloud`
4. Set expiration (recommend 90 days)
5. **Repository access**: Select "Only select repositories"
   - Choose: `WanderingWithPride/40thBdayAppRebuild`
6. **Repository permissions**:
   - Contents: **Read and write**
   - Metadata: **Read-only** (automatic)
7. Click "Generate token"
8. **COPY THE TOKEN IMMEDIATELY**

## Step 4: Add Token to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Find your app: `40thBdayAppRebuild`
3. Click the ⚙️ Settings button
4. Click "Secrets" in the left sidebar
5. Add/update:
   ```toml
   GITHUB_TOKEN = "your_token_here"
   ```
6. Click "Save"
7. Your app will automatically restart

## Step 5: Verify

After updating your token and restarting the app, check the Streamlit Cloud logs:

Look for these messages:
- ✅ `✅ GitHub token loaded from st.secrets`
- ✅ `🔍 Attempting to load from GitHub with token prefix: ghp_xxx...` or `github_pat_...`
- ✅ `🔍 Response status: 200`

If you still see:
- ❌ `🔍 Response status: 401`
- ❌ `❌ GitHub authentication failed (401)`

Then the token still doesn't have the right permissions.

## Common Issues

### "Token was working before"
- **Token expired**: Check expiration date
- **Token was regenerated**: Old token is now invalid
- **Repository was renamed**: Fine-grained tokens won't work if repo path changed
- **GitHub changed token format**: Unlikely but possible

### "I regenerated the token but it still doesn't work"
- Make sure you **saved the NEW token** in Streamlit Cloud secrets
- Make sure there are **no extra spaces** before/after the token
- Make sure the token includes the **full string** (usually 40-93 characters)
- **Restart the Streamlit app** after updating secrets

### "Token works in test_apis_live.py but not in the app"
- The token might not be properly set in Streamlit Cloud secrets
- The token might be set as an environment variable locally but not in the cloud

## Debug Commands

### Local Testing (if you have the token as an environment variable):
```bash
export GITHUB_TOKEN="your_token_here"
python test_apis_live.py
```

### Test with curl:
```bash
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/WanderingWithPride/40thBdayAppRebuild/contents/data/trip_data.json
```

If this returns data, your token works. If it returns 401, the token doesn't have permission.

## Still Not Working?

1. **Delete the old token** on GitHub (to avoid confusion)
2. **Create a brand new Classic token** with `repo` scope
3. **Update Streamlit Cloud secrets** with the new token
4. **Restart your app** (Settings → Reboot)
5. **Check the logs** in Streamlit Cloud

---

## Technical Details

Both `Authorization: token XXX` and `Authorization: Bearer XXX` formats work with GitHub's API.
The code now uses `token` format which is the traditional GitHub format and is still fully supported.
