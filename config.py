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
THEMES = {
    "workload": [
        "overwhelming", "unsustainable", "long hours", "exhausted",
        "pressure", "unmanageable", "stress", "burnout", "capacity",
        "demanding", "relentless", "backlog", "targets", "ratio"
    ],
    
    "staffing": [
        "understaffed", "shortages", "recruitment", "retention",
        "agency staff", "bank shifts", "rota gaps", "sickness absence",
        "vacancies", "skill mix", "skill drain", "agency rates"
    ],
    
    "management": [
        "supportive", "unresponsive", "micromanagement",
        "leadership", "transparency", "consultation", "trust",
        "favouritism", "nepotism", "autocratic", "bureaucracy"
    ],
    
    "facilities": [
        "outdated equipment", "leaking roof", "asbestos",
        "infrastructure", "ventilation", "heating", "lighting",
        "infection control", "ward space", "privacy", "crowding"
    ],
    
    "career_development": [
        "band progression", "dead-end job", "promotion", "apprenticeship",
        "career stagnation", "training budget", "qualifications",
        "skill recognition", "pay scales", "agenda for change", "CEPD"
    ],
    
    "compensation": [
        "cost of living", "salary freeze", "pay disparity", "London weighting",
        "bank rates", "overtime pay", "pension deductions", "food banks",
        "financial stress", "living wage", "tax burden", "overtime ban"
    ],
    
    "work_environment": [
        "bullying culture", "racial discrimination", "harassment",
        "fear of speaking up", "toxic atmosphere", "cliques", "ostracized",
        "discrimination", "racism", "BAME", "ethnic minority", "equity"
    ],
    
    "patient_care_impact": [
        "corridor nursing", "missed observations", "medication errors",
        "delayed discharges", "waiting lists", "cancelled clinics",
        "safety incidents", "near misses", "DATIX", "patient harm",
        "breaches", "12hr waits"
    ],
    
    "flexibility_worklife": [
        "childcare conflicts", "school run", "elder care", "shift patterns",
        "work-life balance", "remote work", "agile working", "WFH",
        "compressed hours", "part-time options", "job share"
    ],
    
    "safety": [
        "dangerous", "unsafe", "hazard", "incident", "injury",
        "accident", "protection", "protective equipment", "risk assessment",
        "compliance", "protocol breach", "corners cut"
    ]
}

# Define exclusion patterns for better accuracy
EXCLUSION_PATTERNS = {
    "workload": ["workload is manageable", "workload is reasonable"],
    "management": ["i am in management", "as a manager"],
    "staffing": ["staffing improved", "well staffed"],
}

# Default column names for input data
DEFAULT_DEPARTMENT_COL = "department"
DEFAULT_COMMENT_COL = "free-text comments" 