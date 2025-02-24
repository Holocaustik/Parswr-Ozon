import stealth as stealth
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
import time
from pprint import pprint

from urls import urls


class Driver_Chrom():

    def __init__(self):
        self.test_url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
        self.ozon = 'https://www.ozon.ru'
        self.asd = 'http://whatismyipaddress.com'

    def loadChrome(self, headless=False):
        uc.TARGET_VERSION = 120
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--verbose')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')


        browser = uc.Chrome(headless=headless, options=chrome_options)
        return browser

    def loadChromTest(self, headless=False, proxy: str = None):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--verbose')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        service = Service(ChromeDriverManager().install())
        chrome_options.add_argument("start-maximized")
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', True)
        chrome_options.add_argument(f'--proxy-server={proxy}') if proxy else ''
        driver = webdriver.Chrome(options=chrome_options,
                                  service=service)

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        stealth(
            driver,
            Accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            proxy=proxy if proxy is not None else '',
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=False,
            run_on_insecure_origins=False,
        )

        return driver

if __name__ == "__main__":
    driver = Driver_Chrom().loadChromTest(headless=False)
    driver.get("https://www.ozon.ru")
    time.sleep()


