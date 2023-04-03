import sqlite3
from peewee import Model, SqliteDatabase, TextField, AutoField
import datetime
import configparser
import os_filemanager


# Открываем файл конфигурации
config = configparser.ConfigParser()
config.read("cnf/ui_configuration.ini")

# Имя файла бд и название таблицы берем из конфига
DB_NAME = config['DataBase']['db_name']
TABLE_NAME = config['DataBase']['table_name']

# Поля таблицы БД
TABLE_SCHEMA = config['DataBase']['fields'].split(', ')

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

# SQL для проверки, существует ли таблица
TABLE_EXISTS_QUERY = f'''
                    SELECT name FROM sqlite_master WHERE type='table' AND name='{TABLE_NAME}';
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
        # interval представляет из себя строковое значение экземпляра timedelta
        self.interval = str(datetime.datetime.now() - self.dt_start)
        # И запись dt_start в формате ДД-ММ-ГГГГ ЧЧ:ММ:СС
        self.dt_start = self.dt_start.strftime("%d-%m-%Y %H:%M:%S")

        return self.interval

    def __repr__(self):
        return self.title

    def serialize(self):
        temporary_json_template: dict
        temporary_json_template = {
            'title': self.title,
            'description': self.description,
            'dt_start': self.dt_start,
            'interval': self.interval
        }
        return temporary_json_template

    class Meta:
        table_name = TABLE_NAME


class DBManager:

    def __init__(self):
        self.name = DB_NAME
        self.table = TABLE_NAME
        self.fields = TABLE_SCHEMA

        manual_database_name = os_filemanager.db_exists()

        # Проверяем существование файла базы данных
        if manual_database_name is not None:
            # Проверяем, БД имеет название, как в конфигурационном файле?
            if manual_database_name != self.name:
                # Если нет, задаем новое
                self.name = os_filemanager.db_exists()
                # Изменение настроек в конфигурационном файле согласно новому названию
                config.set('DataBase', 'db_name', manual_database_name)
                with open('cnf/ui_configuration.ini', 'w') as configfile:
                    config.write(configfile)
                self.error = 'Reboot required! The default name of the database has changed.'

            self.con = sqlite3.connect(self.name)
            self.cursor = self.con.cursor()

            self.cursor.execute(TABLE_EXISTS_QUERY)
            result = self.cursor.fetchall()

            if len(result) != 0:
                self.error = None
            else:
                self.error = 'Database table does not exist!'

        else:
            self.con = None
            self.cursor = None
            self.error = 'The database file does not exist!'

    def __enter__(self, table=TABLE_NAME, database=DB_NAME):
        return None

    def default(self):
        # Если были ошибки при соединении с БД, вернуть просто объект экземпляра
        if self.error is not None:
            return self

        # Проверяем, может таблица уже существует
        self.cursor.execute(TABLE_EXISTS_QUERY)

        result = self.cursor.fetchall()
        # Если таблица существует, возвращаем экземпляр класса с ошибкой
        if len(result) != 0:
            self.error = 'The table currently exists!'
            return self

        # Создать таблицу
        self.cursor.execute(CREATE_TABLE_QUERY)
        self.con.commit()

        # Проверить, таблица создалась
        self.cursor.execute(TABLE_EXISTS_QUERY)
        result = self.cursor.fetchall()
        if len(result) != 0:
            self.error = 'Table created, no point in reading.'
        else:
            self.error = 'An error occurred while creating the table!'

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.con.close()


if __name__ == "__main__":

    # Перед всей работой с базой, и т.п. надо просто проверить существование базы, таблицы,
    # проверить схему таблицы. Это можно поручить классу DBManager
    # TMInterval.create_table()
    # TMInterval.create(title='Hello', interval='3000', dt_start='10 10 10')
    pass
