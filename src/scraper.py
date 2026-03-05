"""Selenium-based scraper for light novel chapters."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .config import CONTENT_SELECTOR, WEBDRIVER_TIMEOUT_SECONDS


class Scraper:
    """Scrapes light novel chapters from readnovelfull.com using Selenium."""

    def __init__(self):
        self.driver = webdriver.Chrome()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def fetch_chapter(self) -> str | None:
        """
        Fetch the current chapter's HTML content.
        Returns the innerHTML of the content div, or None on failure.
        """
        try:
            content_div = WebDriverWait(self.driver, WEBDRIVER_TIMEOUT_SECONDS).until(
                EC.presence_of_element_located((By.ID, CONTENT_SELECTOR))
            )
            return content_div.get_attribute("innerHTML")
        except NoSuchElementException:
            return None
        except TimeoutException:
            return None
        except Exception:
            return None

    def go_to_next_chapter(self) -> None:
        """Navigate to the next chapter using the right arrow key."""
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.RIGHT)
        except Exception as e:
            print(f"Error while going to the next chapter: {e}")

    def scrape_chapters(self, first_chapter_url: str, num_chapters: int) -> list[str]:
        """
        Scrape the requested number of chapters starting from the given URL.
        Returns a list of chapter HTML contents (may be shorter if some fail).
        """
        self.driver.get(first_chapter_url)
        chapters: list[str] = []

        for i in range(num_chapters):
            print(f"Running for Chapter {i + 1}")
            content = self.fetch_chapter()
            if content is not None:
                chapters.append(content)
            else:
                print(f"Chapter content not found for chapter {i + 1}")
            self.go_to_next_chapter()

        return chapters
