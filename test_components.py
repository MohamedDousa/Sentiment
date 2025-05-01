#!/usr/bin/env python
"""
Test components for the Employee Feedback Analysis Tool
Run this script to test that all components are working properly
"""

import os
import sys
import pandas as pd
from pathlib import Path
import traceback

def test_preprocessing():
    """Test the data preprocessing module"""
    try:
        from preprocessing import load_data, preprocess_data, group_by_department
        
        print("\n--- Testing preprocessing module ---")
        
        # Test loading data
        file_path = "sample_data.csv"
        if not os.path.exists(file_path):
            print(f"Error: Sample file '{file_path}' not found.")
            return False
            
        print("Loading data...")
        data = load_data(file_path)
        print(f"✓ Loaded {len(data)} rows successfully")
        
        # Test preprocessing
        print("Preprocessing data...")
        processed_data = preprocess_data(data)
        print(f"✓ Processed data contains {len(processed_data)} rows")
        
        # Test department grouping
        print("Grouping by department...")
        dept_data = group_by_department(processed_data)
        print(f"✓ Created aggregations for {len(dept_data)} departments")
        
        return True
        
    except Exception as e:
        print(f"Error in preprocessing test: {str(e)}")
        traceback.print_exc()
        return False

def test_nlp_pipeline():
    """Test the NLP pipeline module"""
    try:
        from preprocessing import load_data, preprocess_data
        from nlp_pipeline import NLPProcessor
        
        print("\n--- Testing NLP pipeline ---")
        
        # Load and preprocess sample data
        file_path = "sample_data.csv"
        data = load_data(file_path)
        processed_data = preprocess_data(data)
        
        # Initialize NLP processor
        print("Initializing NLP processor...")
        nlp = NLPProcessor()
        print("✓ NLP processor initialized")
        
        # Test sentiment analysis
        print("Testing sentiment analysis...")
        sample_text = "The workload is overwhelming and we are severely understaffed."
        sentiment = nlp.analyze_sentiment(sample_text)
        print(f"✓ Sentiment analysis result: {sentiment:.2f}")
        
        # Test theme detection
        print("Testing theme detection...")
        themes = nlp.extract_themes(sample_text)
        print(f"✓ Detected themes: {', '.join(themes)}")
        
        # Process a small batch of comments
        print("Processing sample comments...")
        sample_df = processed_data.head(5).copy()
        sample_df['comment_results'] = sample_df['free_text_comments'].apply(nlp.process_comment)
        print(f"✓ Processed {len(sample_df)} comments with sentiment and themes")
        
        return True
        
    except Exception as e:
        print(f"Error in NLP pipeline test: {str(e)}")
        traceback.print_exc()
        return False

def test_predictive_model():
    """Test the predictive model module"""
    try:
        from preprocessing import load_data, preprocess_data, group_by_department
        from nlp_pipeline import process_nlp_pipeline
        from predictive_model import PredictiveModel
        
        print("\n--- Testing predictive model ---")
        
        # Load and process sample data
        file_path = "sample_data.csv"
        data = load_data(file_path)
        processed_data = preprocess_data(data)
        
        # Process NLP
        print("Running NLP pipeline...")
        nlp_results = process_nlp_pipeline(processed_data)
        
        # Group by department
        dept_data = group_by_department(nlp_results)
        
        # Initialize and test predictive model
        print("Initializing predictive model...")
        model = PredictiveModel()
        print("✓ Predictive model initialized")
        
        # Prepare features
        print("Preparing features...")
        X, _, departments = model.prepare_features(dept_data)
        print(f"✓ Prepared features with shape {X.shape}")
        
        # Test prediction
        print("Testing risk prediction...")
        risk_scores = model.predict_risk_scores(X, departments)
        print(f"✓ Generated risk scores for {len(risk_scores)} departments")
        
        # Test explanations
        print("Testing SHAP explanations...")
        explanations = model.get_shap_explanations(X, departments)
        print(f"✓ Generated explanations for {len(explanations)} departments")
        
        return True
        
    except Exception as e:
        print(f"Error in predictive model test: {str(e)}")
        traceback.print_exc()
        return False

def test_api():
    """Test the API functionality"""
    try:
        import requests
        
        print("\n--- Testing API (server must be running) ---")
        
        # Check if API is running
        try:
            response = requests.get("http://localhost:8000/")
            if response.status_code == 200:
                print("✓ API server is running")
            else:
                print(f"× API server returned status code {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("× API server is not running. Start it with: uvicorn api:app --reload")
            return False
        
        return True
        
    except Exception as e:
        print(f"Error in API test: {str(e)}")
        traceback.print_exc()
        return False

def main():
    """Run all component tests"""
    print("Testing Employee Feedback Analysis Tool components")
    
    # Create test results dictionary
    results = {}
    
    # Run tests
    results["preprocessing"] = test_preprocessing()
    results["nlp_pipeline"] = test_nlp_pipeline()
    results["predictive_model"] = test_predictive_model()
    results["api"] = test_api()
    
    # Print summary
    print("\n--- Test Summary ---")
    for test, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{test.ljust(20)}: {status}")
    
    # Overall result
    if all(results.values()):
        print("\nAll tests passed! The system is functioning correctly.")
    else:
        print("\nSome tests failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 