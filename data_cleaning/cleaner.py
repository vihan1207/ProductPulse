"""Cleaning utilities for product records.

This module prepares raw product data for storage and analysis.
It standardizes basic fields like source, name, price, and specifications.
"""

import re
from typing import Any, Optional


def normalize_price(price_str: Any) -> Optional[float]:
    """Convert a price value such as '$1,299.99' into a float.

    This function removes currency symbols, commas, and extra spaces,
    then returns a numeric value. If the input is empty or invalid,
    it returns None.
    """
    if price_str is None:
        return None

    # Convert non-string values to strings so the function stays robust.
    if not isinstance(price_str, str):
        price_str = str(price_str)

    # Keep only digits and the decimal point.
    cleaned_value = re.sub(r"[^\d.]", "", price_str)

    if not cleaned_value:
        return None

    # Protect against malformed values like "1.2.3".
    if cleaned_value.count(".") > 1:
        cleaned_value = cleaned_value.replace(".", "", cleaned_value.count(".") - 1)

    try:
        return float(cleaned_value)
    except ValueError:
        return None


def clean_record(record: dict) -> Optional[dict]:
    """Return a cleaned copy of a single product record.

    The function standardizes common fields so downstream code can work
    with a consistent structure.
    """
    if not record:
        return None

    cleaned = {}

    # Clean simple text fields.
    cleaned["source"] = str(record.get("source", "")).strip()
    cleaned["name"] = str(record.get("name", "")).strip()

    # Clean the price using a dedicated helper function.
    cleaned["price"] = normalize_price(record.get("price", ""))

    # Clean specifications into a normalized dictionary.
    specs = record.get("specifications", {})
    cleaned_specs = {}

    if isinstance(specs, dict):
        for key, value in specs.items():
            normalized_key = str(key).strip().lower()
            normalized_value = str(value).strip()

            if normalized_key and normalized_value:
                cleaned_specs[normalized_key] = normalized_value

    cleaned["specifications"] = cleaned_specs
    return cleaned

