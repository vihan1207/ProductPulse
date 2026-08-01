"""Main data collection workflow for fetching, parsing, and saving product data."""

import sys
from pathlib import Path

# Make sure the project root is importable even when this module is run directly.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_collection.config import get_config
from src.data_collection.parsers import parse_product
from src.data_collection.storage import ensure_dirs, save_processed, save_raw
from src.data_collection.utils import fetch_html


class DataCollector:
    """Collect product data from a list of URLs."""

    def __init__(self, cfg=None):
        """Initialize the collector using the provided or default configuration."""
        self.cfg = cfg or get_config()
        ensure_dirs(self.cfg)

    def collect_from_urls(self, urls: list) -> list:
        """Fetch, parse, and save product details for each URL."""
        results = []

        if not urls:
            return results

        for index, url in enumerate(urls, 1):
            print(f"Fetching URL {index}/{len(urls)}: {url}")

            html = fetch_html(url, self.cfg["user_agent"], self.cfg["timeout"])
            if not html:
                continue

            save_raw(url, html, self.cfg)

            parsed = parse_product(html, source=url)
            if parsed:
                results.append(parsed)

        if results:
            save_processed(results, self.cfg)

        return results
