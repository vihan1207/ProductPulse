import unittest
from unittest.mock import patch

from main import run_pipeline


class MainPipelineTests(unittest.TestCase):
    def test_run_pipeline_skips_when_no_record_is_returned(self) -> None:
        with patch("main.parse_product", return_value=None):
            with patch("main.clean_record") as mock_clean_record:
                with patch("main.save_cleaned") as mock_save_cleaned:
                    run_pipeline("<html></html>", "Amazon", "sample.json")

        mock_clean_record.assert_not_called()
        mock_save_cleaned.assert_not_called()


if __name__ == "__main__":
    unittest.main()
