import datetime
import json
import re
import asyncio
from proxybroker import Broker
import json
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
import  socket
from http import cookies


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


def get_multy_funk(tasks: list = None, function: object = None, max_workers: int = None, SPREADSHEET_ID: str = '', range: str = None, what_need_save: list = None) -> None:
    """
      Описание функции
        Эта функция запускает переданную ей функцию в кол-ве процессов, которые ей передали и записывает результат в таблицу:


      Эта функция принимает 6 аргументов:

      1 - tasks (Это список объектов, которые будут передаваться в функцию в качестве переменных для выполнения)

      2 - function (Фцнкция, которая будет запускаться)

      3 - max_workers (Кол-во процессов в которых будет работать функция)

      4 - SPREADSHEET_ID (ID таблицы в которую записывается результат)

      5 - range (Куда в таблице нужно записать данные)

      6 - what_need_save (Что нужно записывать)

      """
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        list(tqdm(executor.map(function, tasks), total=len(tasks), desc="Processing", ncols=100))
    if range is not None:
        what_need_save = what_need_save if len(what_need_save) == 1 else list(what_need_save)
        GoogleSheet(SPREADSHEET_ID).append_data(value_range_body=what_need_save, range=range)


def intercept(request):
    cookie = cookies.SimpleCookie()
    cookie.load(request.headers['Cookie'] or '')
    cookie['_lr_uf_-xnoogq'] = 'fa845c27-e6da-43eb-a3dd-b2d02ac950d6'

    del request.headers['Cookie']
    request.headers['Cookie'] = '; '.join(f'{k}={v.value}' for k, v in cookie.items())

class Proxy():
    def __init__(self):
        self.proxy_list = []

    async def show(self, proxies):
        while True:
            proxy = await proxies.get()
            if proxy is None: break
            self.proxy_list.append(f'{proxy.host}:{proxy.port}')



    def get_proxy(self, col: int=10):
        tasks = self.get_tasks_proxy(col)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(tasks)
        print(self.proxy_list)
        return self.proxy_list

    def get_tasks_proxy(self, col: int=10):
        proxies = asyncio.Queue()
        broker = Broker(proxies)
        tasks = asyncio.gather(
            broker.find(types=['HTTP', 'HTTPS'],  countries=["RU"], limit=col),
            self.show(proxies))
        return tasks

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(local_ip)


def extract_json_from_html(html_text):
    # Используем регулярное выражение для извлечения текста JSON из HTML
    json_pattern = re.compile(r'<pre>(.*?)</pre>', re.DOTALL)
    match = json_pattern.search(html_text)
    if match:
        json_text = match.group(1)
        try:
            # Преобразуем строку JSON в объект Python
            json_data = json.loads(json_text)
            return json_data
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON")
            return None
    # else:
    #     print("JSON не найден в тексте HTML")
    #     return None



if __name__ == "__main__":
    Proxy().get_proxy(20)