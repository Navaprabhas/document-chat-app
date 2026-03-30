#!/bin/bash

echo "============================================================"
echo "Starting Document Chat Application"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found"
    echo "Please run ./install.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found"
    echo "Creating from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please edit .env and add your API keys"
    echo "Then run this script again"
    exit 1
fi

# Run the application
echo "Starting Streamlit application..."
echo ""
echo "The application will open in your browser at:"
echo "http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run app.py
