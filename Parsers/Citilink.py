import datetime
import time
from find_name import find_name
from selenium.webdriver.common.by import By
from browser import Driver_Chrom
from push_to_google_sheets import GoogleSheet
from urls import urls
import multiprocessing
from other import remove_duplicates, get_multy_funk


class ParserCitilink():

    def __init__(self, brand: list = [], company: str = None):
        self.SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
        self.SPREADSHEET_ID_NEW = '1Z1vbksKPw7xx07whBa3tHj6H7uoT7uQbx8WReSHCHC0'
        self.result = multiprocessing.Manager().list()
        self.result_new = multiprocessing.Manager().list()
        self.unic_name = multiprocessing.Manager().list()
        self.brand = brand
        self.company = company

    def parser_page(self, *args, **kwargs) -> None:
        page, brand = args[0]
        try:
            with Driver_Chrom().loadChromTest(headless=False) as driver:
                driver.get(f'{brand["url"]}&p={page}')
                print(f'{brand["url"]}&p={page}')
                time.sleep(5)
                all_cards = driver.find_elements(By.XPATH, urls['citilink']['xpath']['all_cards'])
                for card in all_cards:
                    try:
                        full_name = card.find_element(By.XPATH, urls['citilink']['xpath']['name']).get_attribute('title')
                        name = find_name(full_name)
                        link = card.find_element(By.XPATH, urls['citilink']['xpath']['name']).get_attribute('href')
                        code = link.split('-')[-1].replace('/', '')
                        print(full_name)
                        price = card.find_element(By.XPATH, urls['citilink']['xpath']['price']).text.replace('₽', '')
                        self.result.append(('Citilink', 'Citilink', name, price, datetime.date.today().strftime('%d. %m. %Y')))
                        self.result_new.append((self.company, code, price, '', '', datetime.date.today().strftime('%d.%m.%Y')))
                    except:
                        pass
        except:
            pass

    def parser_main(self) -> None:
        tasks = [(page, {'brand': brand, 'url': urls['citilink']['url']['brand'].get(brand)}) for brand in self.brand for page in range(1, 5)]
        get_multy_funk(tasks=tasks, function=self.parser_page, max_workers=2, SPREADSHEET_ID=self.SPREADSHEET_ID, range=urls['google_sheets_name']['main_parser'], what_need_save=self.result)
        GoogleSheet(self.SPREADSHEET_ID_NEW).append_data(value_range_body=list(self.result_new), range=urls['google_sheets_name']['main_parser_new'])


if __name__ == "__main__":
    brand = ['hammer']
    company = 'ОПТ-ТРЕЙД'
    ParserCitilink(brand=brand, company=company).parser_main()
