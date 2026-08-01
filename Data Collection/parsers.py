"""Utilities for parsing product HTML content."""

from bs4 import BeautifulSoup


def parse_product(html: str, source: str) -> dict:
    """Extract product details from HTML content."""
    if not html:
        return {
            "Source": source,
            "Product Name": None,
            "Price": None,
            "Specifications": {},
        }

    soup = BeautifulSoup(html, "html.parser")

    product_name_tag = (
        soup.select_one("h1")
        or soup.select_one(".product-title")
        or soup.select_one("meta[property='og:title']")
    )
    if product_name_tag and product_name_tag.name == "meta":
        product_name = product_name_tag.get("content", "").strip() or None
    else:
        product_name = product_name_tag.get_text(strip=True) if product_name_tag else None

    price_tag = soup.select_one(".price") or soup.select_one(".product-price")
    price = price_tag.get_text(strip=True) if price_tag else None

    specs = {}
    specs_container = soup.select_one(".specs table") or soup.select_one(".specs")

    if specs_container:
        for row in specs_container.select("tr"):
            cols = row.find_all(["th", "td"])
            if len(cols) >= 2:
                key = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                specs[key] = value

    return {
        "Source": source,
        "Product Name": product_name,
        "Price": price,
        "Specifications": specs,
    }
