# Employee Feedback Analysis Tool

An AI-powered tool to analyze employee feedback and identify departments at risk of operational issues using NLP and machine learning.

## Overview

This tool processes unstructured employee feedback (free-text comments) to:
- Analyze sentiment using DistilBERT
- Detect themes/topics across 35+ categories
- Predict department risk scores on a 1-5 scale
- Provide explainable insights using SHAP values
- Visualize results in an interactive dashboard

## Key Components

### 1. Data Pipeline
- Accepts CSV/Excel files with department names and free-text comments
- Cleans and normalizes text data
- Groups comments by department

### 2. NLP Engine
- Sentiment analysis using DistilBERT transformer model
- Custom theme detection across 35+ categories
- Rule-based pattern matching with exclusion filters

### 3. Risk Prediction
- XGBoost model predicts department risk scores
- SHAP values explain key risk factors
- Fallback to DBSCAN clustering when labeled data is unavailable

### 4. API Layer (FastAPI)
- File upload and processing endpoint
- Risk score endpoints with department-level insights
- Theme analysis and comment sampling

### 5. Dashboard (Streamlit)
- Interactive visualizations of risk scores
- Theme frequency analysis
- Comment explorer with sentiment filtering
- Department-level drilldowns

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/employee-feedback-analysis.git
cd employee-feedback-analysis
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

1. Start the API server:
```
uvicorn api:app --reload
```

2. Start the Streamlit dashboard:
```
streamlit run dashboard.py
```

3. Access the dashboard in your web browser at http://localhost:8501

### Using the Dashboard

1. Upload a CSV or Excel file containing:
   - A 'department' column with department names
   - A 'free-text comments' column with employee feedback

2. View the risk analysis results:
   - Department risk scores visualization
   - Theme frequency breakdown
   - Department-specific insights
   - Sample comments filtered by sentiment or theme

## Project Structure

```
employee-feedback-analysis/
│
├── api.py                # FastAPI backend
├── dashboard.py          # Streamlit frontend
├── main.py               # Integration script
├── preprocessing.py      # Data loading and cleaning
├── nlp_pipeline.py       # Text analysis and theme detection
├── predictive_model.py   # Risk scoring models
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

## Target Users

- HR managers
- Hospital administrators
- Operational risk teams
- Employee experience departments

## Outcome

This tool helps organizations proactively address workplace issues by identifying at-risk departments and understanding key drivers of employee dissatisfaction.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 