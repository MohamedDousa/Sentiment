"""
Staff Feedback Analysis Dashboard - Streamlit Cloud Version

This standalone version is designed to be deployed on Streamlit Cloud.
It includes:
1. Direct data processing (without needing a separate API server)
2. All visualization components from the original dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import io
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import traceback
import sys

# Set page configuration
st.set_page_config(
    page_title="Feedback Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Handle import errors more gracefully
try:
    # Import local modules for processing
    from preprocessing import load_data, preprocess_data, group_by_department
    from nlp_pipeline import process_nlp_pipeline, NLPProcessor
    import_success = True
except ImportError as e:
    st.error(f"Error importing required modules: {str(e)}")
    st.error(f"Python version: {sys.version}")
    st.error(f"Sys path: {sys.path}")
    import_success = False
    st.stop()

# Initialize session state to store data
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'department_data' not in st.session_state:
    st.session_state.department_data = None
if 'themes_summary' not in st.session_state:
    st.session_state.themes_summary = {}
if 'data_summary' not in st.session_state:
    st.session_state.data_summary = {}
if 'last_updated' not in st.session_state:
    st.session_state.last_updated = None

# Sidebar for file upload and navigation
st.sidebar.title("Staff Feedback Analysis")

# File upload
st.sidebar.header("Data Upload")
uploaded_file = st.sidebar.file_uploader("Upload Staff Feedback Data", type=["csv", "xlsx", "xls"])

# Processing function for uploaded data
def process_uploaded_file(file):
    try:
        with st.spinner("Processing data... This may take a minute."):
            # Create temp directory if needed
            os.makedirs("temp", exist_ok=True)
            
            # Load data
            raw_data = load_data(file)
            
            if raw_data.empty:
                st.error("The uploaded file contains no valid data.")
                return False
                
            # Preprocess data
            processed_data = preprocess_data(raw_data)
            
            # Run NLP pipeline
            nlp_processor = NLPProcessor()
            processed_data = process_nlp_pipeline(processed_data, nlp_processor)
            
            # Group by department
            department_data = group_by_department(processed_data)
            
            # Store in session state
            st.session_state.processed_data = processed_data
            st.session_state.department_data = department_data
            st.session_state.data_loaded = True
            st.session_state.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Generate themes summary
            themes_summary = {}
            for column in processed_data.columns:
                if column.startswith('theme_') and column != 'theme_comment':
                    theme_name = column.replace('theme_', '')
                    if theme_name != 'comment':  # Skip the comment theme
                        count = processed_data[column].sum()
                        themes_summary[theme_name] = int(count)
            st.session_state.themes_summary = themes_summary
            
            # Generate data summary
            sentiment_distribution = {
                "positive": int(len(processed_data[processed_data['sentiment_score'] > 0.6])),
                "neutral": int(len(processed_data[(processed_data['sentiment_score'] >= 0.4) & (processed_data['sentiment_score'] <= 0.6)])),
                "negative": int(len(processed_data[processed_data['sentiment_score'] < 0.4]))
            }
            
            # Count departments with high risk (more negative comments)
            dept_risks = {}
            high_risk_count = 0
            
            for dept, data in department_data.items():
                negative_pct = len(data[data['sentiment_score'] < 0.4]) / len(data) if len(data) > 0 else 0
                risk_score = 1 + (negative_pct * 4)  # Scale to 1-5
                is_high_risk = risk_score > 3.5
                
                if is_high_risk:
                    high_risk_count += 1
                    
                dept_risks[dept] = {
                    "risk_score": risk_score,
                    "high_risk": is_high_risk
                }
            
            data_summary = {
                "total_comments": len(processed_data),
                "total_departments": len(department_data) if department_data else 0,
                "high_risk_departments": high_risk_count,
                "sentiment_distribution": sentiment_distribution,
                "last_updated": st.session_state.last_updated
            }
            
            st.session_state.data_summary = data_summary
            
            return True
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.error(f"Traceback: {traceback.format_exc()}")
        return False

# Process data button
if uploaded_file:
    if st.sidebar.button("Process Data"):
        success = process_uploaded_file(uploaded_file)
        if success:
            st.sidebar.success(f"✅ Processed {st.session_state.data_summary['total_comments']} comments across {st.session_state.data_summary['total_departments']} departments")
        else:
            st.sidebar.error("❌ Error processing file")

# Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Select a page",
    ["Home", "Department Details", "Comment Explorer", "Themes Analysis", "Insights & Solutions", "About"]
)

# Helper Functions
def get_sample_comments(department=None, theme=None, limit=5):
    """Get sample comments based on filters"""
    if not st.session_state.data_loaded:
        return []
        
    try:
        data = st.session_state.processed_data
        
        # Apply filters
        if department and department != "All":
            data = data[data['department'] == department]
            
        if theme and theme != "All":
            theme_col = f"theme_{theme}"
            if theme_col in data.columns:
                data = data[data[theme_col] == 1]
        
        # Get sample
        if len(data) > limit:
            samples = data.sample(limit)
        else:
            samples = data
            
        # Convert to dict format similar to API
        result = []
        for _, row in samples.iterrows():
            comment_dict = {
                "department": row.get('department', 'Unknown'),
                "free_text_comments": row.get('free_text_comments', ''),
                "sentiment_score": float(row.get('sentiment_score', 0.5))
            }
            
            # Add theme fields
            for col in row.index:
                if col.startswith('theme_'):
                    comment_dict[col] = int(row[col])
                    
            result.append(comment_dict)
            
        return result
    except Exception as e:
        st.error(f"Error getting sample comments: {str(e)}")
        return []

def get_department_risk(department):
    """Get risk information for a specific department"""
    if not st.session_state.data_loaded or not department:
        return None
        
    try:
        if department not in st.session_state.department_data:
            return None
            
        dept_data = st.session_state.department_data[department]
        
        # Calculate risk score based on sentiment
        negative_pct = len(dept_data[dept_data['sentiment_score'] < 0.4]) / len(dept_data) if len(dept_data) > 0 else 0
        risk_score = 1 + (negative_pct * 4)  # Scale to 1-5
        is_high_risk = risk_score > 3.5
        
        # Find top themes
        theme_counts = {}
        for col in dept_data.columns:
            if col.startswith('theme_') and col != 'theme_comment':
                theme_name = col.replace('theme_', '')
                if theme_name != 'comment':  # Skip the comment theme
                    count = dept_data[col].sum()
                    if count > 0:
                        theme_counts[theme_name] = int(count)
        
        # Sort themes by count
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        top_themes = [{"theme": t[0], "count": t[1]} for t in sorted_themes[:5]]
        
        return {
            "department": department,
            "risk_score": risk_score,
            "high_risk": is_high_risk,
            "top_themes": top_themes
        }
    except Exception as e:
        st.error(f"Error getting department risk: {str(e)}")
        return None

def get_departments():
    """Get list of all departments"""
    if not st.session_state.data_loaded:
        return []
        
    try:
        return list(st.session_state.department_data.keys())
    except Exception as e:
        st.error(f"Error getting departments: {str(e)}")
        return []

# Now we'll import the page functions from dashboard.py
# The functions will reference the helper functions and session state above
from dashboard import home_page, department_details, comment_explorer, themes_analysis, insights_solutions, about

# Main content based on selected page
if not st.session_state.data_loaded and page != "About":
    st.title("Staff Feedback Analysis Dashboard")
    st.info("No data loaded. Please upload a file using the sidebar.")
else:
    if page == "Home":
        home_page()
    elif page == "Department Details":
        department_details()
    elif page == "Comment Explorer":
        comment_explorer()
    elif page == "Themes Analysis":
        themes_analysis()
    elif page == "Insights & Solutions":
        insights_solutions()
    else:
        about()

# Add export options
if st.session_state.data_loaded:
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export as PDF Report"):
            from dashboard import generate_pdf_report
            generate_pdf_report()
            
    with col2:
        if st.button("Export as PowerPoint"):
            from dashboard import generate_pptx_report
            generate_pptx_report() 