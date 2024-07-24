urls = {
    'clean_json_1': '<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">',
    'clean_json': '<html><head><meta name="color-scheme" content="light dark"><meta charset="utf-8"></head><body><pre>',
    'google_sheets_name': {
        'collecting_products': 'Парсер справочник товаров!A1:H1',
        'collecting_sellers': 'Парсер справочник продавцов!A1:H1',
        'main_parser': "парсер OZON WB!A1:E1",
        "main_parser_new": "Результат парсера!A1:D1",
        "main_parser_Ozon_anal": "Парсер!A1:D1"



    },
    'Ozon': {
        'url': {
            'brand': {
                'hammer-flex': 'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=https://www.ozon.ru/brand/hammer-flex-100248083/?currency_price=1000.000%3B86670.000',
                'hammer': 'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=https://www.ozon.ru/brand/hammer-26303172/?currency_price=1000.000%3B86670.000',
                # 'hammerflex': 'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=https://www.ozon.ru/brand/hammerflex-100283180/?currency_price=1000.000%3B86670.000',
                # 'HAMMER': 'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=https://www.ozon.ru/brand/hammer-87265380/category/instrumenty-dlya-remonta-i-stroitelstva-9856/?currency_price=1000.000%3B86670.000',
                'tesla': 'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=https://www.ozon.ru/brand/tesla-100085446/category/stroitelstvo-i-remont-9700/?currency_price=1000.000%3B86670.000',
                'wester': 'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=https://www.ozon.ru/brand/wester-27762156/category/stroitelstvo-i-remont-9700/?currency_price=1000.000%3B86670.000',
                'zubr': 'https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=https://www.ozon.ru/brand/zubr-26303502/category/instrumenty-dlya-remonta-i-stroitelstva-9856/',
                'ferm': 'https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=https://www.ozon.ru/brand/ferm-87317356/',
                'ingco': 'https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=https://www.ozon.ru/brand/ingco-72464691/',
                'Foxweld': 'https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=https://www.ozon.ru/category/svarochnoe-oborudovanie-10046/?brand=100504861%2C87112978%2C100524464/?currency_price=1000.000%3B86670.000',
                'All': "https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=https://www.ozon.ru/category/elektroinstrumenty-9857/?batteryvoltage=309459%2C168118%2C308701%2C168119%2C168120%2C168117&category_was_predicted=true&deny_category_prediction=true&from_global=true&includedbattery=37725&opened=features%2Cbatteryvoltage&text=%D1%88%D1%83%D1%80%D1%83%D0%BF%D0%BE%D0%B2%D0%B5%D1%80%D1%82&type=47216",
                }},
        'jmespath': {
            'STM': {
                'main': 'items[*].[mainState[*].atom.textAtom.text, mainState[*].atom.priceV2.price[0].text || mainState[*].atom.priceWithTitle.price, topRightButtons[*].favoriteProductMoleculeV2.id]',
                # 'main': 'items[*].[mainState[*?id=="name"].atom.textAtom.text | [0], mainState[*].atom.priceV2.price[0].text || mainState[*].atom.priceWithTitle.price, topRightButtons[*].favoriteProductMoleculeV2.id]'
                'main_1': 'items[*].[mainState[*].atom.textAtom.text, c.price[0].text || mainState[*].atom.priceWithTitle.price, topRightButtons[*].favoriteProductMoleculeV2.id], mainState[*].atom.testInfo',
                'seller_name': 'seller.name || name',
                'seller_id': 'seller.link || id',
                'credentials': 'credentials',
                'price': 'cardPrice || price || originalPrice',
                'seller': "webCurrentSeller-735663-default-1"},
            'LEX ': 'items[*].[mainState[*].atom.textAtom.text, mainState[*].atom.priceWithTitle.price, action.link]',
            'Foxweld': 'items[*].[mainState[*].atom.textAtom.text, mainState[*].atom.priceWithTitle.price || mainState[*].atom.priceV2.price[0].text, action.link]'
        },
        'xpath': {
            'seller': "//a[contains(@href, 'https://www.ozon.ru/seller/')]",
            'price': "//span[contains(text(), 'без Ozon Карты')]//preceding::span[2]",
            'seller_info_button': "//a[contains(@href, 'https://www.ozon.ru/seller')]//following-sibling::div//following-sibling::div",
            'seller_info': "//div[contains(@class, 'vue-portal-target')]//child::*"
        },
        'key_json': {
            'main': 'searchResultsV2',
            'webPrice': 'webPrice',
            'seller': 'webStickyProducts',
            'seller_1': 'webCurrentSeller',
            'tth': "webCharacteristics"
        }
    },
    'WB': {
        'brand': {
            'hammer': 22609,
            'wester': 17920,
            'tesla': 1234
            # 17919 Tesla, убрап так как там много говна и нет нашего товара
            },
        'xpath': {
            # 'seller': "//a[contains(@class, 'seller-info__name seller-info__name--link')]",
            'seller': "//span[contains(@class, 'seller-info__name')]",
            'price': "//span[contains(text(), 'без Ozon Карты')]//preceding::span[2]"
        }
    },
    'sber': {
        'url': {
            'brand': {
                "hammer": 'https://sbermegamarket.ru/catalog/?q=hammer&collectionId=14576',
                "tesla": 'https://megamarket.ru/catalog/?q=tesla&collectionId=6095769',
                "wester": 'https://megamarket.ru/catalog/?q=wester&collectionId=15153',
                # 'https://megamarket.ru/catalog/?q=wester&collectionId=12007'],
            }},
        'xpath': {
            'seller_xpath': './/div[contains(@class, "product-offer-name")]/div[1]',
            'seller_xpath_main': '//span[contains(@class, "pdp-merchant-rating-block__merchant-name")]',
            'price_xpath': './/span[contains(@class, "product-offer-price__amount")]',
            'price_xpath_main': '//span[contains(@class, "pdp-sales-block__price-final")]',
            'card_xpath': './/div[contains(@class, "catalog-item-desktop")]',
            # 'card_link_xpath': './/div[contains(@class, "catalog-item-desktop")]//div[@class="item-title"]/a',
            'card_link_xpath': './/div[@class="item-title"]/a',
            'card_offers': '//a[contains(@class, "more-offers-button")]',
            'offers': '//div[contains(@class, "product-offer_with-payment-method")]',
            'link': '//div[@class="item-title"]/a',
            # 'name_xpath': './/div[contains(@class, "item-title")]',
            'name_xpath': '//h1[@itemprop = "name"]',
            'next_page': '//li[@class="next"]',
        }
    },
    'VI': {
        'url': {
            'brand': {
                'hammer': 'https://spb.vseinstrumenti.ru/brand/hammer---2088444/',
                'tesla': 'https://spb.vseinstrumenti.ru/brand/tesla--2071870/',
                'wester': 'https://spb.vseinstrumenti.ru/brand/wester-1359/',
                'vihr': 'https://spb.vseinstrumenti.ru/brand/vihr-1007/',
                'zubr': 'https://spb.vseinstrumenti.ru/brand/zubr-665/',
                'interskol': 'https://spb.vseinstrumenti.ru/brand/interskol-19/',
                'champion': 'https://spb.vseinstrumenti.ru/brand/champion-602/',
                'husqvarna': 'https://spb.vseinstrumenti.ru/brand/husqvarna-4/',
                'patriot': 'https://spb.vseinstrumenti.ru/brand/patriot-426/',
                'greenworks': 'https://spb.vseinstrumenti.ru/brand/greenworks-13753/',
                'condtrol': 'https://spb.vseinstrumenti.ru/brand/condtrol-649/',
                'ada': 'https://spb.vseinstrumenti.ru/brand/ada-890/',

            },
        },
        'xpath': {
            'last_page': '//a[@class="number"]',
            'xpath_for_cards_VI': "//div[contains(@data-qa,'products-tile')]",
            'xpath_for_price_VI': ".//p[@data-qa='product-price-current']",
            'xpath_for_name_VI': ".//a[@data-qa='product-name']",
            'check_availability_VI': ".// div[contains(@data-qa, 'not-available')]",
            'item_code_xpath': ".//p[contains(@data-qa, 'product-code-text')]",
        }
    },
    'citilink': {
        'url': {
            'brand': {'hammer': 'https://www.citilink.ru/search/?text=hammer',
                      'tesla': '',
                      'wester': ''}
        },
        'xpath': {
            'all_cards': '//div[@data-meta-product-id]',
            'name': './/a[@title]',
            'price': './/span[@data-meta-price]',
        }
    },
}
