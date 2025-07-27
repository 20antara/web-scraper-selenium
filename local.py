import logging
import os
from scraper.elpais import (
    is_spanish_website,
    go_to_opinion_section,
    get_first_n_opinion_articles,
    extract_article_details,
)
from utils.image_downloader import download_image
from scraper.browser import get_webdriver
from translator.api import translate_text
from analyzer.text_analysis import print_repeated_words
from dotenv import load_dotenv
from utils.logging import (
        setup_basic_logger,
        setup_session_logger
        )

#Load Rapid API key for translation
load_dotenv() 
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

setup_basic_logger()

def main():

    driver = None 
    logger = None
    try:
        # Initialize Selenium WebDriver
        browser = "chrome"
        driver = get_webdriver(browser)
        logger = setup_session_logger(driver)

        driver.get("https://elpais.com/")
        logger.info("Navigated to elpais.com.")

        # Task 1
        if is_spanish_website(driver, logger):
            logger.info("Verified: El País is displayed in Spanish.")
        else:
            logger.warning("The website is not displayed in Spanish.")
            # Redirecting to Spanish Edition
            logger.info("Redirecting to Spanish edition URL...")
            driver.get("https://elpais.com/?ed=es")
            if is_spanish_website(driver, logger):
                logger.info("Successfully switched to Spanish edition.")
            else:
                logger.error("Failed to switch to Spanish edition.")
                raise Exception("Spanish edition could not be loaded.")
            
        # Task 2
        go_to_opinion_section(driver, logger)
        logger.info("Navigated to opinion section.")
        logger.info("Scraping articles from opinion section.")
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
                download_image(article['cover_image_url'], img_filename, logger)
        logger.info("Successfully scraped articles from the Opinion section.")

        # Task 3
        logger.info("Translation from spanish to english using Rapid Translate Multi Traduction API:")
        spanish_titles = [details["title"] for details in articles]
        english_titles = translate_text(spanish_titles, logger, "es", "en") 
        for idx, (es, en) in enumerate(zip(spanish_titles, english_titles)):
            logger.info(f"Article {idx+1} - Spanish: {es} | English: {en}")   
        logger.info("Successfully translated Spanish titles to English.")

        # Task 4
        logger.info("Analysis if there are words repeating.")
        print_repeated_words(english_titles, logger, 2)
        logger.info("Successfully analysed words.")

        # Success
        caps = driver.capabilities
        platform = caps.get("platformName", caps.get("platform", "unknown")).replace(" ", "_")
        browser = caps.get("browserName", "unknown").replace(" ", "_")
        logger.info(f"Successfully tested on {browser} in platform {platform} !")
        
    except Exception as e:
        (logger or logging).exception(f"An error occurred: {e}")

    finally:
        if driver:
            driver.quit()
            (logger or logging).info("Browser closed.")

if __name__ == "__main__":
    main()
