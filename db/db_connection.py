import sqlite3
import sqlite3 as sq


class DB_my_connection():
    def __init__(self, table_name=None):
        self.table_name = table_name

    def create_db(self):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            cursor.execute("""CREATE TABLE codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    rasdel_name TEXT,
                    brand TEXT,
                    product_code INTEGER,
                    product_name TEXT,
                    product_link TEXT,
                    rew INTEGER DEFAULT 0,
                    rating REAL DEFAULT 0,
                    product_stock INTEGER,
                    product_price INTEGER
                )""")

    def create_table(self):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            text_for_create_table = f'CREATE TABLE IF NOT EXISTS params (id INTEGER PRIMARY KEY AUTOINCREMENT, radel TEXT, params TEXT)'
            cursor.execute(text_for_create_table)
            con.commit()

    def create_table_with_params(self):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            text_for_create_table = f'CREATE TABLE IF NOT EXISTS {self.table_name}_with_params (id INTEGER PRIMARY KEY AUTOINCREMENT)'
            cursor.execute(text_for_create_table)

    def create_table_html(self):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            cursor.execute("""CREATE TABLE codes_html (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rasdel TEXT,
                    card_code INTEGER,
                    review INTEGER DEFAULT 0,
                    price INTEGER,
                    rat REAL DEFAULT 0,
                    date TEXT
                )""")

    def create_table_atribut_value(self):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            cursor.execute("""CREATE TABLE attributes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rasdel TEXT,
                    code INTEGER,
                    name TEXT,
                    sales_id INTEGER DEFAULT 0,
                    sales_name TEXT,
                    sales_credentials TEXT,
                    attribute TEXT,
                    value TEXT
                )""")

    def insert_in_db(self, dict=None):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            cursor.execute("""INSERT INTO codes
                           VALUES (
                           NULL,
                           :date,
                           :rasdel_name,
                           :id,
                           :name,
                           :link,
                           :rew,
                           :rating,
                           :stock,
                           :price
                           )
                           """, dict)

            con.commit()

    def insert_in_db_params(self, dict):
        print(dict)
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            text_for_insert_value_in_table = f'INSERT INTO params VALUES (NULL, ?, ?)'
            cursor.executemany(text_for_insert_value_in_table, dict)

            con.commit()

    def insert_in_db(self, dict=None):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            cursor.executemany("""INSERT INTO codes
                           VALUES (
                           NULL,
                           :date,
                           :rasdel_name,
                           :brand,
                           :id,
                           :name,
                           :link,
                           :rew,
                           :rating,
                           :stock,
                           :price
                           )
                           """, dict)

            con.commit()

    def add_column(self, column):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            try:
                new_text = f'ALTER TABLE {self.table_name}_with_params ADD COLUMN {column} TEXT'
                cursor.execute(new_text)
            except sqlite3.OperationalError:
                print('Имя столбца уже существует!')
            else:
                print('Создание и добавление столбца!')
                con.commit()

    def insert_in_db_codes_html(self, my_dict=None):
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            cursor.executemany("""INSERT INTO codes_html 
                        VALUES (
                        NULL,
                        :rasdel,
                        :card_code,
                        :review,
                        :price,
                        :rat,
                        :date
                        )
                        """, my_dict)

            con.commit()

    def insert_in_table_with_params(self, rasdel=None, my_dict=None):
        with sq.connect('db/parser_ozon.db') as con:

            cursor = con.cursor()
            for item in my_dict:
                text_for_sql = f'INSERT INTO {rasdel}_with_params VALUES (NULL, {", ".join([":" + i for i in item])})'
                print(item)
                cursor.execute(text_for_sql, item)

    def insert_in_table_with_params_attributes(self, rasdel: str = None, my_dict: list = None):
        print(my_dict)
        with sq.connect('db/parser_ozon.db') as con:
            cursor = con.cursor()
            text_for_sql = f'INSERT INTO attributes VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.executemany(text_for_sql, my_dict)
