#!/usr/bin/env python
"""
Static HTML Export for Staff Feedback Analysis Dashboard

This script exports dashboard visualizations as static HTML files that can be viewed
without running the Streamlit app or API server.
"""

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import plotly.io as pio
import json
import shutil
from pathlib import Path

# Import the processing functions
from preprocessing import load_data, preprocess_data, group_by_department
from nlp_pipeline import process_nlp_pipeline, NLPProcessor

# Output directory for static files
OUTPUT_DIR = "static_export"

def ensure_output_dir():
    """Ensure the output directory exists, create if it doesn't"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "js"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "css"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "images"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "data"), exist_ok=True)

def export_sentiment_distribution(data):
    """Export sentiment distribution visualization"""
    # Create sentiment data
    sentiment_dist = {
        "positive": len(data[data['sentiment_score'] > 0.6]),
        "neutral": len(data[(data['sentiment_score'] >= 0.4) & (data['sentiment_score'] <= 0.6)]),
        "negative": len(data[data['sentiment_score'] < 0.4])
    }
    
    sentiment_data = []
    for sentiment, count in sentiment_dist.items():
        sentiment_data.append({
            "sentiment": sentiment.capitalize(),
            "count": count
        })
    
    sentiment_df = pd.DataFrame(sentiment_data)
    
    # Create Plotly pie chart
    fig = px.pie(
        sentiment_df,
        values="count",
        names="sentiment",
        title="Overall Sentiment Distribution",
        color="sentiment",
        color_discrete_map={
            "Positive": "green",
            "Neutral": "gray",
            "Negative": "red"
        }
    )
    
    # Export as HTML
    filename = os.path.join(OUTPUT_DIR, "sentiment_distribution.html")
    fig.write_html(
        filename,
        include_plotlyjs="cdn",
        full_html=True,
        config={"displayModeBar": False, "responsive": True}
    )
    
    # Save the data as JSON for potential reuse
    json_filename = os.path.join(OUTPUT_DIR, "data", "sentiment_data.json")
    sentiment_df.to_json(json_filename, orient="records")
    
    return filename

def export_themes_overview(data):
    """Export theme overview visualization"""
    # Create theme data for visualization
    theme_data = []
    for column in data.columns:
        if column.startswith('theme_') and column != 'theme_comment':
            theme_name = column.replace('theme_', '')
            # Skip themes containing "comment" as they skew results
            if "comment" not in theme_name.lower():
                count = data[column].sum()
                theme_data.append({
                    "theme": theme_name,
                    "count": int(count)
                })
    
    theme_df = pd.DataFrame(theme_data)
    theme_df = theme_df.sort_values("count", ascending=False)
    
    # Display top 10 themes
    fig = px.bar(
        theme_df.head(10),
        x="theme",
        y="count",
        title="Top 10 Themes (excluding 'comment' themes)",
        labels={"theme": "Theme", "count": "Occurrence Count"},
        color="count",
        color_continuous_scale="Blues"
    )
    fig.update_layout(xaxis_tickangle=-45)
    
    # Export as HTML
    filename = os.path.join(OUTPUT_DIR, "themes_overview.html")
    fig.write_html(
        filename,
        include_plotlyjs="cdn",
        full_html=True,
        config={"displayModeBar": False, "responsive": True}
    )
    
    # Save the data as JSON for potential reuse
    json_filename = os.path.join(OUTPUT_DIR, "data", "themes_data.json")
    theme_df.to_json(json_filename, orient="records")
    
    return filename

def export_civility_themes(data):
    """Export civility and respect themes visualization"""
    # Create theme data
    theme_data = []
    for column in data.columns:
        if column.startswith('theme_') and column != 'theme_comment':
            theme_name = column.replace('theme_', '')
            # Skip themes containing "comment" as they skew results
            if "comment" not in theme_name.lower():
                count = data[column].sum()
                theme_data.append({
                    "theme": theme_name,
                    "count": int(count)
                })
    
    theme_df = pd.DataFrame(theme_data)
    
    # Filter for civility/respect related themes
    respect_themes = [
        'respect_communication', 'workplace_culture', 'leadership_behavior',
        'workplace_policies', 'inclusion_diversity', 'training_development',
        'recognition_appreciation'
    ]
    
    respect_theme_df = theme_df[theme_df['theme'].isin(respect_themes)]
    respect_theme_df = respect_theme_df.sort_values("count", ascending=False)
    
    if not respect_theme_df.empty:
        fig = px.bar(
            respect_theme_df,
            x="theme",
            y="count",
            title="Civility & Respect Themes",
            labels={"theme": "Theme", "count": "Occurrence Count"},
            color="count",
            color_continuous_scale="Greens"
        )
        fig.update_layout(xaxis_tickangle=-45)
        
        # Export as HTML
        filename = os.path.join(OUTPUT_DIR, "civility_themes.html")
        fig.write_html(
            filename,
            include_plotlyjs="cdn",
            full_html=True,
            config={"displayModeBar": False, "responsive": True}
        )
        
        # Save the data as JSON for potential reuse
        json_filename = os.path.join(OUTPUT_DIR, "data", "civility_themes_data.json")
        respect_theme_df.to_json(json_filename, orient="records")
        
        return filename
    return None

def export_theme_sentiment_analysis(data):
    """Export theme sentiment analysis visualization"""
    # Get top 10 themes
    theme_data = []
    for column in data.columns:
        if column.startswith('theme_') and column != 'theme_comment':
            theme_name = column.replace('theme_', '')
            # Skip themes containing "comment" as they skew results
            if "comment" not in theme_name.lower():
                count = data[column].sum()
                theme_data.append({
                    "theme": theme_name,
                    "count": int(count)
                })
    
    theme_df = pd.DataFrame(theme_data)
    theme_df = theme_df.sort_values("count", ascending=False)
    top_themes = theme_df.head(10)['theme'].tolist()
    
    # For each theme, analyze sentiment
    theme_sentiment_data = {}
    for theme in top_themes:
        theme_col = f"theme_{theme}"
        if theme_col in data.columns:
            # Get comments with this theme
            theme_comments = data[data[theme_col] == 1]
            
            # Count sentiment categories
            sentiment_counts = {
                "POSITIVE": len(theme_comments[theme_comments['sentiment_score'] > 0.6]),
                "NEUTRAL": len(theme_comments[(theme_comments['sentiment_score'] >= 0.4) & (theme_comments['sentiment_score'] <= 0.6)]),
                "NEGATIVE": len(theme_comments[theme_comments['sentiment_score'] < 0.4])
            }
            
            theme_sentiment_data[theme] = sentiment_counts
    
    # Create visualization data
    sentiment_rows = []
    for theme, counts in theme_sentiment_data.items():
        total = sum(counts.values())
        
        if total > 0:
            # Calculate percentages
            pos_pct = (counts["POSITIVE"] / total * 100) if total > 0 else 0
            neu_pct = (counts["NEUTRAL"] / total * 100) if total > 0 else 0
            neg_pct = (counts["NEGATIVE"] / total * 100) if total > 0 else 0
            
            # Format theme name for display
            display_theme = theme.replace("_", " ").title()
            
            # Add row for each sentiment category
            sentiment_rows.append({"theme": display_theme, "sentiment": "Positive", "percentage": pos_pct, "count": counts["POSITIVE"]})
            sentiment_rows.append({"theme": display_theme, "sentiment": "Neutral", "percentage": neu_pct, "count": counts["NEUTRAL"]})
            sentiment_rows.append({"theme": display_theme, "sentiment": "Negative", "percentage": neg_pct, "count": counts["NEGATIVE"]})
    
    # Create DataFrame
    sentiment_df = pd.DataFrame(sentiment_rows)
    
    # Create a stacked bar chart
    fig = px.bar(
        sentiment_df,
        x="theme",
        y="percentage",
        color="sentiment",
        title="Sentiment Distribution by Theme",
        labels={"theme": "Theme", "percentage": "Percentage (%)", "sentiment": "Sentiment"},
        color_discrete_map={
            "Positive": "green",
            "Neutral": "gray",
            "Negative": "red"
        },
        barmode="stack"
    )
    
    fig.update_layout(xaxis_tickangle=-45)
    
    # Export as HTML
    filename = os.path.join(OUTPUT_DIR, "theme_sentiment.html")
    fig.write_html(
        filename,
        include_plotlyjs="cdn",
        full_html=True,
        config={"displayModeBar": False, "responsive": True}
    )
    
    # Create a grouped bar chart
    # Create a column chart specifically for positive and negative percentages
    pivot_df = sentiment_df.pivot(index="theme", columns="sentiment", values="percentage").reset_index()
    
    # Sort by negative percentage (descending)
    if 'Negative' in pivot_df.columns:
        pivot_df = pivot_df.sort_values("Negative", ascending=False)
    
    fig2 = px.bar(
        pivot_df,
        x="theme",
        y=["Negative", "Neutral", "Positive"] if all(col in pivot_df.columns for col in ["Negative", "Neutral", "Positive"]) else pivot_df.columns[1:],
        title="Sentiment Distribution by Theme",
        labels={"theme": "Theme", "value": "Percentage (%)", "variable": "Sentiment"},
        color_discrete_map={
            "Positive": "green",
            "Neutral": "gray",
            "Negative": "red"
        },
        barmode="group"
    )
    
    fig2.update_layout(xaxis_tickangle=-45)
    
    # Export as HTML
    grouped_filename = os.path.join(OUTPUT_DIR, "theme_sentiment_grouped.html")
    fig2.write_html(
        grouped_filename,
        include_plotlyjs="cdn",
        full_html=True,
        config={"displayModeBar": False, "responsive": True}
    )
    
    # Save the data as JSON for potential reuse
    json_filename = os.path.join(OUTPUT_DIR, "data", "theme_sentiment_data.json")
    sentiment_df.to_json(json_filename, orient="records")
    
    return filename, grouped_filename

def export_theme_categories(data):
    """Export theme categories visualization"""
    # Define theme categories
    theme_categories = {
        "Communication & Transparency": [
            "respect_communication", "listening"
        ],
        "Leadership & Management": [
            "leadership_behavior", "lead_by_example"
        ],
        "Culture & Team Environment": [
            "workplace_culture", "culture_improvement", "teambuilding", "respect_promotion"
        ],
        "Policies & Accountability": [
            "workplace_policies", "policy_enforcement", "accountability", "reporting_mechanism"
        ],
        "Development & Recognition": [
            "training_development", "staff_training", "management_training", "recognition_appreciation"
        ],
        "Diversity & Inclusion": [
            "inclusion_diversity"
        ]
    }
    
    # Count mentions by category
    category_counts = {}
    for category, themes in theme_categories.items():
        count = 0
        for theme in themes:
            theme_col = f"theme_{theme}"
            if theme_col in data.columns:
                count += data[theme_col].sum()
        category_counts[category] = int(count)
    
    # Create DataFrame
    category_data = []
    for category, count in category_counts.items():
        if count > 0:
            category_data.append({
                "category": category,
                "count": count
            })
    
    category_df = pd.DataFrame(category_data)
    category_df = category_df.sort_values("count", ascending=False)
    
    # Create a pie chart
    fig = px.pie(
        category_df,
        values="count",
        names="category",
        title="Distribution of Themes by Category",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Export as HTML
    filename = os.path.join(OUTPUT_DIR, "theme_categories.html")
    fig.write_html(
        filename,
        include_plotlyjs="cdn",
        full_html=True,
        config={"displayModeBar": False, "responsive": True}
    )
    
    # Save the data as JSON for potential reuse
    json_filename = os.path.join(OUTPUT_DIR, "data", "theme_categories_data.json")
    category_df.to_json(json_filename, orient="records")
    
    return filename

def export_solutions(data):
    """Export solutions visualization"""
    # Define solution categories with keywords
    specific_solutions = {
        "better_communication": {
            "keywords": ["better communication", "improve communication", "communicate better", "open communication"],
            "display_name": "Better Communication"
        },
        "management_training": {
            "keywords": ["management training", "train managers", "leadership training", "leader training"],
            "display_name": "Management/Leadership Training"
        },
        "staff_training": {
            "keywords": ["staff training", "employee training", "training for staff", "train employees"],
            "display_name": "Staff Training & Development"
        },
        "accountability": {
            "keywords": ["accountability", "hold accountable", "consequences", "responsible", "responsibility"],
            "display_name": "Accountability Measures"
        },
        "culture_improvement": {
            "keywords": ["better culture", "improve culture", "positive culture", "workplace culture"],
            "display_name": "Culture Improvement"
        },
        "lead_by_example": {
            "keywords": ["lead by example", "leading by example", "role model", "role models", "role modeling"],
            "display_name": "Leading by Example"
        },
        "teambuilding": {
            "keywords": ["team building", "team activities", "social events", "get together", "social activities"],
            "display_name": "Team Building Activities"
        },
        "recognition_programs": {
            "keywords": ["recognition", "rewards", "incentives", "award", "appreciate", "appreciation"],
            "display_name": "Recognition & Appreciation"
        },
        "policy_enforcement": {
            "keywords": ["enforce policy", "policies", "guidelines", "rules", "procedures", "enforce rules"],
            "display_name": "Policy Enforcement"
        },
        "reporting_mechanism": {
            "keywords": ["reporting", "report system", "anonymous reports", "complaint system", "complaint process"],
            "display_name": "Reporting Mechanisms"
        },
        "respect_promotion": {
            "keywords": ["respect", "respectful", "civility", "civil", "polite", "politeness", "courteous"],
            "display_name": "Promoting Respect & Civility"
        },
        "listening": {
            "keywords": ["listen", "listening", "hear concerns", "hear feedback", "listening skills"],
            "display_name": "Better Listening"
        }
    }
    
    # Count comments mentioning each solution
    for solution_key, solution_data in specific_solutions.items():
        comment_count = 0
        for keyword in solution_data["keywords"]:
            # Check for keyword in free_text_comments
            matches = data[data['free_text_comments'].str.contains(keyword, case=False, na=False)]
            comment_count += len(matches)
        
        specific_solutions[solution_key]["count"] = comment_count
    
    # Create visualization data
    solution_counts = []
    for sol_key, sol_data in specific_solutions.items():
        count = sol_data["count"]
        if count > 0:
            solution_counts.append({
                "solution": sol_data["display_name"],
                "count": count
            })
    
    # Sort solutions by count
    solution_df = pd.DataFrame(solution_counts)
    solution_df = solution_df.sort_values("count", ascending=False)
    
    # Calculate percentage of total comments
    total_comments = len(data)
    solution_df["percentage"] = (solution_df["count"] / total_comments * 100).round(1)
    
    # Create a bar chart
    fig = px.bar(
        solution_df,
        x="solution",
        y="count",
        title=f"Number of Comments Mentioning Each Solution Type",
        labels={"solution": "Solution Type", "count": "Number of Comments"},
        color="count",
        color_continuous_scale="Viridis",
        text="percentage"
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(xaxis_tickangle=-45)
    
    # Export as HTML
    filename = os.path.join(OUTPUT_DIR, "solutions.html")
    fig.write_html(
        filename,
        include_plotlyjs="cdn",
        full_html=True,
        config={"displayModeBar": False, "responsive": True}
    )
    
    # Save the data as JSON for potential reuse
    json_filename = os.path.join(OUTPUT_DIR, "data", "solutions_data.json")
    solution_df.to_json(json_filename, orient="records")
    
    return filename

def create_index_html(visualization_files):
    """Create an index.html file linking to all visualizations"""
    index_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Staff Feedback Analysis Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                padding: 20px;
                background-color: #f5f7fa;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
            }
            .header { 
                text-align: center; 
                margin-bottom: 30px; 
                color: #333;
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .visualization-card {
                margin-bottom: 20px;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                background-color: white;
            }
            .card-header {
                background-color: #4287f5;
                color: white;
                padding: 15px;
                font-size: 18px;
            }
            .card-body {
                padding: 0;
            }
            iframe {
                border: none;
                width: 100%;
                height: 500px;
            }
            .dashboard-section {
                margin-bottom: 40px;
            }
            .section-title {
                margin-bottom: 20px;
                color: #333;
                border-bottom: 2px solid #4287f5;
                padding-bottom: 10px;
            }
            .footer {
                text-align: center;
                margin-top: 50px;
                padding: 20px;
                color: #666;
                font-size: 14px;
                border-top: 1px solid #ddd;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Staff Feedback Analysis Dashboard</h1>
                <p>Static HTML export of dashboard visualizations</p>
                <p class="text-muted">Generated on: GENERATION_DATE</p>
            </div>
            
            <div class="dashboard-section">
                <h2 class="section-title">Overview</h2>
                OVERVIEW_VISUALIZATIONS
            </div>
            
            <div class="dashboard-section">
                <h2 class="section-title">Theme Analysis</h2>
                THEME_VISUALIZATIONS
            </div>
            
            <div class="dashboard-section">
                <h2 class="section-title">Solutions & Insights</h2>
                SOLUTIONS_VISUALIZATIONS
            </div>
            
            <div class="footer">
                <p>
                    Staff Feedback Analysis Tool | 
                    <a href="data/">Download Data</a>
                </p>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """.replace("GENERATION_DATE", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Sort visualizations by section
    overview_visuals = []
    theme_visuals = []
    solutions_visuals = []
    
    for vis_file in visualization_files:
        filename = os.path.basename(vis_file)
        iframe_html = f'<div class="visualization-card"><div class="card-header">{filename.replace(".html", "").replace("_", " ").title()}</div><div class="card-body"><iframe src="{filename}"></iframe></div></div>'
        
        if filename in ["sentiment_distribution.html"]:
            overview_visuals.append(iframe_html)
        elif filename in ["solutions.html"]:
            solutions_visuals.append(iframe_html)
        else:
            theme_visuals.append(iframe_html)
    
    # Replace section placeholders with visualization iframes
    index_content = index_content.replace("OVERVIEW_VISUALIZATIONS", "\n".join(overview_visuals))
    index_content = index_content.replace("THEME_VISUALIZATIONS", "\n".join(theme_visuals))
    index_content = index_content.replace("SOLUTIONS_VISUALIZATIONS", "\n".join(solutions_visuals))
    
    # Write index.html
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(index_content)
    
    return os.path.join(OUTPUT_DIR, "index.html")

def export_dashboard(data_file):
    """Export dashboard as static HTML files"""
    print(f"Starting export of dashboard from data file: {data_file}")
    
    # Create output directory
    ensure_output_dir()
    
    try:
        # Load and process data
        print("Loading and processing data...")
        raw_data = load_data(data_file)
        processed_data = preprocess_data(raw_data)
        
        # Run NLP pipeline
        print("Running NLP pipeline...")
        nlp_processor = NLPProcessor()
        processed_data = process_nlp_pipeline(processed_data, nlp_processor)
        
        # Export visualizations
        print("Exporting visualizations...")
        visualization_files = []
        
        # Export sentiment distribution
        sentiment_file = export_sentiment_distribution(processed_data)
        visualization_files.append(sentiment_file)
        print(f"Exported sentiment distribution to {sentiment_file}")
        
        # Export themes overview
        themes_file = export_themes_overview(processed_data)
        visualization_files.append(themes_file)
        print(f"Exported themes overview to {themes_file}")
        
        # Export civility themes
        civility_file = export_civility_themes(processed_data)
        if civility_file:
            visualization_files.append(civility_file)
            print(f"Exported civility themes to {civility_file}")
        
        # Export theme sentiment analysis
        theme_sentiment_file, grouped_file = export_theme_sentiment_analysis(processed_data)
        visualization_files.append(theme_sentiment_file)
        visualization_files.append(grouped_file)
        print(f"Exported theme sentiment analysis to {theme_sentiment_file} and {grouped_file}")
        
        # Export theme categories
        categories_file = export_theme_categories(processed_data)
        visualization_files.append(categories_file)
        print(f"Exported theme categories to {categories_file}")
        
        # Export solutions
        solutions_file = export_solutions(processed_data)
        visualization_files.append(solutions_file)
        print(f"Exported solutions to {solutions_file}")
        
        # Create index.html
        index_file = create_index_html(visualization_files)
        print(f"Created index file at {index_file}")
        
        print(f"Export complete! Open {index_file} in a web browser to view the dashboard")
        return index_file
        
    except Exception as e:
        print(f"Error during export: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Export dashboard as static HTML files")
    parser.add_argument("--data", "-d", required=True, help="Path to data file (CSV or Excel)")
    parser.add_argument("--output", "-o", help="Output directory (default: static_export)")
    
    args = parser.parse_args()
    
    if args.output:
        OUTPUT_DIR = args.output
    
    # Run export
    index_file = export_dashboard(args.data)
    
    if index_file:
        # Try to open the file in a browser
        try:
            import webbrowser
            webbrowser.open(f"file://{os.path.abspath(index_file)}")
        except:
            pass 