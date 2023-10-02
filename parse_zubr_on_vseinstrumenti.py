import datetime
import json
import time
from selenium.webdriver.common.by import By
from browser import Driver_Chrom
from push_to_google_sheets import GoogleSheet


def parser_VI(): 
    brand_list = ['vihr-1007', 'zubr-665', 'interskol-19', 'hammer---2088444', 'champion-602/', 'husqvarna-4/', 'patriot-426/', 'greenworks-13753/', 'condtrol-649/', 'ada-890/']
    SPREADSHEET_ID = '1gZ6PBDwoROytLXYvdjuGLMNy1Jx6dlIUxYFs6O_8t74'
    result = []
    for brand in brand_list:
        url = f'https://spb.vseinstrumenti.ru/brand/{brand}/?asc=desc&orderby=price'
        driver = Driver_Chrom().loadChromTest(headless=True)
        driver.get(url)
        time.sleep(2)
        last_page = min(int(driver.find_elements(By.XPATH, '//a[@class="number"]')[-1].text), 50)
        for page in range(1, last_page):
            if page > 1:
                url = f'https://spb.vseinstrumenti.ru/brand/{brand}/page{page}/?asc=desc&orderby=price'
            else:
                url = f'https://spb.vseinstrumenti.ru/brand/{brand}/?asc=desc&orderby=price'
            driver.get(url)
            time.sleep(3)
            names = driver.find_elements(By.XPATH, '//a[@data-qa="product-name"]')
            prices = driver.find_elements(By.XPATH, '//p[contains(text(), " р.")]')
            for i in range(len(names)):
                brand = brand
                name = names[i].text
                try:
                    price = prices[i].text.strip(' р.').replace(' ', '')
                except:
                    price = 0
                date = datetime.date.today().strftime('%d. %m. %Y')
                result.append([brand, name, price, date])
    driver.close()
    driver.quit()

    data = result
    gs = GoogleSheet(SPREADSHEET_ID)
    gs.append_data(value_range_body=data, range="Парсер!A1:D1")


if __name__ == "__main__":
    parser_VI()
    # while True:
    #     now = time.localtime()
    #     if now.tm_hour == 9 and now.tm_min == 32 and now.tm_sec == 0:
    #         parser_VI()
    #         # Добавьте паузу, чтобы избежать множественного запуска в указанное время
    #         time.sleep(60)  # Подождите 60 секунд перед следующей проверкой
    #     else:
    #         # Добавьте паузу, чтобы избежать непрерывной проверки времени
    #         time.sleep(1)  # Подождите 1 секунду перед следующей проверкой

