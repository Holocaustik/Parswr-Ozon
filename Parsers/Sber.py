import datetime
import json
import time
from find_name import find_name
import jmespath
from selenium.webdriver.common.by import By
from browser import Driver_Chrom
from push_to_google_sheets import GoogleSheet
from other import remove_duplicates, get_multy_funk
from urls import urls
import concurrent.futures
from tqdm import tqdm
import multiprocessing


class ParserSber():
    def __init__(self, brand: list = [], company: str = None):
        self.SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
        self.brand = brand
        self.company = company
        self.SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
        self.result = multiprocessing.Manager().list()
        self.list_links = multiprocessing.Manager().list()
        self.unic_name = multiprocessing.Manager().list()

    def parser_links(self, item: dict = {}) -> None:
        with Driver_Chrom().loadChromTest(headless=False) as driver:
            print(item["url"])
            driver.get(item["url"])
            flag = True
            while flag:
                time.sleep(3)
                # offers = driver.find_elements(By.XPATH, urls['sber']['xpath']['card_link_xpath'])
                offers = driver.find_elements(By.XPATH, urls['sber']['xpath']['card_xpath'])
                for item in offers:
                    try:
                        item.find_element(By.XPATH, './/button[@class="btn btn-secondary similar-goods-btn sm"]')
                        return
                    except:
                        link = item.find_element(By.XPATH, urls['sber']['xpath']['card_link_xpath'])
                        self.list_links.append(link.get_attribute('href').replace('/#?related_search=hammer', ''))
                    # [self.list_links.append(item.get_attribute('href').replace('/#?related_search=hammer', '')) for item in offers]
                try:
                    elem = driver.find_element(By.XPATH, urls['sber']['xpath']['next_page'])
                    elem.click()
                except:
                    flag = False

    def parser_item(self, url):
        with Driver_Chrom().loadChromTest(headless=False) as driver:
            driver.get(url)
            try:
                driver.find_element(By.XPATH, urls['sber']['xpath']['card_offers']).click()
                offers = driver.find_elements(By.XPATH, urls['sber']['xpath']['offers'])
                time.sleep(2)
                for item in offers:
                    result = self.get_atributs(driver_elem=item, driver=driver, type='more')
                    self.result.append(
                        ('SBER', result["seller"], result['name_small'], result["price"], datetime.date.today().strftime('%d.%m.%Y')))
            except:
                try:
                    result = self.get_atributs(driver=driver, type='one')
                    self.result.append(
                        ('SBER', result["seller"], result['name_small'], result["price"], datetime.date.today().strftime('%d.%m.%Y')))
                except:
                    return

    def get_atributs(self, driver, driver_elem=None, type: str = ''):
        seller_xpath = 'seller_xpath_main' if type == 'one' else 'seller_xpath'
        name_full = driver_elem.find_element(By.XPATH, urls['sber']['xpath']['name_xpath']).text if driver_elem is not None else driver.find_element(By.XPATH, urls['sber']['xpath']['name_xpath']).text
        name_small = find_name(name_full)
        seller = driver_elem.find_element(By.XPATH, urls['sber']['xpath'][seller_xpath]).text.split('  ')[0] if driver_elem is not None else driver.find_element(By.XPATH, urls['sber']['xpath'][seller_xpath]).text
        price = driver_elem.find_element(By.XPATH, urls['sber']['xpath']['price_xpath']).text.replace(' ₽', "") if driver_elem is not None else driver.find_element(By.XPATH, urls['sber']['xpath']['price_xpath_main']).text
        return {'name_full': name_full, "name_small": name_small, 'seller': seller, 'price': price}

    def main(self):
        tasks = [{'brand': brand, 'url': urls['sber']['url']['brand'].get(brand)} for brand in self.brand]
        get_multy_funk(tasks=tasks, function=self.parser_links, max_workers=5)
        get_multy_funk(tasks=self.list_links, function=self.parser_item, max_workers=5, what_need_save=self.result, range=urls['google_sheets_name']['main_parser'],  SPREADSHEET_ID=self.SPREADSHEET_ID)


if __name__ == "__main__":
    brand = ["hammer", "tesla"]
    ParserSber(brand=brand).main()
