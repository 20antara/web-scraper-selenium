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

load_dotenv() 
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


def main(): 

    # Setup logging for the entire script
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s:%(name)s: %(message)s"
    )

    driver = None 

    try:
        # Initialize Selenium WebDriver
        driver = get_webdriver("firefox")
        
        driver.get("https://elpais.com/")

        # Task 1
        # Ensuring if the website is in spanish language
        if is_spanish_website(driver):
            logging.info("Verified: El País is displayed in Spanish.")
        else:
            logging.warning("The website is not displayed in Spanish.")

            # Redirecting to Spanish Edition
            logging.info("Redirecting to Spanish edition URL...")
            driver.get("https://elpais.com/?ed=es")

            if is_spanish_website(driver):
                logging.info("Successfully switched to Spanish edition.")
            else:
                logging.error("Failed to switch to Spanish edition.")
                raise Exception("Spanish edition could not be loaded.")
            
        # Task 2
        # Scraping Articles from the Opinion Section
        go_to_opinion_section(driver)
        article_links = get_first_n_opinion_articles(driver, n=5)
        articles = []
        for idx, art in enumerate(article_links):
            article = extract_article_details(driver, art['url'])
            articles.append(article)
            print(f"\nArticle {idx+1} -\nTitle: {article['title']}\nContent: {article['content']}")
            if article['cover_image_url']:
                img_filename = f"output/article_{idx+1}_cover.jpg"
                download_image(article['cover_image_url'], img_filename)
        logging.info("Successfully scraped articles from the Opinion section.")

        # Task 3
        # Translating Spanish titles to English
        spanish_titles = [details["title"] for details in articles]
        english_titles = translate_text(spanish_titles, "es", "en") 
        print("\nTranslation:")
        for idx, (es, en) in enumerate(zip(spanish_titles, english_titles)):
            print(f"Article {idx+1} - Spanish: {es} | English: {en}")   
        logging.info("Successfully translated Spanish titles to English.")

        # Task 4
        # Finding repeated words
        print_repeated_words(english_titles, 2)
        logging.info("Successfully analysed words.")
    except Exception as e:
        logging.exception(f"An error occurred: {e}")

    finally:
        if driver:
            driver.quit()
            logging.info("Browser closed.")

if __name__ == "__main__":
    main()
