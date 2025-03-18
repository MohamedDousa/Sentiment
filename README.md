# Staff Feedback Analysis Tool

An AI-powered tool to analyze staff feedback on workplace civility and respect, providing actionable insights through NLP and interactive visualizations.

## Overview

This tool processes unstructured staff feedback (free-text comments) to:
- Analyze sentiment using DistilBERT
- Detect themes/topics related to workplace civility and respect
- Extract suggested solutions from employee comments
- Analyze sentiment distribution by theme
- Visualize results in an interactive dashboard
- Provide actionable insights for improving workplace culture

## Key Components

### 1. Data Pipeline
- Accepts CSV/Excel files with department names and free-text comments
- Handles single-question feedback formats (like the NQPS Q4 document)
- Cleans and normalizes text data
- Groups comments by department

### 2. NLP Engine
- Sentiment analysis using DistilBERT transformer model
- Custom theme detection for workplace civility topics
- Rule-based pattern matching with exclusion filters
- Solution extraction through keyword pattern matching
- Theme-level sentiment distribution analysis

### 3. API Layer (FastAPI)
- File upload and processing endpoint
- Theme analysis and comment sampling
- Department-level insights
- Sentiment distribution metrics
- Theme-specific comment retrieval for sentiment analysis

### 4. Dashboard (Streamlit)
- Interactive visualizations of sentiment and themes
- Solution frequency analysis with examples
- Comment explorer with sentiment and theme filtering
- Department-level drilldowns
- Theme Sentiment Analysis with positive/neutral/negative breakdowns
- Dedicated Insights & Solutions page for actionable recommendations

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/staff-feedback-analysis.git
cd staff-feedback-analysis
```

2. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Download necessary model files:
```
python -m spacy download en_core_web_sm
```

## Usage

### Running the Application

1. Run the complete application using the run script:
```
python run.py
```
This will start both the API server and the Streamlit dashboard.

2. Access the dashboard in your web browser at http://localhost:8501

### Using the Dashboard

1. Upload a CSV or Excel file containing:
   - Free-text comments from staff about workplace civility and respect
   - The tool can handle both multi-question surveys with department information
   - And single-question formats (like NQPS Q4) without explicit department data

2. View the analysis results:
   - Sentiment distribution visualization
   - Theme frequency breakdown
   - Theme sentiment analysis showing positive/neutral/negative distributions
   - Solution categorization with exact counts
   - Comment samples filtered by sentiment, theme, or department
   - Detailed insights and actionable recommendations

### Theme Sentiment Analysis

The Theme Sentiment Analysis feature provides deeper insights into how staff feel about each workplace theme:

1. Access it through the "Themes Analysis" page and select the "Theme Sentiment Analysis" tab
2. The analysis shows:
   - Sentiment distribution for each theme (positive, neutral, negative percentages)
   - Sentiment comparison across themes with both stacked and grouped visualizations
   - Detailed metrics including sentiment ratios for each theme
   - Key insights highlighting the most positive and most negative themes
   - Recommended focus areas based on sentiment patterns

This feature helps you understand not just what themes are mentioned, but whether staff comments about each theme are primarily positive or negative, enabling more targeted action planning.

## Project Structure

```
staff-feedback-analysis/
│
├── api.py                # FastAPI backend
├── dashboard.py          # Streamlit frontend
├── run.py                # Integration script to run both API and dashboard
├── preprocessing.py      # Data loading and cleaning
├── nlp_pipeline.py       # Text analysis and theme detection
├── development_summary.md # Documentation of development decisions and updates
├── update_dev_summary.py # Script to update development summary
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

## Target Users

- HR managers
- Hospital administrators
- Team leaders
- Employee experience departments

## Outcome

This tool helps organizations proactively address workplace civility issues by understanding staff concerns, identifying specific problem areas, and extracting actionable solutions directly from staff feedback.

## Documentation

For detailed information about the development process, key decisions, and recent updates, see the `development_summary.md` file.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 