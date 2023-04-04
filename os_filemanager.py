import os


# Проверяем наличие файла с расширением .db в корневом каталоге
def db_exists(counts):
    # Читаем корневой каталог
    files = os.listdir('.')

    if counts == 'one':
        for file_name in files:
            # Если такой файл существует, возвращаем его название
            if '.db' in file_name:
                return file_name
        # Если файла не существует, возвращаем
        return None
    elif counts == 'all':
        db_files = []
        for file_name in files:
            # Собираем в массив все файлы с таким расширением
            if '.db' in file_name:
                db_files.append(file_name)
        if len(db_files):
            return db_files
        # Если не существует ни одного файла с таким расширением, возвращаем
        return None



# Проверка на существование всех файлов программы
def check_tm_configuration():
    pass


# И записать потом имя в файл конфигурации
# Так же схема БД должна генериться из файла конфигурации
# Правда проблема с
