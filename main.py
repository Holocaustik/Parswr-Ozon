import pychrome
import time
from pprint import pprint

from selenium import webdriver

# Создание экземпляра Chrome WebDriver
chrome_options = webdriver.ChromeOptions()

# Запустите Chrome в режиме без UI (без графического интерфейса)
chrome_options.add_argument("--headless")

# Запуск Chrome WebDriver
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"/Users/vladimirivliev/PycharmProjects/pythonProject1/chromdirectory/chromedriver")
driver.get("https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=https://www.ozon.ru/brand/hammer-26303172/?currency_price=1000.000%3B86670.000")
pprint(driver.page_source)
# Подключение к DevTools Protocol
browser = pychrome.Browser(url=driver.command_executor._url)
tab = browser.new_tab()

# Активация DevTools Protocol
tab.start()

# Активация режима Pretty Print
tab.Page.enable()
tab.Runtime.enable()

# Перейдите на нужную страницу
tab.Page.navigate(url="https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=https://www.ozon.ru/brand/hammer-26303172/?currency_price=1000.000%3B86670.000")

# Дождитесь загрузки страницы (или выполните другие действия)

# Активация Pretty Print (активация галочки автоформирования)
script = """
var config = {
  "indent": 4,
  "quote": "\"",
  "keySeparator": ": "
};
Runtime.evaluate({
  "expression": "JSON.stringify(JSON.parse(document.body.innerText), null, 4)",
  "returnByValue": true,
  "awaitPromise": true
}).then(result => {
  document.body.innerText = result.result.value;
  console.log("Pretty Print enabled");
});
"""
tab.Runtime.evaluate(expression=script)

# Дождитесь обработки Pretty Print (или выполните другие действия)

# Закрытие браузера и завершение сеанса
tab.stop()
tab.close_tab()
driver.quit()
