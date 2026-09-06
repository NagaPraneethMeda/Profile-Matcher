# Streamlit Cloud Deployment Guide

## ✅ What Was Fixed

I've fixed the deployment errors by:
1. **Pinned dependency versions** in `requirements.txt` - cloud environments need specific versions
2. **Added error handling** for import errors in `app.py`
3. **Updated `.streamlit/config.toml`** for cloud optimization
4. **Added `.streamlit/secrets.toml`** for environment configuration
5. **Created `setup.sh`** for custom setup on cloud

## 🚀 Deploy to Streamlit Cloud (Recommended)

### Step 1: Verify GitHub Repository
Your app is already in: `https://github.com/NagaPraneethMeda/Profile-Matcher`

### Step 2: Go to Streamlit Cloud
1. Open https://streamlit.io/cloud
2. Click "**New app**"
3. Sign in with GitHub (if not already)

### Step 3: Configure Your Deployment
- **Repository**: `NagaPraneethMeda/Profile-Matcher`
- **Branch**: `master`
- **Main file path**: `app.py`

### Step 4: Deploy
Click "**Deploy**"

That's it! Streamlit Cloud will:
- ✓ Install dependencies from `requirements.txt`
- ✓ Run your `app.py`
- ✓ Host it at: `https://<your-app-name>.streamlit.app`

## 📋 Pre-Deployment Checklist

- ✅ `requirements.txt` has pinned versions
- ✅ `app.py` has error handling for imports
- ✅ `.streamlit/config.toml` exists
- ✅ Code pushed to GitHub (`master` branch)
- ✅ No `__pycache__` or `.env` files committed

## 🛠 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pypdf'"
**Solution**: Already fixed! Requirements now specify exact versions.

### Error: "No module named 'docx'"
**Solution**: Already fixed! Using `python-docx>=0.8.11` in requirements.

### Error: "Streamlit version conflict"
**Solution**: Clear cache and redeploy:
- In Streamlit Cloud settings → Clear Cache → Reboot App

### App runs locally but fails on cloud
**Solution**: Check logs:
- Streamlit Cloud → Click your app → View logs (terminal icon)
- Look for error messages about missing packages

## 🔄 Auto-Deployment

Once deployed:
- Every push to `master` branch = automatic redeploy
- Changes appear live within 2-3 minutes
- No need to manually deploy again

## 📊 App URL Structure
```
https://<username>-<repo-name>-<random-id>.streamlit.app
```

For your app:
```
https://nagapraneethmeda-profile-matcher-<id>.streamlit.app
```

## 🆘 Getting Help

If issues persist:

1. **Check Streamlit Cloud Logs**
   - Open your app in Streamlit Cloud
   - Click terminal icon to view deployment logs

2. **Local Testing**
   ```bash
   streamlit run app.py
   ```
   If works locally but not on cloud → dependency issue

3. **Common Fixes**
   ```bash
   # Clear Python cache
   find . -type d -name __pycache__ -exec rm -r {} +
   
   # Reinstall packages
   pip install -r requirements.txt --upgrade
   ```

4. **Streamlit Documentation**
   - https://docs.streamlit.io/deploy/streamlit-cloud

## 📝 Current Files Optimized for Cloud

```
✅ app.py                    # With error handling
✅ requirements.txt          # Pinned versions
✅ .streamlit/config.toml    # Cloud optimized
✅ .streamlit/secrets.toml   # Environment config
✅ setup.sh                  # Setup script
```

## 🎯 Next Steps

1. Go to https://streamlit.io/cloud
2. Click "**New app**"
3. Select `NagaPraneethMeda/Profile-Matcher` repo
4. Select `master` branch
5. Enter `app.py` as main file
6. Click "**Deploy**"

**Done! Your app will be live in 2-3 minutes** 🎉
