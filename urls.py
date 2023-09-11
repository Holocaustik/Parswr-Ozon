urls = {
    'clean_json': '<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">',
    'google_sheets_name': {
        'collecting_products': 'Парсер справочник товаров!A1:H1',
        'collecting_sellers': 'Парсер справочник продавцов!A1:H1',
        'main_parser': "парсер OZON WB!A1:E1",
        "main_parser_new": "Результат парсера!A1:D1"

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
                'ingco': 'https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=https://www.ozon.ru/brand/ingco-72464691/'
                }},
        'jmespath': {
            'STM': {
                'main': 'items[*].[mainState[*].atom.textAtom.text, mainState[*].atom.priceV2.price[0].text || mainState[*].atom.priceWithTitle.price, topRightButtons[*].favoriteProductMoleculeV2.id]',
                'seller_name': 'seller.name || name',
                'seller_id': 'seller.link || id',
                'credentials': 'credentials',
                'price': 'cardPrice || price || originalPrice'},
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
            'seller_1': 'webCurrentSeller'
        }
    },
    'WB': {
        'brand': {
            'hammer': 22609,
            'wester': 17920
            # 17919 Tesla, убрап так как там много говна и нет нашего товара
            },
        'xpath': {
            'seller': "//a[contains(@class, 'seller-info__name seller-info__name--link')]",
            'price': "//span[contains(text(), 'без Ozon Карты')]//preceding::span[2]"
        }
    },
    'sber': {
        'url': {
            'STM': [
                'https://sbermegamarket.ru/catalog/?q=hammer&collectionId=14576',
                'https://megamarket.ru/catalog/?q=tesla&collectionId=6095769',
                'https://megamarket.ru/catalog/?q=wester&collectionId=15153',
                'https://megamarket.ru/catalog/?q=wester&collectionId=12007'],
        },
        'xpath': {
            'seller_xpath': './/div[contains(@class, "product-offer-name")]/div[1]',
            'seller_xpath_main': '//span[contains(@class, "pdp-merchant-rating-block__merchant-name")]',
            'price_xpath': './/span[contains(@class, "product-offer-price__amount")]',
            'price_xpath_main': '//span[contains(@class, "pdp-sales-block__price-final")]',
            # 'card_link_xpath': './/div[contains(@class, "catalog-item-desktop")]',
            'card_link_xpath': './/div[contains(@class, "catalog-item-desktop")]//div[@class="item-title"]/a',
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
            'xpath_for_cards_VI': "//div[@data-qa='products-tile']",
            'xpath_for_price_VI': ".//p[@data-qa='product-price-current']",
            'xpath_for_name_VI': ".//a[@data-qa='product-name']",
            'check_availability_VI': ".// div[contains(@data-qa, 'not-available')]",
            'item_code_xpath': ".//p[contains(@data-qa, 'product-code-text')]",
        }
    },
    'citilink': {
        'url': {
            'brand': {'hammer': 'https://www.citilink.ru/search/?text=hammer',}
        },
        'xpath': {
            'all_cards': '//div[@data-meta-product-id]',
            'name': './/a[@title]',
            'price': './/span[@data-meta-price]',
        }
    },
}
