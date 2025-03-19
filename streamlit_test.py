"""
Staff Feedback Analysis Dashboard - Test Version

This is a simplified test version to verify that deployment works correctly.
"""

import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Feedback Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add page title and description
st.title("Staff Feedback Analysis Dashboard")
st.subheader("Test Version")

st.success("✅ Streamlit is working correctly!")

st.markdown("""
## Next Steps

1. This test app confirms that the deployment environment is working
2. Once this test app is running, we can deploy the full application
3. The full app includes data processing and visualization components

To continue, return to GitHub and update the deployment settings to use `streamlit_app.py` instead of this test file.
""") 