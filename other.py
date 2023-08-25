import datetime
import json
import re
import time
from pprint import pprint
from find_name import find_name
import jmespath
from selenium.webdriver.common.by import By
from browser import Driver_Chrom
from push_to_google_sheets import GoogleSheet
from urls import urls
import concurrent.futures
from tqdm import tqdm
import multiprocessing



def remove_duplicates(input_list: list = [], key: str = None) -> list:
    seen = set()
    output_list = []

    for d in input_list:
        # Преобразуем словарь в неизменяемый хешируемый тип (tuple)
        if key:
            item = tuple(d[key].items()) if isinstance(d[key], dict) else d[key]
        else:
            item = tuple(d.items())

        # Если элемент не встречался ранее, добавляем его в выходной список и отмечаем как виденный
        if item not in seen:
            seen.add(item)
            output_list.append(d)
    print(len(output_list))
    return output_list




# num = {'isAvailable': True,
#  'lexemes': {'currency': 'Валюта',
#              'includeVatTextMobile': 'Цена с НДС',
#              'moreText': 'Подробнее',
#              'notRefundVatText': 'НДС не возмещается',
#              'withOzonCard': 'c Ozon Картой',
#              'withoutOzonCard': 'без Ozon Карты',
#              'withoutVatText': 'без НДС',
#              'withoutVatTextCapitalize': 'Без НДС',
#              'withoutVatTextMobile': 'Цена без НДС'},
#  'originalPrice': '17\u2009699\u2009₽',
#  'params': {'showPpu': True,
#             'withOzonAccount': '/modal/withOzonAccount',
#             'withoutOzonAccount': '/modal/withoutOzonAccount'},
#  'price': '8\u2009909\u2009₽',
#  'showOriginalPrice': True}
#
# num1 = {'coverImageUrl': 'https://cdn1.ozone.ru/s3/multimedia-3/c50/6574059783.jpg',
#  'name': 'Углошлифовальная машина (болгарка) Hammer Flex USM1650D',
#  'params': {'triggeringObjectSelector': '#short-product-info-trigger-new'},
#  'seller': {'link': '/seller/255333/',
#             'logoImageUrl': 'https://cdn1.ozonusercontent.com/s3/marketing-api/banners/ut/YY/utYYIaPqbeGB87yUvCQpUkHiN2RXExwA.png',
#             'name': 'PERFECTO',
#             'subtitle': 'Товары на все случаи'},
#  'sku': 1016232949}
#
#
#
# num2 = {'cellTrackingInfo': {'uis': {'1': '9e16259469872f4986b83bd7914272452930d562', '2': 'cbda50952695e352407aa5f561dfbe6db44feb8b', '6': 'e7902f5556d506c755d1694b490fb2133b6399b8', '8': '0292cfb5a09674aed785d3c120bae3640d4b410e', '9': '5f88d40335b4551a2b45cb7a61c4ccf7e0148628', 'premiumSubscribe': 'c9e49d9ab1f4a1b52db3a6afd8686d1d6a68893a'}, 'sellers': {'main': 'a79819fdd405c4f00b0074fac47d28b0794f8627'}}, 'lexemes': {'premiumBtnText': 'Premium-магазин', 'sellerNameTitleDef': 'Продавец'}, 'id': 867758, 'name': 'Hammer, Tesla, Wester', 'link': 'https://www.ozon.ru/seller/hammer-tesla-wester-867758/', 'credentials': ['ООО "ОПТ-ТРЕЙД"', '188640, ЛО, М.Р-Н Всеволожский, г. Всеволожск, пр. Всеволожский д. 17 ком. 217', '1227800031722', 'Режим работы — согласно режиму работы OZON'], 'logoImageUrl': 'https://cdn1.ozonusercontent.com/s3/marketing-api/banners/dk/lC/c96/dklCOGzhNT4Zbf0NXmNiweJyacdIun24.jpg', 'backgroundImageUrl': '', 'mainAdvantages': [{'id': 2, 'content': {'headRs': [{'type': 'textBold', 'content': '4,7'}, {'type': 'text', 'content': ' рейтинг товаров'}], 'hintRs': [{'type': 'text', 'content': 'Рейтинг строится из средней оценки товаров продавца'}]}, 'title': '', 'key': 'rating16', 'link': '', 'iconImageUrl': ''}, {'id': 3, 'content': {'headRs': [{'type': 'textBold', 'content': '97% '}, {'type': 'text', 'content': 'вовремя'}], 'hintRs': [{'type': 'text', 'content': 'Столько заказов за последние 30 дней продавец передал в доставку без опозданий'}]}, 'title': '', 'key': 'car16', 'link': '', 'iconImageUrl': ''}], 'secondaryAdvantages': [{'id': 8, 'content': {'headRs': [{'type': 'text', 'content': 'Безопасная оплата онлайн'}]}, 'title': '', 'key': 'creditCard24', 'link': '', 'iconImageUrl': 'https://cdn1.ozone.ru/graphics/pdp/icons/safety_pay.svg'}, {'id': 9, 'content': {'headRs': [{'type': 'text', 'content': 'Возврат 30 дней, с '}, {'type': 'link', 'content': 'Ozon Premium', 'href': '/highlight/premium/', 'target': '_blank', 'keyValue': 'premiumSubscribe'}, {'type': 'text', 'content': ' — 60 дней'}], 'hintRs': [{'type': 'text', 'content': 'Сроки и условия возврата товаров. '}, {'type': 'link', 'content': 'Подробнее', 'href': 'https://docs.ozon.ru/common/otmena-i-vozvrat-zakaza/kak-vernut-tovar', 'target': '_blank', 'keyValue': 'returns'}]}, 'title': 'Условия возврата', 'key': 'returnPolicy24', 'link': '', 'iconImageUrl': 'https://cdn1.ozone.ru/graphics/pdp/icons/refund.svg'}], 'subtitle': 'Официальный представитель', 'isPremium': True, 'premiumLink': '/modal/PremiumPlusSellerInfoWeb', 'subscription': 'premiumPlus', 'params': {'advantageHintDeliveryInTimeText': 'Столько заказов за последние 30 дней продавец передал в доставку без опозданий', 'advantageHintIndividualBonusesText': 'Бонусы продавца начисляются за покупки. Эти бонусы вы сможете потратить на будущие покупки у этого продавца. Бонусы, которые вам начислили продавцы, доступны в разделе Баллы личного кабинета Ozon. 1 бонус = 1 рубль', 'advantageTitleIndividualBonusesText': 'Бонусы продавца', 'disclaimer': 'Обращаем Ваше внимание, что OZON не продаёт и не доставляет алкогольную продукцию. Здесь Вы можете забронировать интересующий Вас товар в магазинах партнёров. Информацию об адресах, где можно приобрести и оплатить алкогольную продукцию, реквизиты продавцов и лицензий на розничную продажу алкогольной продукции смотрите %link%.', 'disclaimerLink': 'https://seller-edu.ozon.ru/docs/work-with-goods/spisok-partnerov-alcohol.html', 'disclaimerLinkText': 'тут', 'returnText': 'Товар надлежащего качества обмену и возврату не подлежит', 'showAuthorizedSeller': False, 'theme': 'apparel'}}
#
#
