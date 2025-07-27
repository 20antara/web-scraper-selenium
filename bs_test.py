import json
import os
import logging
from scraper.elpais import (
    is_spanish_website,
    go_to_opinion_section,
    get_first_n_opinion_articles,
    extract_article_details,
)
from utils.image_downloader import download_image
from translator.api import translate_text
from analyzer.text_analysis import print_repeated_words
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver

from utils.logging import (
    setup_basic_logger,
    setup_session_logger
)

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# Setup basic logging for the entire script
setup_basic_logger()

def set_browserstack_status(driver, status, reason):
    """
    Update BrowserStack session status.
    status: 'passed' or 'failed'
    reason: string
    """
    try:
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"%s", "reason": %s}}'
            % (status, json.dumps(reason))
        )
    except Exception as e:
        logging.warning(f"Failed to set BrowserStack status: {type(e).__name__}: {e}")

def test_bs_main():
    logging.info("Remote Test Execution Started...")
    driver = None
    logger = None
    try:
        options = ChromeOptions()
        options.set_capability('sessionName', 'ElPais Translation Test')
        driver = webdriver.Chrome(options=options)
        driver.get("https://elpais.com/")

        logger = setup_session_logger(driver)
        
        # Task 1: Language check
        if is_spanish_website(driver, logger):
            logger.info("Verified: El País is displayed in Spanish.")
        else:
            logger.warning("The website is not displayed in Spanish.")
            logger.info("Redirecting to Spanish edition URL...")
            driver.get("https://elpais.com/?ed=es")
            if is_spanish_website(driver, logger):
                logger.info("Successfully switched to Spanish edition.")
            else:
                logger.error("Failed to switch to Spanish edition.")
                raise Exception("Spanish edition could not be loaded.")

        # Task 2: Scraping Articles from the Opinion Section
        go_to_opinion_section(driver, logger)
        logger.info("Navigated to the Opinion section")
        article_links = get_first_n_opinion_articles(driver, logger, n=5)
        if len(article_links) < 5:
            raise Exception("First five articles could not be extracted, check the website.")

        articles = []
        for idx, art in enumerate(article_links):
            article = extract_article_details(driver, art['url'], logger)
            articles.append(article)
            logger.info(f"\nArticle {idx+1} -\nTitle: {article['title']}\nContent: {article['content']}")
            if article['cover_image_url']:
                img_filename = f"output/article_{idx+1}_cover.jpg"
                try:
                    download_image(article['cover_image_url'], img_filename, logger)
                except Exception as imgerr:
                    logger.warning(f"Image download failed: {imgerr}")
        logger.info("Successfully scraped articles from the Opinion section.")

        # Task 3: Translating Titles
        logger.info("Translation from spanish to english using Rapid Translate Multi Traduction API:")
        spanish_titles = [details["title"] for details in articles]
        english_titles = translate_text(spanish_titles, logger, "es", "en")
        for idx, (es, en) in enumerate(zip(spanish_titles, english_titles)):
            logger.info(f"Article {idx+1} - Spanish: {es} | English: {en}")
        logger.info("Successfully translated Spanish titles to English.")

        # Task 4: Finding repeated words
        logger.info("Analysis if there are words repeating.")
        print_repeated_words(english_titles, logger, 2)
        logger.info("Successfully analysed words.")


        # Success
        caps = driver.capabilities
        platform = caps.get("platformName", caps.get("platform", "unknown")).replace(" ", "_")
        browser = caps.get("browserName", "unknown").replace(" ", "_")
        logger.info(f"Successfully tested on {browser} in platform {platform} !")    
        # Set BrowserStack session as passed
        set_browserstack_status(driver, "passed", "All tasks completed successfully.")

    except Exception as e:
        (logger or logging).exception(f"Test failed: {e}")
        if driver and hasattr(driver, "session_id") and driver.session_id:
            set_browserstack_status(driver, "failed", f"{type(e).__name__}: {e}")

    finally:
        if driver:
            driver.quit()
            (logger or logging).info("Browser closed.")

if __name__ == "__main__":
    test_bs_main()
