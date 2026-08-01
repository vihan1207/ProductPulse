"""Compatibility wrapper for the cleaner module used by the test suite."""

from pathlib import Path
import importlib.util

_module_path = Path(__file__).resolve().parent.parent / "data_cleaning" / "cleaner.py"
_spec = importlib.util.spec_from_file_location("cleaner_module", _module_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Unable to load cleaner module from {_module_path}")

_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

normalize_price = _module.normalize_price
clean_record = _module.clean_record
