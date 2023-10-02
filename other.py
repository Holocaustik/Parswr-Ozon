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
