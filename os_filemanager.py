import os
def dir_old_is_exist() -> None:
    """
    Создает папку OLD, если ее не существует

    :return: None
    """
    # Создаем папку, если ее не существует
    if not os.path.isdir('OLD'):
        os.mkdir('OLD')


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
    dir_old_is_exist()

    dot_db_files = db_exists('all')

    if dot_db_files is None:
        return '.db files do not exist', 'No database files found!'

    for file_name in dot_db_files:
        # Переносим все файлы с расширением .db в папку OLD
        os.replace(file_name, f'OLD/{file_name}')

    return 'Ok', 'Invalid .db files have been moved to the OLD folder.'


# Проверка на существование файлов с *.ini в каталоге /cnf
def check_tm_confile():

    dir_old_is_exist()

    # Читаем каталог /cnf
    files = os.listdir('./cnf')

    # Если файл с таким именем есть в каталоге cnf, переместить его в /OLD
    if 'configuration.ini' in files:
        # Переносим все файлы с расширением .db в папку OLD
        os.replace('./cnf/configuration.ini', f'OLD/configuration.ini')


# И записать потом имя в файл конфигурации
# Так же схема БД должна генериться из файла конфигурации
# Правда проблема с
