# 🚀 Deploy to Streamlit Cloud

Complete guide to deploy your Document Chat Application to Streamlit Cloud.

## 📋 Prerequisites

- GitHub account
- Google AI API key (from https://makersuite.google.com/app/apikey)
- Streamlit Cloud account (free at https://share.streamlit.io)

## 🔧 Step 1: Push to GitHub

### Option A: Using Git Commands

```bash
cd document-chat-app

# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Document Chat Application with Google Gemini"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/Navaprabhas/document-chat-app.git

# Push to GitHub
git push -u origin main
```

### Option B: Using GitHub Desktop

1. Open GitHub Desktop
2. Click "Add" → "Add Existing Repository"
3. Select the `document-chat-app` folder
4. Click "Publish repository"
5. Name it: `document-chat-app`
6. Click "Publish Repository"

## 🌐 Step 2: Deploy on Streamlit Cloud

### 2.1 Sign Up / Sign In

1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Authorize Streamlit to access your repositories

### 2.2 Create New App

1. Click **"New app"** button
2. Fill in the details:
   - **Repository**: `Navaprabhas/document-chat-app`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom URL (e.g., `document-chat-navaprabhas`)

### 2.3 Configure Secrets (Optional)

**For Public Deployment (Recommended):**
Skip this step! Don't add any secrets. Users will enter their own API keys when they use the app.

**For Private/Personal Use Only:**
If you want to use your own API key without entering it each time, click "Advanced settings" and add your API key to secrets.

### 2.4 Deploy

1. Click **"Deploy!"**
2. Wait 2-3 minutes for deployment
3. Your app will be live at: `https://document-chat-navaprabhas.streamlit.app`

## ✅ Verify Deployment

Once deployed, test your app:

1. ✅ Enter your Google Gemini API key
2. ✅ Upload a PDF document
3. ✅ Click "Process Documents"
4. ✅ Ask a question
5. ✅ Verify response with citations
6. ✅ Check "View Sources" works

## 🔒 Security Best Practices

### For Public Deployment:

1. **Don't add API keys to Streamlit Secrets** - Let users enter their own
2. **Users enter their own API keys** - Keys are stored only in browser session
3. **No billing concerns** - Each user uses their own Google AI quota
4. **Privacy** - API keys never leave the user's browser session

```python
# In app.py, add at the top
import streamlit as st
from datetime import datetime, timedelta

# Simple rate limiting
if 'last_query_time' not in st.session_state:
    st.session_state.last_query_time = datetime.now()

# Check if user is querying too fast
time_since_last = datetime.now() - st.session_state.last_query_time
if time_since_last < timedelta(seconds=2):
    st.warning("Please wait a moment before asking another question.")
    st.stop()
```

## 🎨 Customize Your Deployment

### Update App Title

In `app.py`, change:
```python
st.set_page_config(
    page_title="Your Custom Title",
    page_icon="📚",
)
```

### Add Custom Domain (Optional)

1. Go to Streamlit Cloud dashboard
2. Click on your app
3. Go to "Settings" → "General"
4. Add your custom domain

## 📊 Monitor Your App

### View Logs

1. Go to Streamlit Cloud dashboard
2. Click on your app
3. Click "Manage app" → "Logs"
4. Monitor real-time logs

### Check Usage

1. Monitor Google AI API usage at: https://console.cloud.google.com
2. Set up billing alerts
3. Monitor Streamlit resource usage

## 🔄 Update Your App

### Method 1: Push to GitHub

```bash
# Make changes to your code
git add .
git commit -m "Update: description of changes"
git push

# Streamlit Cloud will auto-deploy in ~2 minutes
```

### Method 2: Reboot from Dashboard

1. Go to Streamlit Cloud dashboard
2. Click "⋮" menu on your app
3. Click "Reboot app"

## 🐛 Troubleshooting

### App Won't Start

**Check:**
1. Logs in Streamlit Cloud dashboard
2. All secrets are configured correctly
3. `requirements.txt` has all dependencies

### API Key Errors

**Solution:**
1. Verify secrets in Streamlit Cloud
2. Check API key is valid at https://makersuite.google.com
3. Ensure no extra spaces in secrets

### Memory Issues

**Solution:**
1. Reduce `CHUNK_SIZE` in secrets
2. Limit file upload size
3. Clear vector store periodically

### Slow Performance

**Solution:**
1. Use `models/gemini-2.5-flash` (fastest)
2. Reduce `TOP_K` to 3-5
3. Optimize chunk size

## 💰 Cost Estimation

### Google AI API (Gemini)

- **Gemini 2.5 Flash**: Very low cost
- **Embeddings**: ~$0.0001 per 1000 tokens
- **Typical usage**: $0.01-0.10 per day for moderate use

### Streamlit Cloud

- **Free tier**: 1 app, unlimited viewers
- **Paid tier**: $20/month for more apps

## 🎯 Production Checklist

Before going live:

- [ ] API keys in Streamlit Secrets (not in code)
- [ ] `.env` file not committed to GitHub
- [ ] Test with multiple PDFs
- [ ] Test error handling
- [ ] Add usage instructions in README
- [ ] Set up monitoring
- [ ] Configure billing alerts
- [ ] Test on mobile devices
- [ ] Add analytics (optional)

## 📱 Share Your App

Once deployed, share your app:

```
🚀 Check out my Document Chat App!
📚 Upload PDFs and chat with them using AI
🔗 https://document-chat-navaprabhas.streamlit.app
```

## 🔗 Useful Links

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Cloud**: https://share.streamlit.io
- **Google AI Studio**: https://makersuite.google.com
- **GitHub Repo**: https://github.com/Navaprabhas/document-chat-app

## 🎉 You're Live!

Your Document Chat Application is now deployed and accessible worldwide!

**App URL**: `https://document-chat-navaprabhas.streamlit.app`

---

**Need help?** Check the logs in Streamlit Cloud dashboard or review the troubleshooting section above.
