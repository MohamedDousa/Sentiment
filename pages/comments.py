import streamlit as st
import pandas as pd
import api_client # Import the client to fetch comments

# Accept arguments passed from dashboard.py
def show_page(departments=None, themes_summary=None):
    st.title("💬 Comment Explorer")

    if not st.session_state.get('data_loaded', False):
        st.warning("No data loaded. Please upload and process a file using the sidebar.")
        return

    st.write("Filter and view individual comments.")

    # --- Filtering Options ---
    filter_cols = st.columns(4)

    # Department Filter
    dept_options = ["All"] + sorted(departments) if departments else ["All"]
    selected_dept = filter_cols[0].selectbox("Department", options=dept_options)
    filter_dept = selected_dept if selected_dept != "All" else None

    # Theme Filter (extract theme names)
    theme_names = ["All"]
    if themes_summary and themes_summary.get('themes'):
        theme_names.extend(sorted(themes_summary['themes'].keys()))
    selected_theme = filter_cols[1].selectbox("Theme", options=theme_names)
    filter_theme = selected_theme if selected_theme != "All" else None

    # Subtheme Filter (dynamic based on selected theme)
    subtheme_names = ["All"]
    if filter_theme and themes_summary and themes_summary.get('subthemes') and filter_theme in themes_summary['subthemes']:
         subtheme_names.extend(sorted(themes_summary['subthemes'][filter_theme].keys()))
    selected_subtheme = filter_cols[2].selectbox("Subtheme", options=subtheme_names, disabled=(not filter_theme or len(subtheme_names) <= 1))
    filter_subtheme = selected_subtheme if selected_subtheme != "All" else None


    # Sentiment Filter
    sentiment_options = ["All", "positive", "neutral", "negative"]
    selected_sentiment = filter_cols[3].selectbox("Sentiment", options=sentiment_options)
    filter_sentiment = selected_sentiment if selected_sentiment != "All" else None

    limit = st.number_input("Max comments to display", min_value=5, max_value=100, value=10, step=5)

    # --- Fetch and Display Comments ---
    if st.button("Search Comments"):
        with st.spinner("Fetching comments..."):
            comments_data = [] # Initialize
            try:
                comments_data = api_client.get_sample_comments(
                    department=filter_dept,
                    theme=filter_theme,
                    subtheme=filter_subtheme,
                    sentiment=filter_sentiment,
                    limit=limit
                )
            except Exception as e:
                st.error(f"Error fetching comments from API: {e}")
                # Optionally log the full error to console
                # print(f"API Client Error: {traceback.format_exc()}")

            # Proceed only if data fetching was successful and returned data
            if comments_data:
                st.write(f"Displaying up to {limit} matching comments:")
                # Format for display
                display_list = []
                for c in comments_data:
                    themes_str = ", ".join([f"{t}{'/' + s if s else ''}" for t, s in c.get('themes_subthemes', [])])
                    display_list.append({
                        "Department": c.get('department'),
                        "Sentiment": f"{c.get('overall_sentiment_category', 'N/A')} ({c.get('overall_sentiment_score', 0.0):.2f})",
                        "Themes/Subthemes": themes_str,
                        "Comment": c.get('original_comment')
                    })
                st.dataframe(pd.DataFrame(display_list), height=400)
            else:
                st.info("No comments found matching your criteria.")

    st.write("---")
    st.write("*Placeholder content for Comment Explorer page.*")