import datetime
import time
from find_name import find_name
import concurrent.futures
from selenium.webdriver.common.by import By
from browser import Driver_Chrom
from push_to_google_sheets import GoogleSheet
from urls import urls
import multiprocessing
from tqdm import tqdm


class ParserVI():

    def __init__(self, brand: list = [], company: str = None):
        self.SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
        self.SPREADSHEET_ID_NEW = '1Z1vbksKPw7xx07whBa3tHj6H7uoT7uQbx8WReSHCHC0'
        self.company = company
        self.result = multiprocessing.Manager().list()
        self.result_collecting_products = multiprocessing.Manager().list()
        self.result_new = multiprocessing.Manager().list()
        self.unic_name = multiprocessing.Manager().list()
        self.brand = brand

    def parser_page(self, *args, **kwargs) -> None:
        page, brand = args[0]
        driver = Driver_Chrom().loadChromTest()
        driver.get(f'{brand["url"]}?page={page}/?asc=desc&orderby=price')
        time.sleep(2)
        all_cards_on_the_page = driver.find_elements(By.XPATH, urls['VI']['xpath']['xpath_for_cards_VI'])
        for card in all_cards_on_the_page:
            try:
                card.find_element(By.XPATH, urls['VI']['xpath']['check_availability_VI'])
                return
            except:
                full_name = card.find_element(By.XPATH, urls['VI']['xpath']['xpath_for_name_VI']).get_attribute('title')
                item_code = card.find_element(By.XPATH, urls['VI']['xpath']['item_code_xpath']).text.replace('код: ', '')
                name = find_name(full_name)
                link = card.find_element(By.XPATH, urls['VI']['xpath']['xpath_for_name_VI']).get_attribute('href')
                price = card.find_element(By.XPATH, urls['VI']['xpath']['xpath_for_price_VI']).text.replace(' р.', '').replace(' ', '')
                if item_code not in self.unic_name:
                    self.result.append(('VI', 'Vseinstrumenti', name, price, datetime.date.today().strftime('%d. %m. %Y'))) if name not in self.unic_name else ''
                    self.result_new.append((self.company, item_code, price, '', '', datetime.date.today().strftime('%d.%m.%Y')))
                    self.result_collecting_products.append(('ОПТ-ТРЕЙД', brand['brand'], 'VI', item_code, full_name, name, link, 999999999))

                    self.unic_name.append(item_code)

    def get_multy_funk(self, tasks: list = None, function: object = None, max_workers: int = None, range: str = None, what_need_save: list = None):
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
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            list(tqdm(executor.map(function, tasks), total=len(tasks), desc="Processing", ncols=100))
        if range is not None:
            GoogleSheet(self.SPREADSHEET_ID).append_data(value_range_body=list(what_need_save), range=range)

    def find_last_page(self, url: str = '') -> int:
        driver = Driver_Chrom().loadChromTest()
        driver.get(url)
        time.sleep(5)
        last_page = min(int(driver.find_elements(By.XPATH, urls['VI']['xpath']['last_page'])[-1].text), 100)
        return last_page

    def parser_main(self) -> None:
        saved_code = GoogleSheet().get_collecting_in_sheet()
        tasks = [(page, {'brand': brand, 'url': urls['VI']['url']['brand'].get(brand)}) if urls['VI']['url']['brand'].get(brand) is not None else '' for brand in self.brand for page in range(1, 5)]
        self.get_multy_funk(tasks=tasks, function=self.parser_page, max_workers=5, what_need_save=self.result, range=urls['google_sheets_name']['main_parser'])
        save_code = list(filter(lambda x: str(x[3]) not in saved_code['product_id'], set(self.result_collecting_products)))

        GoogleSheet(self.SPREADSHEET_ID_NEW).append_data(value_range_body=list(self.result_new), range=urls['google_sheets_name']['main_parser_new'])
        GoogleSheet(self.SPREADSHEET_ID).append_data(value_range_body=list(save_code), range=urls['google_sheets_name']['collecting_products'])
        GoogleSheet(self.SPREADSHEET_ID_NEW).append_data(value_range_body=list(save_code), range=urls['google_sheets_name']['collecting_products'])



if __name__ == "__main__":
    brand = ['hammer']
    company = 'ОПТ-ТРЕЙД'
    ParserVI(brand=brand, company=company).parser_main()
