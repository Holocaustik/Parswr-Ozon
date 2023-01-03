import datetime
import json
import re
import time
from selenium.webdriver.common.by import By
from browser import Driver_Chrom
from push_to_google_sheets import GoogleSheet


def krc_wb():
    SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
    data = []
    url_ozon = 'https://www.wildberries.ru/brands/hammer/stroitelnye-instrumenty?sort=pricedown&page='
    for page in range(1, 6):
        driver = Driver_Chrom().loadChrome(headless=True)
        driver.get(f'{url_ozon}{page}')
        time.sleep(5)
        divs = driver.find_elements(By.XPATH, '//div[contains(@class, "product-card__wrapper")]')
        link_class = driver.find_elements(By.XPATH, '//div[@class="product-card__tip-wrap"]//following::div[1]//img')
        result = []

        for item in divs:
            class_name = item.find_element(By.XPATH, '//span[contains(@class, "goods-name")]').get_attribute('class')
            price_class = item.find_element(By.XPATH, '//span[contains(@class, "lower-price")]').get_attribute('class')
            pre = item.find_element(By.CLASS_NAME, 'j-thumbnail').get_attribute('src')
            name = item.find_element(By.CLASS_NAME, class_name).text
            price = item.find_element(By.CLASS_NAME, price_class).text
            test_name = name.split()
            clean_name_str = ' '.join([i if re.search('[a-zA-Z]', i) else '' for i in test_name])
            clean_name_number = ' '.join([i if re.search('[0-9 -]', i) else '' for i in test_name])
            new_name = f'HAMMER {clean_name_str.strip().strip(",").strip("  2x2Ач LiION").strip("   SDS+").strip("  1x1.5Ач LiION").replace("&#X2F;", "/").replace("&#34;", "").replace("Flex ", "")}' if len(clean_name_str) > 0 else clean_name_number.strip(',')
            end_index = pre.index('/images')
            new_link = pre[:end_index]
            result.append([price, new_link, new_name])
        driver.close()
        driver.quit()
        for item in result:
            info_card = '/info/ru/card.json'
            info_sales = '/info/sellers.json'
            new_driver = Driver_Chrom().loadChrome(headless=True)
            new_url = f'{item[1]}{info_sales}'
            new_driver.get(new_url)
            time.sleep(5)
            sales_name = json.loads(new_driver.page_source.strip('<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">'))['trademark']
            data.append(['WB', sales_name, item[2], item[0], datetime.date.today().strftime('%d. %m. %Y')])
            new_driver.close()
            new_driver.quit()
    gs = GoogleSheet(SPREADSHEET_ID)
    gs.append_data(value_range_body=data, range="парсер OZON WB!A1:E1")


if __name__ == "__main__":
    krc_wb()

