import datetime
import json
import time
from find_name import find_name
import jmespath
from selenium.webdriver.common.by import By
from browser import Driver_Chrom
from push_to_google_sheets import GoogleSheet
from urls import urls
import concurrent.futures
from tqdm import tqdm
import multiprocessing


class ParserSber():
    def __init__(self, brand: list = [], company: str = None):
        self.brand = brand
        self.company = company
        self.SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
        self.result = multiprocessing.Manager().list()
        self.list_links = multiprocessing.Manager().list()
        self.unic_name = multiprocessing.Manager().list()

    def parser_links(self, url: str = '') -> None:
        with Driver_Chrom().loadChromTest(headless=True) as driver:
            driver.get(url)
            flag = True
            while flag:
                time.sleep(3)
                offers = driver.find_elements(By.XPATH, urls['sber']['xpath']['card_link_xpath'])
                [self.list_links.append(item.get_attribute('href').replace('/#?related_search=hammer', '')) for item in offers]
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
                    print(result)

            except:
                result = self.get_atributs(driver=driver, type='one')
                print(result)

    def get_atributs(self, driver, driver_elem=None, type: str = ''):
        seller_xpath = 'seller_xpath_main' if type == 'one' else 'seller_xpath'
        name = driver_elem.find_element(By.XPATH, urls['sber']['xpath']['name_xpath']).text if driver_elem is not None else driver.find_element(By.XPATH, urls['sber']['xpath']['name_xpath']).text
        seller = driver_elem.find_element(By.XPATH, urls['sber']['xpath'][seller_xpath]).text.split('  ')[0] if driver_elem is not None else driver.find_element(By.XPATH, urls['sber']['xpath'][seller_xpath]).text
        price = driver_elem.find_element(By.XPATH, urls['sber']['xpath']['price_xpath']).text.replace(' ₽') if driver_elem is not None else driver.find_element(By.XPATH, urls['sber']['xpath']['price_xpath_main']).text
        return {'name': name, 'seller': seller, 'price': price}








    def main(self):
        url = 'https://megamarket.ru/catalog/details/ushm-hammer-usm710d-710vt-12000ob-min-125mm-100043407779/#?details_block=prices'
        # url = 'https://megamarket.ru/catalog/details/drel-shurupovert-hammer-acd12a-15ach-s-dvumya-akkumulyatorami-735855-100028939311/#?related_search=hammer'
        self.parser_item(url)
        # for url in urls['sber']['url']['STM']:
        #     self.parser_links(url)


if __name__ == "__main__":
    ParserSber().main()
