#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Client for Staff Feedback Analysis Tool
"""

import requests
import streamlit as st # Keep for error reporting if needed, but prefer logging
import traceback
import json
from typing import List, Dict, Optional, Any # Import typing

# Define API endpoint (centralized here)
API_URL = "http://localhost:8000"  # Ensure this matches your FastAPI server URL

# --- Helper Function for Error Handling ---
def _handle_api_error(response: requests.Response, context: str):
    """Logs API errors and optionally shows them in Streamlit."""
    error_msg = f"API Error ({context}): Status {response.status_code}"
    try:
        details = response.json().get("detail", response.text)
        error_msg += f" - {details}"
    except json.JSONDecodeError:
        error_msg += f" - {response.text[:200]}..." # Show partial text if not JSON
    print(error_msg) # Log to console
    # st.error(error_msg) # Optionally display in Streamlit UI
    return None # Indicate error by returning None or empty structure

# --- API Client Functions ---

def check_api_connection() -> bool:
    """Check if the API server is reachable."""
    try:
        response = requests.get(f"{API_URL}/", timeout=5) # Add timeout
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"API connection error: {str(e)}")
        return False

def upload_file(file) -> Optional[Dict[str, Any]]:
    """Upload a feedback file (CSV/XLSX) to the API for processing."""
    print(f"[api_client] Attempting to upload file: {file.name}") # DEBUG
    try:
        files = {"file": (file.name, file, file.type)}
        # Increase timeout significantly for large file processing
        response = requests.post(f"{API_URL}/upload", files=files, timeout=300) # Increased timeout to 300 seconds

        print(f"[api_client] API Response Status Code: {response.status_code}") # DEBUG
        if response.status_code == 200:
            print("[api_client] File upload successful (Status 200)") # DEBUG
            return response.json()
        else:
            print("[api_client] File upload failed (Non-200 Status). Handling error.") # DEBUG
            return _handle_api_error(response, "File Upload")
    except requests.exceptions.Timeout as e_timeout: # Capture the specific exception
        error_msg = f"[api_client] Timeout error during file upload (120s): {str(e_timeout)}" # Use the captured variable
        print(error_msg)
        return {"status": "error", "detail": "API request timed out during processing. The file might be too large or processing is taking too long."}
    except requests.exceptions.RequestException as e_req: # Capture the specific exception
        error_msg = f"[api_client] RequestException during file upload: {str(e_req)}"
        print(error_msg)
        return {"status": "error", "detail": f"Network error connecting to API: {str(e_req)}"}
    except Exception as e_generic: # Capture any other exception
        error_msg = f"[api_client] Unexpected error during file upload function: {str(e_generic)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return {"status": "error", "detail": f"Client-side error during upload: {str(e_generic)}"}

# Renamed from get_all_risks
def get_all_department_analysis() -> List[Dict[str, Any]]:
    """Fetch analysis summaries for all departments."""
    try:
        response = requests.get(f"{API_URL}/analysis/departments", timeout=30)
        if response.status_code == 200:
            data = response.json()
            # Expecting List[DepartmentAnalysis]
            return data if isinstance(data, list) else []
        elif response.status_code == 404:
             print("No department analysis data found (404). Returning empty list.")
             return []
        else:
            _handle_api_error(response, "Get All Department Analysis")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching all department analysis: {str(e)}\n{traceback.format_exc()}")
        return []

# Renamed from get_department_risk
def get_department_analysis(department_name: str) -> Optional[Dict[str, Any]]:
    """Fetch analysis summary for a specific department."""
    try:
        response = requests.get(f"{API_URL}/analysis/department/{department_name}", timeout=15)
        if response.status_code == 200:
            # Expecting DepartmentAnalysis model content
            return response.json()
        else:
            # Handles 404 Not Found as well
            return _handle_api_error(response, f"Get Department Analysis ({department_name})")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching analysis for department {department_name}: {str(e)}")
        return None

# New function
def get_overall_analysis() -> Optional[Dict[str, Any]]:
    """Fetch the overall analysis summary for the entire dataset."""
    try:
        response = requests.get(f"{API_URL}/analysis/overall", timeout=30)
        if response.status_code == 200:
            # Expecting OverallAnalysis model content
            return response.json()
        else:
            return _handle_api_error(response, "Get Overall Analysis")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching overall analysis: {str(e)}")
        return None


def get_departments() -> List[str]:
    """Fetch the list of unique department names."""
    try:
        response = requests.get(f"{API_URL}/departments", timeout=10)
        if response.status_code == 200:
            # Expecting {"departments": ["Dept A", "Dept B"]}
            return response.json().get("departments", [])
        else:
            _handle_api_error(response, "Get Departments")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching departments: {str(e)}")
        return []

# Renamed from get_themes_summary
def get_detailed_themes(department: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Fetch detailed theme/subtheme info, optionally filtered by department."""
    try:
        params = {}
        if department:
            params["department"] = department

        response = requests.get(f"{API_URL}/themes/detailed", params=params, timeout=20)
        if response.status_code == 200:
            # Expecting ThemeSummary model content: {"themes": {...}, "subthemes": {...}}
            return response.json()
        else:
            return _handle_api_error(response, f"Get Detailed Themes (Dept: {department})")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching detailed themes: {str(e)}")
        return None

def get_data_summary() -> Optional[Dict[str, Any]]:
    """Fetch high-level summary statistics of the loaded data."""
    try:
        response = requests.get(f"{API_URL}/data/summary", timeout=15)
        if response.status_code == 200:
            # Expecting DataSummary model content
            return response.json()
        else:
            # Handles 404 if data not loaded
            return _handle_api_error(response, "Get Data Summary")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data summary: {str(e)}")
        return None

def get_sample_comments(department: Optional[str] = None,
                        theme: Optional[str] = None,
                        subtheme: Optional[str] = None,
                        sentiment: Optional[str] = None,
                        limit: int = 10) -> List[Dict[str, Any]]:
    """Fetch sample comments with multiple filtering options."""
    try:
        params = {"limit": limit}
        if department: params["department"] = department
        if theme: params["theme"] = theme
        if subtheme: params["subtheme"] = subtheme
        if sentiment: params["sentiment"] = sentiment

        response = requests.get(f"{API_URL}/comments/sample", params=params, timeout=20)
        if response.status_code == 200:
            # Expecting CommentSampleResponse: {"samples": [...], "total_matching": ...}
            return response.json().get("samples", [])
        else:
            _handle_api_error(response, "Get Sample Comments")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching comments: {str(e)}")
        return []