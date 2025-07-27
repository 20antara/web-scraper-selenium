import logging
import os
from selenium.webdriver.remote.webdriver import WebDriver

def get_bs_logfile_name(driver: WebDriver) -> str:
    """
    Generate a unique logfile name per session using capabilities/session info.
    Assumes BrowserStack SDK injects session details.
    """
    caps = driver.capabilities
    # Build a label from commonly set capability fields
    platform = caps.get("platformName", caps.get("platform", "unknown")).replace(" ", "_")
    browser = caps.get("browserName", "unknown").replace(" ", "_")
    browser_version = caps.get("browserVersion", caps.get("version", ""))
    device = caps.get("deviceName", caps.get("device", ""))
    # Format: logs/session_bstack_{platform}_{browser}_{version or device}.log
    if device:
        fname = f"logs/session_bstack_{platform}_{device}_{browser}.log"
    else:
        fname = f"logs/session_bstack_{platform}_{browser}_{browser_version}.log"
    return fname

def setup_session_logger(driver) -> logging.Logger:
    """
    Sets up a logger that writes to a unique file for this session.
    """
    logfile = get_bs_logfile_name(driver)
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    logger = logging.getLogger(logfile)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
    fh = logging.FileHandler(logfile, mode='w')
    fh.setFormatter(formatter)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(fh)
    return logger

def setup_basic_logger():
    """
    Setup basic logging for the entire script
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s:%(name)s: %(message)s"
    )
