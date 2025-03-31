# Instructions for Running the Staff Feedback Analysis Tool

This document provides step-by-step instructions for setting up and running the Staff Feedback Analysis Tool.

## Prerequisites

- Python 3.9 or higher
- Virtual environment tool (recommended)

## Setup Instructions

### 1. Clone the Repository

If you're using Git:

```bash
git clone <repository-url>
cd staff-feedback-analysis
```

### 2. Create and Activate a Virtual Environment

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies and Required Models

Run the setup script to install all dependencies and download required models:

```bash
python setup.py
```

Alternatively, you can do this manually:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Configure Environment (Optional)

Copy the example environment file and edit as needed:

```bash
cp .env.example .env
```

Edit the `.env` file to customize settings if needed.

## Running the Application

The application consists of two components:
1. The FastAPI backend (API)
2. The Streamlit frontend (Dashboard)

### Method 1: Run Using the Run Script

The simplest way to run both components is to use the run script:

```bash
python run.py
```

This will start both the API server and dashboard, and open a browser window automatically.

### Method 2: Run Components Separately

#### Start the API Server:

```bash
uvicorn api:app --reload
```

The API will be available at http://localhost:8000.

#### Start the Dashboard:

```bash
streamlit run dashboard.py
```

The dashboard will be available at http://localhost:8501.

## Using the Dashboard

### 1. Upload Data

- Click "Upload Staff Feedback Data" in the sidebar
- Select a CSV or Excel file containing free-text comments
- The tool can process both:
  - Multi-question surveys with department information
  - Single-question formats (like NQPS Q4) without explicit department data
- Click "Process Data" to analyze the comments

### 2. Explore the Dashboard Pages

The dashboard offers several pages accessible from the sidebar:

- **Home**: Overview of sentiment distribution and key themes
- **Department Details**: Department-specific analysis (if applicable)
- **Comment Explorer**: Browse and filter individual comments
- **Themes Analysis**: Detailed analysis of detected themes, including sentiment distribution by theme
- **Insights & Solutions**: Actionable recommendations based on staff feedback
- **About**: Information about the tool and how it works

### 3. Theme Analysis Page

The Theme Analysis page now has a tabbed interface with three sections:

- **Theme Distribution**: Shows the frequency of each theme in the feedback
- **Theme Sentiment Analysis**: Analyzes sentiment distribution for each theme (see details below)
- **Civility Insights**: Focuses specifically on civility and respect-related themes

#### Using the Theme Sentiment Analysis Tab

This feature provides deeper insights into how staff feel about each detected theme:

1. Select the "Theme Sentiment Analysis" tab on the Themes Analysis page
2. The system will analyze up to 100 comments for each of the top 10 themes
3. A progress bar will show the analysis progress
4. Once complete, you'll see:
   - A stacked bar chart showing positive/neutral/negative sentiment distribution for each theme
   - A grouped bar chart for easier comparison across themes
   - A detailed data table with exact percentages and sentiment ratios
   - Key insights highlighting the most positive and most negative themes
   - Recommended focus areas based on the sentiment distribution

This analysis helps you understand not just which themes are most frequent, but whether comments about each theme are primarily positive or negative, enabling more targeted action planning.

### 4. Insights & Solutions Page

The Insights & Solutions page provides:

- **Key Solutions**: Categorized solutions mentioned in comments with exact counts
- **Theme Analysis**: Top 5 themes with detailed breakdown of problems and proposed solutions
- **Theme Categories**: Thematic grouping of related themes with representative quotes
- Each solution category includes examples from actual comments

### 5. Exporting Analysis Results

The tool now includes comprehensive export functionality to share analysis results with stakeholders who may not have access to the live dashboard.

#### Export Options

1. **Static HTML Exports**
   - Standalone web pages with interactive visualizations
   - Can be viewed in any web browser without installing software
   - Perfect for sharing via email or hosting on an intranet

2. **PDF Reports**
   - Professional PDF document with all visualizations and metrics
   - Includes data tables, charts, and actionable insights
   - Ideal for printing and distributing in meetings

3. **PowerPoint Presentations**
   - Ready-to-present slides with key visualizations
   - Organized presentation flow from overview to recommendations
   - Easily customizable for executive presentations

#### How to Generate Exports

Run the export script with your data file:

```bash
python export_dashboard.py --data your_data_file.csv
```

Additional options:
- `--output-dir my_exports`: Specify a custom output directory
- `--formats html`: Export only HTML files
- `--formats pdf`: Export only PDF report
- `--formats pptx`: Export only PowerPoint presentation
- `--formats all`: Export all formats (default)

Example:
```bash
python export_dashboard.py --data data/staff_feedback.csv --output-dir exports --formats all
```

#### Accessing the Exports

After running the export script, you'll find:
- HTML files in the `static_exports` directory (or custom directory/html)
- PDF and PowerPoint files in the `reports` directory (or custom directory/reports)

The HTML exports include an index.html file that links to all visualizations for easy navigation.

## Testing the Application

### 1. Component Testing

To verify that all components are working correctly:

```bash
python test_components.py
```

This will run tests for the preprocessing module, NLP pipeline, and API connection.

### 2. Process Sample Data

Sample datasets are included in the repository for testing:

1. Start the application using one of the methods above
2. Open the dashboard in your browser
3. Upload either:
   - `sample_data.csv` for multi-question format
   - `NQPS Q4 2024_2025 narrative question.xlsx` for single-question format
4. Explore the analysis results

## Maintaining Documentation

The project includes a development summary document that tracks changes and decisions:

- View the current development summary: `development_summary.md`
- Update the summary with new changes:
  ```bash
  python update_dev_summary.py
  ```
  When prompted, enter details about the latest changes.

## Troubleshooting

### Common Issues

1. **Error: Port already in use**
   - Another application is using the required port
   - Change the port in the `.env` file or kill the process using that port

2. **Error: ModuleNotFoundError**
   - Make sure you've installed all dependencies with `pip install -r requirements.txt`
   - Ensure you're running the application from the project root directory

3. **Error: Model download failed**
   - Ensure you have internet connectivity
   - Try running `python -m spacy download en_core_web_sm` manually

4. **Dashboard cannot connect to API**
   - Ensure the API server is running
   - Check that the API_URL in dashboard.py is correct

5. **No comments appearing in analysis**
   - Check your data format - ensure it has a column with free-text comments
   - For single-question formats, check that the question text is properly detected

6. **Theme Sentiment Analysis is slow**
   - This is normal for large datasets as it needs to process comments for each theme
   - The progress bar will show analysis progress
   - You can reduce the analysis time by limiting comment size in the code

7. **Export errors**
   - Ensure all required packages are installed (`fpdf`, `python-pptx`, `kaleido`, etc.)
   - Check that you have write permissions in the output directories
   - For PDF generation issues, ensure your system has proper font support

## Getting Help

If you encounter any issues not covered in this guide, please:

1. Check the logs in the terminal window
2. Refer to the README.md file for additional information
3. Check the development_summary.md for recent changes
4. Submit an issue in the project repository 