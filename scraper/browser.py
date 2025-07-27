import logging
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

logger = logging.getLogger("webdriver")

def get_webdriver(
    browser: str = "chrome",
    headless: bool = True,
    window_size: str = "1920,1080"
) -> webdriver.Remote:
    """
    Returns a Selenium WebDriver instance for the selected browser.

    Args:
        browser (str): Browser type. One of: 'chrome', 'firefox', 'edge', 'safari', 'ie'
        headless (bool): Whether to run browser in headless mode (if supported)
        window_size (str): Browser window size (e.g. '1920,1080')

    Returns:
        WebDriver instance for the selected browser.

    Raises:
        ValueError: For unsupported browsers or bad window_size formats.
        NotImplementedError: If unsupported OS/browser combo is chosen.
        WebDriverException: If driver or browser is missing or misconfigured.
    """
    browser = browser.lower()
    logger.info(f"Initializing WebDriver for browser: '{browser}', headless={headless}.")

    # Parse and validate window_size
    width, height = 1920, 1080  # default fallback
    if window_size:
        try:
            width, height = [int(dim) for dim in window_size.split(",")]
        except Exception as ex:
            logger.warning(f"Invalid window_size '{window_size}', using default 1920x1080. Error: {ex}")

    try:
        if browser == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument('--headless=new')
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')
            options.add_argument(f'--window-size={width},{height}')
            logger.info("Launching Chrome WebDriver...")
            return webdriver.Chrome(options=options)

        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument('--headless')
            options.add_argument(f'--width={width}')
            options.add_argument(f'--height={height}')
            logger.info("Launching Firefox WebDriver...")
            return webdriver.Firefox(options=options)

        elif browser == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument('--headless=new')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'--window-size={width},{height}')
            logger.info("Launching Edge WebDriver...")
            return webdriver.Edge(options=options)

        elif browser == "safari":
            if sys.platform != "darwin":
                error_msg = "Safari WebDriver is only available on macOS."
                raise NotImplementedError(error_msg)
            # Safari headless support is limited
            logger.info("Launching Safari WebDriver...")
            return webdriver.Safari()

        elif browser == "ie":
            if not sys.platform.startswith("win"):
                error_msg = "Internet Explorer WebDriver is only available on Windows."
                raise NotImplementedError(error_msg)

            options = webdriver.IeOptions()
            logger.info("Launching Internet Explorer WebDriver...")
            return webdriver.Ie(options=options)

        else:
            error_msg = f"Unsupported browser: '{browser}'. Use one of: chrome, firefox, edge, safari, ie."
            raise ValueError(error_msg)
        
    except Exception as e:
        # Log and re-raise for caller to handle
        logger.error(f"Failed to initialize the '{browser}' WebDriver: {type(e).__name__}")
        raise 


