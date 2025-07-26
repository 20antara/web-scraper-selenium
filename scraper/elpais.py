import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

def is_spanish_website(driver: WebDriver) -> bool:
    """
    Checks the <html lang="..."> tag to confirm the site is in Spanish.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Returns:
        bool: True if site language is Spanish, False otherwise.
    """
    try:
        html_tag = driver.find_element(By.TAG_NAME, "html")
        lang = html_tag.get_attribute("lang")
        logger.info(f"Detected page language: {lang}")
        return lang is not None and lang.lower().startswith("es")
    except Exception as e:
        logger.error(f"Error detecting the page")
        raise

def go_to_opinion_section(driver: WebDriver):
    """Navigate to El País Opinión section."""
    try:
        # opinion_link = driver.find_element(By.LINK_TEXT, "Opinión")
        opinion_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Opinión"))
        )

        opinion_link.click()

    except NoSuchElementException:
        logger.warning("Could not find Opinión link, navigating directly.")
        driver.get("https://elpais.com/opinion/")

    except Exception as e:
        logger.error(f"Unexpected error navigating to Opinión")
        raise 

    time.sleep(2)  # Wait for navigation

def get_first_n_opinion_articles(driver: WebDriver, n: int = 5) -> list[dict]:
    """
    Fetches the URLs for the first n Opinion articles listed on the page.
    Returns: List of dicts with structure { 'url': str }
    """
    articles_data = []     
    article_elements = driver.find_elements(By.TAG_NAME, "article") 
    for art in article_elements[:n]:
        try:
            link_elem = art.find_element(By.CSS_SELECTOR, "header h2 a")
            url = link_elem.get_attribute("href")
            articles_data.append({'url': url})
        except Exception as e:
            logger.warning(f"Failed to extract article link")
            raise

    return articles_data


def extract_article_details(driver: WebDriver, article_url: str) -> dict:
    """
    Extracts title, summary/content, and cover image from an article.
    Assumes: In article > header there is one h1, one h2, and one img.
    """
    driver.get(article_url)
    time.sleep(1.5)  # Use WebDriverWait in production

    results = {
        "url": article_url,
        "title": None,
        "content": None,
        "cover_image_url": None,
    }
    try:
        # Get <header> inside <article>
        header = driver.find_element(By.CSS_SELECTOR, "article > header")

        # h1: Title
        try:
            results["title"] = header.find_element(By.TAG_NAME, "h1").text.strip()
        except Exception:
            results["title"] = None

        # h2: Summary/content
        try:
            results["content"] = header.find_element(By.TAG_NAME, "h2").text.strip()
        except Exception:
            results["content"] = None
            print("content")

        # img: Cover image
        try:
            results["cover_image_url"] = header.find_element(By.TAG_NAME, "img").get_attribute("src")
        except Exception:
            results["cover_image_url"] = None

    except Exception as e:
        logger.error(f"Failed to extract details from {article_url}")
        raise

    return results


