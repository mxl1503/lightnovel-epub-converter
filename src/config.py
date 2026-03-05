"""Configuration constants and paths for the light novel EPUB converter."""

from pathlib import Path

# Paths (robust to CWD)
SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "created_ebooks"
CSS_PATH = SRC_DIR / "styles.css"

# Scraping
CONTENT_SELECTOR = "chr-content"  # ID for readnovelfull.com
WEBDRIVER_TIMEOUT_SECONDS = 10

# EPUB metadata
DEFAULT_LANGUAGE = "en"
DEFAULT_AUTHOR = "default"
