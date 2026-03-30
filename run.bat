@echo off
echo ============================================================
echo Starting Document Chat Application
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found
    echo Please run install.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist .env (
    echo WARNING: .env file not found
    echo Creating from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env and add your API keys
    echo Then run this script again
    pause
    exit /b 1
)

REM Run the application
echo Starting Streamlit application...
echo.
echo The application will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

streamlit run app.py

pause
