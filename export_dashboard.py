#!/usr/bin/env python
"""
Export Dashboard Data and Visualizations

This script exports dashboard data and visualizations in multiple formats:
1. Static HTML files (for web viewing)
2. PDF report (for printing and sharing)
3. PowerPoint presentation (for presenting findings)

Usage:
    python export_dashboard.py --data data/staff_feedback.csv

"""

import os
import argparse
import time
from datetime import datetime

# Import export modules
from export_static import (
    export_sentiment_distribution,
    export_themes_overview,
    export_civility_themes,
    export_theme_sentiment_analysis,
    export_theme_categories,
    export_solutions_summary,
    create_index_html,
    ensure_output_dir as ensure_static_dir
)
from export_reports import (
    generate_pdf_report,
    generate_pptx_report,
    ensure_output_dir as ensure_reports_dir
)

def export_all(data_file, output_dir=None):
    """
    Run all export functions to create a complete export package
    
    Args:
        data_file (str): Path to the data file
        output_dir (str, optional): Base output directory
    
    Returns:
        dict: Paths to generated output files
    """
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create base output directory if specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        static_dir = os.path.join(output_dir, "html")
        reports_dir = os.path.join(output_dir, "reports")
    else:
        static_dir = "static_exports"
        reports_dir = "reports"
    
    # Create directories
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    
    # Store output paths
    output_files = {}
    
    print(f"Starting export process using data from: {data_file}")
    print(f"HTML exports will be saved to: {static_dir}")
    print(f"PDF and PowerPoint exports will be saved to: {reports_dir}")
    
    # 1. Export static HTML files
    print("\n--- Generating Static HTML Exports ---")
    # Temporarily override the output directory
    os.environ["STATIC_EXPORT_DIR"] = static_dir
    ensure_static_dir()
    
    # Export visualizations
    sentiment_file = export_sentiment_distribution(data_file)
    themes_file = export_themes_overview(data_file)
    civility_file = export_civility_themes(data_file)
    theme_sentiment_file = export_theme_sentiment_analysis(data_file)
    theme_categories_file = export_theme_categories(data_file)
    solutions_file = export_solutions_summary(data_file)
    
    # Create index file
    index_file = create_index_html([
        sentiment_file,
        themes_file,
        civility_file,
        theme_sentiment_file,
        theme_categories_file,
        solutions_file
    ])
    
    output_files["html_index"] = index_file
    output_files["html_files"] = [
        sentiment_file,
        themes_file,
        civility_file,
        theme_sentiment_file,
        theme_categories_file,
        solutions_file
    ]
    
    print(f"HTML exports completed. Main index file: {index_file}")
    
    # 2. Export PDF report
    print("\n--- Generating PDF Report ---")
    # Temporarily override the output directory
    os.environ["REPORTS_DIR"] = reports_dir
    ensure_reports_dir()
    
    pdf_file = os.path.join(reports_dir, f"feedback_analysis_report_{timestamp}.pdf")
    pdf_path = generate_pdf_report(data_file, pdf_file)
    
    if pdf_path:
        output_files["pdf_report"] = pdf_path
        print(f"PDF report generated: {pdf_path}")
    else:
        print("PDF report generation failed.")
    
    # 3. Export PowerPoint presentation
    print("\n--- Generating PowerPoint Presentation ---")
    pptx_file = os.path.join(reports_dir, f"feedback_analysis_report_{timestamp}.pptx")
    pptx_path = generate_pptx_report(data_file, pptx_file)
    
    if pptx_path:
        output_files["pptx_report"] = pptx_path
        print(f"PowerPoint presentation generated: {pptx_path}")
    else:
        print("PowerPoint presentation generation failed.")
    
    # Final summary
    elapsed_time = time.time() - start_time
    print(f"\nExport process completed in {elapsed_time:.2f} seconds.")
    print("Generated files:")
    print(f"  - HTML index: {output_files.get('html_index', 'Failed')}")
    print(f"  - PDF report: {output_files.get('pdf_report', 'Failed')}")
    print(f"  - PowerPoint: {output_files.get('pptx_report', 'Failed')}")
    
    return output_files

def main():
    """Main function to parse arguments and run exports"""
    parser = argparse.ArgumentParser(description="Export dashboard data in multiple formats")
    parser.add_argument("--data", "-d", required=True, help="Path to data file (CSV or Excel)")
    parser.add_argument("--output-dir", "-o", help="Base output directory for all exports")
    parser.add_argument("--formats", "-f", choices=["html", "pdf", "pptx", "all"],
                        default="all", help="Export formats to generate")
    
    args = parser.parse_args()
    
    try:
        export_all(args.data, args.output_dir)
        print("\nExport completed successfully! You can now share these static files.")
    except Exception as e:
        print(f"\nError during export process: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 