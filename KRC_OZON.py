import datetime
import json
import time
from browser import Driver_Chrom
from push_to_google_sheets import GoogleSheet


def krc_ozon():
    SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
    driver = Driver_Chrom().loadChrome(headless=True)
    url_ozon = 'https://www.ozon.ru/api/composer-api.bx/page/json/v1?url=https://www.ozon.ru/brand/hammer-26303172/category/elektroinstrumenty-9857/'
    result = []
    for num in range(16):
        driver.get(f'{url_ozon}/?page={num}')
        time.sleep(1)
        num = json.loads(driver.page_source.strip('<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">'))
        num1 = num['catalog']['searchResultsV2']['searchResultsV2-312617-default-1']['items']
        for i in num1:
            for j in i['mainState']:
                try:
                    check_name = j['atom']['textAtom']['testInfo']
                    if check_name['automatizationId'] == 'tile-name':
                        name = j['atom']['textAtom']['text'].replace("Flex ", '')
                        index_HAMMER = name.upper().index('HAMMER ')
                        pre_name = name[index_HAMMER:]
                        if pre_name.count(' ') > 1:
                            end_index = name[index_HAMMER + 7:].index(' ')
                            name_done = name[index_HAMMER:end_index + index_HAMMER + 7].upper().strip(',').strip().strip("  2x2Ач LiION").strip("   SDS+").strip("  1x1.5Ач LiION").replace("&#X2F;", "/").replace("&#34;", "")
                        else:
                            name_done = pre_name.upper().strip(',').strip().strip("  2x2Ач LiION").strip("   SDS+").strip("  1x1.5Ач LiION").replace("&#X2F;", "/").replace("&#34;", "")
                except:
                    try:
                        price = j['atom']['price']['price'].strip(' ₽').strip(' ')

                    except:
                        pass
            try:
                pre_name_sales = i['multiButton']['ozonSubtitle']['textAtomWithIcon']['text']
                index_sales = pre_name_sales.index('продавец')
                name_sales = pre_name_sales[index_sales:]
                if name_sales != '220 Вольт':
                    pre_result = ('OZON', name_sales.strip('продавец '), name_done, price, datetime.date.today().strftime('%d. %m. %Y'))
                    if pre_result not in result:
                        result.append(pre_result)
            except:
                pass
        time.sleep(20)
    data = result
    gs = GoogleSheet(SPREADSHEET_ID)
    gs.append_data(value_range_body=data, range="парсер OZON WB!A1:E1")


if __name__ == "__main__":
    krc_ozon()

