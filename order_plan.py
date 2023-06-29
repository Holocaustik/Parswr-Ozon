import pandas as pd
from datetime import datetime, timedelta
from push_to_google_sheets import GoogleSheet
order_plan = {}
coming_plan = {}
current_stock = {
        628168: 800,
        28168: 2000
    }
# sales_plan = {
#     "Product": {
#         628168: {
#             "Month": {
#                 "30.06.2023": 160,
#                 "31.07.2023": 187,
#                 "31.08.2023": 147,
#                 "30.09.2023": 131,
#                 "31.10.2023": 131,
#                 "30.11.2023": 165,
#                 "31.12.2023": 125,
#                 "31.01.2024": 140,
#                 "29.02.2024": 135,
#                 "31.03.2024": 113,
#                 "30.04.2024": 220,
#                 "31.05.2024": 160,
#                 "30.06.2024": 134,
#                 "31.07.2024": 154,
#                 "31.08.2024": 147,
#                 "30.09.2024": 131,
#                 "31.10.2024": 131,
#                 "30.11.2024": 250,
#                 "31.12.2024": 200,
#                 "31.01.2025": 80,
#                 "28.02.2025": 140,
#                 "31.03.2025": 180,
#                 "30.04.2025": 240,
#                 "31.05.2025": 300,
#             }
#         },
#         28168: {
#             "Month": {
#                 "30.06.2023": 134,
#                 "31.07.2023": 154,
#                 "31.08.2023": 147,
#                 "30.09.2023": 131,
#                 "31.10.2023": 131,
#                 "30.11.2023": 165,
#                 "31.12.2023": 125,
#                 "31.01.2024": 140,
#                 "29.02.2024": 135,
#                 "31.03.2024": 113,
#                 "30.04.2024": 109,
#                 "31.05.2024": 105,
#                 "30.06.2024": 134,
#                 "31.07.2024": 154,
#                 "31.08.2024": 147,
#                 "30.09.2024": 131,
#                 "31.10.2024": 131}
#                 }
#     }
#     }
current_orderes = {
        628168: {
            "31.10.2023": 0},
        28168: {
            "30.09.2023": 1000
        }
    }

sales_plan = GoogleSheet().get_sales_plan()

def supper(sales_plan, n) -> dict:
    for item, sales in sales_plan["Product"].items():
        pupper_test(sales, item, n)
    return ""

def pupper(data, item, n):
    new_list = []
    turnower_list = []
    counter = 5
    sales_list = list(data["Month"].values())
    sales_date_list = list(data["Month"].keys())
    carant_stock = current_stock.get(item)
    order_plan[item] = {"Month": {}}
    coming_plan[item] = {"Month": {}}
    for i in range(n, len(sales_list) ):
        current_order = current_orderes.get(item).get(sales_date_list[i - n], 0)
        order_planed = coming_plan.get(item)["Month"].get(sales_date_list[i - n + 2], 0) if item in coming_plan else 0
        carant_stock = max(carant_stock - sales_list[i - n] + current_order + order_planed, 0)
        new_list.append(carant_stock)
        try:
            avg_stock = sum(new_list[i-n:i]) / n if i - n >= n else sum(new_list[:i]) / len(new_list)
            sum_sales = sum(sales_list[i-n:i])
            turnower = avg_stock / sum_sales * n
            new_order = sum(sales_list[i:i + n + 1])
            turnower_list.append([sales_date_list[i-n], turnower])
            if turnower < 3.5:
                if counter >= n and new_order > 0:
                    order_plan[item]["Month"][sales_date_list[i-n - 2]] = new_order
                    coming_plan[item]["Month"][sales_date_list[i]] = new_order
                    counter = 0
                else:
                    counter += 1
        except:
            pass
    print(sales_list)
    print(order_plan)
    print(new_list)
    print(turnower_list)




    for date, val in data["Month"].items():
        # print(val)
        pass


def pupper_test(data, item, n):
    print(data)
    new_list = []
    turnower_list = []
    counter = 5
    sales_list = list(data["Month"].values())
    print(sales_list)
    sales_date_list = list(data["Month"].keys())
    carant_stock = current_stock.get(item, 0)
    order_plan[item] = {"Month": {}}
    coming_plan[item] = {"Month": {}}
    for i in range(len(sales_list)):
        current_order = current_orderes.get(item).get(sales_date_list[i], 0) if item in current_orderes else 0
        # order_planed = order_plan.get(item)["Month"].get(sales_date_list[i], 0) if item in order_plan else 0
        print(max(carant_stock - sales_list[i] + current_order, 0))

        carant_stock = max(carant_stock - sales_list[i] + current_order, 0)
        new_list.append(carant_stock)
        turnower = 0
        avg_stock = 0
        sum_sales = 0
        new_order = 0
        if len(new_list) > n:
            avg_stock = round(sum(new_list[i - n:i]) / n if i > n + 4 else sum(new_list[i - n:i]) / len(new_list[i - n:i]))
            sum_sales = round(sum(sales_list[i:i + n]))
            turnower = avg_stock / max(1, sum_sales) * n
            turnower_list.append([sales_date_list[i], turnower])
            if turnower < n:
                if counter >= n:
                    new_order = round(sum(sales_list[i:i + n + 1]), -2)
                    order_plan[item]["Month"][sales_date_list[i - n + 1]] = new_order
                    carant_stock += new_order
                    coming_plan[item]["Month"][sales_date_list[i]] = new_order
                    counter = 0
                else:
                    counter += 1
        print(f'Дата: {sales_date_list[i]}, Текущий сток: {carant_stock} ,  Оборачиваемость {turnower}, Продажи {sales_list[i]}, средние остатки {avg_stock}, Сумма продаж {sum_sales}, получили заказ  {new_order}')

    print(sales_list)
    print(order_plan)
    print(new_list)
    print(turnower_list)



supper(sales_plan, 5)