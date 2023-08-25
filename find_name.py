import re


def find_name(full_name: str = '') -> str:

    test_name = re.search("[A-Z]+[0-9/-]+[/A-ZА-Я0-9]+", full_name.replace('&amp;#x2F;', '/').replace('&#x2F;', ''))
    test_name_1 = re.search("[A-ZА-Я]+[0-9/]+", full_name.replace('&#x2F;', ''))
    test_name_2 = re.search("[A-ZА-Я]+[0-9/]+[/A-ZА-Я0-9]+",
                            full_name.replace('Hammer', '').replace('HAMMER', '').replace('Flex', '').replace('flex',
                                                                                                              '').replace(
                                '&amp;#x2F;', '/').replace('&#x2F;', ''))
    test_name_3 = re.search(r"[A-ZА-Я/]+ *\d+", full_name.replace('&amp;#x2F;', '/'))
    test_name_4 = re.search(r'([A-Z]+\s[A-Z0-9\-]+\s[A-Z]+)', full_name.replace('&amp;#x2F;', '/'))
    name = test_name.group(
        0) if test_name else test_name_1.group(0) if test_name_1 else test_name_2.group(
        0) if test_name_2 else test_name_3.group(0) if test_name_3 else test_name_4.group(
        0) if test_name_4 else full_name
    return name.replace('TESLA ', '')


# full_name = 'Клеевой пистолет &amp;#x2F; клей пистолет HAMMER GN-07'
# name = find_name(full_name)
# print(name)