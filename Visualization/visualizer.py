"""Visualization helpers for ProductPulse.

This module loads the analysis results and creates simple charts so the
project can present insights clearly in interviews and demos.
"""

import ast
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Make sure the project root is available on the import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_collection.config import ANALYSIS_DATA_DIR, VISUALIZATION_DATA_DIR


def load_analysis_data() -> pd.DataFrame:
    """Load the analysis CSV file from the analysis output folder."""
    csv_path = Path(ANALYSIS_DATA_DIR) / "analysis_results.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Analysis file not found: {csv_path}")

    # Read the CSV and keep the first column as the index.
    df = pd.read_csv(csv_path, index_col=0)
    df.index = df.index.astype(str)
    return df


def save_visualizations(df: pd.DataFrame) -> None:
    """Create and save simple charts from the analysis results."""
    output_dir = Path(VISUALIZATION_DATA_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Example chart 1: number of products per source.
    if "products_per_source" in df.index:
        raw_value = df.loc["products_per_source"].iloc[0]
        source_counts = ast.literal_eval(raw_value) if isinstance(raw_value, str) else raw_value

        if isinstance(source_counts, dict) and source_counts:
            chart_data = pd.Series(source_counts)
            plt.figure(figsize=(8, 6))
            chart_data.plot(kind="bar", color="skyblue")
            plt.title("Number of Products per Source")
            plt.xlabel("Source")
            plt.ylabel("Number of Products")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(output_dir / "products_per_source.png")
            plt.close()

    # Example chart 2: average price summary.
    if "average_price" in df.index:
        raw_value = df.loc["average_price"].iloc[0]
        average_price = float(raw_value) if pd.notna(raw_value) else 0.0

        plt.figure(figsize=(6, 4))
        plt.bar(["Average Price"], [average_price], color="lightgreen")
        plt.title("Average Product Price")
        plt.ylabel("Price")
        plt.tight_layout()
        plt.savefig(output_dir / "average_price.png")
        plt.close()
