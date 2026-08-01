"""Helper utilities for HTTP-based data collection."""

import requests
from typing import Optional


def fetch_html(url: str, user_agent: str, timeout: int = 10) -> Optional[str]:
    """Fetch HTML content from a URL and return it as text."""
    try:
        headers = {"User-Agent": user_agent}
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        print(f"Warning: failed to fetch {url}: {exc}")
        return None
