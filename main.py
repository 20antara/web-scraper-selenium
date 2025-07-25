import logging
from scraper.browser import get_webdriver
from scraper.elpais import is_spanish_website

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s:%(name)s: %(message)s"
    )
    
    driver = get_webdriver()

    try:
        # Task 1
        driver.get("https://elpais.com/")

        if is_spanish_website(driver):
            logging.info("Verified: El Pais is displayed in Spanish.")
        else:
            logging.warning("The website is not displayed in Spanish.")

            # Redirecting to Spanish Edition
            logging.info("Redirecting to Spanish edition URL...")
            driver.get("https://elpais.com/?ed=es")

            # Recheck after redirect
            if is_spanish_website(driver):
                logging.info("Successfully switched to Spanish edition.")
            else:
                logging.error("Failed to switch to Spanish edition.")
                raise Exception("Spanish edition could not be loaded.")

    except Exception as e:
        logging.exception(f"An error occurred: {e}")

    finally:
        driver.quit()
        logging.info("Browser closed.")

if __name__ == "__main__":
    main()

