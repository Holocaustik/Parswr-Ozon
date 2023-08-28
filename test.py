import time

from browser import Driver_Chrom

# from  KRC import ParserKRC
# import time
#
# def my_task():
#     # Ваш код, который нужно выполнить каждое утро
#     print("Запуск задачи каждое утро")
#
# while True:
#     now = time.localtime()
#     if now.tm_hour == 7 and now.tm_min == 00 and now.tm_sec == 0:
#         ParserKRC().main()
#         # Добавьте паузу, чтобы избежать множественного запуска в указанное время
#         time.sleep(60)  # Подождите 60 секунд перед следующей проверкой
#     else:
#         # Добавьте паузу, чтобы избежать непрерывной проверки времени
#         time.sleep(1)  # Подождите 1 секунду перед следующей проверкой
#
#
url = 'https://megamarket.ru/api/mobile/v1/promoContentService/promoContent/get'
par = 'https://megamarket.ru/catalog/details/drel-shurupovert-hammer-acd12a-15ach-s-dvumya-akkumulyatorami-735855-100028939311/'

driver = Driver_Chrom().loadChromTest(headless=False)
driver.get(url, param=par)
time.sleep(5)