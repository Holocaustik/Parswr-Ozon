import stealth as stealth
import undetected_chromedriver
from selenium import webdriver
from selenium_stealth import stealth
import time

class Driver_Chrom():

    def __init__(self):
        self.test_url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
        self.ozon = 'https://www.ozon.ru'
        self.asd = 'http://whatismyipaddress.com'

    def loadChrome(self, headless=True):
        chrome_options = undetected_chromedriver.ChromeOptions()
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--verbose')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')


        browser = undetected_chromedriver.Chrome(headless=headless, options=chrome_options)
        return browser

    def loadChromTest(self, headless=True):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("start-maximized")
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=chrome_options,
                                  executable_path=r"/Users/vladimirivliev/PycharmProjects/pythonProject1/chromdirectory/chromedriver")

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
            # user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36",
            Accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=False,
            run_on_insecure_origins=False,
        )

        # # url = "https://bot.sannysoft.com/"
        # url = "https://leroymerlin.ru/search/?q=hammer"
        # # url = "https://market.yandex.ru/search?cvredirect=1&text=hammer&rs=eJwzamEOYCxgPMrIkKBkCyQZuEDkgxs2QHKB-k6QSMMekEgrSIRBBsRecAxMHgWLbwCpVzhiBSQb7oNEGsrBKvlA4glzQeyGUBD7QBNI1sEfLF4OYh_g2gsyZwJIZMEmkIiCHtjMSJAuhxSwG9hAahQUQGocLlmDRNpB4gdK9oPM8QGpZ1gJtuU_WJcYSH1CGNgXJ8F6_4LN2QUSaXgGNmE1mJ2xG6R3OthVbWCRk2ATHoPNbwfJJoiCxdXBbvsIElfQBbNDwfaqgl3ODDbfFmxXGjg0PMCkO1jvemtw2IL1uoB1hYLVXwT7VBHsWk4rABUChdQ%2C&allowCollapsing=1&local-offers-first=1"
        # driver.get(url)
        # time.sleep(25)
        # driver.quit()
        return driver

