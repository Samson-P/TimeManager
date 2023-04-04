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


# Перенос некорректного файла .db в папку OLD
def recycle_db_files():
    # Создаем папку, если ее не существует
    if not os.path.isdir('OLD'):
        os.mkdir('OLD')

    dot_db_files = db_exists('all')

    if dot_db_files is None:
        return '.db files do not exist', 'No database files found!'

    for file_name in dot_db_files:
        # Переносим все файлы с расширением .db в папку OLD
        os.replace(file_name, f'OLD/{file_name}')

    return 'Ok', 'Invalid .db files have been moved to the OLD folder.'


# Проверка на существование всех файлов программы
def check_tm_configuration():
    pass


# И записать потом имя в файл конфигурации
# Так же схема БД должна генериться из файла конфигурации
# Правда проблема с
