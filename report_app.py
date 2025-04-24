import streamlit as st
import pandas as pd
import plotly.express as px
import api_client # Reuse the existing client to fetch data
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Feedback Analysis Report",
    page_icon="📄",
    layout="wide"
)

# --- Helper Functions ---

def format_sentiment_dist(dist_dict):
    """Formats sentiment distribution for display."""
    if not isinstance(dist_dict, dict):
        return "N/A"
    pos = dist_dict.get('positive', 0)
    neu = dist_dict.get('neutral', 0)
    neg = dist_dict.get('negative', 0)
    return f"Pos: {pos}, Neu: {neu}, Neg: {neg}"

def plot_sentiment_distribution(sentiment_dist, title="Sentiment Distribution"):
    """Creates a bar chart for sentiment distribution."""
    if not isinstance(sentiment_dist, dict) or not sentiment_dist:
        st.info("No sentiment data to plot.")
        return

    # Ensure all categories exist for consistent plotting
    cats = ['positive', 'neutral', 'negative']
    counts = [sentiment_dist.get(cat, 0) for cat in cats]
    
    df_plot = pd.DataFrame({'Sentiment': cats, 'Count': counts})
    fig = px.bar(df_plot, x='Sentiment', y='Count', title=title,
                 color='Sentiment',
                 color_discrete_map={'positive': 'green', 'neutral': 'grey', 'negative': 'red'})
    st.plotly_chart(fig, use_container_width=True)


# --- Main Application ---

st.title("📊 Staff Feedback Analysis Report")
st.markdown(f"_Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S' )}_ ")

st.markdown("--- ")

# 1. Check API Connection
api_ok = api_client.check_api_connection()
if not api_ok:
    st.error("❌ Cannot connect to the backend API server. Please ensure it's running.")
    st.stop() # Stop execution if API is down

st.success("✅ Connected to API server.")

# 2. Fetch Data
data_summary = None
overall_analysis = None
department_analysis_list = None
data_loaded = False

with st.spinner("Fetching analysis data from API..."):
    try:
        data_summary = api_client.get_data_summary()
        overall_analysis = api_client.get_overall_analysis()
        department_analysis_list = api_client.get_all_department_analysis()

        # Check if data exists
        if overall_analysis and overall_analysis.get("comment_count", 0) > 0:
            data_loaded = True
            st.info(f"Data last updated: {data_summary.get('last_updated', 'N/A')}")
        else:
            st.warning("API is connected, but no processed data found. Please upload data via the main dashboard.")

    except Exception as e:
        st.error(f"Failed to fetch data from API: {str(e)}")
        st.stop()

# 3. Display Report Sections (if data loaded)
if data_loaded:
    st.markdown("--- ")
    st.header("Overall Summary")

    if data_summary:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Comments Analyzed", data_summary.get('total_comments', 'N/A'))
        col2.metric("Total Departments", data_summary.get('total_departments', 'N/A'))
        col3.metric("Avg Comments/Dept", f"{data_summary.get('avg_comments_per_department', 'N/A'):.1f}")

    if overall_analysis:
        st.metric("Overall Average Sentiment Score", f"{overall_analysis.get('avg_sentiment', 0.5):.2f}")
        plot_sentiment_distribution(overall_analysis.get('sentiment_distribution'), "Overall Sentiment Distribution (Based on Comment Average)")
        st.caption("Note: Sentiment distribution above reflects the average sentiment category of each comment.")

    st.markdown("--- ")
    st.header("Theme Analysis Summary")

    if overall_analysis and 'themes' in overall_analysis:
        theme_data_list = []
        themes_dict = overall_analysis.get('themes', {})
        for theme, stats in themes_dict.items():
             theme_data_list.append({
                 "Theme": theme,
                 "Comment Count": stats.get('comment_count', 0),
                 "Avg Comment Sentiment": stats.get('avg_sentiment', 0.5),
                 "Sentence Sentiments": format_sentiment_dist(stats.get('sentiment_distribution', {})),
             })
        
        if theme_data_list:
             theme_df = pd.DataFrame(theme_data_list).sort_values("Comment Count", ascending=False)
             st.dataframe(theme_df.style.format({'Avg Comment Sentiment': '{:.2f}'}), use_container_width=True)
             st.caption("Note: 'Avg Comment Sentiment' is the average of overall comment scores for comments mentioning this theme. 'Sentence Sentiments' shows the distribution of positive/neutral/negative *sentences* within those comments.")
        else:
             st.info("No theme data available in the overall analysis.")
    else:
        st.info("Overall theme analysis data not available.")


    st.markdown("--- ")
    st.header("Department Summary")

    if department_analysis_list:
        dept_data_list = []
        for dept_analysis in department_analysis_list:
             dept_data_list.append({
                 "Department": dept_analysis.get('department', 'Unknown'),
                 "Comment Count": dept_analysis.get('comment_count', 0),
                 "Avg Sentiment": dept_analysis.get('avg_sentiment', 0.5),
                 "Sentiment Distribution (Overall)": format_sentiment_dist(dept_analysis.get('sentiment_distribution', {}))
             })
        
        if dept_data_list:
            dept_df = pd.DataFrame(dept_data_list).sort_values("Avg Sentiment", ascending=True) # Sort by lowest sentiment first
            st.dataframe(dept_df.style.format({'Avg Sentiment': '{:.2f}'}), use_container_width=True)
        else:
             st.info("No department analysis data available.")
    else:
        st.info("Department analysis list not available.")

else:
    # Message shown earlier if data is not loaded
    pass

st.markdown("--- ")
st.caption("End of Report") 