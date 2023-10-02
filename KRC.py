import datetime
import time
from selenium.webdriver.common.by import By
from Parsers.Sber import ParserSber
from browser import Driver_Chrom
from find_name import find_name
from push_to_google_sheets import GoogleSheet
from Parsers.OzonMulti import ParserOzon
from Parsers.WBMulti import ParserWB
from Parsers.VI import ParserVI
from Parsers.Citilink import ParserCitilink


class ParserKRC():

    def __init__(self):
        self.SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'

        self.mvideo_url = 'https://www.mvideo.ru/product-list-page/f/category=moiki-vysokogo-davleniya-214,massazhery-226,pylesosy-2438,feny-stroitelnye-7955,elektropily-7956,dreli-i-shurupoverty-7959,perforatory-7960,gaikoverty-i-vintoverty-7961,shlifovalnye-mashiny-7967,gazonokosilki-i-trimmery-8028,nasosy-i-nasosnye-stancii-8056,frezery-8077,kultivatory-8193,elektrorubanki-8369,kraskopulty-i-aerografy-8700/brand=hammer/tolko-v-nalichii=da?q=hammer'
        self.mvideo_cards_xpath = "//a[contains(@class, 'product-title__text product-title--clamp')]"
        self.mvideo_cards_xpath_price = "//span[contains(@class, 'price__main-value')]"

        self.cards_xpath_eldarado = "//li[@data-dy = 'product']"
        self.name_xpath_eldarado = ".//a[@data-dy = 'title']"
        self.price_xpath_eldarado = ".//span[@data-pc= 'offer_price']"
        self.url_eldorado = 'https://www.eldorado.ru/a/elektroinstrument/b/HAMMER/'
        self.check_availability = './/span[contains(text(), "Нет в наличии")]'

        self.url_holodilnik = 'https://www.holodilnik.ru/construction_repair/all/hammer/sankt-peterburg/'
        self.cards_xpath_holodilnik = "//div[@class = 'goods-tile preview-product']"
        self.name_xpath_holodilnik = ".//div[@class = 'product-name']"
        self.price_xpath_holodilnik = ".//meta[@itemprop = 'price']"

        self.url_maxidom = 'https://www.maxidom.ru/search/catalog/?q=hammer'
        self.cards_xpath_maxidom = "//article[contains(@class, 'item-list group b-catalog-list-product')]"
        self.name_xpath_maxidom = ".//span[@itemprop = 'name']"
        self.price_xpath_maxidom = ".//span[@class = 'b-catalog-list-product__price']"

    def parserMvideo(self, driver=None):
        driver = driver if driver else Driver_Chrom().loadChromTest(headless=True)
        result = []
        flag = True
        for page in range(1, 20):
            if flag:
                driver.get(f'{self.mvideo_url}&page={page}')
                time.sleep(2)
                try:
                    names = list(
                        map(lambda x: self.find_name(x.text), driver.find_elements(By.XPATH, self.mvideo_cards_xpath)))
                    prices = list(map(lambda x: x.text.replace(' ₽', '').replace(' ', ''),
                                      driver.find_elements(By.XPATH, self.mvideo_cards_xpath_price)))
                    result.extend(list(
                        zip(['Mvideo' for _ in range(len(names))], ['Mvideo' for _ in range(len(names))], names, prices,
                            [datetime.date.today().strftime('%d. %m. %Y') for _ in range(len(names))])))
                except:
                    flag = False
            else:
                break
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=result, range="парсер OZON WB!A1:E1")

    def parser_eldorado(self, driver=None):
        driver = driver if driver else Driver_Chrom().loadChromTest(headless=False)
        result = []
        unic_name = set()
        for page in range(1, 20):
            try:
                driver.get(f'{self.url_eldorado}?page={page}')
                time.sleep(15)
                all_cards = driver.find_elements(By.XPATH, self.cards_xpath_eldarado)
                for card in all_cards:
                    # print(card.text)
                    name = find_name(card.find_element(By.XPATH, self.name_xpath_eldarado).text)
                    price = card.find_element(By.XPATH, self.price_xpath_eldarado).text
                    if name not in unic_name:
                        result.append(
                            ('Eldarado', 'Eldarado', name, price, datetime.date.today().strftime('%d. %m. %Y')))
                        unic_name.add(name)
                        print(name, price)
                    else:
                        print('Finish')
            except:
                break
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=result, range="парсер OZON WB!A1:E1")

    def parser_holodilnik(self, driver=None):
        driver = driver if driver else Driver_Chrom().loadChromTest(headless=True)
        result = []
        for page in range(1, 3):
            driver.get(f'{self.url_holodilnik}?page={page}')
            time.sleep(2)
            all_cards = driver.find_elements(By.XPATH, self.cards_xpath_holodilnik)
            [result.append(('Holodilnik', 'Holodilnik',
                            self.find_name(i.find_element(By.XPATH, self.name_xpath_holodilnik).text),
                            i.find_element(By.XPATH, self.price_xpath_holodilnik).get_attribute('content').replace(' ₽',
                                                                                                                   ''),
                            datetime.date.today().strftime('%d. %m. %Y'))) for i in all_cards]
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=result, range="парсер OZON WB!A1:E1")

    def parser_maxidom(self, driver=None):
        driver = driver if driver else Driver_Chrom().loadChromTest(headless=True)
        result = []
        for page in range(1, 10):
            driver.get(f'{self.url_maxidom}&PAGEN_1={page}')
            time.sleep(1)
            all_cards = driver.find_elements(By.XPATH, self.cards_xpath_maxidom)
            try:
                for card in all_cards:
                    full_name = card.find_element(By.XPATH, self.name_xpath_maxidom).text
                    name = find_name(full_name)
                    price = card.find_element(By.XPATH, self.price_xpath_maxidom).text.replace(' ', '')
                    print(name)
                    result.append(('Maxidom', 'Maxidom', name, price, datetime.date.today().strftime('%d. %m. %Y')))
            except:
                break
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=result, range="парсер OZON WB!A1:E1")

    def main(self):
        GoogleSheet().delete_all()
        driver = Driver_Chrom().loadChromTest(headless=True)
        brand = ['hammer', 'tesla', 'wester']
        company = 'ОПТ-ТРЕЙД'
        ParserOzon(brand=brand, company=company).parser_main()
        print("ParserOzon")
        time.sleep(10)
        ParserWB(brand=brand, company=company).parser_main()
        print('ParserWB')
        ParserVI(brand=brand, company=company).parser_main()
        print('ParserVI')
        ParserSber(brand=brand).main()
        print('SBER')
        ParserCitilink(brand=brand, company=company).parser_main()
        self.parserMvideo(driver)
        print('parserMvideo')
        self.parser_eldorado(driver)
        print('parser_eldorado')
        self.parser_maxidom(driver)
        print('parser_maxidom')
        self.parser_holodilnik(driver)
        print('parser_holodilnik')
        driver.close()
        driver.quit()
        GoogleSheet().parse_and_append_data()


if __name__ == "__main__":
    ParserKRC().main()
