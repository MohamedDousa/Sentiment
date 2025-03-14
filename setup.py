#!/usr/bin/env python
# Setup script for installing required models

import subprocess
import sys

def main():
    print("Setting up the Employee Feedback Analysis Tool...")
    
    # Install dependencies if needed
    print("\nInstalling dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Install spaCy model
    print("\nDownloading spaCy English language model...")
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    
    print("\nSetup complete! You can now run the application.")
    print("1. Start API server: uvicorn api:app --reload")
    print("2. Start dashboard: streamlit run dashboard.py")

if __name__ == "__main__":
    main() 