import sqlite3
from peewee import Model, SqliteDatabase, TextField, AutoField
import datetime


DB_NAME = 'dt_control.db'
TABLE_NAME = 'dt_control'

# Поля таблицы БД для
TABLE_SCHEMA = ['id_dt_interval', 'title', 'description', 'dt_start', 'interval']

# SQL для создания таблицы
CREATE_TABLE_QUERY = f'''
CREATE TABLE dt_control (
    id_dt_interval INTEGER PRIMARY KEY AUTOINCREMENT,
    title          TEXT    NOT NULL,
    description    TEXT,
    dt_start       TEXT    NOT NULL,
    interval       TEXT    NOT NULL
);
'''

# SQL для записи новой строки
TABLE_INSERT_QUERY = '''
                INSERT INTO {}(title, description, dt_start, interval) 
                VALUES ('{}', '{}', '{}', '{}');
            '''


# Определяем базовую модель от которой будут наследоваться остальные
class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(DB_NAME)


# Определяем модель исполнителя
class TMInterval(BaseModel):
    id_dt_interval = AutoField(column_name='id_dt_interval')
    title = TextField(column_name='title')
    description = TextField(column_name='description', null=True)
    dt_start = TextField(column_name='dt_start')
    interval = TextField(column_name='interval')

    def __init__(self, title, description='N/A', dt_start=None):
        """

        :param title: Род деятельности
        :param description: Детали
        """
        super().__init__(title=title, description=description)
        self.dt_start = dt_start or datetime.datetime.now()

    def stop(self):
        # Здесь реализовано вычитание dt_start из .now()
        # interval представляет из себя экземпляр класса timedelta
        self.interval = datetime.datetime.now() - self.dt_start
        # И запись dt_start в формате ДД-ММ-ГГГГ ЧЧ:ММ:СС
        self.dt_start = self.dt_start.strftime("%d-%m-%Y %H:%M:%S")

        return self.interval

    def __repr__(self):
        return self.title

    def serialize(self):
        return self

    class Meta:
        table_name = TABLE_NAME


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


if __name__ == "__main__":
    tm1 = TimeInterval('10', 'совершенно 1')
    print(tm1.show_now())
    print(tm1.write())

    err, tm = TimeInterval().read()
    print(err)
    print(len(tm))
    print(tm[0].title)
