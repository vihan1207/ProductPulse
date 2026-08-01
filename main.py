"""Main entry point for the ProductPulse pipeline.

This file shows the full workflow in a simple, interview-friendly order:
1. Parse raw product data from HTML.
2. Clean the parsed record.
3. Save the cleaned output.
4. Load the cleaned data and export analysis results.
5. Create simple visualizations from the analysis data.
"""

import sys
from pathlib import Path

# Make sure the project root is importable when this file is run directly.
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_analysis.analyzer import analyze_data, export_results, load_cleaned_data
from data_cleaning.cleaner import clean_record
from data_reporting.report_generator import generate_reports, load_visualization
from src.data_collection.collector import DataCollector
from src.data_collection.parsers import parse_product
from src.data_collection.storage import save_cleaned
from visualization.visualizer import load_analysis_data, save_visualizations


def run_pipeline(html: str, source: str, filename: str) -> None:
    """Run the parsing, cleaning, and saving steps for one product page."""
    print(f"Processing product from source: {source}")

    # Step 1: Extract product data from the HTML content.
    record = parse_product(html, source)

    # If parsing did not return a valid record, stop early.
    if not record:
        print("No product record was produced. Pipeline stopped for this item.")
        return

    # Step 2: Clean the extracted data into a standard format.
    cleaned_record = clean_record(record)

    # Step 3: Save the cleaned result to a JSON file.
    save_cleaned(cleaned_record, filename)

    print(f"Saved cleaned output to: {filename}")


def run_analysis() -> None:
    """Load cleaned data, analyze it, and export the results."""
    # Step 1: Load the cleaned JSON files into a single DataFrame.
    df = load_cleaned_data()

    # If no cleaned data is available, stop early.
    if df.empty:
        print("No cleaned data found. Analysis was skipped.")
        return

    # Step 2: Create simple analysis results from the data.
    results = analyze_data(df)

    # Step 3: Export the results for business review.
    export_results(results)
    print("Analysis complete. Results were saved in the data/analysis folder.")


def get_sample_html() -> str:
    """Return sample HTML from a local file if available, otherwise use a built-in fallback."""
    sample_html_path = PROJECT_ROOT / "sample_product.html"

    if sample_html_path.exists():
        with sample_html_path.open("r", encoding="utf-8") as handle:
            return handle.read()

    return """
    <html>
      <body>
        <h1>Sample Product</h1>
        <div class="price">$199.99</div>
        <div class="specs">
          <table>
            <tr><th>Brand</th><td>ExampleBrand</td></tr>
            <tr><th>Color</th><td>Black</td></tr>
          </table>
        </div>
      </body>
    </html>
    """


def run_visualization() -> None:
    """Load analysis data and create simple charts for presentation."""
    print("Starting visualization step...")

    analysis_df = load_analysis_data()
    if analysis_df.empty:
        print("No analysis data found. Visualization was skipped.")
        return

    save_visualizations(analysis_df)
    print("Visualizations are complete. Charts were saved as images.")


def main() -> None:
    """Run the pipeline and analysis in a clear, easy-to-follow flow."""
    print("Starting ProductPulse pipeline...")

    # Step 1: Use sample HTML so the pipeline always has something to process.
    html_content = get_sample_html()
    run_pipeline(html_content, source="Amazon", filename="cleaned_product.json")

    # Step 2: Optionally collect several products from URLs using the collector.
    collector = DataCollector()
    urls = [
        "https://a.co/d/05BQPo5B",
        "https://a.co/d/0eRESLXw",
    ]

    try:
        results = collector.collect_from_urls(urls)
        print(f"Collected {len(results)} products.")
    except Exception as exc:
        print(f"Data collection step skipped due to an error: {exc}")

    # Step 3: Run the analysis step after collection or cleaning.
    run_analysis()

    # Step 4: Run the visualization step after analysis results are ready.
    run_visualization()

    # Step 5: Generate business-ready reports from the visualization data.
    run_reporting()

    print("ProductPulse pipeline finished successfully.")


def run_reporting() -> None:
    """Load visualization data and generate business reports."""
    print("Generating reports from the latest analysis...")

    visualization_df = load_visualization()
    if visualization_df.empty:
        print("No visualization data found. Reporting was skipped.")
        return

    # Generate Excel and CSV reports for presentation or sharing.
    generate_reports(visualization_df)
    print("Reporting completed. Reports were exported.")

if __name__ == "__main__":
    main()


