import webbrowser
import configparser
import os_filemanager
import getpass

# Открываем файл конфигурации по умолчанию
def_config = configparser.ConfigParser()
def_config.read("cnf/default_configuration.ini")
cur_config = configparser.ConfigParser()
cur_config.read("cnf/configuration.ini")

# Имя файла бд и название таблицы берем из конфига
DB_NAME = def_config['DataBase']['db_name']
TABLE_NAME = def_config['DataBase']['table_name']

# Поля таблицы БД
TABLE_SCHEMA = def_config['DataBase']['fields'].split(', ')


# Определяем базовую модель от которой будут наследоваться остальные
class ConfManager:
    default_configuration = def_config
    # Добываем системное имя пользователя
    uname = getpass.getuser()

    def __init__(self):
        os_filemanager.duplicate_tm_confile()
        self.current_configuration = configparser.ConfigParser()
        self.current_configuration.read("cnf/configuration.ini")
        self.ui_theme = self.current_configuration['UI']['theme']
        self.ui_locale = self.current_configuration['UI']['locale']
        self.global_source_url = self.current_configuration['Global']['source']
        self.database_db_name = self.current_configuration['DataBase']['db_name']
        self.database_table_name = self.current_configuration['DataBase']['table_name']
        self.database_fields = self.current_configuration['DataBase']['fields']

    def create(self, mode=None, **kwargs):
        # Проверим, есть ли конфиг-файл сейчас, если есть, выкидываем в OLD
        os_filemanager.check_tm_confile()

        # Создаем заполняем текущий конфиг
        if mode is None:
            self.default_configuration.set('UI', 'uname', self.uname)
            # Переписываем файл с замененным именем пользователя в новый конфиг
            with open('cnf/configuration.ini', 'w') as new_configfile:
                self.default_configuration.write(new_configfile)
        else:
            self.default_configuration.set('UI', 'theme', kwargs['theme'])
            self.default_configuration.set('UI', 'uname', self.uname)
            self.default_configuration.set('UI', 'locale', kwargs['locale'])
            with open('cnf/configuration.ini', 'w') as new_configfile:
                self.default_configuration.write(new_configfile)

        self.current_configuration = self.default_configuration

        return self

    def set(self, block, keyword, value):
        self.current_configuration.set(block, keyword, value)
        with open('cnf/configuration.ini', 'w') as new_configfile:
            self.current_configuration.write(new_configfile)
        return self

    def open_source(self):
        webbrowser.open(self.global_source_url)

    # Возвращаем объект текущего конфига
    def __repr__(self):
        return self.current_configuration


if __name__ == "__main__":
    cm = ConfManager()
    cm.create(mode='personal',
              theme='BrightColors',
              locale='En',
              db_name='dt_control.db',
              table_name='dt_control',
              fields='id_dt_interval, title, description, dt_start, interval',
              login='samson',
              password='password',
              )

    print(cm.__repr__()['UI']['uname'])

    cm.set('UI', 'uname', 'nikitaos')

    print(cm.__repr__()['UI']['uname'])

    # Обычное использование
    cm2 = ConfManager()
    print(cm2.__repr__()['DataBase']['db_name'])
    cm2.set('DataBase', 'db_name', 'ololo')
    print(cm2.__repr__()['DataBase']['db_name'])
