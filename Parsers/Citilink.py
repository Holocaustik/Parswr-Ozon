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


class ParserCitilink():

    def __init__(self):
        self.SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
        self.result = multiprocessing.Manager().list()
        self.unic_name = multiprocessing.Manager().list()

    def parser_page(self, page: int = 1) -> None:
        driver = Driver_Chrom().loadChromTest()
        driver.get(f'{urls["citilink"]["url"]["STM"][0]}&p={page}')
        time.sleep(5)
        all_cards = driver.find_elements(By.XPATH, urls['citilink']['xpath']['all_cards'])
        try:
            for card in all_cards:
                full_name = card.find_element(By.XPATH, urls['citilink']['xpath']['name']).get_attribute('title')
                print(full_name)
                name = find_name(full_name)
                price = card.find_element(By.XPATH, urls['citilink']['xpath']['price']).text.replace('₽', '')
                self.result.append(('Citilink', 'Citilink', name, price, datetime.date.today().strftime('%d. %m. %Y')))
        except:
            print('here')
            pass
    def get_save_result_too_google_sheets(self, result: list) -> None:
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=list(result), range="парсер OZON WB!A1:E1")

    def parser_main(self) -> None:
        for self.url in urls['VI']['url']['STM']:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                list(tqdm(executor.map(self.parser_page, list(range(1, 10))), total=len(list(range(1, 20))), desc="Processing parser_item", ncols=100))
        self.get_save_result_too_google_sheets(result=self.result)


if __name__ == "__main__":
    ParserCitilink().parser_main()
