#!/bin/bash
# Start script for Employee Feedback Analysis Tool

# Ensure we're in the project directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
else
    source venv/bin/activate
fi

# Start the application using main.py
echo "Starting Employee Feedback Analysis Tool..."
python main.py

# If the application was interrupted, make sure to clean up
echo "Application stopped. Exiting..." 