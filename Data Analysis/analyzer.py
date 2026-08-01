"""Analyze cleaned product data and export simple business insights.

This module is written in a clear, interview-friendly style so the main steps are
easy to follow: load data, calculate summaries, and export the results.
"""

import json
import os
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_collection.config import CLEANED_DATA_DIR

# Folder where analysis outputs should be written.
ANALYSIS_DATA_DIR = "data/analysis"


def _resolve_data_dir(path_value: str) -> Path:
    """Return an absolute path for the given data directory."""
    path = Path(path_value)
    if path.is_absolute():
        return path
    return (PROJECT_ROOT / path).resolve()


CLEANED_DATA_DIR = str(_resolve_data_dir(CLEANED_DATA_DIR))


def load_cleaned_data() -> pd.DataFrame:
    """Load all cleaned JSON files into one pandas DataFrame.

    The function scans the cleaned-data folder, reads every JSON file, and combines
    the records into a single table for analysis.
    """
    records = []
    cleaned_dir = Path(CLEANED_DATA_DIR)

    if not cleaned_dir.exists():
        return pd.DataFrame()

    # Read each JSON file if it exists and contains product records.
    for filename in sorted(os.listdir(cleaned_dir)):
        if not filename.endswith(".json"):
            continue

        path = cleaned_dir / filename
        if not path.exists():
            continue

        try:
            with path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (json.JSONDecodeError, TypeError, ValueError):
            continue

        if isinstance(payload, dict):
            records.append(payload)
        elif isinstance(payload, list):
            records.extend(item for item in payload if isinstance(item, dict))

    if records:
        return pd.DataFrame(records)

    return pd.DataFrame()


def analyze_data(df: pd.DataFrame) -> pd.DataFrame:
    """Create a small summary table with basic product insights.

    The output includes:
    - average price
    - count of products per source
    - top product titles
    """
    if df.empty:
        return pd.DataFrame()

    analysis = {
        "average_price": df["price"].dropna().mean(),
        "products_per_source": df["source"].value_counts().to_dict(),
        "top_titles": df["name"].value_counts().head(5).to_dict(),
    }

    # Convert the dictionary into a DataFrame so it is easy to export.
    return pd.DataFrame.from_dict(analysis, orient="index")


def export_results(df: pd.DataFrame) -> None:
    """Export analysis results to CSV and Excel files."""
    output_dir = Path(ANALYSIS_DATA_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "analysis_results.csv"
    excel_path = output_dir / "analysis_results.xlsx"

    df.to_csv(csv_path, index=True)
    df.to_excel(excel_path, index=True)
 
