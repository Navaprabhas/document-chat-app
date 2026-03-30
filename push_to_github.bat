@echo off
echo ========================================
echo   Push to GitHub - Document Chat App
echo ========================================
echo.

echo Step 1: Create repository on GitHub
echo Go to: https://github.com/new
echo.
echo Repository name: document-chat-app
echo Description: AI-powered document chat using Google Gemini
echo Visibility: Public
echo DO NOT check "Initialize with README"
echo.
pause

echo.
echo Step 2: Adding remote and pushing...
echo.

git remote add origin https://github.com/Navaprabhas/document-chat-app.git
git push -u origin main

echo.
echo ========================================
echo   Push Complete!
echo ========================================
echo.
echo Next: Deploy on Streamlit Cloud
echo Go to: https://share.streamlit.io
echo.
echo See DEPLOY_NOW.md for detailed instructions
echo.
pause
