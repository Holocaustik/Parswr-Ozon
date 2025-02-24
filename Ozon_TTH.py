import datetime
import json
import time
from pprint import pprint
import re
import pandas as pd
import pyautogui
import os

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
        self.SPREADSHEET_ID_NEW = '12N4FtooJWayK6sRS7RUA5kg1ohbil5Gw7stmjRNgYog'
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
        with Driver_Chrom().loadChromTest(headless=False) as driver:
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

    def parser_item_Ozon(self, item) -> None:
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
        with Driver_Chrom().loadChromTest(headless=False) as driver:
            url = f'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url={link}/?layout_container=pdpPage2column&layout_page_index=2'
            driver.get(url)
            driver.get_pinned_scripts()
            # Открываем новое окно
            driver.execute_script(f"window.open('{url}');")
            time.sleep(2)

            # Получаем все идентификаторы окон
            # window_handles = driver.window_handles
            #
            # # Переключаемся на новое окно
            driver.switch_to.window(driver.window_handles[1])
            driver.refresh()
            try:
                all_json = extract_json_from_html(driver.page_source)
                check = [key for key in all_json['widgetStates'] if key.startswith(urls['Ozon']['key_json']['tth'])]
                num = json.loads(all_json['widgetStates'][check[-1]])["characteristics"] if len(check) > 0 else ''
                # pprint(num)
                if len(num) > 0:
                    resalt_good = {code: {}}
                    for item in num[1]["short"] if len(num) > 1 else num[0]["short"]:
                        # print(item)
                        param = item["name"]
                        value = item["values"][0]["text"].replace('\n', ' ')
                        # print(f"{param} {value}")
                        if param not in self.unic_params: self.unic_params.append(param)
                        resalt_good[code][param] = value
                    self.result.append(resalt_good)
                else:
                    return
            except:
                return

    def parser_item_WB(self, item) -> None:
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
        print(item)
        code, Thumb = item
        with Driver_Chrom().loadChromTest(headless=True) as driver:
            pattern = r"https:\/\/basket-(\d+)\.wbbasket\.ru\/vol(\d+)\/part(\d+)\/"
            match = re.search(pattern, Thumb)
            basket = match.group(1)
            vol = match.group(2)
            part = match.group(3)
            for url in range(1, 20):
                try:
                    link = f'https://basket-{basket}.wbbasket.ru/vol{vol}/part{part}/{code}/info/ru/card.json'
                    driver.get(link)
                    all_json = extract_json_from_html(driver.page_source)["options"]
                    if len(all_json) > 0:
                        resalt_good = {code: {}}
                        for item in all_json:
                            param = item["name"]
                            value = item["value"].replace('\n', ' ')
                            if param not in self.unic_params: self.unic_params.append(param)
                            resalt_good[code][param] = value
                        self.result.append(resalt_good)
                        return
                    else:
                        print("ghj")
                except:
                    pass

    def extract_data(self,  dicts_list, keys_list):
        keys = list(keys_list)
        keys.insert(0, "SKU")
        data_rows = list(map(lambda d: [int(list(d.keys())[0])] + [d[list(d.keys())[0]].get(k, '') for k in keys_list], dicts_list))
        return [keys] + data_rows

    def get_tth_ozon(self):
        goods = filter(lambda x: int(x[18]) > 0, GoogleSheet().get_current_stock(self.SPREADSHEET_ID_NEW, "УШМ!A2:AQ3000")["values"])
        tasks = list(map(lambda x: [x[0], x[23]], goods))
        get_multy_funk(tasks, self.parser_item_Ozon, max_workers=1)
        num = self.extract_data(self.result, list(set(self.unic_params)))
        GoogleSheet().append_data_FoxWeld(self.SPREADSHEET_ID_NEW, f'Справочник!A1:F1', num)

    def get_tth_wb(self):
        # goods = filter(lambda x: int(x[15]) > 1000, GoogleSheet().get_current_stock(self.SPREADSHEET_ID_NEW, "Бады!A2:AC10000")["values"])
        tasks = self.read_excel_columns("/Users/vladimirivliev/PycharmProjects/pythonProject1/Файлы/Пиджаки/Пиджаки.xlsx")
        # print(goods)
        # tasks = list(map(lambda x: [x[0], x[23]], goods))
        get_multy_funk(tasks, self.parser_item_WB, max_workers=10)
        num = self.extract_data(self.result, list(set(self.unic_params)))
        GoogleSheet().append_data_FoxWeld(self.SPREADSHEET_ID_NEW, f'Справочник!A1:F1', num)

    def read_excel_columns(self, file_name):
        # Проверим, существует ли файл
        if not os.path.exists(file_name):
            print(f"Ошибка: файл не найден по пути {file_name}")
            return []

        try:
            # Чтение Excel файла из текущей директории
            df = pd.read_excel(file_name)
            print(f"Содержимое файла:\n{df.head()}")  # Выводим первые несколько строк для проверки

            # Проверим, есть ли столбцы с индексами 0 и 23
            if len(df.columns) > 23:
                # Получаем значения из столбцов с индексами 0 и 23
                result = df.iloc[:, [0, 24]].values.tolist()
                return result
            else:
                print(f"Ошибка: в файле меньше 24 столбцов")
                return []
        except Exception as e:
            print(f"Произошла ошибка при чтении файла: {e}")
            return []

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
    ParserOzon(brand=brand, company=company).get_tth_ozon()

