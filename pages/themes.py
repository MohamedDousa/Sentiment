import streamlit as st
import pandas as pd
import plotly.express as px
import api_client # To fetch detailed themes if needed

# Accept arguments passed from dashboard.py
def show_page(detailed_themes_overall=None, departments=None):
    st.title("📊 Themes Analysis")

    if not st.session_state.get('data_loaded', False):
        st.warning("No data loaded. Please upload and process a file using the sidebar.")
        return

    # Option to view overall or by department
    view_options = ["Overall Trust"] + sorted(departments) if departments else ["Overall Trust"]
    selected_view = st.selectbox("Select View:", options=view_options)

    # Fetch data based on selection
    theme_data_to_display = None
    if selected_view == "Overall Trust":
        theme_data_to_display = detailed_themes_overall
        st.subheader("Overall Theme & Subtheme Analysis")
    else:
        with st.spinner(f"Fetching theme data for {selected_view}..."):
            theme_data_to_display = api_client.get_detailed_themes(department=selected_view)
        st.subheader(f"Theme & Subtheme Analysis for: {selected_view}")

    if not theme_data_to_display:
        st.error("Could not load theme data for the selected view.")
        return

    # Display Main Themes
    st.markdown("#### Main Themes")
    main_themes = theme_data_to_display.get("themes", {})
    if main_themes:
        theme_list = []
        for theme, data in main_themes.items():
            theme_list.append({
                "Theme": theme,
                "Comment Count": data.get("comment_count", 0),
                "Avg Sentiment": data.get("avg_sentiment", 0.5),
                "Positive": data.get("sentiment_distribution", {}).get("positive", 0),
                "Neutral": data.get("sentiment_distribution", {}).get("neutral", 0),
                "Negative": data.get("sentiment_distribution", {}).get("negative", 0),
            })
        theme_df = pd.DataFrame(theme_list).sort_values("Comment Count", ascending=False)
        st.dataframe(theme_df.style.format({"Avg Sentiment": "{:.2f}"}))

        # Simple bar chart
        fig = px.bar(theme_df.head(15), x='Theme', y='Comment Count', title="Top 15 Themes by Comment Count",
                     color='Avg Sentiment', color_continuous_scale=px.colors.sequential.RdBu_r, range_color=[0,1])
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No main themes found for this view.")

    # Display Subthemes
    st.markdown("#### Subthemes")
    subthemes = theme_data_to_display.get("subthemes", {})
    if subthemes:
         subtheme_list = []
         for theme, sub_dict in subthemes.items():
             for subtheme, data in sub_dict.items():
                 subtheme_list.append({
                     "Main Theme": theme,
                     "Subtheme": subtheme,
                     "Comment Count": data.get("comment_count", 0),
                     "Avg Sentiment": data.get("avg_sentiment", 0.5),
                     "Positive": data.get("sentiment_distribution", {}).get("positive", 0),
                     "Neutral": data.get("sentiment_distribution", {}).get("neutral", 0),
                     "Negative": data.get("sentiment_distribution", {}).get("negative", 0),
                 })
         subtheme_df = pd.DataFrame(subtheme_list).sort_values("Comment Count", ascending=False)
         st.dataframe(subtheme_df.style.format({"Avg Sentiment": "{:.2f}"}))
    else:
         st.info("No subthemes found for this view.")


    st.write("---")
    st.write("*Placeholder content for Themes Analysis page.*")