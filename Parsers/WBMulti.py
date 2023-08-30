import datetime
import json
import time
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
from other import remove_duplicates


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


    def parser_page(self, *args, **kwargs):
        page, brand = args[0]
        driver = Driver_Chrom().loadChromTest()
        url = f'https://catalog.wb.ru/brands/h/catalog?appType=1&brand={brand["url"]}&curr=rub&dest=-1257786&page={page}&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,1,31,66,22,110,48,71,114&sort=pricedown&priceU=150000%3B4679000&spp=0'
        driver.get(url)
        time.sleep(7)
        try: res = json.loads(driver.page_source.strip(urls['clean_json']))['data']['products']
        except: return
        self.get_data_main(res=res, brand=brand['brand'])
        driver.close()
        driver.quit()

    def get_data_main(self, res: list = [], brand: str = ''):
        for item in res:
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
        driver = Driver_Chrom().loadChromTest(headless=False)
        driver.execute_script("window.open('about:blank', '_blank');")
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[1])
        driver.get(seller_info['link'])
        time.sleep(3)
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
        except:
            pass
        driver.close()
        driver.quit()

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
        driver = Driver_Chrom().loadChromTest()
        driver.execute_script("window.open('about:blank', '_blank');")
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[1])
        driver.get(item_info['link'])
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, urls['WB']['xpath']['seller'])))
        seller = driver.find_element(By.XPATH, urls['WB']['xpath']['seller']).text
        self.result.append(('WB', seller, item_info['name_small'], item_info['price'], datetime.date.today().strftime('%d.%m.%Y')))
        self.result_new.append((item_info['company'], item_info['code'], item_info['price'], datetime.date.today().strftime('%d.%m.%Y')))

        driver.close()
        driver.quit()

    def get_save_result_too_google_sheets(self, result: list, range: str = '') -> None:
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=list(result), range=range)

    def multy_get_funk(self, tasks: list = None, function: object = None, max_workers: int = None, range_value: str = None, what_need_save: list = None):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            list(tqdm(executor.map(function, tasks), total=len(tasks), desc="Processing", ncols=100))
        if range_value is not None:
            print(what_need_save)
            self.get_save_result_too_google_sheets(what_need_save, range=range_value)

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

        tasks = [(page, url) for url in urls['WB']['brands']['STM'] for page in range(1, 30)]

        self.multy_get_funk(function=self.parser_page, tasks=tasks, max_workers=self.max_threads)

        unic_list = remove_duplicates(input_list=self.list_items, key='code')
        self.multy_get_funk(function=self.parser_item, tasks=unic_list, max_workers=self.max_threads, what_need_save=self.result, range_value=urls['google_sheets_name']['main_parser'])
        GoogleSheet(self.SPREADSHEET_ID_NEW).append_data(value_range_body=list(self.result_new),
                                                         range=urls['google_sheets_name']['main_parser_new'])

        filter_unic_seller = self.get_unic_seller_id(saved_id=saved_code_multy_seller, need_to_add=self.unic_seller)
        if len(filter_unic_seller) > 0:
            self.multy_get_funk(function=self.collecting_sellers, tasks=filter_unic_seller, max_workers=self.max_threads, what_need_save=self.list_seller, range_value=urls['google_sheets_name']['collecting_sellers'])
            GoogleSheet(self.SPREADSHEET_ID_NEW).append_data(value_range_body=list(self.list_seller),
                                                             range=urls['google_sheets_name']['collecting_sellers'])

        filter_unic_product = self.get_unic_product_id(saved_id=saved_code_multy_product, need_to_add=self.unic_code)
        if len(filter_unic_product) > 0:
            self.get_save_result_too_google_sheets(filter_unic_product, range=urls['google_sheets_name']['collecting_products'])
            GoogleSheet(self.SPREADSHEET_ID_NEW).append_data(value_range_body=list(filter_unic_product),
                                                             range=urls['google_sheets_name']['collecting_products'])


if __name__ == "__main__":
    ParserWB().parser_main()
