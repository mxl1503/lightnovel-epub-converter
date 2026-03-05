"""EPUB building logic for light novel conversion."""

import uuid
from pathlib import Path

from ebooklib import epub

from .config import (
    CSS_PATH,
    DEFAULT_AUTHOR,
    DEFAULT_LANGUAGE,
    OUTPUT_DIR,
)


class EpubBuilder:
    """Builds EPUB files from scraped chapter content."""

    def __init__(self, title: str, author: str = DEFAULT_AUTHOR):
        self.title = title
        self.author = author
        self.book = epub.EpubBook()
        self.chapters: list[str] = []

        self._setup_metadata()

    def _setup_metadata(self) -> None:
        """Set EPUB metadata."""
        self.book.set_identifier(str(uuid.uuid4()))
        self.book.set_title(self.title)
        self.book.set_language(DEFAULT_LANGUAGE)
        self.book.add_author(self.author)

    def add_chapter(self, html_content: str) -> None:
        """Add a chapter's HTML content to the book."""
        self.chapters.append(html_content)

    def add_chapters(self, chapters: list[str]) -> None:
        """Add multiple chapters at once."""
        self.chapters.extend(chapters)

    def write(self, output_path: str | None = None) -> str:
        """
        Build and write the EPUB file.
        Returns the path to the written file.
        """
        path = output_path or str(OUTPUT_DIR / f"{self.title}.epub")

        for i, chapter_content in enumerate(self.chapters, 1):
            chapter = epub.EpubHtml(
                title=f"Chapter {i}",
                file_name=f"chap_{i:02d}.xhtml",
                lang=DEFAULT_LANGUAGE,
            )
            chapter.content = chapter_content
            self.book.add_item(chapter)
            self.book.spine.append(chapter)

        self.book.toc = tuple(
            epub.Link(f"chap_{i:02d}.xhtml", f"Chapter {i}", f"chap{i}")
            for i in range(1, len(self.chapters) + 1)
        )

        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        self._add_css()

        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        epub.write_epub(path, self.book, {})

        return path

    def _add_css(self) -> None:
        """Add the stylesheet to the EPUB."""
        style_content = CSS_PATH.read_text()
        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="styles/styles.css",
            media_type="text/css",
            content=style_content,
        )
        self.book.add_item(nav_css)
