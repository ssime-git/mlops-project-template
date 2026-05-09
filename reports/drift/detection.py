# Evidently Reports - Drift Detection
# Phase 4: Data and model drift monitoring
#
# Usage:
#   python -m reports.drift.detection --reference data/raw/reference.csv --current data/raw/current.csv

import argparse
import pandas as pd
from evidently.dashboard import Dashboard
from evidently.tabs import DataDriftTab, NumTargetDriftTab, CatTargetDriftTab


def generate_drift_report(reference_path: str, current_path: str, output_path: str = "reports/drift/drift_report.html"):
    """
    Generate drift detection report using Evidently.
    
    Parameters:
        reference_path: Path to reference (baseline) dataset
        current_path: Path to current dataset to compare
        output_path: Path to save the HTML report
    """
    # Load datasets
    reference = pd.read_csv(reference_path)
    current = pd.read_csv(current_path)
    
    # Create dashboard with data drift tab
    dashboard = Dashboard(tabs=[
        DataDriftTab(),
        NumTargetDriftTab(),
        CatTargetDriftTab(),
    ])
    
    # Calculate metrics and generate report
    dashboard.calculate(
        reference_data=reference,
        current_data=current,
        column_mapping=None  # Auto-detect columns
    )
    
    # Save report
    dashboard.save(output_path)
    print(f"Drift report saved to: {output_path}")
    
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Evidently drift report")
    parser.add_argument("--reference", required=True, help="Path to reference dataset")
    parser.add_argument("--current", required=True, help="Path to current dataset")
    parser.add_argument("--output", default="reports/drift/drift_report.html", help="Output path")
    
    args = parser.parse_args()
    generate_drift_report(args.reference, args.current, args.output)