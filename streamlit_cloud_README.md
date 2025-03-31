# Staff Feedback Analysis Tool - Streamlit Cloud Version

This repository contains the Staff Feedback Analysis Tool, designed to analyze anonymous staff feedback and identify themes related to workplace civility and respect.

## Streamlit Cloud Deployment

This version has been specifically configured for deployment on Streamlit Cloud. The key differences from the local version are:

1. **Standalone Processing**: All data processing is done within the Streamlit app itself, without requiring a separate API server.
2. **Direct Import**: The app directly imports preprocessing and NLP pipeline modules.
3. **Session State**: Uses Streamlit's session state to store processed data instead of API calls.

## How to Deploy

1. **Fork/Clone this Repository**: Create your own copy on GitHub
2. **Connect to Streamlit Cloud**: 
   - Sign up at [streamlit.io/cloud](https://streamlit.io/cloud)
   - Connect your GitHub account
   - Select this repository
   - Choose `streamlit_app.py` as the main file
   - Click "Deploy"

## Usage

1. **Upload Data**: Use the sidebar to upload a CSV or Excel file with staff feedback data
2. **Process Data**: Click the "Process Data" button to analyze the feedback
3. **Explore Results**: Navigate through the dashboard tabs to see:
   - Theme Analysis
   - Sentiment Distribution
   - Department Details
   - Comment Explorer
   - Insights & Solutions

## Sample Data

The repository includes sample data files you can use to test the dashboard:
- `sample_data.csv`
- `Sample.xlsx`

## Configuration

The app uses the following configuration files:
- `.streamlit/config.toml`: Streamlit configuration
- `requirements.txt`: Python dependencies
- `packages.txt`: System dependencies
- `runtime.txt`: Python version specification

## Troubleshooting

If you encounter issues with the deployment:

1. **Memory Limits**: If the app exceeds Streamlit Cloud's memory limits, consider:
   - Reducing the size of your input data
   - Simplifying NLP processing
   - Using lighter-weight models

2. **Missing Dependencies**: Check the error logs in Streamlit Cloud and add any missing packages to `requirements.txt`

3. **Deployment Failures**: Ensure your GitHub repository is public and contains all necessary files

## Contact

For issues or contributions, please open an issue on the GitHub repository. 