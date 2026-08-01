"""Generate CSV and Excel reports from analysis data.

This module is written in a simple, interview-friendly way so the reporting flow
is easy to explain: load data, prepare the report, and export it to files.
"""

import sys
from pathlib import Path

import pandas as pd

# Make sure the project root is available on the import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_collection.config import ANALYSIS_DATA_DIR, REPORTS_DATA_DIR as REPORTS_OUTPUT_DIR

# Output folder for generated business reports.
# Using the centralized config keeps the folder structure consistent across the project.
REPORTS_DATA_DIR = Path(REPORTS_OUTPUT_DIR)


def load_visualization() -> pd.DataFrame:
    """Load the analysis data that will be used for reporting."""
    # Build an absolute path so the script behaves the same way from any folder.
    analysis_file = (PROJECT_ROOT / ANALYSIS_DATA_DIR / "analysis_results.csv").resolve()

    if not analysis_file.exists():
        print("No analysis file found. Returning an empty report.")
        return pd.DataFrame()

    # Read the CSV into a DataFrame so it can be exported as a report.
    return pd.read_csv(analysis_file, index_col=0)


def generate_reports(df: pd.DataFrame) -> None:
    """Generate Excel and CSV reports from a DataFrame."""
    REPORTS_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Save the report as CSV for easy sharing and review.
    csv_report_path = REPORTS_DATA_DIR / "report.csv"
    df.to_csv(csv_report_path, index=False)

    # Save the same report as Excel for business users.
    excel_report_path = REPORTS_DATA_DIR / "report.xlsx"
    df.to_excel(excel_report_path, index=False, engine="openpyxl")

    print(f"Reports generated: {csv_report_path}, {excel_report_path}")
