import json
import logging
import os
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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s"
)

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def set_browserstack_status(driver, status, reason):
    """
    Update BrowserStack session status.
    status: 'passed' or 'failed'
    reason: string
    """
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"%s", "reason": %s}}'
        % (status, json.dumps(reason))
    )

def test_bs_main():
    driver = None
    try:
        # Local driver method is patched by browserstack-sdk according to browserstack.yml
        options = ChromeOptions()
        options.set_capability('sessionName', 'ElPais Translation Test')
        driver = webdriver.Chrome(options=options)

        driver.get("https://elpais.com/")

        # Language check
        if is_spanish_website(driver):
            logging.info("Verified: El País is displayed in Spanish.")
        else:
            logging.warning("The website is not displayed in Spanish.")
            driver.get("https://elpais.com/?ed=es")
            if is_spanish_website(driver):
                logging.info("Successfully switched to Spanish edition.")
            else:
                raise Exception("Spanish edition could not be loaded.")

        # Scraping articles from Opinion section
        # go_to_opinion_section(driver)
        driver.get("https://elpais.com/opinion/")
        article_links = get_first_n_opinion_articles(driver, n=5)
        articles = []
        for idx, art in enumerate(article_links):
            article = extract_article_details(driver, art['url'])
            articles.append(article)
            print(f"\nArticle {idx+1} -\nTitle: {article['title']}\nContent: {article['content']}")
            if article['cover_image_url']:
                img_filename = f"output/article_{idx+1}_cover.jpg"
                try:
                    download_image(article['cover_image_url'], img_filename)
                except Exception as imgerr:
                    logging.warning(f"Image download failed: {imgerr}")

        # Translating Spanish titles
        spanish_titles = [details["title"] for details in articles]
        english_titles = translate_text(spanish_titles, "es", "en")
        print("\nTranslation:")
        for idx, (es, en) in enumerate(zip(spanish_titles, english_titles)):
            print(f"Article {idx+1} - Spanish: {es} | English: {en}")

        # Repeated words
        print_repeated_words(english_titles, 2)

        set_browserstack_status(driver, "passed", "All tasks completed successfully.")
    except Exception as e:
        logging.exception(f"Test failed: {e}")
        # Show exception on BrowserStack dashboard
        # if driver:
        #     set_browserstack_status(driver, "failed", f"{type(e).__name__}: {e}")
        if driver and hasattr(driver, "session_id") and driver.session_id:
            set_browserstack_status(driver, "failed",f"{type(e).__name__}: {e}")

    finally:
        if driver:
            driver.quit()
            logging.info("Browser closed.")

if __name__ == "__main__":
    test_bs_main()