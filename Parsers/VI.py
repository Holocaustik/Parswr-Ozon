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

    def __init__(self):
        self.SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
        self.result = multiprocessing.Manager().list()
        self.unic_name = multiprocessing.Manager().list()

    def parser_page(self, page: int = 1) -> None:
        driver = Driver_Chrom().loadChromTest()
        driver.get(f'{self.url}?page={page}/?asc=desc&orderby=price')
        time.sleep(2)
        all_cards_on_the_page = driver.find_elements(By.XPATH, urls['VI']['xpath']['xpath_for_cards_VI'])
        for card in all_cards_on_the_page:
            try:
                card.find_element(By.XPATH, urls['VI']['xpath']['check_availability_VI'])
                return
            except:
                full_name = card.find_element(By.XPATH, urls['VI']['xpath']['xpath_for_name_VI']).get_attribute('title')
                name = find_name(full_name)
                price = card.find_element(By.XPATH, urls['VI']['xpath']['xpath_for_price_VI']).text.replace(' р.', '').replace(' ', '')
                self.result.append(('VI', 'Vseinstrumenti', name, price, datetime.date.today().strftime('%d. %m. %Y'))) if name not in self.unic_name else ''
                self.unic_name.append(name)

    def get_save_result_too_google_sheets(self, result: list) -> None:
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=list(result), range="парсер OZON WB!A1:E1")

    def find_last_page(self, url: str = '') -> int:
        driver = Driver_Chrom().loadChromTest()
        driver.get(url)
        time.sleep(5)
        last_page = min(int(driver.find_elements(By.XPATH, urls['VI']['xpath']['last_page'])[-1].text), 100)
        return last_page

    def parser_main(self) -> None:
        for self.url in urls['VI']['url']['STM']:
            last_page = self.find_last_page(self.url)
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                list(tqdm(executor.map(self.parser_page, list(range(1, last_page))), total=len(list(range(1, last_page))), desc="Processing parser_item", ncols=100))
        self.get_save_result_too_google_sheets(result=self.result)


if __name__ == "__main__":
    ParserVI().parser_main()
