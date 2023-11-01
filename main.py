# coding=utf-8
import datetime
import sys
import json
import time

import PySimpleGUI as SimpleGUI
import subprocess

import first_use
import os_filemanager
from conf_creator import ConfManager
from sqlite_adapter import TMInterval, DBManager
import tm_vision

config = ConfManager()

# Иконка приложения
ICONS_PATH = {
    'main': 'ico/main.ico',
    'error': 'ico/error.ico',
    'save': 'ico/save.ico',
    'import': 'ico/import.ico',
    'data_loss': 'ico/data_loss.ico',
    'leave': 'ico/leave.ico',
    'refresh': 'ico/refresh.ico',
}
# Общая тема окон DarkGreen4
SimpleGUI.theme(config.ui_theme)

# Меню приложения
menu_def = [['Файл', ['Пуск', 'Стоп', 'Перезапустить', 'Сохранить круги', 'Выйти', 'Импортировать из файла sql/json']],
            ['Изменить', ['Отменить последний круг', 'Создать круг вручную']],
            ['Помощь', 'Справка']]


# Открытие окна предупреждения о возможной потере данных о не сохраненных кругах
def cancel_frame(mode):
    # Шаблон окна для выхода из программы
    CAUTION = [
        [SimpleGUI.Text('Хотите выйти из программы?')],
        [SimpleGUI.Text('Не сохраненные данные будут потеряны.')],
        [SimpleGUI.Button('Да'), SimpleGUI.Cancel()]
    ]

    # Иконка окна по умолчанию - выход
    cancel_ico = ICONS_PATH['leave']

    # Добавляем логику сохранения текущей сессии перед выходом только в случае
    # наличия не сохраненных кругов
    match mode:
        case 'saving':
            CAUTION[2].append(
                SimpleGUI.Button('Сохранить сессию и выйти')
            )
            # Иконка окна в случае с потерей данных
            cancel_ico = ICONS_PATH['data_loss']
        case 'without_saving':
            pass
        case _:
            pass

    quit_frame = SimpleGUI.Window('Внимание', layout=CAUTION, icon=cancel_ico)
    event, _ = quit_frame.read()
    quit_frame.close()
    del quit_frame
    return event


def refresh_frame():
    # Шаблон окна для перезапуска приложения с потерей данных о кругах
    REFRESH = [
        [SimpleGUI.Text('Хотите перезапустить таймер?')],
        [SimpleGUI.Text('Не сохраненные данные будут потеряны.')],
        [SimpleGUI.Button('да'), SimpleGUI.Cancel()]
    ]
    window = SimpleGUI.Window('Внимание', layout=REFRESH, icon=ICONS_PATH['refresh'])
    event, _ = window.read()
    window.Close()
    del window
    return event


def save_frame(query_set):
    # Создаем шаблон формы с Checkbox-сами кругов, которые хотим сохранить
    SAVE_FORM = [
        [SimpleGUI.Checkbox(f'{job.title}', default=True)] for job in query_set
    ]
    # Добавляем кнопки "Сохранить" и "Выйти"
    SAVE_FORM.append(
        [SimpleGUI.Button('Сохранить'), SimpleGUI.Cancel()]
    )
    # Инициализируем окно как экземпляр класса SimpleGUI.Window, подгоняем по размеру к содержимому
    window = SimpleGUI.Window('Выберите круги',
                              layout=SAVE_FORM, size=(300, 30 * len(query_set) + 40),
                              icon=ICONS_PATH['save']
                              )
    event, values = window.read()
    window.close()
    return event, values


# Кеширование не сохраненных данных
def fm_tmp(query_set):
    jobs_to_json = []
    for tm_interval in query_set:
        jobs_to_json.append(tm_interval.serialize())

    to_json_file = {'dt_created': datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), 'data': jobs_to_json}

    with open('tm_tmp.json', 'w') as file:
        json.dump(to_json_file, file)


def master_frame():
    # Шаблон главного окна приложения
    TMInterface = [
        [SimpleGUI.Menu(menu_def)],
        [
            SimpleGUI.Text('Таймер'), SimpleGUI.Button('Пуск', bind_return_key=True, disabled=False),
            SimpleGUI.Button('Стоп', bind_return_key=True, disabled=True), SimpleGUI.Button('Перезапуск')
        ],
        [SimpleGUI.Text('Режим:'), SimpleGUI.Radio('без перерывов', '', True), SimpleGUI.Radio('с перерывами', '')],
        [SimpleGUI.Text('Род деятельности'), SimpleGUI.InputText(key='title')],
        # sg.FileBrowse()
        [SimpleGUI.Text('Заметки')],
        [SimpleGUI.Multiline(key='description', size=(63, 7))],
        [
            SimpleGUI.Button('Сохранить', bind_return_key=True, disabled=True),
            SimpleGUI.Cancel(), SimpleGUI.Button('Справка'),
            SimpleGUI.Button('Таблица', bind_return_key=True, disabled=False)
        ]
    ]
    return SimpleGUI.Window('Time Manager', layout=TMInterface, icon=ICONS_PATH['main'])


