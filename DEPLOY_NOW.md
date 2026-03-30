# 🚀 Quick Deploy Guide

Your app is ready to deploy! Follow these simple steps.

## ✅ What's Already Done

- ✅ Git repository initialized
- ✅ All files committed (24 files)
- ✅ API key removed from code (secure)
- ✅ `.gitignore` configured properly
- ✅ Branch set to `main`

## 📤 Step 1: Create GitHub Repository & Push

### Option A: Using GitHub Website (Recommended)

1. Go to https://github.com/new
2. Fill in:
   - **Repository name**: `document-chat-app`
   - **Description**: `AI-powered document chat application using Google Gemini and RAG`
   - **Visibility**: Public (or Private if you prefer)
   - ⚠️ **DO NOT** check "Initialize with README" (we already have files)
3. Click **"Create repository"**
4. Copy the repository URL (should be: `https://github.com/Navaprabhas/document-chat-app.git`)

5. In your terminal (in the `document-chat-app` folder), run:

```bash
git remote add origin https://github.com/Navaprabhas/document-chat-app.git
git push -u origin main
```

### Option B: Using GitHub CLI (if installed)

```bash
gh repo create document-chat-app --public --source=. --remote=origin --push
```

## 🌐 Step 2: Deploy on Streamlit Cloud

### 2.1 Sign In

1. Go to https://share.streamlit.io
2. Click **"Sign in with GitHub"**
3. Authorize Streamlit

### 2.2 Deploy App

1. Click **"New app"** (big button)
2. Fill in:
   - **Repository**: `Navaprabhas/document-chat-app`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: Choose a name (e.g., `document-chat-navaprabhas`)

3. Click **"Advanced settings"**

4. In **"Secrets"** section, paste this EXACTLY:

```toml
GOOGLE_API_KEY = "AIzaSyDP_6xWSlaBM4z6B6rdfkVYhVJKgECDBFQ"
LLM_PROVIDER = "google"
GOOGLE_MODEL = "models/gemini-2.5-flash"
GOOGLE_EMBEDDING_MODEL = "models/gemini-embedding-2-preview"
EMBEDDING_MODEL = "google"
CHUNK_SIZE = "1000"
CHUNK_OVERLAP = "200"
TOP_K = "5"
TEMPERATURE = "0.7"
MAX_TOKENS = "2000"
MAX_HISTORY_MESSAGES = "10"
```

5. Click **"Save"**
6. Click **"Deploy!"**

### 2.3 Wait for Deployment

- Takes 2-3 minutes
- Watch the logs for any errors
- Once done, your app will be live!

## 🎉 Your App URL

After deployment, your app will be at:

```
https://document-chat-navaprabhas.streamlit.app
```

(Or whatever custom URL you chose)

## ✅ Test Your Deployed App

1. Upload a PDF
2. Click "Process Documents"
3. Ask a question
4. Verify you get an answer with citations
5. Check "View Sources" expander

## 🔄 Update Your App Later

Whenever you make changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

Streamlit will auto-deploy in ~2 minutes!

## 🐛 If Something Goes Wrong

### Can't push to GitHub?

```bash
# Check if remote is set
git remote -v

# If not set, add it
git remote add origin https://github.com/Navaprabhas/document-chat-app.git

# Try pushing again
git push -u origin main
```

### Streamlit deployment fails?

1. Check logs in Streamlit dashboard
2. Verify all secrets are configured
3. Make sure API key is valid
4. Check `requirements.txt` is correct

### API errors in deployed app?

1. Go to Streamlit dashboard
2. Click your app → Settings → Secrets
3. Verify `GOOGLE_API_KEY` is correct
4. No extra spaces or quotes issues

## 📞 Need Help?

- Check `STREAMLIT_DEPLOY.md` for detailed guide
- Check `TROUBLESHOOTING.md` for common issues
- View logs in Streamlit Cloud dashboard

## 🎯 Quick Commands Reference

```bash
# Check git status
git status

# View commit history
git log --oneline

# Check remote
git remote -v

# Force push (if needed)
git push -f origin main
```

---

**Ready to deploy?** Start with Step 1 above! 🚀
