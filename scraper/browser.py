from selenium import webdriver

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

import sys

def get_webdriver(
    browser: str = "chrome",
    headless: bool = True,
    window_size: str = "1920,1080"
) -> webdriver.Remote:
    """
    Returns a Selenium WebDriver instance for the selected browser.
    
    Parameters:
        browser (str): Which browser to use. Options:
                       'chrome', 'firefox', 'edge', 'safari'
        headless (bool): Whether to run in headless mode.
        window_size (str): Size of the browser window, e.g. '1920,1080'
    
    Returns:
        WebDriver instance for the chosen browser.
    """
    browser = browser.lower()
    
    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
        options.add_argument(f'--window-size={window_size}')
        return webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        if window_size:
            options.add_argument(f'--width={window_size.split(",")[0]}')
            options.add_argument(f'--height={window_size.split(",")[1]}')
        return webdriver.Firefox(options=options)

    elif browser == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument('--headless=new')
        options.add_argument(f'--window-size={window_size}')
        return webdriver.Edge(options=options)

    elif browser == "safari":
        if sys.platform != "darwin":
            raise NotImplementedError("Safari WebDriver is only available on macOS.")
        # Safari does not yet support a documented headless mode
        return webdriver.Safari()

    else:
        raise ValueError(f"Unsupported browser: {browser}. Use one of: chrome, firefox, edge, safari.")

# # ===================
# # Usage Examples:
# # ===================

# # Chrome, headless (default)
# driver = get_webdriver()
# # Firefox, UI visible
# driver = get_webdriver(browser="firefox", headless=False)
# # Edge, headless, window size 1366x768
# driver = get_webdriver(browser="edge", headless=True, window_size="1366,768")

# # Will raise error if used on non-Mac, or if Safari is not installed
# # driver = get_webdriver(browser="safari")
