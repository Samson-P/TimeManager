import sqlite3
import datetime

DB_NAME = 'dt_control.db'
TABLE_NAME = 'dt_control'
TABLE_SCHEMA = ['id_dt_interval', 'title', 'description', 'dt_start', 'interval']

CREATE_TABLE_QUERY = f'''
    CREATE TABLE {TABLE_NAME}
        (id_dt_interval INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        dt_start TEXT NOT NULL,
        interval TEXT NOT NULL)
'''

TABLE_INSERT_QUERY = '''
                INSERT INTO {}(title, description, dt_start, interval) 
                VALUES ('{}', '{}', '{}', '{}');
            '''


class DBManager:

    def __init__(self):
        self.name = DB_NAME
        self.table = TABLE_NAME
        self.fields = TABLE_SCHEMA

        try:
            self.con = sqlite3.connect(self.name)
            self.cursor = self.con.cursor()
            self.error = None
        except sqlite3.Error as err:
            self.con = None
            self.cursor = None
            self.error = err

    def __enter__(self, table=TABLE_NAME, database=DB_NAME):
        # проверить, может таблица с таким именем уже существует
        table_exists_query = f'''
            SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';
            '''

        self.cursor.execute(table_exists_query)
        result = self.cursor.fetchall()

        if len(result) == 0:
            self.cursor.execute(CREATE_TABLE_QUERY)
            self.con.commit()
            self.cursor.execute(table_exists_query)
            result = self.cursor.fetchall()
            if len(result) != 0:
                self.error = 'table created, no point in reading'
            else:
                self.error = f"An error occurred while creating the table!\n{result[0]}"
        else:
            self.error = None

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.con.close()


# Основной класс
class TimeInterval:
    def __init__(self, interval, title, description=None, id_dt_interval=None, dt_start=None):
        """

        :param interval: Продолжительность работы
        :param title: Заголовок, собственно, род деятельности
        :param description: Описание, чем конкретно занимался, подзадачи
        """
        self.id = id_dt_interval
        self.dt_start = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.interval = interval

        self.title = title
        self.description = description

    def __repr__(self):
        return self

    def __str__(self):
        return f"<{str(self.title)[:10]}..., в теч.{self.interval}c>"

    def write(self):
        """

        :return: None если Ок, если проблемы -- str
        """

        # проверить, таблица с таким именем существует, если нет - создать
        # если таблицы не было, и создать ее не получилось, выходим с Ошибкой
        with DBManager() as db:

            # команда на вставку строки в таблицу
            table_insert_query = f'''
                    INSERT INTO {TABLE_NAME}(title, description, dt_start, interval) 
                    VALUES('{self.title}', '{self.description}', '{self.dt_start}', '{self.interval}');
                '''

            db.cursor.execute(table_insert_query)

            db.con.commit()
            return None

    def read(self, limit=10):
        """

        :param limit: Ограничение, количество строк, которое прочитаем из БД
        :return: None если Ok, если проблема -- str
        """

        # проверить, таблица с таким именем существует, если нет - создать
        # если создали - завершаем программу
        with DBManager() as db:
            if db.error == 'table created, no point in reading':
                return f"Table {TABLE_NAME} created successfully. Table is empty!", None

            # прочитаем последние 10 записей
            read_table_query = f"SELECT * FROM {TABLE_NAME} ORDER BY id_dt_interval DESC LIMIT {limit}"

            db.cursor.execute(read_table_query)
            rows = db.cursor.fetchall()
            query_set: list = []

            for row in rows:
                tm = TimeInterval(
                    id_dt_interval=row[0],
                    title=row[1],
                    description=row[2],
                    dt_start=row[3],
                    interval=row[4]
                    )
                query_set.append(tm)
            return None, query_set

    def show_now(self):
        return f"{self.dt_start}\t|{str(self.title)[:10]}...\t|{str(self.description)[:10]}...\t|{self.interval}\n"


if __name__ == "__main__":
    tm1 = TimeInterval('10', 'совершенно 1')
    print(tm1.show_now())
    print(tm1.write())

    err, tm = TimeInterval().read()
    print(err)
    print(len(tm))
    print(tm[0].title)
