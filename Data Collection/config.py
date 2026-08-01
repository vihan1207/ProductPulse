"""Configuration settings for the data collection module.

This file is the single source of truth for project paths and basic settings.
Keeping everything here makes the project easier to maintain, easier to test,
and easier to explain during interviews.
"""

# 1) Main configuration dictionary
# These values define the default folders and small runtime settings used by the pipeline.
DEFAULT_CONFIG = {
    "data_dir": "data",
    "raw_data_dir": "data/raw",
    "processed_data_dir": "data/processed",
    "cleaned_data_dir": "data/cleaned",
    "analysis_data_dir": "data/analysis",
    "reports_data_dir": "data/analysis/reports",
    "visualization_data_dir": "data/visualization",
    "user_agent": "ProductPulseBot/1.0",
    "timeout": 10,
}

# 2) Simple aliases for easier use in other modules
# These constants make the code more readable and reduce repetition across the project.
RAW_DATA_DIR = DEFAULT_CONFIG["raw_data_dir"]
PROCESSED_DATA_DIR = DEFAULT_CONFIG["processed_data_dir"]
CLEANED_DATA_DIR = DEFAULT_CONFIG["cleaned_data_dir"]
ANALYSIS_DATA_DIR = DEFAULT_CONFIG["analysis_data_dir"]
REPORTS_DATA_DIR = DEFAULT_CONFIG["reports_data_dir"]
VISUALIZATION_DATA_DIR = DEFAULT_CONFIG["visualization_data_dir"]


def get_config():
    """Return a fresh copy of the configuration dictionary.

    This prevents accidental changes to the shared defaults when another module
    modifies the returned dictionary.
    """
    return DEFAULT_CONFIG.copy()

