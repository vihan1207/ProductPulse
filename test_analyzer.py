import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_analysis import analyzer


class AnalyzerTests(unittest.TestCase):
    def test_load_cleaned_data_reads_json_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cleaned_dir = Path(tmpdir) / "cleaned"
            cleaned_dir.mkdir()

            first_file = cleaned_dir / "a.json"
            second_file = cleaned_dir / "b.json"
            first_file.write_text(json.dumps([{"source": "Amazon", "name": "Phone", "price": 10}]), encoding="utf-8")
            second_file.write_text(json.dumps([{"source": "eBay", "name": "Laptop", "price": 20}]), encoding="utf-8")

            with patch("data_analysis.analyzer.CLEANED_DATA_DIR", str(cleaned_dir)):
                df = analyzer.load_cleaned_data()

            self.assertEqual(len(df), 2)
            self.assertEqual(df["source"].tolist(), ["Amazon", "eBay"])

    def test_load_cleaned_data_handles_single_record_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cleaned_dir = Path(tmpdir) / "cleaned"
            cleaned_dir.mkdir()

            product_file = cleaned_dir / "single.json"
            product_file.write_text(json.dumps({"source": "Amazon", "name": "Phone", "price": 10}), encoding="utf-8")

            with patch("data_analysis.analyzer.CLEANED_DATA_DIR", str(cleaned_dir)):
                df = analyzer.load_cleaned_data()

            self.assertEqual(len(df), 1)
            self.assertEqual(df.iloc[0]["source"], "Amazon")

    def test_export_results_creates_csv_and_excel(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            analysis_dir = Path(tmpdir) / "analysis"

            with patch("data_analysis.analyzer.ANALYSIS_DATA_DIR", str(analysis_dir)):
                analyzer.export_results(pd.DataFrame({"metric": [1]}))

            self.assertTrue((analysis_dir / "analysis_results.csv").exists())
            self.assertTrue((analysis_dir / "analysis_results.xlsx").exists())


if __name__ == "__main__":
    unittest.main()
