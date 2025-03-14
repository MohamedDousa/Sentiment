#!/usr/bin/env python
"""
Run script for the Employee Feedback Analysis Tool
This script starts both the API server and the Streamlit dashboard
"""

import os
import subprocess
import time
import webbrowser
import threading
import sys

def check_server_ready(url, retries=10, delay=2):
    """Check if a server is ready by sending requests to the given URL."""
    import requests
    print(f"Checking if server is ready at {url}...")
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"Server at {url} is ready!")
                return True
        except requests.exceptions.RequestException as e:
            error_type = type(e).__name__
            if attempt < retries - 1:  # Don't print "retrying" on the last attempt
                print(f"Attempt {attempt+1}/{retries} failed ({error_type}). Retrying in {delay} seconds...")
            else:
                print(f"Final attempt {retries}/{retries} failed ({error_type}).")
        time.sleep(delay)
    print(f"Server at {url} is not responding after {retries} attempts.")
    return False

def start_api_server():
    """Start the FastAPI server"""
    print("Starting API server...")
    api_process = subprocess.Popen([sys.executable, "-m", "uvicorn", "api:app", "--reload"])
    if check_server_ready("http://localhost:8000"):  # Check server readiness
        print("API server running at http://localhost:8000")
        return api_process
    else:
        print("Error: API server failed to start.")
        return None

def start_dashboard():
    """Start the Streamlit dashboard"""
    print("Starting Streamlit dashboard...")
    dashboard_process = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    if check_server_ready("http://localhost:8501"):
        print("Dashboard running at http://localhost:8501")
        return dashboard_process
    else:
        print("Error: Dashboard failed to start.")
        return None

def open_browser():
    """Open web browser to the dashboard"""
    webbrowser.open("http://localhost:8501")

def main():
    """Main function to run the complete application"""
    # Create temp directory if it doesn't exist
    os.makedirs("temp", exist_ok=True)

    api_process = None
    dashboard_process = None

    try:
        # Start API server
        api_process = start_api_server()
        if not api_process:
            return

        # Start dashboard
        dashboard_process = start_dashboard()
        if not dashboard_process:
            return

        # Open browser
        time.sleep(2)  # Small delay to ensure the dashboard is fully loaded
        open_browser()

        # Keep the main thread alive until interrupted
        print("\nServers are running. Press Ctrl+C to shut down...")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
    finally:
        # Cleanup processes
        if api_process:
            print("Terminating API server...")
            api_process.terminate()
            try:
                api_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                api_process.kill()

        if dashboard_process:
            print("Terminating dashboard...")
            dashboard_process.terminate()
            try:
                dashboard_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                dashboard_process.kill()

        print("Shutdown complete.")

if __name__ == "__main__":
    main() 