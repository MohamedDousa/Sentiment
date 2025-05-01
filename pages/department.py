import streamlit as st
import pandas as pd
import api_client # To potentially fetch specific data if needed
# import config # Removed config import

def display_department_details(dept_name, dept_data):
    """Helper function to display details for a single department."""
    st.subheader(f"📊 Analysis for: {dept_name}")

    if not dept_data:
        st.warning(f"Could not retrieve data for {dept_name}.")
        return

    # Display key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Comments", dept_data.get('comment_count', 'N/A'))
    avg_sent = dept_data.get('avg_sentiment')
    avg_sent_display = f"{avg_sent:.2f}" if avg_sent is not None else "N/A"
    col2.metric("Avg. Sentiment", avg_sent_display)
    neg_comments = dept_data.get('sentiment_distribution', {}).get('negative', 0)
    col3.metric("Negative Comments", neg_comments)

    st.markdown("**Themes & Potential Actions**")
    themes = dept_data.get('themes', {})
    subthemes = dept_data.get('subthemes', {})

    if not themes:
        st.info("No specific themes identified for this department in the current data.")
        return

    # Sort themes by comment count or negativity?
    sorted_themes = sorted(themes.items(), key=lambda item: item[1].get('comment_count', 0), reverse=True)

    for theme_name, theme_stats in sorted_themes:
        # Calculate negativity for context
        total_theme_comments = sum(theme_stats.get('sentiment_distribution', {}).values())
        neg_theme_comments = theme_stats.get('sentiment_distribution', {}).get('negative', 0)
        neg_theme_perc = (neg_theme_comments / total_theme_comments * 100) if total_theme_comments > 0 else 0

        with st.expander(f"**{theme_name}** ({theme_stats.get('comment_count', 0)} comments, {neg_theme_perc:.0f}% negative)"):
            # Display sentiment distribution for the theme
            st.write(f"Sentiment: Positive {theme_stats.get('sentiment_distribution', {}).get('positive', 0)}, Neutral {theme_stats.get('sentiment_distribution', {}).get('neutral', 0)}, Negative {neg_theme_comments}")
            st.write(f"Average Sentiment for Theme: {theme_stats.get('avg_sentiment', 0.5):.2f}")

            # Display subtheme details only
            if theme_name in subthemes:
                st.markdown("__Subthemes__")
                for subtheme_name, subtheme_stats in subthemes[theme_name].items():
                    # Calculate subtheme negativity
                    total_sub_comments = sum(subtheme_stats.get('sentiment_distribution', {}).values())
                    neg_sub_comments = subtheme_stats.get('sentiment_distribution', {}).get('negative', 0)
                    neg_sub_perc = (neg_sub_comments / total_sub_comments * 100) if total_sub_comments > 0 else 0
                    
                    st.write(f"- **{subtheme_name}**: {subtheme_stats.get('comment_count', 0)} comments ({neg_sub_perc:.0f}% negative)")
            else:
                st.write("_No specific subthemes identified for this theme._")

            # Add link/button to view sample comments for this theme/dept?
            # st.button(f"View comments for {theme_name} in {dept_name}", key=f"comments_{dept_name}_{theme_name}")

# Modify show_page to use multiselect and the helper function
def show_page(departments: list = None, all_department_data: list = None):
    st.title("🏢 Department Analysis")

    if not departments or not all_department_data:
        st.warning("Department data not loaded. Please upload and process a file.")
        return

    # Allow selecting multiple departments
    selected_departments = st.multiselect(
        "Select Departments to View/Compare",
        options=sorted(departments),
        default=departments[0] if departments else None # Default to the first department if available
    )

    if not selected_departments:
        st.info("Please select one or more departments from the list above.")
        return

    # Display data for each selected department
    for dept_name in selected_departments:
        # Find the data for the selected department
        dept_data = next((d for d in all_department_data if d.get('department') == dept_name), None)
        
        if dept_data:
            display_department_details(dept_name, dept_data)
            st.divider() # Add a separator between departments
        else:
            st.error(f"Could not find analysis data for department: {dept_name}")