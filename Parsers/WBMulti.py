import datetime
import json
import time
from pprint import pprint

from find_name import find_name
from selenium.webdriver.common.by import By
from browser import Driver_Chrom
from tqdm import tqdm
import concurrent.futures
from push_to_google_sheets import GoogleSheet
from urls import urls
import multiprocessing
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from other import remove_duplicates, get_multy_funk, extract_json_from_html


class ParserWB(object):

    def __init__(self, brand: list = [], company: str = None):
        self.SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
        self.SPREADSHEET_ID_NEW = '1Z1vbksKPw7xx07whBa3tHj6H7uoT7uQbx8WReSHCHC0'
        self.result = multiprocessing.Manager().list()
        self.result_collecting_products = multiprocessing.Manager().list()
        self.list_items = multiprocessing.Manager().list()
        self.max_threads = 10
        self.list_seller = multiprocessing.Manager().list()
        self.unic_seller = multiprocessing.Manager().list()
        self.unic_code = multiprocessing.Manager().list()
        self.result_new = multiprocessing.Manager().list()
        self.company = company
        self.brand = brand

    def parser_page(self, *args, **kwargs) -> None:
        page, brand = args[0]
        with Driver_Chrom().loadChromTest(headless=True) as driver:
            url = f'https://catalog.wb.ru/brands/h/catalog?appType=1&brand={brand["url"]}&curr=rub&dest=-1257786&page={page}'
            driver.get(url)
            time.sleep(3)
            try: res = extract_json_from_html(driver.page_source)
            except: return
        self.get_data_main(res=res, brand=brand['brand'])

    def get_data_main(self, res: list = [], brand: str = '') -> None:
        if res:
            for item in res["data"]["products"]:
                # print(item)
                data_main = {
                    'link': f'https://www.wildberries.ru/catalog/{int(item["id"])}/detail.aspx',
                    'name_small': find_name(item['name']),
                    'full_name': item['name'],
                    'price': int(item['salePriceU']) / 100,
                    'company': self.company,
                    'seller_id': item['supplierId'],
                    'code': item["id"]}
                self.unic_code.append(('ОПТ-ТРЕЙД', brand, 'WB', data_main['code'], data_main['full_name'], data_main['name_small'], data_main['link'], data_main['seller_id']))
                self.unic_seller.append({'seller_id': data_main["seller_id"], 'link': data_main['link']})
                self.list_items.append(data_main)

    def collecting_sellers(self, seller_info: dict = None) -> None:
        with Driver_Chrom().loadChromTest(headless=False) as driver:
            driver.execute_script("window.open('about:blank', '_blank');")
            window_handles = driver.window_handles
            driver.switch_to.window(window_handles[1])
            driver.get(seller_info['link'])
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, urls['WB']['xpath']['seller'])))
            seller = driver.find_element(By.XPATH, urls['WB']['xpath']['seller']).text
            try:
                button = driver.find_element(By.XPATH, '//span[@class = "seller-info__tip-info tip-info-gray"]')
                button.click()
                time.sleep(1)
                result = driver.find_elements(By.XPATH, '//div[@class = "tooltip__content"]')[-1].text.splitlines()
                name, adress, ogrn, kpp = self.find_seller_info(result=result)
                seller_link = f'https://www.wildberries.ru/seller/{seller_info["seller_id"]}'
                self.list_seller.append(('WB', seller_info['seller_id'], seller, seller_link, name, ogrn, kpp, adress))
            except: pass

    def find_seller_info(self, result: list = []) -> list:
        if len(result) == 2:
            name = result[0]
            ogrn = result[1]
            kpp = ''
            adress = ''
        if len(result) == 3:
            name = result[0]
            adress = ''
            ogrn = result[2]
            kpp = result[3]
        if len(result) == 4:
            name = result[0]
            adress = result[1]
            ogrn = result[2]
            kpp = result[3]
        else:
            name, adress, ogrn, kpp = ['', '', '', '', ]
        return [name, adress, ogrn, kpp]

    def parser_item(self, item_info: dict = None) -> None:
        try:
            with Driver_Chrom().loadChromTest(headless=True) as driver:
                url = f'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={item_info["code"]}'
                driver.get(url)
                time.sleep(1)
                seller = extract_json_from_html(driver.page_source)["data"]["products"][0]["supplier"]
                self.result.append(('WB', seller, item_info['name_small'], item_info['price'], datetime.date.today().strftime('%d.%m.%Y')))
                self.result_new.append((item_info['company'], item_info['code'], item_info['price'], '', '', datetime.date.today().strftime('%d.%m.%Y')))
        except:
            return

    def get_unic_seller_id(self, saved_id: list = [], need_to_add: list = []) -> list:
        unique_seller_id = set()
        result = []
        for item in need_to_add:
            if item['seller_id'] not in unique_seller_id and str(item['seller_id']) not in saved_id:
                result.append(item)
                unique_seller_id.add(item['seller_id'])
        return result

    def get_unic_product_id(self, saved_id: list = [], need_to_add: list = []) -> list:
        unique_product_id = set()
        result = []
        for item in need_to_add:
            if item[3] not in unique_product_id and str(item[3]) not in saved_id:
                result.append(item)
                unique_product_id.add(item[3])
        return result

    def parser_main(self) -> None:
        # собираем коды товаров и продавцов из справочника на Гугл листе
        saved_code = GoogleSheet().get_collecting_in_sheet()
        saved_code_multy_product = saved_code['product_id']
        saved_code_multy_seller = saved_code['seller_id']

        tasks = [(page, {'brand': brand, 'url': urls['WB']['brand'].get(brand)}) for brand in self.brand for page in range(1, 5)]
        get_multy_funk(function=self.parser_page, tasks=tasks, max_workers=self.max_threads, SPREADSHEET_ID=self.SPREADSHEET_ID)
        unic_list = remove_duplicates(input_list=self.list_items, key='code')
        get_multy_funk(function=self.parser_item, tasks=unic_list, max_workers=self.max_threads, what_need_save=self.result, range=urls['google_sheets_name']['main_parser'], SPREADSHEET_ID=self.SPREADSHEET_ID)
        time.sleep(15)
        # GoogleSheet(self.SPREADSHEET_ID_NEW).append_data(value_range_body=list(self.result_new),range=urls['google_sheets_name']['main_parser_new'])
        # filter_unic_seller = self.get_unic_seller_id(saved_id=saved_code_multy_seller, need_to_add=self.unic_seller)
        # if len(filter_unic_seller) > 0:
        #     get_multy_funk(function=self.collecting_sellers, tasks=filter_unic_seller, max_workers=self.max_threads, what_need_save=self.list_seller, range=urls['google_sheets_name']['collecting_sellers'], SPREADSHEET_ID=self.SPREADSHEET_ID)
        #     time.sleep(15)
        #     GoogleSheet(self.SPREADSHEET_ID_NEW).append_data(value_range_body=list(self.list_seller), range=urls['google_sheets_name']['collecting_sellers'])
        # filter_unic_product = self.get_unic_product_id(saved_id=saved_code_multy_product, need_to_add=self.unic_code)
        # if len(filter_unic_product) > 0:
        #     GoogleSheet(self.SPREADSHEET_ID_NEW).append_data(value_range_body=filter_unic_product, range=urls['google_sheets_name']['collecting_products'])
        #     time.sleep(15)
        #     GoogleSheet(self.SPREADSHEET_ID_NEW).append_data(value_range_body=list(filter_unic_product), range=urls['google_sheets_name']['collecting_products'])


if __name__ == "__main__":
    brand = ['hammer', 'wester']
    company = 'ОПТ-ТРЕЙД'
    ParserWB(company=company, brand=brand).parser_main()
