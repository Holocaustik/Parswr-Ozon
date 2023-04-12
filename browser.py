import undetected_chromedriver


class Driver_Chrom():
    def __init__(self):
        self.test_url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
        self.ozon = 'https://www.ozon.ru'
        self.asd = 'http://whatismyipaddress.com'

    def loadChrome(self, headless=False):
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