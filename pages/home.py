import streamlit as st

# Accept arguments passed from dashboard.py, handle None values
def show_page(data_summary=None, overall_analysis=None, department_analysis_list=None):
    st.title("🏠 Home")
    st.write("Welcome to the Staff Feedback Analysis Dashboard.")

    if not st.session_state.get('data_loaded', False):
        st.warning("No data loaded. Please upload and process a file using the sidebar.")
        return

    st.subheader("Overall Summary")
    if overall_analysis:
        st.metric("Total Comments Processed", overall_analysis.get("comment_count", "N/A"))
        st.metric("Average Sentiment Score", f"{overall_analysis.get('avg_sentiment', 0.5):.2f}")
        # Add more summary info here later
    else:
        st.info("Overall analysis data is not available.")

    # Add more content based on data_summary, overall_analysis, department_analysis_list
    # For example: Display top themes, departments with lowest sentiment, etc.
    st.write("---")
    st.write("*Placeholder content for Home page.*")

# Ensure session state check is robust
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Example of accessing session state directly if needed, though passing args is cleaner
# if st.session_state.data_loaded:
#    st.write("Data is loaded.")
# else:
#    st.write("Data is not loaded.")