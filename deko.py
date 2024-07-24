import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
from selenium_stealth import stealth

def loadChromTest(headless=False, proxy: str = None):
    chrome_options = Options()
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--verbose')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    if headless:
        chrome_options.add_argument("--headless")

    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')

    service = Service(executable_path=r"/Users/vladimirivliev/PycharmProjects/pythonProject1/chromdirectory/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            run_on_insecure_origins=False
            )

    # Дополнительные HTTP заголовки
    driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
        "headers": {
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    })

    # Эмуляция реального поведения пользователя
    def emulate_real_user_behavior(driver):
        actions = ActionChains(driver)
        actions.move_by_offset(100, 100).perform()  # Движение мыши
        time.sleep(random.uniform(1, 3))  # Случайные задержки

    return driver

# Пример использования
driver = loadChromTest(headless=False, proxy=None)
driver.get('https://spb.lemanapro.ru/product/ushm-bolgarka-hammer-usm900e-950vt-3000-12000-ob-min-125mm-90163662/')
time.sleep(5)  # Задержка для загрузки страницы

# # Эмуляция поведения пользователя
# emulate_real_user_behavior(driver)
