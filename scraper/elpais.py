import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def is_spanish_website(driver: WebDriver, logger, timeout:int = 10) -> bool:
    """
    Checks the <html lang="..."> tag to confirm the site is in Spanish.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        timeout: Time to wait before the html loads

    Returns:
        bool: True if site language is Spanish, False otherwise.
    """
    try:
        # Wait for the <html> lang attribute to be set/updated dynamically
        WebDriverWait(driver, timeout).until(
            lambda d: d.find_element(By.TAG_NAME, "html").get_attribute("lang") is not None
        )
        html_tag = driver.find_element(By.TAG_NAME, "html")
        lang = html_tag.get_attribute("lang")
        logger.info(f"Detected page language: {lang}")
        return lang is not None and lang.lower().startswith("es")
    except Exception as e:
        logger.error(f"Error detecting the page")
        raise

def go_to_opinion_section(driver: WebDriver, logger, timeout:int = 10):
    """
    Navigate to El País Opinión section.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        timeout: Time to wait before the html loads
    """
    try:
        opinion_link = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Opinión"))
        )
        opinion_link.click()
        # Now wait for navigation to /opinion page to complete
        WebDriverWait(driver, timeout).until(
            lambda d: "/opinion" in d.current_url
        )
    except (TimeoutException, NoSuchElementException):
        logger.warning("Could not find clickable Opinión link, navigating directly to section.")
        driver.get("https://elpais.com/opinion/")

    except Exception as e:
        logger.error(f"Unexpected error navigating to Opinión")
        raise 


def get_first_n_opinion_articles(driver: WebDriver, logger, n: int = 5, timeout: int = 10) -> list[dict]:
    """
    Fetches the URLs for the first n Opinion articles listed on the page.
    Waits robustly for articles to appear.
    
    Args:
        driver (WebDriver): Selenium driver instance
        n (int): Number of articles to fetch (default 5)
        timeout (int): Seconds to wait for articles to appear (default 10)
    Returns:
        List[dict]: [{ 'url': str }]
    """
    articles_data = []
    try:
        # Wait for at least one <article> to be present
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
        article_elements = driver.find_elements(By.TAG_NAME, "article")
        if not article_elements:
            logger.warning("No <article> elements found on Opinión page.")
            return []

        for art in article_elements[:n]:
            try:
                link_elem = art.find_element(By.CSS_SELECTOR, "header > h2 > a")
                url = link_elem.get_attribute("href")
                if url:
                    articles_data.append({'url': url})
                else:
                    logger.warning("Article missing link URL.")
            except Exception as e:
                logger.warning(f"Failed to extract article link: {type(e).__name__}: {e}")

        logger.info(f"Collected {len(articles_data)} article URLs from Opinión section.")
        return articles_data

    except TimeoutException:
        logger.error(f"Timed out waiting for <article> elements on page.")
        return []
    except Exception as e:
        logger.exception(f"Unexpected error while collecting article links: {e}")
        raise


def extract_article_details(driver, article_url, logger, timeout=10):
    """
    Loads a news article and extracts its title, content/summary, and cover image.
    Robust to missing elements and dynamic loading.

    Args:
        driver (WebDriver): Selenium driver instance
        article_url: Url of the article to fetch the details
        timeout (int): Seconds to wait for articles to appear (default 10)
    """
    driver.get(article_url)

    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article > header"))
        )
    except TimeoutException:
        logger.error(f"Timeout waiting for main article header at {article_url}")

    results = {
        "url": article_url,
        "title": None,
        "content": None,
        "cover_image_url": None,
    }

    try:
        try:
            header = driver.find_element(By.CSS_SELECTOR, "article > header")
        except Exception:
            logger.warning(f"No 'article > header' found at {article_url}, using <article> as fallback.")
            header = driver.find_element(By.TAG_NAME, "article")

        # Extract title (h1)
        try:
            results["title"] = header.find_element(By.TAG_NAME, "h1").text.strip()
        except Exception:
            logger.warning(f"Missing <h1> (title) in {article_url}")

        # Extract summary/content (h2)
        try:
            results["content"] = header.find_element(By.TAG_NAME, "h2").text.strip()
        except Exception:
            logger.warning(f"Missing <h2> (summary/content) in {article_url}")

        # Extract cover image (first img)
        try:
            results["cover_image_url"] = header.find_element(By.TAG_NAME, "img").get_attribute("src")
        except Exception:
            logger.info(f"No cover image found in header at {article_url}")

    except Exception as e:
        logger.error(f"Failed to extract article details from {article_url}: {type(e).__name__}: {e}")
        raise

    return results
