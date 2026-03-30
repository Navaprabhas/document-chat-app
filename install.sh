#!/bin/bash

echo "============================================================"
echo "Document Chat Application - Installation"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

echo "[1/5] Python found"
python3 --version
echo ""

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists"
else
    python3 -m venv venv
    echo "Virtual environment created"
fi
echo ""

# Activate virtual environment and install dependencies
echo "[3/5] Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo ""

# Setup environment file
echo "[4/5] Setting up environment file..."
if [ -f ".env" ]; then
    echo ".env file already exists"
else
    cp .env.example .env
    echo ".env file created - PLEASE EDIT IT WITH YOUR API KEYS"
fi
echo ""

# Run setup script
echo "[5/5] Running setup validation..."
python setup.py
echo ""

echo "============================================================"
echo "Installation Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Run: ./run.sh"
echo ""
echo "Or manually:"
echo "1. Activate environment: source venv/bin/activate"
echo "2. Run application: streamlit run app.py"
echo ""
