@echo off
echo ============================================================
echo Document Chat Application - Windows Installation
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)

echo [1/5] Python found
python --version
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    echo Virtual environment created
)
echo.

REM Activate virtual environment and install dependencies
echo [3/5] Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Setup environment file
echo [4/5] Setting up environment file...
if exist .env (
    echo .env file already exists
) else (
    copy .env.example .env
    echo .env file created - PLEASE EDIT IT WITH YOUR API KEYS
)
echo.

REM Run setup script
echo [5/5] Running setup validation...
python setup.py
echo.

echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Run: run.bat
echo.
echo Or manually:
echo 1. Activate environment: venv\Scripts\activate.bat
echo 2. Run application: streamlit run app.py
echo.
pause
