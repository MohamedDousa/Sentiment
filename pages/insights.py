import streamlit as st
import pandas as pd
import plotly.express as px
# import config # Removed config import

# Accept arguments passed from dashboard.py
def show_page(data_summary: dict = None, overall_analysis: dict = None, department_analysis_list: list = None):
    st.title("🔍 Insights & Key Areas")

    if not data_summary or not overall_analysis:
        st.warning("No data loaded. Please upload and process a file on the Home page.")
        return

    st.header("Overall Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Comments", data_summary.get('total_comments', 'N/A'))
    col2.metric("Departments Analysed", data_summary.get('total_departments', 'N/A'))
    # Format avg_sentiment from overall_analysis if available
    avg_sentiment = overall_analysis.get('avg_sentiment')
    avg_sentiment_display = f"{avg_sentiment:.2f}" if avg_sentiment is not None else "N/A"
    col3.metric("Average Sentiment Score", avg_sentiment_display)

    # Reverted Section: Display most frequent negative themes instead of solutions
    st.header("Key Themes")

    if overall_analysis and 'themes' in overall_analysis:
        st.subheader("Most Frequent Themes with Negative Average Sentiment (Overall)")
        overall_themes = overall_analysis.get("themes", {})
        if overall_themes:
            theme_list = []
            # Filter for themes with avg sentiment < 0.45 (negative leaning)
            # You might adjust this threshold
            negative_sentiment_threshold = 0.45 
            for theme, data in overall_themes.items():
                if data.get("avg_sentiment", 0.5) < negative_sentiment_threshold: 
                    theme_list.append({
                        "Theme": theme,
                        "Comment Count": data.get("comment_count", 0),
                        "Avg Sentiment": data.get("avg_sentiment", 0.5),
                        "Negative Comments": data.get("sentiment_distribution", {}).get("negative", 0)
                    })
            # Display top N themes sorted by comment count
            if theme_list:
                neg_theme_df = pd.DataFrame(theme_list).sort_values("Comment Count", ascending=False).head(10)
                # Use st.dataframe for better table rendering
                st.dataframe(neg_theme_df.style.format({"Avg Sentiment": "{:.2f}"}))
            else:
                st.info(f"No themes found with average sentiment below {negative_sentiment_threshold}.")
        else:
            st.write("No overall theme data available.")
    else:
        st.info("Overall theme analysis data is not available.")

    # Placeholder for department-specific insights or trends over time
    st.header("Department Hotspots")
    if department_analysis_list:
         # Example: List departments with lowest average sentiment
         sorted_depts = sorted(department_analysis_list, key=lambda x: x.get('avg_sentiment', 0.5))
         st.write("Departments with lowest average sentiment scores:")
         for dept_info in sorted_depts[:5]: # Show top 5 lowest
             dept_name = dept_info.get('department', 'Unknown')
             avg_sent = dept_info.get('avg_sentiment', 0.5)
             st.write(f"- {dept_name}: {avg_sent:.2f}")
    else:
         st.info("Department-level analysis data not available.")

    st.write("---")
    st.write("*Placeholder content for Insights page.*")