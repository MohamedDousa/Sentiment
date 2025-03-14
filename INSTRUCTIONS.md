# Instructions for Running the Employee Feedback Analysis Tool

This document provides step-by-step instructions for setting up and running the Employee Feedback Analysis Tool.

## Prerequisites

- Python 3.9 or higher
- Virtual environment tool (recommended)

## Setup Instructions

### 1. Clone the Repository

If you're using Git:

```bash
git clone <repository-url>
cd employee-feedback-analysis
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

### Method 1: Run Using the Main Script

The simplest way to run both components is to use the main script:

```bash
python main.py
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

## Testing the Application

### 1. Component Testing

To verify that all components are working correctly:

```bash
python test_components.py
```

This will run tests for the preprocessing module, NLP pipeline, predictive model, and API connection.

### 2. Process Sample Data

A sample dataset is included in the repository for testing:

1. Start the application using one of the methods above
2. Open the dashboard in your browser
3. Upload the `sample_data.csv` file
4. Explore the analysis results

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
   - Check that the API_URL in config.py is correct

## Getting Help

If you encounter any issues not covered in this guide, please:

1. Check the logs in the terminal window
2. Refer to the README.md file for additional information
3. Submit an issue in the project repository 