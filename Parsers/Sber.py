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
    def __init__(self):
        self.SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
        self.result = multiprocessing.Manager().list()
        self.list_links = multiprocessing.Manager().list()
        self.unic_name = multiprocessing.Manager().list()

    def parser_links(self, url: str = '') -> None:
        driver = Driver_Chrom().loadChromTest(headless=False)
        driver.get(url)
        flag = True
        counter = 1
        while flag:
            time.sleep(30)
            print(urls['sber']['xpath']['card_link_xpath'])
            offers = driver.find_elements(By.XPATH, urls['sber']['xpath']['card_link_xpath'])
            print(len(offers))
            [self.result.append({
                'name': find_name(driver.find_element(By.XPATH, urls['sber']['xpath']['name_xpath']).text),
                    'seller': offer.find_element(By.XPATH, urls['sber']['xpath']['seller_xpath']).text,
                    'price': offer.find_element(By.XPATH, urls['sber']['xpath']['price_xpath']).text}) for offer in offers]
            driver.execute_script("window.scrollBy(0, 6500);")
            time.sleep(2)
            try:
                elem = driver.find_element(By.XPATH, urls['sber']['xpath']['next_page'])
                elem.click()
                counter += 1
            except:
                print(self.result)
                flag = False


    def main(self):
        for url in urls['sber']['url']['STM']:
            self.parser_links(url)


if __name__ == "__main__":
    ParserSber().main()
