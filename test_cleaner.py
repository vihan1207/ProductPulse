import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "Data Cleaning" / "cleaner.py"
SPEC = importlib.util.spec_from_file_location("cleaner_module", MODULE_PATH)
cleaner_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(cleaner_module)


class CleanerTests(unittest.TestCase):
    def test_normalize_price_removes_currency_symbols_and_commas(self) -> None:
        self.assertEqual(cleaner_module.normalize_price("$1,299.99"), 1299.99)
        self.assertEqual(cleaner_module.normalize_price(""), None)

    def test_clean_record_normalizes_basic_fields(self) -> None:
        record = {
            "source": "  Amazon  ",
            "name": "  Smart Phone  ",
            "price": "$799.00",
            "specifications": {"  RAM ": "  8GB  ", "Storage ": "256GB"},
        }

        cleaned = cleaner_module.clean_record(record)

        self.assertEqual(cleaned["source"], "Amazon")
        self.assertEqual(cleaned["name"], "Smart Phone")
        self.assertEqual(cleaned["price"], 799.0)
        self.assertEqual(cleaned["specifications"], {"ram": "8GB", "storage": "256GB"})


if __name__ == "__main__":
    unittest.main()
