import datetime
import json
import time
from pprint import pprint
from find_name import find_name
import jmespath
from selenium.webdriver.common.by import By
from browser import Driver_Chrom
from push_to_google_sheets import GoogleSheet
from urls import urls
import concurrent.futures
from tqdm import tqdm
import multiprocessing
from other import remove_duplicates


class ParserOzon():

    def __init__(self):
        self.SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
        self.result = multiprocessing.Manager().list()
        self.list_items = multiprocessing.Manager().list()
        self.unic_code = multiprocessing.Manager().list()

    def parser_page(self, page: int = 1, url=None) -> None:
        driver = Driver_Chrom().loadChromTest()
        driver.get(f'{url}&page={page}&sorting=price_desc')
        time.sleep(2)
        all_json = json.loads(driver.page_source.strip(urls['clean_json']))
        check = [key for key in all_json['widgetStates'] if key.startswith(urls['Ozon']['key_json']['main'])]
        res = jmespath.search(urls['Ozon']['jmespath']['STM']['main'], json.loads(all_json['widgetStates'][check[0]])) if len(check) > 0 else ''
        [self.list_items.append({'link': f'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=%2Fproduct/{item[2][0]}',
                                 'name': find_name(item[0][0]),
                                 'price': item[1][0].strip(' ₽').strip(' ').replace('\u2009', ''),
                                 'code': item[2][0]}) for item in res]
        driver.close()
        driver.quit()




    def parser_item(self, item_info: dict = None) -> None:
        driver = Driver_Chrom().loadChromTest()
        driver.get(item_info['link'])
        time.sleep(2)
        find_seller = driver.find_elements(By.XPATH, urls['Ozon']['xpath']['seller'])
        seller = find_seller[-1].text if len(find_seller) > 1 else find_seller[0].text if len(find_seller) > 0 else ''
        try: price = driver.find_element(By.XPATH, urls['Ozon']['xpath']['price']).text.strip(' ₽').strip(' ').replace('\u2009', '')
        except: price = item_info['price']
        self.result.append(('OZON', seller, item_info['name'], price, datetime.date.today().strftime('%d.%m.%Y')))
        driver.close()
        driver.quit()

    def get_save_result_too_google_sheets(self, result: list) -> None:
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=list(result), range="парсер OZON WB!A1:E1")

    def parser_main(self) -> None:
        for url in urls['Ozon']['url']['STM']:
            self.parser_page(page=1, url=url)
            self.parser_item(self.list_items[0])



if __name__ == "__main__":
    ParserOzon().parser_main()
