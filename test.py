import json
import time
from pprint import pprint

import jmespath
from browser import Driver_Chrom
jmespath_ozon = 'items[*].[mainState[*].atom.textAtom.text,mainState[*].atom.priceWithTitle.price || mainState[*].atom.price.price, multiButton.ozonButton.addToCartButtonWithQuantity.action.id]'

link = 'https://www.ozon.ru/api/composer-api.bx/page/json/v1?url=https://www.ozon.ru/brand/hammer-26303172/'
driver = Driver_Chrom().loadChrome(headless=True)
driver.get(f'{link}')
time.sleep(5)
# print(driver.page_source)
clean_json_ozon = '<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">'
all_json = json.loads(driver.page_source.strip(clean_json_ozon))
check = [x for x, y in all_json['catalog']['searchResultsV2'].items()]
print(check)
pprint(all_json)
pprint(all_json['catalog']['searchResultsV2'][check[0]])
res = jmespath.search(jmespath_ozon, all_json['catalog']['searchResultsV2'][check[0]])
for item in res:
    # print(item)
    item_code = item[2]
    name = item[0][0]
    price = item[1][0].strip(' ₽').strip(' ').replace('\u2009', '')
    link = f'https://www.ozon.ru/product/{item[2]}'
    print(name, price, link)
