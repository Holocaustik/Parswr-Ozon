from google.cloud import bigquery
import os

# def insert_data_into_bigquery(project_id, dataset_id, table_id, rows):
#
#     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/vladimirivliev/PycharmProjects/pythonProject1/credentials/credentials1.json'
#
#     # Создаем объект клиента BigQuery
#     client = bigquery.Client(project=project_id)
#
#     # Определяем ссылку на таблицу
#     table_ref = client.dataset(dataset_id).table(table_id)
#
#     # Создаем объект таблицы
#     table = client.get_table(table_ref)
#
#     # Вставляем строки данных в таблицу
#     errors = client.insert_rows(table, rows)
#
#     if errors == []:
#         print('Данные успешно записаны в таблицу BigQuery.')
#     else:
#         print('Произошла ошибка при записи данных в таблицу BigQuery:', errors)
#
# # Пример использования функции
# project_id = 'parser-ozon-363016'
# dataset_id = 'parser_result'
# table_id = 'Parser_everyday'
# rows = [
#     {
#         'Internet_resource': 'example.com',
#         'salesman': 'John Doe',
#         'product': 'Example Product',
#         'customer_price': 100.0,
#         'date': '2023-06-12'
#     },
#     # Дополнительные строки данных...
# ]
#
# insert_data_into_bigquery(project_id, dataset_id, table_id, rows)

from google.cloud import bigquery

def insert_data_with_sql_query(project_id, sql_query):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/vladimirivliev/PycharmProjects/pythonProject1/credentials/credentials1.json'

    # Создаем объект клиента BigQuery
    client = bigquery.Client(project=project_id)

    # Выполняем SQL запрос
    query_job = client.query(sql_query)

    # Ожидаем завершения выполнения запроса
    query_job.result()

    print('Запись успешно добавлена в таблицу BigQuery.')

# Пример использования функции
project_id = '363016'
sql_query = '''
    INSERT INTO `parser-ozon-363016.parser_result.Parser_everyday` (Internet_resource, salesman, product, customer_price, date)
    VALUES ('example.com', 'John Doe', 'Example Product', 100.0, '2023-06-12');
'''

insert_data_with_sql_query(project_id, sql_query)
