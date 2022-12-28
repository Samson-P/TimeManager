import sqlite3

# создаем БД или подключаемся к существующей
connection = sqlite3.connect('shows.db')

# создаем объект курсора
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Shows
              (Title TEXT, Director TEXT, Year INT)''')
