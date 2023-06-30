import pandas as pd
from datetime import datetime, timedelta
from push_to_google_sheets import GoogleSheet
from openpyxl import Workbook
from statistics import mean

order_plan = {}
coming_plan = {}
current_stock = GoogleSheet().get_current_stock()
current_orderes = GoogleSheet().get_current_orders()
sales_plan = GoogleSheet().get_sales_plan()


def supper(sales_plan, n) -> dict:
    result = []

    for item, sales in sales_plan["Product"].items():
        num = pupper_test(sales, item, n)
        result.append(num[0])
    GoogleSheet().delete_orders()
    GoogleSheet().append_orders(range="Остатки прогнозные!A1:W1", value_range_body=result)
    # save_list_to_excel(result, "orders.xlsx")
    return ""


# Функция для сохранения списка в файле Excel
def save_list_to_excel(data_list, file_name):
    workbook = Workbook()
    sheet = workbook.active

    # Запись данных в таблицу
    for row_idx, row_data in enumerate(data_list, start=1):
        for col_idx, value in enumerate(row_data, start=1):
            if isinstance(value, list):
                value = ', '.join(str(x) for x in value)  # Преобразование списка в строку
            sheet.cell(row=row_idx, column=col_idx, value=value)

    # Сохранение файла
    workbook.save(file_name)

def pupper_test(data, item, n):
    result_for_table = [item]
    new_list = []
    turnower_list = []
    counter = 5
    planovie_zakazi = []
    sales_list = list(data["Month"].values())
    sales_date_list = list(data["Month"].keys())
    carant_stock = current_stock.get(item, 0)
    order_plan[item] = {"Month": {}}
    coming_plan[item] = {"Month": {}}
    for i in range(len(sales_list)):
        current_order = current_orderes["Product"].get(item).get(sales_date_list[i], 0) if item in current_orderes["Product"] else 0
        carant_stock = max(int(carant_stock) - sales_list[i] + current_order, 0)
        new_list.append(carant_stock)
        result_for_table.append(carant_stock)
        turnower = 0
        avg_stock = 0
        sum_sales = 0
        new_order = 0
        if len(new_list) > n:
            avg_stock = mean(new_list[i - n:i])
            sum_sales = round(sum(sales_list[i - n:i]))
            turnower = avg_stock / max(1, sum_sales) * n
            turnower_list.append([sales_date_list[i], turnower])
            if turnower < n:
                if counter >= n:
                    new_order = round(sum(sales_list[i:i + n + 2]), -2)
                    order_plan[item]["Month"][sales_date_list[i - n]] = new_order
                    print([item, sales_date_list[i - n], new_order])
                    GoogleSheet().append_orders(range="Новые заказы!A1:C1", value_range_body=[item, sales_date_list[i - n], new_order])

                    carant_stock += new_order
                    coming_plan[item]["Month"][sales_date_list[i]] = new_order
                    counter = 0
                else:
                    counter += 1
        # print(f'Дата: {sales_date_list[i]}, Текущий сток: {carant_stock} ,  Оборачиваемость {turnower}, Продажи {sales_list[i]}, средние остатки {avg_stock}, Сумма продаж {sum_sales}, получили заказ  {new_order}')

    return result_for_table


supper(sales_plan, 5)
