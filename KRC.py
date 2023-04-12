import datetime
import json
import re
import time
from pprint import pprint
import base64
import jmespath
from selenium.webdriver.common.by import By
from browser import Driver_Chrom
from push_to_google_sheets import GoogleSheet


class ParserKRC():

    def __init__(self):
        self.SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
        # self.url_ozon = 'https://www.ozon.ru/api/composer-api.bx/page/json/v1?url=https://www.ozon.ru/category/elektroinstrumenty-9857/hammer-26303172/'
        self.url_ozon = 'https://www.ozon.ru/api/composer-api.bx/page/json/v1?url=https://www.ozon.ru/brand/hammer-26303172/'
        # self.url_ozon = 'https://www.ozon.ru/api/composer-api.bx/page/json/v1?url=https://www.ozon.ru/brand/ferm-87317356/'
        # self.url_ozon = 'https://www.ozon.ru/api/composer-api.bx/page/json/v1?url=https://www.ozon.ru/brand/ingco-72464691/'
        self.clean_json_ozon = '<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">'
        # self.jmespath_ozon = 'items[*].[mainState[*].atom.textAtom.text,mainState[*].atom.priceWithTitle.price || mainState[*].atom.price.price, multiButton.ozonButton.addToCartButtonWithQuantity.action.id]'
        self.jmespath_ozon = 'items[*].[mainState[*].atom.textAtom.text,mainState[*].atom.priceWithTitle.price || mainState[*].atom.price.price, topRightButtons[*].favoriteProductMoleculeV2.id]'
        self.jmespath_ozon_LEX = 'items[*].[mainState[*].atom.textAtom.text, mainState[*].atom.priceWithTitle.price, action.link]'
        self.url_ozon_LEX = 'https://www.ozon.ru/api/composer-api.bx/page/json/v1?url=https://www.ozon.ru/brand/lex-139273401/category/bytovaya-tehnika-10500/'

        self.card_link_xpath = '//div[@class="item-title"]/a'
        self.card_ofers = '//a[contains(@class, "more-offers-button")]'
        self.offers = '//div[contains(@class, "product-offer_with-payment-method")]'
        self.name_xpath = './/h1[contains(@itemprop, "name")]'
        self.seller_xpath = './/div[contains(@class, "product-offer-name__name")]'
        self.price_xpath = './/span[contains(@class, "product-offer-price__amoun")]'
        self.next_page = '//li[@class="next"]'
        self.url_sber = 'https://sbermegamarket.ru/catalog/?q=hammer&collectionId=14576'

        self.xpath_for_name_VI = ".//a[@data-qa='product-name']"
        self.xpath_for_price_VI = ".//p[@data-qa='product-price-current']"
        self.xpath_for_cards_VI = "//div[@data-qa='products-tile']"
        self.check_availability_VI = ".// div[contains(@data-qa, 'not-available')]"

        self.url_citilink = 'https://www.citilink.ru/search/?text=hammer'

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

    def find_name(self, full_name: str = '') -> str:
        test_name = re.search("[A-ZА-Я]+[0-9/]+[/A-ZА-Я0-9]+",full_name.replace('&amp;#x2F;', '/').replace('&#x2F;', ''))
        test_name_1 = re.search("[A-ZА-Я]+[0-9/]+", full_name.replace('&#x2F;', ''))
        test_name_2 = re.search("[A-ZА-Я]+[0-9/]+[/A-ZА-Я0-9]+",full_name.replace('Hammer', '').replace('HAMMER', '').replace('Flex', '').replace('flex', '').replace(' ', '').replace('&amp;#x2F;', '/').replace('&#x2F;', ''))
        test_name_3 = re.search(r"[A-ZА-Я/]+ *\d+", full_name.replace('&amp;#x2F;', '/'))
        name = test_name.group(0) if test_name else test_name_1.group(0) if test_name_1 else test_name_2.group(0) if test_name_2 else test_name_3.group(0).replace(' ', '') if test_name_3 else full_name
        return name

    def parser_ozon(self, driver=None):
        driver = driver if driver else Driver_Chrom().loadChrome(headless=True)
        result = []
        unic_code = set()
        flag = True
        for page in range(1, 40):
            print(f'Page {page}')
            if flag:
                try:
                    driver.get(f'{self.url_ozon}?page={page}')
                    time.sleep(2)
                    all_json = json.loads(driver.page_source.strip(self.clean_json_ozon))
                    check = [x for x, y in all_json['catalog']['searchResultsV2'].items()]
                    res = jmespath.search(self.jmespath_ozon, all_json['catalog']['searchResultsV2'][check[0]])
                    for item in res:
                        try:
                            item_code = item[2][0]
                            if item_code not in unic_code:
                                name = self.find_name(item[0][0])
                                price = item[1][0].strip(' ₽').strip(' ').replace('\u2009', '')
                                link = f'https://www.ozon.ru/product/{item_code}'
                                driver.get(link)
                                time.sleep(2)
                                find_seller = driver.find_elements(By.XPATH, "//a[contains(@href, 'https://www.ozon.ru/seller/')]")
                                seller = find_seller[-1].text if len(find_seller) > 1 else find_seller[0].text
                                result.append(('OZON', seller, name, price, datetime.date.today().strftime('%d.%m.%Y')))
                                unic_code.add(item_code)
                            else:
                                print('Дубликат')
                        except:
                            print('Тут ошибка')
                except:
                    print('сработал флаг')
                    flag = True
            else:
                break
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=result, range="парсер OZON WB!A1:E1")
        return result

    def parser_wb(self, driver=None):
        driver = driver if driver else Driver_Chrom().loadChrome(headless=True)
        result = []
        flag = True
        for page in range(1, 10):
            if flag:
                try:
                    wb_url = f'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-2162196,-1257786&emp=0&lang=ru&locale=ru&page={page}&pricemarginCoeff=1.0&query=HAMMER&priceU=100000%3B2400000&reg=0&regions=80,64,83,4,38,33,70,68,69,86,75,30,40,48,1,66,31,22,71&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false'
                    driver.get(f'{wb_url}')
                    all_json = json.loads(driver.page_source.strip(self.clean_json_ozon))['data']['products']
                    for item in all_json:
                        name = self.find_name(item['name'])
                        price = int(item['salePriceU']) / 100
                        try:
                            link = f'https://www.wildberries.ru/catalog/{item["id"]}/detail.aspx'
                            driver.get(link)
                            time.sleep(1)
                            seller = driver.find_element(By.XPATH,"//a[contains(@class, 'seller-info__name seller-info__name--link')]").text
                            result.append(('WB', seller, name, price, datetime.date.today().strftime('%d.%m.%Y')))
                        except:
                            pass
                except:
                    flag = False
            else:
                break
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=result, range="парсер OZON WB!A1:E1")

    def parser_sber(self, driver=None):
        driver = driver if driver else Driver_Chrom().loadChrome(headless=True)
        unik_name = set()
        all_links = []
        result = []
        driver.get(self.url_sber)
        flag = True
        while flag:
            num = driver.find_elements(By.XPATH, self.card_link_xpath)
            time.sleep(2)
            try:
                for i in num:
                    link = i.get_attribute('href').replace('/#?related_search=hammer', '')
                    all_links.append(link)
            except:
                pass
            try:
                driver.find_element(By.XPATH, self.next_page).click()
            except:
                flag = False

        for href in all_links:
            driver.get(href)
            time.sleep(2)
            name = self.find_name(driver.find_element(By.XPATH, self.name_xpath).text)
            print(name)
            try:
                driver.find_element(By.XPATH, self.card_ofers).click()
                time.sleep(1)
                ofers_check = driver.find_elements(By.XPATH, self.offers)
                for offer in ofers_check:
                    try:
                        seller = offer.find_element(By.XPATH, self.seller_xpath).text
                        price = offer.find_element(By.XPATH, self.price_xpath).text
                        print(seller, price)
                        if f'{seller}{name}' not in unik_name:
                            result.append(('SBER', seller, name, price, datetime.date.today().strftime('%d.%m.%Y')))
                            unik_name.add(f'{seller}{name}')
                    except:
                        pass
            except:
                pass
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=result, range="парсер OZON WB!A1:E1")

    def parser_vi(self, driver=None):
        driver = driver if driver else Driver_Chrom().loadChrome(headless=True)
        result = []
        url = f'https://spb.vseinstrumenti.ru/brand/hammer---2088444/?asc=desc&orderby=price'
        driver.get(url)
        time.sleep(5)
        last_page = min(int(driver.find_elements(By.XPATH, '//a[@class="number"]')[-1].text), 100)
        for page in range(1, last_page):
            if page > 1:
                url = f'https://spb.vseinstrumenti.ru/brand/hammer---2088444/page{page}/?asc=desc&orderby=price'
            else:
                url = f'https://spb.vseinstrumenti.ru/brand/hammer---2088444/?asc=desc&orderby=price'
            driver.get(url)
            time.sleep(5)
            all_cards_on_the_page = driver.find_elements(By.XPATH, self.xpath_for_cards_VI)
            for card in all_cards_on_the_page:
                try:
                    card.find_element(By.XPATH, self.check_availability_VI)
                    break
                except:
                    full_name = card.find_element(By.XPATH, self.xpath_for_name_VI).get_attribute('title')
                    name = self.find_name(full_name)
                    price = card.find_element(By.XPATH, self.xpath_for_price_VI).text.replace(' р.', '').replace(' ', '')
                    result.append(('VI', 'Vseinstrumenti', name, price, datetime.date.today().strftime('%d. %m. %Y')))
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=result, range="парсер OZON WB!A1:E1")

    def parser_citilink(self, driver=None):
        driver = driver if driver else Driver_Chrom().loadChrome(headless=True)
        result = []
        for page in range(1, 20):
            driver.get(f'{self.url_citilink}&p={page}')
            time.sleep(1)
            all_cards = driver.find_elements(By.XPATH, '//div[@data-meta-product-id]')
            try:
                for card in all_cards:
                    full_name = card.find_element(By.XPATH, './/a[@title]').get_attribute('title')
                    name = self.find_name(full_name)
                    price = card.find_element(By.XPATH, './/span[@data-meta-price]').text.replace('₽', '')
                    result.append(('Citilink', 'Citilink', name, price, datetime.date.today().strftime('%d. %m. %Y')))
            except:
                break
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=result, range="парсер OZON WB!A1:E1")

    def parserMvideo(self, driver=None):
        driver = driver if driver else Driver_Chrom().loadChrome(headless=True)
        result = []
        flag = True
        for page in range(1, 20):
            if flag:
                driver.get(f'{self.mvideo_url}&page={page}')
                time.sleep(2)
                try:
                    names = list(map(lambda x: self.find_name(x.text), driver.find_elements(By.XPATH, self.mvideo_cards_xpath)))
                    prices = list(map(lambda x: x.text.replace(' ₽', '').replace(' ', ''), driver.find_elements(By.XPATH, self.mvideo_cards_xpath_price)))
                    result.extend(list(zip(['Mvideo' for _ in range(len(names))], ['Mvideo' for _ in range(len(names))], names, prices, [datetime.date.today().strftime('%d. %m. %Y') for _ in range(len(names))])))
                except:
                    flag = False
            else:
                break
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=result, range="парсер OZON WB!A1:E1")

    def parser_eldorado(self, driver=None):
        driver = driver if driver else Driver_Chrom().loadChrome(headless=True)
        result = []
        unic_name = set()
        for page in range(1, 20):
            try:
                driver.get(f'{self.url_eldorado}?page={page}')
                time.sleep(5)
                all_cards = driver.find_elements(By.XPATH, self.cards_xpath_eldarado)
                for card in all_cards:
                    name = self.find_name(card.find_element(By.XPATH, self.name_xpath_eldarado).text)
                    price = card.find_element(By.XPATH, self.price_xpath_eldarado).text
                    if name not in unic_name:
                        result.append(('Eldarado', 'Eldarado', name, price, datetime.date.today().strftime('%d. %m. %Y')))
                        unic_name.add(name)
                        print(name, price)
                    else:
                        print('Finish')
            except:
                break
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=result, range="парсер OZON WB!A1:E1")

    def parser_holodilnik(self, driver=None):
        driver = driver if driver else Driver_Chrom().loadChrome(headless=True)
        result = []
        for page in range(1, 3):
            driver.get(f'{self.url_holodilnik}?page={page}')
            time.sleep(2)
            all_cards = driver.find_elements(By.XPATH, self.cards_xpath_holodilnik)
            [result.append(('Holodilnik', 'Holodilnik', self.find_name(i.find_element(By.XPATH, self.name_xpath_holodilnik).text), i.find_element(By.XPATH, self.price_xpath_holodilnik).get_attribute('content').replace(' ₽', ''), datetime.date.today().strftime('%d. %m. %Y'))) for i in all_cards]
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=result, range="парсер OZON WB!A1:E1")

    def parser_ozon_LEX(self, driver=None):
        driver = driver if driver else Driver_Chrom().loadChrome(headless=True)
        result = []
        unic_code = set()
        flag = True
        for page in range(1, 20):
            if flag:
                try:
                    driver.get(f'{self.url_ozon_LEX}/?page={page}')
                    time.sleep(2)
                    all_json = json.loads(driver.page_source.strip(self.clean_json_ozon))
                    check = [x for x, y in all_json['catalog']['searchResultsV2'].items()]
                    res = jmespath.search(self.jmespath_ozon_LEX, all_json['catalog']['searchResultsV2'][check[0]])
                    # pprint(res)
                    for item in res:
                        try:
                            item_code = item[2]
                            if item_code not in unic_code:
                                name = self.find_name(item[0][0])
                                price = item[1][0].strip(' ₽').strip(' ').replace('\u2009', '')
                                link = f'https://www.ozon.ru{item[2]}'
                                driver.get(link)
                                time.sleep(2)
                                find_seller = driver.find_elements(By.XPATH, "//a[contains(@href, 'https://www.ozon.ru/seller/')]")
                                seller = find_seller[-1].text if len(find_seller) > 1 else find_seller[0].text
                                if 'LEXHH6040BL' in name.upper():
                                    print('Тут')
                                    screenshot = driver.get_screenshot_as_base64()
                                    image_bytes = base64.b64decode(screenshot)
                                    gs = GoogleSheet()
                                    gs.save_scrinchot(image_bytes, f'{name}_{seller}.png')
                                    print('nут')
                                print(name, price, seller)
                                result.append(('OZON', seller, name, price, datetime.date.today().strftime('%d.%m.%Y')))
                                unic_code.add(item_code)
                        except:
                            pass
                except:
                    flag = False
            else:
                break
        gs = GoogleSheet(self.SPREADSHEET_ID)
        gs.append_data(value_range_body=result, range="парсер OZON WB!A1:E1")
        return result

    def main(self):
        driver = Driver_Chrom().loadChrome(headless=True)
        # self.parser_ozon_LEX(driver)
        self.parser_ozon(driver)
        self.parser_wb(driver)
        self.parser_vi(driver)
        self.parser_citilink(driver)
        self.parserMvideo(driver)
        self.parser_sber(driver)
        self.parser_eldorado(driver)
        self.parser_holodilnik(driver)
        driver.close()
        driver.quit()


if __name__ == "__main__":
    ParserKRC().parser_ozon()