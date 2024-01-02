from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import ebooklib
from ebooklib import epub
import random

def go_to_next_chapter(driver):
    # Choose between Keys.RIGHT or Keys.D based on the website's functionality
    try:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.RIGHT)  
        # If chapter content isn't downloading properly, add a sleep in to allow
        # the website to load properly

        # time.sleep(1) 
    except Exception as e:
        print(f"Error while going to the next chapter: {e}")

def main():
    first_chapter_url = input("Please enter the url of chapter to start downloading from (supports readnovelfull.com): ")
    num_chapters = int(input("Please enter the number of chapters to download: "))
    title = input("Please enter the title of the E-Book: ")  

    driver = webdriver.Chrome()
    driver.get(first_chapter_url)
    
    chapters = []
    for i in range(num_chapters):
        try:
            print(f"Running for Chapter {i + 1}")

            content_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "chr-content"))
            )

            html_content = content_div.get_attribute('innerHTML')
            chapters.append(html_content)
        except NoSuchElementException:
            print(f"Chapter content not found for chapter {i + 1}")
        except TimeoutException:
            print(f"Timed out waiting for chapter {i + 1}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        go_to_next_chapter(driver)

    book = epub.EpubBook()

    # Set metadata
    random_num = random.randint(100000, 999999)
    book.set_identifier(f"id{random_num}")
    book.set_title(title)
    book.set_language("en")
    book.add_author("default")

    for i, chapter_content in enumerate(chapters, 1):
        # Create a chapter
        chapter = epub.EpubHtml(title=f"Chapter {i}", file_name=f"chap_{i:02d}.xhtml", lang="en")
        chapter.content = chapter_content

        # Add chapter to the book
        book.add_item(chapter)

        # Add chapter to the book's spine
        book.spine.append(chapter)

    # Define the Table Of Contents
    book.toc = tuple(epub.Link(f"chap_{i:02d}.xhtml", f"Chapter {i}", f"chap{i}") for i in range(1, len(chapters) + 1))

    # Add default NCX and Navigation file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Read the CSS file
    with open("src/styles.css", "r") as css_file:
        style_content = css_file.read()
    nav_css = epub.EpubItem(uid="style_nav", file_name="src/styles.css", media_type="text/css", content=style_content)

    # Add CSS file
    book.add_item(nav_css)

    # Create the EPUB file
    epub.write_epub(f"created_ebooks/{title}.epub", book, {})

    driver.quit()

    print(f"Ebook called {title} now created in the created_ebooks directory!")

if __name__ == "__main__":
    main()