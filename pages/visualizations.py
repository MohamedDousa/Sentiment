# pages/visualizations.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional

# Helper function to safely get nested data (optional but good practice)
def safe_get(data_dict, key_list, default=None):
    """Safely access nested dictionary keys."""
    current = data_dict
    for key in key_list:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

# --- Visualization Functions ---

def plot_overall_sentiment_distribution(overall_analysis: Optional[Dict[str, Any]]):
    """Plots a pie chart for overall sentiment distribution."""
    dist = safe_get(overall_analysis, ['sentiment_distribution'], {})
    if not dist or sum(dist.values()) == 0:
        st.info("No sentiment data available.")
        return

    df = pd.DataFrame(list(dist.items()), columns=['Sentiment', 'Count'])
    fig = px.pie(df, values='Count', names='Sentiment', title="Overall Sentiment Distribution",
                 color='Sentiment',
                 color_discrete_map={'positive': 'green', 'neutral': 'grey', 'negative': 'red'})
    st.plotly_chart(fig, use_container_width=True)

def plot_dept_sentiment_comparison(department_analysis_list: Optional[List[Dict[str, Any]]]):
    """Plots a bar chart comparing average sentiment scores across departments."""
    if not department_analysis_list:
        st.info("No department analysis data available.")
        return

    # Extract department names and avg sentiment
    data = []
    for dept_data in department_analysis_list:
        dept_name = dept_data.get('department_name')
        avg_sentiment = safe_get(dept_data, ['summary', 'avg_sentiment'])
        if dept_name is not None and avg_sentiment is not None:
            data.append({'Department': dept_name, 'Average Sentiment Score': avg_sentiment})

    if not data:
        st.info("Could not extract department sentiment data.")
        return

    df = pd.DataFrame(data)
    df = df.sort_values(by='Average Sentiment Score', ascending=False)

    fig = px.bar(df, x='Department', y='Average Sentiment Score', title="Average Sentiment Score by Department",
                 color='Average Sentiment Score', color_continuous_scale=px.colors.sequential.RdYlGn,
                 range_color=[0, 1]) # Use range 0-1 for sentiment
    fig.update_layout(yaxis_title="Avg. Sentiment (0=Neg, 1=Pos)")
    st.plotly_chart(fig, use_container_width=True)

def plot_theme_prevalence(overall_analysis: Optional[Dict[str, Any]]):
    """Plots a bar chart showing the number of comments per main theme."""
    themes_data = safe_get(overall_analysis, ['themes'], {})
    if not themes_data:
        st.info("No theme data available.")
        return

    data = []
    for theme, details in themes_data.items():
        data.append({'Theme': theme, 'Comment Count': details.get('comment_count', 0)})

    if not data:
        st.info("Could not extract theme prevalence data.")
        return

    df = pd.DataFrame(data)
    df = df.sort_values(by='Comment Count', ascending=False)

    fig = px.bar(df, x='Theme', y='Comment Count', title="Theme Prevalence by Comment Count")
    fig.update_layout(xaxis_title="Theme", yaxis_title="Number of Comments")
    st.plotly_chart(fig, use_container_width=True)

def plot_theme_sentiment_treemap(overall_analysis: Optional[Dict[str, Any]]):
    """Plots a treemap of themes, sized by count, colored by sentiment."""
    themes_data = safe_get(overall_analysis, ['themes'], {})
    if not themes_data:
        st.info("No theme data available for treemap.")
        return

    data = []
    for theme, details in themes_data.items():
        count = details.get('comment_count', 0)
        sentiment = details.get('avg_sentiment')
        if count > 0 and sentiment is not None: # Only include themes with comments and sentiment
            data.append({
                'Theme': theme,
                'Comment Count': count,
                'Average Sentiment': sentiment
            })

    if not data:
        st.info("No valid theme data for treemap.")
        return

    df = pd.DataFrame(data)

    fig = px.treemap(df,
                     path=[px.Constant("All Themes"), 'Theme'], # Add a root node
                     values='Comment Count',
                     color='Average Sentiment',
                     color_continuous_scale='RdYlGn',
                     range_color=[0, 1],
                     title="Themes by Comment Count and Average Sentiment")
    fig.update_traces(textinfo = "label+value+percent parent")
    st.plotly_chart(fig, use_container_width=True)

def plot_subtheme_breakdown(overall_analysis: Optional[Dict[str, Any]], selected_theme: str):
    """Plots a bar chart for subthemes within a selected main theme."""
    subthemes_data = safe_get(overall_analysis, ['subthemes', selected_theme], {})
    if not subthemes_data:
        st.info(f"No subtheme data available for theme '{selected_theme}'.")
        return

    data = []
    for subtheme, details in subthemes_data.items():
        count = details.get('comment_count', 0)
        sentiment = details.get('avg_sentiment')
        if count > 0 and sentiment is not None:
             data.append({
                 'Subtheme': subtheme,
                 'Comment Count': count,
                 'Average Sentiment': sentiment
             })

    if not data:
        st.info(f"Could not extract valid subtheme data for '{selected_theme}'.")
        return

    df = pd.DataFrame(data)
    df = df.sort_values(by='Comment Count', ascending=False)

    fig = px.bar(df, x='Subtheme', y='Comment Count',
                 color='Average Sentiment', color_continuous_scale='RdYlGn', range_color=[0,1],
                 title=f"Subtheme Breakdown for '{selected_theme}'")
    fig.update_layout(xaxis_title="Subtheme", yaxis_title="Number of Comments")
    st.plotly_chart(fig, use_container_width=True)