def error_frame(message, err_name='Error'):
    """
    Процедура отрисовки окна с ошибкой

    :param message: Обязательное поле содержания ошибки
    :param err_name: Необязательное поле короткого названия ошибки (default='Error')
    :return: None
    """
    # Шаблон окна ошибки
    ERROR = [
        [SimpleGUI.Text(message)],
        [SimpleGUI.Cancel()]
    ]
    # Инициализируем окно как экземпляр класса SimpleGUI.Window
    window = SimpleGUI.Window(err_name, layout=ERROR, icon=ICONS_PATH['error'])
    # Показываем окно без отслеживания нажатий
    window.read()
    window.close()


# Точка входа в оконное приложение
def frame():
    jobs: list = []
    window = master_frame()
    # Забираем экземпляры кнопок пуск и стоп
    stop_button = window['Стоп']
    start_button = window['Пуск']
    save_button = window['Сохранить']
    title_input_area = window['title']
    description_input_area = window['description']
    # И экземпляр модели БД
    tm: TMInterval
    while True:
        event, values = window.read()
        match event:
            case 'Таблица':
                tm_vision.show_table()
                pass
            case 'Пуск':
                # Только если поле "Род деятельности" не пусто...
                if values['title'] == '':
                    # Скрываем главное окно
                    window.hide()
                    # Вызов ошибки
                    error_frame('Введите данные в поле "Род деятельности"!', err_name='Поле пусто!')
                    # Делаем главное окно обратно видимым
                    window.un_hide()
                else:
                    # ... происходит логика "Пуск"
                    tm = TMInterval(title=values['title'])
                    # Обновляем состояние кнопок
                    start_button.update(disabled=True)
                    stop_button.update(disabled=False)
            case 'Стоп':
                tm.description = values['description']
                # Вычислим интервал времени
                tm.stop()
                jobs.append(tm)
                tm.delete()
                # Обновляем состояние кнопок
                start_button.update(disabled=False)
                stop_button.update(disabled=True)
                # Так как jobs теперь не пустой, делаем кнопку "Сохранить" кликабельной
                save_button.update(disabled=False)
                title_input_area.update(value='')
                description_input_area.update(value='')
            case 'Сохранить' | 'Сохранить круги':
                # Отображаем окно, отслеживаем нажатие
                save_event, save_values = save_frame(jobs)
                match save_event:
                    case 'Сохранить':
                        tmp_jobs = jobs
                        jobs = []
                        for job in tmp_jobs:
                            # Сохраняем только выбранные в save_values
                            if save_values[tmp_jobs.index(job)]:
                                job.save()
                        for job in tmp_jobs:
                            if not save_values[tmp_jobs.index(job)]:
                                # В памяти остаются только не сохраненные круги
                                jobs.append(job)
                        del tmp_jobs
                        # Если список кругов не пуст, делаем кнопку "Сохранить" кликабельной
                        save_button.update(disabled=not bool(jobs))
                    case _:
                        pass
            case 'Справка':
                # Открываем справку в отдельном потоке
                subprocess.Popen([sys.executable, 'notes.py'])
            case 'Cancel' | 'Выйти':
                if not jobs:
                    cancel_event = cancel_frame('without_saving')
                else:
                    cancel_event = cancel_frame('saving')
                match cancel_event:
                    case 'Да':
                        # Выход без сохранения сессии
                        jobs.clear()
                        window.close()
                        return 0
                    case 'Сохранить сессию и выйти':
                        # Выход с сохранением сессии во временном файле
                        fm_tmp(jobs)
                        jobs.clear()
                        window.close()
                        return 0
            case 'Перезапуск' | 'Перезапустить':
                refresh_event = refresh_frame()
                if refresh_event == 'да':
                    # Закрываем окно
                    window.close()
                    # Удаляем круги прошлой сессии
                    jobs.clear()
                    # Единичку возвращаем, чтобы окно перезапустилось
                    return 1
            case SimpleGUI.WIN_CLOSED:
                # Сохраняем сессию и закрываем окно
                if jobs:
                    fm_tmp(jobs)
                jobs.clear()
                window.close()
                return 0
            case _:
                jobs.clear()
                window.close()
                pass


# Точка входа в приложение
if __name__ == "__main__":

    # Инициализация БД
    db = DBManager()
    #
    status_code, err_desc = db.error
    print(f'{status_code}: {err_desc}')

    # Если до входа в программу, при подключении к БД или в других узлах возникла ошибка, отрабатываем ее
    if 'Ok' != status_code:

        # Проверяем статус, если это "first use", запускаем в том же потоке first_use.main()
        match status_code:
            case 'first use':
                # Не существует файла БД и _ЗАПИСЕЙ В КЭШе_, значит у нас имеет место первое использование
                # создам модель для сбора данных, подтвержденных на этапе первого запуска
                # избавляемся от старого конфига
                os_filemanager.check_tm_confile()
                time.sleep(2)
                first_use.main()

                db.create_db()
                status_code, err_desc = db.error
            case _:
                status_code = 'logout'

    # Применяем новые настройки темы, если они менялись
    SimpleGUI.theme(ConfManager().ui_theme)

    # Если инициализация БД произошла успешно, запускаем приложение
    if 'Ok' == status_code:
        while True:
            out = frame()
            if out == 0:
                break
