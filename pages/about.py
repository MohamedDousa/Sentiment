import streamlit as st

def show_page():
    st.title("ℹ️ About")
    st.write("""
    This application analyzes staff feedback comments using Natural Language Processing (NLP).

    **Functionality:**
    *   Upload feedback data (Excel/CSV) with 'Department' and 'Feedback' columns.
    *   Performs sentiment analysis (Positive, Negative, Neutral) on each comment.
    *   Identifies predefined themes and subthemes mentioned in comments.
    *   Aggregates results to provide:
        *   Overall Trust-wide analysis.
        *   Breakdown by individual department.
    *   Allows exploration of comments based on filters.

    **Version:** 1.1.0

    **Note:** This tool uses rule-based theme extraction and a pre-trained sentiment model. Results provide insights but should be interpreted in context. Solution identification is not currently implemented.
    """)