"""
Configuration settings for the Employee Feedback Analysis Tool
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# API settings
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_URL = f"http://{API_HOST}:{API_PORT}"

# Dashboard settings
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8501"))

# File storage settings
TEMP_DIR = os.path.join(BASE_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)  # Ensure temp directory exists

# Model settings
SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
RISK_THRESHOLD = 0.6  # Threshold for high-risk classification (0-1)
RISK_SCORE_MIN = 1.0  # Minimum risk score (1-5 scale)
RISK_SCORE_MAX = 5.0  # Maximum risk score (1-5 scale)

# Theme detection settings
# Dictionary with themes and associated keywords can be customized here
# NOTE: This dictionary is now defined within nlp_pipeline.py's __init__
# THEMES = { ... }

# Define exclusion patterns for better accuracy
# NOTE: This dictionary is now defined within nlp_pipeline.py's __init__
# EXCLUSION_PATTERNS = { ... }

# Default column names for input data
DEFAULT_DEPARTMENT_COL = "department"
DEFAULT_COMMENT_COL = "free-text comments"

# REMOVED: THEME_SOLUTIONS dictionary is removed as requested.
# THEME_SOLUTIONS = { ... } 