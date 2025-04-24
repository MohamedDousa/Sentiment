# Staff Feedback Analysis Tool

## Overview

This tool analyzes free-text staff feedback comments from surveys or other sources. It performs sentiment analysis (at the sentence level) and identifies relevant themes and subthemes within the comments.

The application consists of:

1.  **FastAPI Backend (`api.py`)**: Handles data uploading, preprocessing, NLP analysis (sentiment, themes), and serves the results via API endpoints.
2.  **Streamlit Dashboard (`dashboard.py` & `pages/`)**: Provides an interactive interface for uploading data, viewing overall summaries, exploring themes, analyzing departments, and browsing individual comments.
3.  **Standalone Report App (`report_app.py`)**: A separate Streamlit application that displays a concise summary report based on the latest processed data from the API.

## Features

*   **Data Upload**: Accepts CSV or Excel files containing department and feedback columns.
*   **Preprocessing**: Cleans text data, handles missing values, standardizes department names.
*   **Sentence-Level Sentiment Analysis**: Uses a pre-trained transformer model (DistilBERT SST-2) to determine sentiment (positive, negative, neutral) for each sentence within a comment. Calculates an overall comment sentiment based on the sentence average.
*   **Hierarchical Theme Extraction**: Identifies predefined themes (e.g., Workload, Management) and subthemes (e.g., Pressure, Staffing Levels) using keyword matching and exclusion patterns.
*   **Aggregation**: Summarizes results overall and by department, including comment counts, average sentiment, and sentiment distributions (based on sentence analysis for themes).
*   **Interactive Dashboard**: Allows users to explore results through various pages (Home, Department Details, Comment Explorer, Themes Analysis, Insights).
*   **Standalone Report**: Provides a quick, read-only summary view.

## Setup & Installation

1.  **Prerequisites**:
    *   Python (version 3.9+ recommended, tested with 3.11)
    *   `pip` (Python package installer)
    *   Git (for cloning)

2.  **Clone Repository**:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

3.  **Create Virtual Environment** (Recommended):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    # .venv\Scripts\activate  # Windows
    ```

4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Download NLTK Data**:
    The application attempts to download the necessary 'punkt' tokenizer data on first run. If this fails (e.g., due to SSL issues), download it manually:
    *   Open a Python interpreter: `python3`
    *   Run: 
        ```python
        import nltk
        nltk.download('punkt')
        exit()
        ```
    *   **macOS SSL Fix (if needed)**: If the manual download fails with an SSL error, navigate to your Python installation folder (e.g., `/Applications/Python 3.11/`) and double-click `Install Certificates.command`. Then retry the manual NLTK download.

## Running the Application

1.  **Start the API Server and Dashboard**: 
    Open a terminal in the project directory and run:
    ```bash
    python main.py
    ```
    This will start the FastAPI server (usually on `http://localhost:8000`) and the main Streamlit dashboard (usually on `http://localhost:8501`). It should automatically open the dashboard in your browser.

2.  **Upload Data**: Use the sidebar in the main dashboard (`http://localhost:8501`) to upload your feedback file (CSV/XLSX).

3.  **View Report (Optional)**:
    *   Ensure the API server from step 1 is still running.
    *   Open a *new* terminal in the project directory.
    *   Run:
        ```bash
        streamlit run report_app.py
        ```
    *   This will open the standalone report (usually on `http://localhost:8502` or another port if 8501 is busy) in your browser.

## Project Structure

*   `api.py`: FastAPI application.
*   `nlp_pipeline.py`: Core NLP processing logic (sentiment, themes).
*   `preprocessing.py`: Data loading and cleaning functions.
*   `api_client.py`: Helper functions for the dashboard/report apps to communicate with the API.
*   `dashboard.py`: Main Streamlit dashboard entry point.
*   `report_app.py`: Standalone Streamlit report application.
*   `pages/`: Directory containing individual Streamlit page modules for the dashboard.
*   `main.py`: Script to launch both the API and the main dashboard.
*   `config.py`: Configuration settings (ports, model names - though some config is now internal).
*   `requirements.txt`: Python dependencies.
*   `README.md`: This file.
*   `Instructions.md`: Step-by-step user instructions.
*   `development_summary.md`: Overview of development changes.
*   `.venv/`: Virtual environment directory (if created).
*   `temp/`: Temporary directory for file uploads (managed by `main.py`).

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