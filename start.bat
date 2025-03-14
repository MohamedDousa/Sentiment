@echo off
REM Start script for Employee Feedback Analysis Tool on Windows

REM Ensure we're in the project directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
) else (
    call venv\Scripts\activate
)

REM Start the application using main.py
echo Starting Employee Feedback Analysis Tool...
python main.py

REM If the application was interrupted, make sure to clean up
echo Application stopped. Exiting... 