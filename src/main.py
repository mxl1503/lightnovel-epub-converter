"""CLI entry point for the light novel EPUB converter."""

import argparse
import re
import sys

from .epub_builder import EpubBuilder
from .scraper import Scraper


def sanitize_title(title: str) -> str:
    """Sanitize title for use as a filename."""
    sanitized = title.strip()
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", sanitized)
    return sanitized or "untitled"


def validate_url(url: str) -> bool:
    """Validate that URL is for a supported site (readnovelfull.com)."""
    return url.strip().startswith("http") and "readnovelfull.com" in url


def get_input(prompt: str, validator=None, converter=None):
    """Get validated input from user with optional validator and converter."""
    while True:
        value = input(prompt).strip()
        if validator and not validator(value):
            print("Invalid input. Please try again.")
            continue
        if converter:
            try:
                return converter(value)
            except (ValueError, TypeError) as e:
                print(f"Invalid input: {e}. Please try again.")
                continue
        return value


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape light novels from readnovelfull.com and convert to EPUB."
    )
    parser.add_argument("--url", help="URL of the first chapter to download")
    parser.add_argument("--chapters", type=int, help="Number of chapters to download")
    parser.add_argument("--title", help="Title of the e-book")
    args = parser.parse_args()

    if args.url:
        first_chapter_url = args.url
        if not validate_url(first_chapter_url):
            print("Error: URL must be from readnovelfull.com and start with http")
            sys.exit(1)
    else:
        first_chapter_url = get_input(
            "Please enter the url of chapter to start downloading from (supports readnovelfull.com): ",
            validator=validate_url,
        )

    if args.chapters is not None:
        num_chapters = args.chapters
        if num_chapters <= 0:
            print("Error: Number of chapters must be positive")
            sys.exit(1)
    else:
        def parse_positive_int(value: str) -> int:
            val = int(value)
            if val <= 0:
                raise ValueError("Must be positive")
            return val

        num_chapters = get_input(
            "Please enter the number of chapters to download: ",
            converter=parse_positive_int,
        )

    if args.title:
        title = sanitize_title(args.title)
    else:
        raw_title = get_input("Please enter the title of the E-Book: ")
        title = sanitize_title(raw_title)

    with Scraper() as scraper:
        chapters = scraper.scrape_chapters(first_chapter_url, num_chapters)

    builder = EpubBuilder(title=title)
    builder.add_chapters(chapters)
    output_path = builder.write()

    print(f"Downloaded {len(chapters)} of {num_chapters} chapters.")
    print(f"Ebook called {title} now created at {output_path}!")


if __name__ == "__main__":
    main()
