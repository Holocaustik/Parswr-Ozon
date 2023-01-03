import datetime
import json
import time
from browser import Driver_Chrom
from push_to_google_sheets import GoogleSheet

#
def get_biggest(numbers: list) -> int:
    SPREADSHEET_ID = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
    gs = GoogleSheet(SPREADSHEET_ID)
    gs.append_data(value_range_body=numbers, range="парсер OZON WB!A1:E1")



print(get_biggest([61, 228, 9, 3, 11]))
get_biggest([7, 71, 72])




len_range, X, Y, A, B = map(int, input().split())
range_list, num, num1 = list(range(1, int(len_range) + 1)), list(range(X, Y + 1))[::-1], list(range(A, B))[::-1]
result = sum([range_list[:X], num, num1, range_list[B:]], [])
print(*result)