def plot_top_themes_by_sentiment(overall_analysis: Optional[Dict[str, Any]], positive: bool = True, top_n: int = 10):
    """Plots top N themes based on highest percentage of positive or negative comments."""
    themes_data = safe_get(overall_analysis, ['themes'], {})
    if not themes_data:
        st.info("No theme data available.")
        return

    data = []
    for theme, details in themes_data.items():
        sentiment_dist = details.get('sentiment_distribution', {})
        pos_count = sentiment_dist.get('positive', 0)
        neg_count = sentiment_dist.get('negative', 0)
        neu_count = sentiment_dist.get('neutral', 0)
        total = pos_count + neg_count + neu_count

        if total > 0:
            neg_perc = (neg_count / total) * 100
            pos_perc = (pos_count / total) * 100
            data.append({
                'Theme': theme,
                'Negative %': neg_perc,
                'Positive %': pos_perc,
                'Total Comments': total
            })

    if not data:
        st.info("Could not calculate theme sentiment percentages.")
        return

    df = pd.DataFrame(data)

    if positive:
        sort_col = 'Positive %'
        title = f"Top {top_n} Most Positive Themes (by % of Positive Comments)"
        df = df.sort_values(by=sort_col, ascending=False).head(top_n)
        x_val, y_val = sort_col, 'Theme'
        color_val = sort_col
        color_scale = 'Greens'
        range_color = [0, 100]
    else:
        sort_col = 'Negative %'
        title = f"Top {top_n} Most Negative Themes (by % of Negative Comments)"
        df = df.sort_values(by=sort_col, ascending=False).head(top_n)
        x_val, y_val = sort_col, 'Theme'
        color_val = sort_col
        color_scale = 'Reds'
        range_color = [0, 100]

    fig = px.bar(df, x=x_val, y=y_val, title=title, orientation='h',
                 color=color_val, color_continuous_scale=color_scale, range_color=range_color,
                 text=x_val)
    fig.update_traces(texttemplate='%{x:.1f}%', textposition='outside')
    fig.update_layout(yaxis_title="Theme", xaxis_title="Percentage",
                      yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)


# --- Main Page Function ---
def show_page(overall_analysis: Optional[Dict[str, Any]],
                department_analysis_list: Optional[List[Dict[str, Any]]],
                detailed_themes_overall: Optional[Dict[str, Any]]):
    """Displays the visualization page."""
    st.title("📊 Data Visualizations")

    if not overall_analysis or not department_analysis_list or not detailed_themes_overall:
        st.warning("No processed data available. Please upload and process a file first.")
        # Check if the API might have data even if session state isn't fully populated yet
        # This might happen on first load before processing
        st.info("Attempting to check API for data...")
        # You might want to add a button here to trigger a data refresh from the API
        # if api_client.check_if_data_exists_on_api(): # Hypothetical function
        #    st.button("Refresh data from API")
        return

    # Use tabs for navigation
    tab_titles = [
        "Overall Sentiment",
        "Department Comparison",
        "Theme Analysis",
        "Subtheme Drilldown",
        "Top Themes (Sentiment)"
    ]
    tab1, tab2, tab3, tab4, tab5 = st.tabs(tab_titles)

    with tab1:
        st.header("Overall Sentiment Distribution")
        st.write("Breakdown of positive, neutral, and negative comments across the entire dataset.")
        plot_overall_sentiment_distribution(overall_analysis)

    with tab2:
        st.header("Department Sentiment Comparison")
        st.write("Average sentiment score for each department (based on overall comment sentiment). Higher score is more positive.")
        plot_dept_sentiment_comparison(department_analysis_list)

    with tab3:
        st.header("Theme Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Theme Prevalence")
            st.write("Number of comments mentioning each main theme.")
            plot_theme_prevalence(overall_analysis)
        with col2:
            st.subheader("Theme Sentiment Overview")
            st.write("Themes sized by comment count and colored by average sentiment (Red=Negative, Green=Positive).")
            plot_theme_sentiment_treemap(overall_analysis)

    with tab4:
        st.header("Subtheme Drilldown")
        # Ensure we have themes to select from
        available_themes = list(safe_get(overall_analysis, ['themes'], {}).keys())
        if not available_themes:
            st.info("No themes with data found to select for drilldown.")
        else:
            selected_theme = st.selectbox("Select a Theme to view Subthemes:", available_themes)
            if selected_theme:
                plot_subtheme_breakdown(overall_analysis, selected_theme)

    with tab5:
        st.header("Top/Bottom Themes by Sentiment")
        st.write("Themes ranked by the percentage of positive or negative comments mentioning them.")
        view_positive = st.toggle("View Most Positive Themes", value=True)
        num_themes_to_show = st.slider("Number of themes to show:", min_value=3, max_value=20, value=10)
        if view_positive:
            plot_top_themes_by_sentiment(overall_analysis, positive=True, top_n=num_themes_to_show)
        else:
            plot_top_themes_by_sentiment(overall_analysis, positive=False, top_n=num_themes_to_show)

    st.divider()
    st.info("""**Note**: 
    *   Sentiment calculations for themes/subthemes (e.g., in treemap, subtheme bars) are based on the average *overall comment sentiment* of comments mentioning that theme/subtheme.
    *   Sentiment percentages (e.g., in Top Themes charts, overall pie chart) are based on the distribution of *sentence-level sentiment* within comments mentioning the theme/subtheme or across all comments.""") 