import datetime
import json
import time
from pprint import pprint
import re
from find_name import find_name
import jmespath
from selenium.webdriver.common.by import By
from browser import Driver_Chrom
from push_to_google_sheets import GoogleSheet
from urls import urls
import multiprocessing
from other import remove_duplicates, get_multy_funk, extract_json_from_html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from http.cookies import SimpleCookie


class ParserOzon(object):

    def __init__(self, brand: list = [], company: str = None):
        self.SPREADSHEET_ID_NEW = '1A8Trme4j0MxNgErgtWHFLqjQbkeBF_LBh7yBei9bp7I'
        self.result = multiprocessing.Manager().list()
        self.unic_params = multiprocessing.Manager().list()
        self.unic_code = multiprocessing.Manager().list()
        self.brand = brand
        self.company = company

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
        with Driver_Chrom().loadChromTest(headless=True) as driver:
            url = f'{brand["url"]}&page={page}'
            driver.get(url)
            driver.get_pinned_scripts()
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            try:
                all_json = extract_json_from_html(driver.page_source)
            except:
                return
            check = [key for key in all_json['widgetStates'] if key.startswith(urls['Ozon']['key_json']['main'])]
            res = jmespath.search(urls['Ozon']['jmespath']['STM']['main'], json.loads(all_json['widgetStates'][check[-1]])) if len(check) > 0 else ''
            for item in res:
                num = [item[2][0], self.company]
                self.list_items.append(num)

    def parser_item(self, item) -> None:
        """
          Описание функции
            Эта функция парсит одну страницу с товаром. Собирает с нее данные:

            1 - seller (Название продавца)

            2 - price (Цена без карты)

            Все это записывается в итоговый список self.result

          Эта функция принимает 1 аргумент в формате словарь. Из него используется:

          1 - name_small (Модель товара)

          2 - price (Цена без карты)

          3 - link (Ссылка на товар, который парсим)

          """
        code, link = item
        with Driver_Chrom().loadChromTest(headless=True) as driver:
            driver.get(f'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url={link}/?layout_container=pdpPage2column&layout_page_index=2')
            driver.get_pinned_scripts()
            time.sleep(2)
            driver.refresh()
            try:
                all_json = extract_json_from_html(driver.page_source)
                check = [key for key in all_json['widgetStates'] if key.startswith(urls['Ozon']['key_json']['tth'])]
                num = json.loads(all_json['widgetStates'][check[-1]])["characteristics"] if len(check) > 0 else ''
                if len(num) > 0:
                    resalt_good = {code: {}}
                    for item in num[0]["short"]:
                        param = item["name"]
                        value = item["values"][0]["text"].replace('\n', ' ')
                        if param not in self.unic_params: self.unic_params.append(param)
                        resalt_good[code][param] = value
                    self.result.append(resalt_good)
                else:
                    return
            except:
                return

    def extract_data(self,  dicts_list, keys_list):
        keys = list(keys_list)
        keys.insert(0, "SKU")
        data_rows = list(map(lambda d: [int(list(d.keys())[0])] + [d[list(d.keys())[0]].get(k, '') for k in keys_list], dicts_list))
        return [keys] + data_rows

    def get_tth(self):
        goods = filter(lambda x: int(x[17]) > -10, GoogleSheet().get_current_stock(self.SPREADSHEET_ID_NEW, "Компрессоры!A2:AC2000")["values"])
        tasks = list(map(lambda x: [x[0], x[23]], goods))
        get_multy_funk(tasks, self.parser_item, max_workers=10)
        num = self.extract_data(self.result, list(set(self.unic_params)))
        GoogleSheet().append_data_FoxWeld(self.SPREADSHEET_ID_NEW, f'Справочник!A1:F1', num)


    def parser_main(self) -> None:

        # создаем связку страница и ссылка для задачника
        tasks = [(page, {'brand': brand, 'url': urls['Ozon']['url']['brand'].get(brand)}) for brand in self.brand for
                 page in range(1, 10)]
        # собираем все ссылки на товары. Сразу запускается по max_workers окон
        get_multy_funk(tasks=tasks, function=self.parser_page, max_workers=5,
                       range=urls['google_sheets_name']['main_parser_Ozon_anal'], what_need_save=self.list_items,
                       SPREADSHEET_ID=self.SPREADSHEET_ID_NEW)

if __name__ == "__main__":
    brand = ["All"]
    company = 'Шурик 18В 2 АКБ'
    ParserOzon(brand=brand, company=company).get_tth()
