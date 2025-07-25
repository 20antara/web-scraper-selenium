import logging
import os
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

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

