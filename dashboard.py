# -*- coding: utf-8 -*-
"""dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1h5jKEAgeXA9i8KfegWpUxIOMPNMrkQjT
"""

# dashboard.py - Main Streamlit Application
import streamlit as st
import pandas as pd # Import pandas for potential display formatting
import traceback  # Add this import

# Local Imports
import api_client
# Import page modules - ensure these exist or adjust imports
from pages import home, department, comments, themes, insights, about, visualizations # Add visualizations here

# --- Page Configuration ---
st.set_page_config(
    page_title="Feedback Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Initialize Session State ---
# Use new keys reflecting the updated API responses
if 'overall_analysis' not in st.session_state:
    st.session_state.overall_analysis = None # Stores overall summary dict
if 'department_analysis_list' not in st.session_state:
    st.session_state.department_analysis_list = None # Stores list of department summary dicts
if 'departments' not in st.session_state:
    st.session_state.departments = None # Stores list of department names
if 'detailed_themes' not in st.session_state: # Can store overall themes here initially
    st.session_state.detailed_themes = None # Stores dict {"themes": ..., "subthemes": ...}
if 'data_summary' not in st.session_state: # Keep data_summary for overview stats
    st.session_state.data_summary = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'last_error' not in st.session_state:
    st.session_state.last_error = None


# --- Helper Function to Load Data ---
def load_data_from_api():
    """Fetches all necessary data from the API and updates session state."""
    st.session_state.last_error = None # Clear previous errors
    try:
        st.session_state.overall_analysis = api_client.get_overall_analysis()
        st.session_state.department_analysis_list = api_client.get_all_department_analysis()
        st.session_state.departments = api_client.get_departments()
        st.session_state.detailed_themes = api_client.get_detailed_themes() # Fetch overall themes initially
        st.session_state.data_summary = api_client.get_data_summary()

        # Determine if data was actually loaded
        if st.session_state.overall_analysis and st.session_state.overall_analysis.get("comment_count", 0) > 0:
            st.session_state.data_loaded = True
            print("Data successfully loaded from API.")
            return True
        else:
            # Handle case where API is up but has no data (e.g., after startup before upload)
            st.session_state.data_loaded = False
            print("API connected, but no processed data found.")
            # Don't treat this as an error, but data is not loaded
            return False # Indicate data not loaded, but no connection error

    except Exception as e:
        st.session_state.last_error = f"Failed to load data from API: {str(e)}"
        print(st.session_state.last_error)
        st.session_state.data_loaded = False
        # Reset data fields on error
        st.session_state.overall_analysis = None
        st.session_state.department_analysis_list = None
        st.session_state.departments = None
        st.session_state.detailed_themes = None
        st.session_state.data_summary = None
        return False # Indicate error


# --- Sidebar Setup ---
st.sidebar.title("Staff Feedback Analysis")

# Check API connection
api_ok = api_client.check_api_connection()
if not api_ok:
    st.sidebar.error("❌ Cannot connect to API server.")
    st.error("Connection Error: Cannot connect to the backend API server. Please ensure it's running and accessible.")
    st.session_state.data_loaded = False # Ensure data_loaded is false if API is down
else:
    st.sidebar.success("✅ Connected to API server")

# File upload section
st.sidebar.header("Data Upload")
uploaded_file = st.sidebar.file_uploader("Upload Feedback Data (CSV/XLSX with Department & Feedback cols)", type=["csv", "xlsx", "xls"])

if uploaded_file:
    if st.sidebar.button("Process Data"):
        if not api_ok:
            st.sidebar.error("Cannot process: API server is not connected.")
        else:
            with st.spinner("Processing data via API... This may take some time."):
                st.session_state.last_error = None # Clear previous errors
                result = api_client.upload_file(uploaded_file)
                # --- DEBUG: Print the raw result from the API ---
                print(f"[Dashboard] Raw API upload result: {result}")
                # -------------------------------------------------
                if result and result.get("status") == "success":
                    st.sidebar.success(f"✅ Processed {result.get('comments_processed', 'N/A')} comments from {result.get('departments_found', 'N/A')} depts.")
                    # --- Force reload of data after successful upload ---
                    with st.spinner("Loading updated analysis results..."):
                         load_data_from_api() # Reload all data
                    st.experimental_rerun() # Rerun script to reflect new data
                else:
                    # Error message should be handled by api_client or shown here
                    error_detail = "Upload failed or API returned an error."
                    if isinstance(result, dict):
                        error_detail = result.get("detail", "Unknown error during processing.")
                    elif result is None:
                        error_detail = "API client failed to get a response."
                    
                    print(f"[Dashboard] Upload Error Detail: {error_detail}") # DEBUG
                    st.session_state.last_error = f"Error processing file: {error_detail}"
                    st.sidebar.error(f"❌ {st.session_state.last_error}")
                    st.session_state.data_loaded = False # Ensure data is marked as not loaded


# --- Initial Data Load (if API is OK and data hasn't been loaded yet) ---
if api_ok and not st.session_state.data_loaded:
     # Attempt to load data only once per session start if API is ok
     if 'initial_load_attempted' not in st.session_state:
         st.session_state.initial_load_attempted = True
         with st.spinner("Loading initial data from API..."):
            load_successful = load_data_from_api()
            if load_successful:
                 st.sidebar.info("Existing data loaded from API.")
            elif st.session_state.last_error:
                 st.sidebar.error(f"Failed to load initial data: {st.session_state.last_error}")
            else:
                 st.sidebar.warning("No data found on API server. Please upload a file.")
     # If initial load failed, show error message if available
     elif st.session_state.last_error:
         st.sidebar.error(f"Failed to load data: {st.session_state.last_error}")


# --- Display Error if any occurred during load/process ---
if st.session_state.last_error and not uploaded_file: # Don't show load error right after upload attempt failed
    st.error(f"An error occurred: {st.session_state.last_error}")

# --- Navigation ---
st.sidebar.header("Navigation")
# Define pages - adjust based on actual files in 'pages/' directory
PAGES = {
    "Home": home,
    "Department Details": department,
    "Comment Explorer": comments,
    "Themes Analysis": themes,
    "Insights": insights, # Renamed from "Insights & Solutions"
    "Visualizations": visualizations, # Add the new page here
    "About": about
}
page_options = list(PAGES.keys())

# Disable pages if data isn't loaded? Maybe allow navigation but show warning on page.
# Let's allow navigation but pages should handle the 'data_loaded' state.
page_selection = st.sidebar.radio("Select a page", page_options)


# --- Page Routing ---
selected_page_module = PAGES[page_selection]

# Display the selected page
# Pass necessary data from session state to the page functions
# Each page's show_page function needs to be updated to accept these arguments
# and handle cases where data might be None.

if selected_page_module:
    try:
        # Example of passing data - adjust arguments based on what each page needs
        if page_selection == "Home":
            # Home might need overall analysis, data summary, maybe top themes/departments
            home.show_page(
                data_summary=st.session_state.data_summary,
                overall_analysis=st.session_state.overall_analysis,
                department_analysis_list=st.session_state.department_analysis_list # Pass list for ranking etc.
            )
        elif page_selection == "Department Details":
            # Department page needs the list of departments for selection,
            # and potentially the full list of analyses to avoid re-fetching per selection (or fetch within page)
            department.show_page(
                 departments=st.session_state.departments,
                 all_department_data=st.session_state.department_analysis_list # Pass all data for easier lookup
            )
        elif page_selection == "Comment Explorer":
            # Comments page needs departments and themes for filtering
             comments.show_page(
                 departments=st.session_state.departments,
                 themes_summary=st.session_state.detailed_themes # Pass detailed themes for filter population
             )
        elif page_selection == "Themes Analysis":
            # Themes page might fetch its own data based on selections, or receive overall themes
            themes.show_page(
                 detailed_themes_overall=st.session_state.detailed_themes, # Pass overall themes
                 departments=st.session_state.departments # For optional department filter
            )
        elif page_selection == "Insights":
            # Insights page needs summary data and potentially ranked lists
            insights.show_page(
                 data_summary=st.session_state.data_summary,
                 overall_analysis=st.session_state.overall_analysis,
                 department_analysis_list=st.session_state.department_analysis_list
            )
        # --- Add routing for Visualizations ---
        elif page_selection == "Visualizations":
            # Visualizations page needs overall analysis, department list, and detailed themes
            visualizations.show_page(
                overall_analysis=st.session_state.overall_analysis,
                department_analysis_list=st.session_state.department_analysis_list,
                detailed_themes_overall=st.session_state.detailed_themes # Pass overall themes for subtheme drilldown etc.
            )
        # --------------------------------------
        elif page_selection == "About":
            about.show_page()
        else:
             st.warning("Page not implemented yet.")

        # Check data loaded status within each page module if necessary
        # Adjusted the condition to exclude 'Visualizations' as well if it should be accessible without data
        # However, visualizations.py currently checks for data itself, so this generic warning might still appear.
        if not st.session_state.data_loaded and page_selection not in ["Home", "About", "Visualizations"]: # Allow visualizations even if data not loaded initially
             st.warning(f"No data loaded. Please upload and process a file to view '{page_selection}'.")

    except AttributeError as e:
         st.error(f"Error loading page '{page_selection}': The page module might be missing the 'show_page' function or expects different arguments. Error: {e}")
         print(f"AttributeError loading page {page_selection}: {e}")
         traceback.print_exc()
    except Exception as e:
         st.error(f"An unexpected error occurred while displaying page '{page_selection}': {e}")
         print(f"Error displaying page {page_selection}: {e}")
         traceback.print_exc()

# --- Footer or other common elements ---
st.sidebar.markdown("---")
st.sidebar.info("Version 1.1.0")