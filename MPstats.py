import datetime
import json
import pickle
import random
import time
from pprint import pprint
import re
from datetime import datetime, timedelta
import pyautogui

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
        self.SPREADSHEET_ID = '13qYO-GroKtUV2G_cO_nu7TH6XsUNt3IwOXYzXxXt4TY'
        self.SPREADSHEET_ID_NEW = '1ULOC955OlwT71wHZQfhzK95BRq64iipWEZi52O2UTfM'
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
        with Driver_Chrom().loadChromTest(headless=False) as driver:
            url = f"https://mpstats.io/api/wb/get/item/{code}/sales?d1=2024-02-14&d2=2025-02-12"
            urlMainPage = "https://mpstats.io"
            driver.get(urlMainPage)
            driver.get_pinned_scripts()
            # Открываем новое окно
            driver.execute_script(f"window.open('{url}');")
            time.sleep(50)

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


    def parser_main(self) -> None:

        # создаем связку страница и ссылка для задачника
        tasks = [(page, {'brand': brand, 'url': urls['Ozon']['url']['brand'].get(brand)}) for brand in self.brand for
                 page in range(1, 10)]
        # собираем все ссылки на товары. Сразу запускается по max_workers окон
        get_multy_funk(tasks=tasks, function=self.parser_page, max_workers=5,
                       range=urls['google_sheets_name']['main_parser_Ozon_anal'], what_need_save=self.list_items,
                       SPREADSHEET_ID=self.SPREADSHEET_ID_NEW)

    def logIN(self):
        headers = [
            'code',
            'data',
            'balance',
            'sales',
            'price',
            'final_price',
            'ozon_card_price',
        ]
        # pathLogInUrl = '//a[contains(@href, "https://mpstats.io/login")]'
        # pathLog = "//input[@placeholder = 'Электронная почта']"
        # pathPassword = "//input[@placeholder = 'Введи пароль']"
        # pathButton = "//div[contains(text(), 'Войти')]"
        self.result.append(headers)
        # logIn = "kozlovamsu@gmail.com"
        # password = "159951Lev100@"
        goods = list(map(lambda x: [x[0], x[23]], filter(lambda x: int(x[17]) > -10, GoogleSheet().get_current_stock(self.SPREADSHEET_ID, "Перфораторы!A2:AC1616")["values"])))
        with Driver_Chrom().loadChromTest(headless=False) as driver:
            urlMainPage = "https://mpstats.io/login?from=main-page-header"
            driver.get(urlMainPage)
            driver.execute_script(f"window.open('{urlMainPage}');")
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(5)
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            # Обновляем страницу, чтобы авторизация прошла
            driver.refresh()
            # pyautogui.moveTo(148, 325)
            # pyautogui.click()
            # pyautogui.typewrite(logIn)
            # time.sleep(3)
            # pyautogui.moveTo(148, 425)
            # pyautogui.click()
            # pyautogui.typewrite(password)
            time.sleep(3)
            # for _ in range(10):
            #     pyautogui.moveTo(150, 510)
            #     pyautogui.click()
            #     time.sleep(3)
            # # Сохраняем cookies
            pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
            check = 0
            for item in goods:
                check += 1
                code = item[0]
                item_url = f"https://mpstats.io/api/oz/get/item/{code}/sales?d1=2024-02-20&d2=2025-02-20"
                driver.get(item_url)
                time.sleep(1)
                try:
                    self.transform_data_to_list(extract_json_from_html(driver.page_source), code)
                    if check == 100:
                        GoogleSheet().append_data_FoxWeld(self.SPREADSHEET_ID_NEW, f'Продажи!A1:F1', list(self.result))
                        self.result = []
                        check = 0
                except:
                    pass
                time.sleep(1)

    def get_catigyes(self):
        # Получаем сегодняшнюю дату
        today = datetime.today()
        # Вычисляем вчерашнюю дату
        yesterday = today - timedelta(days=1)

        # Форматируем вчерашнюю дату в нужный формат
        formatted_yesterday = yesterday.strftime("%Y-%m-%d")
        with Driver_Chrom().loadChromTest(headless=False) as driver:
            urlMainPage = "https://mpstats.io/login?from=main-page-header"
            categories = [["УШМ (болгарки)", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/УШМ (болгарки)"],
                          ["Шуруповерты", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Шуруповерты"],
                          ["Электродрели", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Электродрели"],
                          ["Гайковерты и винтоверты", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Гайковерты и винтоверты"],
                          ["Перфораторы", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Перфораторы"],
                          ["Эксцентриковые шлифмашины", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Эксцентриковые шлифмашины"],
                          ["Строительные фены", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Строительные фены"],
                          ["Шлифмашины", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Шлифмашины"],
                          ["Циркулярные пилы", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Циркулярные пилы"],
                          ["Граверы", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Граверы"],
                          ["Электролобзики", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Электролобзики"],
                          ["Электрорубанки", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Электрорубанки"],
                          ["Сабельные пилы", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Сабельные пилы"],
                          ["Строительные миксеры и венчики", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Строительные миксеры и венчики"],
                          ["Фрезерные машины", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Фрезерные машины"],
                          ["Бензопилы и электропилы", "Дом и сад/Дача и сад/Садовая техника/Бензопилы и электропилы"],
                          ["Триммеры", "Дом и сад/Дача и сад/Садовая техника/Триммеры"],
                          ["Мойки высокого давления и аксессуары", "Дом и сад/Дача и сад/Садовая техника/Мойки высокого давления и аксессуары"],
                          ["Газонокосилки", "Дом и сад/Дача и сад/Садовая техника/Газонокосилки"],
                          ["Кусторезы", "Дом и сад/Дача и сад/Садовая техника/Кусторезы"],
                          ["Воздуходувки и пылесосы", "Дом и сад/Дача и сад/Садовая техника/Воздуходувки и пылесосы"],
                          ["Промышленные насосы", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Промышленные насосы"],
                          ["Электрогенераторы", "Строительство и ремонт/Силовая техника и оборудование/Электрогенераторы"],
                          ["Лазерные уровни (нивелиры)", "Строительство и ремонт/Инструменты для ремонта и строительства/Измерительные инструменты/Лазерные уровни (нивелиры)"],
                          ["Измерители длин и углов", "Строительство и ремонт/Инструменты для ремонта и строительства/Измерительные инструменты/Измерители длин и углов"],
                          ["Виброоборудование", "Строительство и ремонт/Силовая техника и оборудование/Виброоборудование"],
                          ["Лазерные уровни (нивелиры)", "Строительство и ремонт/Инструменты для ремонта и строительства/Электроинструменты/Электродрели"],
                          ]
            "10T4IL20KWLEpBr53FypgO-NSNRKAbePhfAR-KtmYkKc"
            "https://docs.google.com/spreadsheets/d/10fCLIqWsAeg6S4FYT4rrruR_uMGAdOfBOkBMOH9IX-4/edit?gid=507806497#gid=507806497"
            category = "Шуруповерты"
            driver.get(urlMainPage)
            driver.execute_script(f"window.open('{urlMainPage}');")
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(5)
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            for item in categories:
                category = item[0]
                path = item[1]
                urlCatPage = f"https://mpstats.io/api/oz/get/category/by_date?path={path}&groupBy=day&d1=2025-02-17&d2={formatted_yesterday}"
                driver.get(urlCatPage)
                time.sleep(5)
                self.transform_data_category_to_list(extract_json_from_html(driver.page_source), category)
                # print(self.result)
        GoogleSheet().append_data_FoxWeld("10fCLIqWsAeg6S4FYT4rrruR_uMGAdOfBOkBMOH9IX-4", f'Продажи категорий журнал!A1:F1', list(self.result))


    def transform_data_to_list(self, data, code):
        # Переводим каждый словарь в список значений
        result = []
        for entry in data:
            row = [
                code,
                entry.get('data', ''),
                entry.get('balance', ''),
                entry.get('sales', ''),
                # entry.get('rating', ''),
                # entry.get('price', ''),
                entry.get('final_price', ''),
                # entry.get('is_new', ''),
                # entry.get('comments', ''),
                # entry.get('discount', ''),
                entry.get('ozon_card_price', ''),  # Если ключ отсутствует, то пустая строка
                # entry.get('is_bestseller', ''),  # Если ключ отсутствует, то пустая строка
                # entry.get('is_new', ''),
                # ", ".join(map(str, entry.get('top_hours', []))),  # Преобразуем список top_hours в строку, если он есть
                # entry.get('description_length', ''),
                # entry.get('name_length', ''),
                # entry.get('package_length', ''),
                # entry.get('package_width', ''),
                # entry.get('package_height', ''),
                # entry.get('commentsvaluation', '')
            ]
            self.result.append(row)

        # Возвращаем результат в виде списка списков
        return result

    def transform_data_category_to_list(self, data, category):
        # Переводим каждый словарь в список значений
        result = []
        for entry in data:
            row = [
                entry.get('period', ''),
                category,
                entry.get('items', ''),
                entry.get('items_with_sells', ''),
                entry.get('sales', ''),
                entry.get('revenue', ''),
                entry.get('brands', ''),
                entry.get('brands_with_sells', ''),
                entry.get('sellers', ''),
                entry.get('sellers_with_sells', ''),
                entry.get('balance', ''),
                entry.get('balance_price', ''),
                entry.get('avg_price', ''),
                entry.get('avg_sale_price', ''),
                entry.get('comments', ''),
                entry.get('rating', ''),
            ]
            self.result.append(row)

        # Возвращаем результат в виде списка списков
        return result

if __name__ == "__main__":
    brand = ["All"]
    company = 'Шурик 18В 2 АКБ'
    ParserOzon(brand=brand, company=company).get_catigyes()
