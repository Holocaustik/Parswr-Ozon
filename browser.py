from selenium import webdriver
from fake_useragent import UserAgent
from seleniumwire import webdriver
import undetected_chromedriver


class Driver_Chrom():
    def __init__(self):
        self.executable_path = '/Users/vladimirivliev/PycharmProjects/parser_ozon with_django/chromdirectory/chromedriver'
        self.test_url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
        self.ozon = 'https://www.ozon.ru'
        self.asd = 'http://whatismyipaddress.com'

    def loadChrome(self):
        download_dir = "Downloads"
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument(r'--user-data-dir=Users/vladimirivliev/Library/Application Support/Google/Chrome/Default')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument("--window-size=1920x1080")
        # chrome_options.add_argument("--disable-notifications")
        # chrome_options.add_argument('--verbose')
        # chrome_options.add_argument(r'--proxy-server=127.0.0.1:9050')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # if not os.path.isdir(download_dir):
        #     os.mkdir(download_dir)
        #     chrome_options.add_experimental_option("prefs", {
        #     "profile.default_content_settings.popups": False,
        #     "download.prompt_for_download": False,
        #     "download.directory_upgrade": True,
        #     "safebrowsing_for_trusted_sources_enabled": False,
        #     "safebrowsing.enabled": False
        #     })
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--disable-software-rasterizer')
        ua = UserAgent()
        user_agent = "user-agent=" + ua.random
        chrome_options.add_argument(user_agent)
        browser = undetected_chromedriver.Chrome(headless=True)
        # browser = webdriver.Chrome(executable_path=self.executable_path, chrome_options=chrome_options)

        return browser