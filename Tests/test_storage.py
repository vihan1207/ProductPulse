import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.data_collection.storage import save_cleaned, save_raw


class StorageTests(unittest.TestCase):
    def test_save_raw_uses_a_windows_safe_filename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {
                "raw_data_dir": str(Path(tmpdir) / "raw"),
                "processed_data_dir": str(Path(tmpdir) / "processed"),
            }

            output_path = save_raw("https://example.com", "<html></html>", config)
            saved_file = Path(output_path)

            self.assertTrue(saved_file.exists())
            self.assertNotIn(":", saved_file.name)

    def test_save_cleaned_writes_to_cleaned_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {
                "raw_data_dir": str(Path(tmpdir) / "raw"),
                "processed_data_dir": str(Path(tmpdir) / "processed"),
                "cleaned_data_dir": str(Path(tmpdir) / "cleaned"),
            }

            output_path = save_cleaned({"name": "Phone"}, "sample.json", config)
            saved_file = Path(output_path)

            self.assertTrue(saved_file.exists())
            self.assertEqual(saved_file.parent, Path(config["cleaned_data_dir"]))

    def test_save_cleaned_uses_default_config_when_none_is_provided(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {
                "raw_data_dir": str(Path(tmpdir) / "raw"),
                "processed_data_dir": str(Path(tmpdir) / "processed"),
                "cleaned_data_dir": str(Path(tmpdir) / "cleaned"),
            }

            with patch("src.data_collection.storage.get_config", return_value=config):
                output_path = save_cleaned({"name": "Phone"}, "sample.json")

            saved_file = Path(output_path)
            self.assertTrue(saved_file.exists())
            self.assertEqual(saved_file.parent, Path(config["cleaned_data_dir"]))


if __name__ == "__main__":
    unittest.main()
