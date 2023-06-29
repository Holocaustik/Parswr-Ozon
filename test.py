from  KRC import ParserKRC
import time

def my_task():
    # Ваш код, который нужно выполнить каждое утро
    print("Запуск задачи каждое утро")

while True:
    now = time.localtime()
    if now.tm_hour == 7 and now.tm_min == 00 and now.tm_sec == 0:
        ParserKRC().main()
        # Добавьте паузу, чтобы избежать множественного запуска в указанное время
        time.sleep(60)  # Подождите 60 секунд перед следующей проверкой
    else:
        # Добавьте паузу, чтобы избежать непрерывной проверки времени
        time.sleep(1)  # Подождите 1 секунду перед следующей проверкой


