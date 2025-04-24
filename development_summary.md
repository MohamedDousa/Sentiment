# Development Summary

## Project Goal

To create a tool that analyzes free-text staff feedback (e.g., from surveys) to extract sentiment, themes, and subthemes, providing insights through an interactive dashboard and a summary report.

## Core Architecture

*   **Backend**: FastAPI (`api.py`) responsible for:
    *   Receiving file uploads (CSV/XLSX).
    *   Preprocessing data (`preprocessing.py`).
    *   Performing NLP analysis (`nlp_pipeline.py`):
        *   Sentence tokenization using NLTK.
        *   Sentiment analysis per sentence (DistilBERT SST-2).
        *   Hierarchical theme/subtheme extraction (keyword/regex based).
        *   Aggregation of results (overall and per department).
    *   Serving analysis results via REST API endpoints.
*   **Frontend**: Streamlit, divided into:
    *   **Main Dashboard (`dashboard.py` + `pages/`)**: Interactive interface for data upload, viewing overall summaries, exploring themes/subthemes, analyzing department details, and browsing filtered comments.
    *   **Report App (`report_app.py`)**: Standalone read-only view displaying key summary metrics and tables.
*   **Launcher (`main.py`)**: Starts both the FastAPI backend and the main Streamlit dashboard.
*   **API Client (`api_client.py`)**: Shared module used by Streamlit apps to communicate with the FastAPI backend.

## Key Development Steps & Decisions

*   **Initial Setup**: Basic FastAPI + Streamlit structure.
*   **Preprocessing**: Implemented robust loading for CSV/Excel, dynamic column finding (`department`, `feedback`), text cleaning.
*   **Theme Engine**: Developed a hierarchical theme/subtheme system using keywords and exclusion patterns in `nlp_pipeline.py`. Refined keywords and exclusions based on testing (e.g., removing ambiguous "it" from IT Systems).
*   **Sentiment Analysis**: Integrated Hugging Face Transformers pipeline (DistilBERT SST-2).
*   **Sentence-Level Sentiment**: Modified the pipeline to analyze sentiment for each sentence (using NLTK `sent_tokenize`) to better handle comments with mixed positive/negative elements. Aggregation was updated to calculate overall comment sentiment based on sentence average, and theme/subtheme sentiment distributions based on the underlying sentence sentiments.
*   **API Endpoints**: Defined endpoints for data upload, overall summary, department list, department details, theme details, and comment sampling.
*   **Dashboard Pages**: Created separate pages (`pages/`) for different views (Home, Department, Comments, Themes, Insights).
*   **Standalone Report**: Added `report_app.py` for a concise summary view.
*   **Error Handling & Robustness**: Added checks for API connectivity, column existence, and error handling for API calls within Streamlit apps.
*   **Dependency Management**: Added NLTK, fixed download issues (LookupError, SSL), cleaned up unused requirements.
*   **Removed Features**: Hardcoded solutions, predictive modeling placeholders, complex export functionalities (PDF/PPTX) were removed to focus on core analysis.

## Current Status

The application provides core functionality for uploading feedback, performing sentence-level sentiment and theme analysis, and exploring results through the dashboard and report app. Key bug fixes related to NLTK downloads and column name mismatches after implementing sentence-level analysis have been addressed.
