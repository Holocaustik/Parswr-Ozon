import datetime
import json
import re
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


class ParserOzon(object):

    def __init__(self):
        self.SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
        self.result = multiprocessing.Manager().list()
        self.result_collecting_products = multiprocessing.Manager().list()
        self.list_items = multiprocessing.Manager().list()
        self.unic_seller = multiprocessing.Manager().list()
        self.list_seller = multiprocessing.Manager().list()
        self.unic_code = multiprocessing.Manager().list()

    def parser_page(self, *args, **kwargs) -> None:
        """
          Описание функции
            Эта функция парсит одну страницу листинга. Собирает с нее данные
            1 - link (Ссылка на товар)
            2 - name_full (Полное наименование товара)
            3 - name_small (Модель товара)
            4 - price (Цена, если есть карта, то будет цена по карте, если нет, то обычная)
            5 - brand (Получает на входе)
            6 - code (Код товара на площадке)

            Все это записывается в список self.list_items
          Эта функция принимает 1 аргумент в формате словарь:

          :param arg1: название бренда
          :type arg1: str

          :param arg2: Ссылка, которую нужно парсить
          :type arg2: str
          """
        page, brand = args[0]
        driver = Driver_Chrom().loadChromTest()
        driver.get(f'{brand["url"]}&page={page}&sorting=price_desc')
        time.sleep(2)
        all_json = json.loads(driver.page_source.strip(urls['clean_json']))
        check = [key for key in all_json['widgetStates'] if key.startswith(urls['Ozon']['key_json']['main'])]
        res = jmespath.search(urls['Ozon']['jmespath']['STM']['main'], json.loads(all_json['widgetStates'][check[-1]])) if len(check) > 0 else ''
        for item in res:
            data = {
                'link': f'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=%2Fproduct/{item[2][0]}',
                 'name_full': item[0][0],
                 'name_small': find_name(item[0][0]),
                 'price': item[1][0].strip(' ₽').strip(' ').replace('\u2009', ''),
                 'brand': brand["brand"],
                 'code': item[2][0]}
            self.list_items.append(data)
            if item[2][0] not in self.saved_code['product_id']:
                self.unic_code.append(data)
                self.saved_code['product_id'].append(item[2][0])

        driver.close()
        driver.quit()

    def parser_item(self, item_info: dict = None) -> None:
        """
          Описание функции
            Эта функция парсит одну страницу с товаром. Собирает с нее данные
            1 - seller (Название продавца)
            2 - price (Цена без карты)

            Все это записывается в итоговый список self.result

          Эта функция принимает 1 аргумент в формате словарь. Из него используется:
          1 - name_small (Модель товара)
          2 - price (Цена без карты)

          """
        driver = Driver_Chrom().loadChromTest()
        driver.get(item_info['link'])
        time.sleep(2)
        all_json = json.loads(driver.page_source.strip(urls['clean_json']))
        seller = self.find_seller(all_json, 'seller_name')
        price = self.find_price(all_json) if self.find_price(all_json) is not None else item_info['price']
        self.result.append(('OZON', seller, item_info['name_small'], price, datetime.date.today().strftime('%d.%m.%Y')))
        driver.close()
        driver.quit()

    def find_seller(self, all_json: json = None, key_json: str = '') -> str:
        json_sales = [key for key in all_json['widgetStates'] if key.startswith(urls['Ozon']['key_json']['seller'])]
        if len(json_sales) > 0:
            result = jmespath.search(urls['Ozon']['jmespath']['STM'][key_json], json.loads(all_json['widgetStates'][json_sales[0]]))
            seller = result.replace('/seller/', '').replace('/', '') if isinstance(result, str) else result
        else:
            json_sales = [key for key in all_json['widgetStates'] if key.startswith(urls['Ozon']['key_json']['seller_1'])]
            result = jmespath.search(urls['Ozon']['jmespath']['STM'][key_json], json.loads(all_json['widgetStates'][json_sales[0]])) if len(json_sales) > 0 else ''
            seller = result.replace('/seller/', '').replace('/', '') if isinstance(result, str) else result if len(json_sales) > 0 else ''
        return seller if seller is not None else 'seller'

    def find_price(self, all_json: json = None) -> int:
        json_price = [key for key in all_json['widgetStates'] if key.startswith(urls['Ozon']['key_json']['webPrice'])]
        price = jmespath.search(urls['Ozon']['jmespath']['STM']['price'], json.loads(all_json['widgetStates'][json_price[0]])) if len(json_price) > 0 else ''
        return price.strip(' ₽').strip(' ').replace('\u2009', '') if price is not None else price

    def get_save_result_too_google_sheets(self, result: list, range: str = '') -> None:
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=list(result), range=range)

    def collecting_products(self, item_info: dict = None) -> None:
        if int(item_info['price']) > 999:
            driver = Driver_Chrom().loadChromTest()
            driver.get(item_info['link'])
            time.sleep(2)
            all_json = json.loads(driver.page_source.strip(urls['clean_json']))
            seller = self.find_seller(all_json, 'seller_id')
            self.result_collecting_products.append(('ОПТ-ТРЕЙД', item_info['brand'], 'OZON', item_info['code'], item_info['name_full'], item_info['name_small'], f'https://www.ozon.ru/product/{item_info["code"]}', seller))
            if seller not in self.saved_code['seller_id']:
                self.unic_seller.append({'link': f'https://www.ozon.ru/product/{item_info["code"]}', 'seller_id': seller})
                self.saved_code['seller_id'].append(seller)
            driver.close()
            driver.quit()

    def collecting_sellers(self, seller_info: dict = None) -> None:
        driver = Driver_Chrom().loadChromTest()
        driver.get(seller_info['link'])
        time.sleep(2)
        try:
            button = driver.find_element(By.XPATH, '//span[@class = "a2-b1 a2-c5 a2-f0"]')
            button.click()
            time.sleep(1)
            result = driver.find_elements(By.XPATH, '//p[@class = "j5p"]')
            try: name, adress, code = [item.text for item in result[:3]]
            except: name, adress, code = 'не нашли', 'не нашли', 'не нашли'
            find_seller = driver.find_elements(By.XPATH, urls['Ozon']['xpath']['seller'])
            seller_name = find_seller[-1].text if len(find_seller) > 1 else find_seller[0].text if len(find_seller) > 0 else ''
            seller_link = find_seller[-1].get_attribute('href') if len(find_seller) > 1 else find_seller[0].get_attribute('href') if len(find_seller) > 0 else ''
            self.list_seller.append(('Ozon', seller_info['seller_id'], seller_name, seller_link, name, code, '', adress))
        except:
            pass
        driver.close()
        driver.quit()

    def multy_get_funk(self, tasks: list = None, function: object = None, max_workers: int = None, range: str = None, what_need_save: list = None):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            list(tqdm(executor.map(function, tasks), total=len(tasks), desc="Processing", ncols=100))
        if range is not None:
            self.get_save_result_too_google_sheets(what_need_save, range=range)

    def parser_main(self) -> None:
        # собираем коды товаров и продавцов из справочника на Гугл листе
        self.saved_code = GoogleSheet().get_collecting_in_sheet()

        # создаем связку страница и ссылка для задачника
        tasks = [(page, brand) for brand in urls['Ozon']['url']['STM'] for page in range(1, 55)]

        # собираем все ссылки на товары. Сразу запускается по max_workers окон
        self.multy_get_funk(function=self.parser_page, tasks=tasks, max_workers=10)

        # из собранных ссылок филтруем только уникальные
        self.unic_list = remove_duplicates(input_list=self.list_items, key='code')

        # заходим в каждую карточку товара из списка уникальных ссылок и собираем данные. Сразу запускается по max_workers окон
        self.multy_get_funk(function=self.parser_item, tasks=self.unic_list, max_workers=10, what_need_save=self.result, range=urls['google_sheets_name']['main_parser'])

        if len(self.unic_code) > 0:
            self.multy_get_funk(function=self.collecting_products, tasks=self.unic_code, max_workers=10, what_need_save=self.result_collecting_products, range=urls['google_sheets_name']['collecting_products'])

        if len(self.unic_seller) > 0:
            self.multy_get_funk(function=self.collecting_sellers, tasks=self.unic_seller, max_workers=10, what_need_save=self.list_seller, range=urls['google_sheets_name']['collecting_sellers'])


if __name__ == "__main__":
    ParserOzon().parser_main()
