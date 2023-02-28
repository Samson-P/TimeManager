import sys
import PySimpleGUI as SimpleGUI
import datetime
import random
import subprocess
from sqlite_adapter import TMInterval

# Общая тема окон DarkGreen4
SimpleGUI.theme('DarkGreen3')

# Меню приложения
menu_def = [['Файл', ['Пуск', 'Стоп', 'Перезапустить', 'Сохранить круги', 'Выйти', 'Импортировать из файла sql/json']],
            ['Изменить', ['Отменить последний круг', 'Создать круг вручную']],
            ['Помощь', 'Справка']]


# Открытие окна предупреждения о возможной потере данных о не сохраненных кругах
def cancel_frame():
    # Шаблон окна для выхода из программы
    CAUTION = [
        [SimpleGUI.Text('Хотите выйти из программы?')],
        [SimpleGUI.Text('Не сохраненные данные будут потеряны.')],
        [SimpleGUI.Button('Да'), SimpleGUI.Button('Сохранить сессию и выйти'), SimpleGUI.Cancel()]
    ]
    quit_frame = SimpleGUI.Window('Внимание', layout=CAUTION)
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
    window = SimpleGUI.Window('Внимание', layout=REFRESH)
    event, _ = window.read()
    window.Close()
    del window
    return event


def fm_tmp(a):
    # Кеширование не сохраненных данных
    with open('tmp.txt', 'w') as file:
        print('This will be written to /some/dir/test.txt', file=file)


def frame():
def master_frame():
    # Шаблон главного окна приложения
    TMInterface = [
        [SimpleGUI.Menu(menu_def)],
        [
            SimpleGUI.Text('Таймер'), SimpleGUI.Button('Пуск', bind_return_key=True, disabled=False),
            SimpleGUI.Button('Стоп', bind_return_key=True, disabled=True), SimpleGUI.Button('Перезапуск')
        ],
        [SimpleGUI.Output(size=(88, 15))],
        [SimpleGUI.Text('Режим:'), SimpleGUI.Radio('без перерывов', '', True), SimpleGUI.Radio('с перерывами', '')],
        [SimpleGUI.Text('Род деятельности'), SimpleGUI.InputText()],
        # sg.FileBrowse()
        [SimpleGUI.Text('Заметки')],
        [SimpleGUI.InputText(size=(88, 1))],
        [
            SimpleGUI.Button('Сохранить', bind_return_key=True, disabled=True),
            SimpleGUI.Cancel(), SimpleGUI.Button('Справка'),
            SimpleGUI.Button('Таблица', bind_return_key=True, disabled=True)
        ]
    ]
    return SimpleGUI.Window('Time Manager', layout=TMInterface)
    window = master_frame()
    # Забираем экземпляры кнопок пуск и стоп
    stop_button = window['Стоп']
    start_button = window['Пуск']
    save_button = window['Сохранить']
    while True:
        event, values = window.read()
        if event == 'таблица':
            show_table()
        if event == 'пуск/стоп':
            start_stop(values)
        if event == 'сохранить':
            save_frame()
        if event == 'справка':
            subprocess.Popen([sys.executable, 'notes.py'])
        if event == 'Cancel':
            layout2 = [
                [sg.Text('Хотите выйти из программы?')],
                [sg.Text('Не сохраненные данные будут потеряны.')],
                [sg.Button('да'), sg.Cancel()]
            ]
            question = sg.Window('', layout2)
            k, b = question.read()
            question.close()
            if k == 'да':
                open('tmp.txt', 'w').write('')
                Jobs.clear()
                tm = TMInterval(title=values[4])
                start_button.update(disabled=True)
                stop_button.update(disabled=False)
                save_button.update(disabled=False)
                tm.stop()
                jobs.append(tm)
                tm.delete()
                cancel_event = cancel_frame()
                refresh_event = refresh_frame()
                window.close()
                return 0
                break
            del layout2, k, b, question
        if event in (None, None):
            return 0
            break
        if event == 'перезапуск':
            layout2 = [
                [sg.Text('Хотите перезапустить таймер?')],
                [sg.Text('Не сохраненные данные будут потеряны.')],
                [sg.Button('да'), sg.Cancel()]
            ]
            question = sg.Window('', layout2)
            k, b = question.read()
            question.close()
            if k == 'да':
                open('tmp.txt', 'w').write('')
                global curd
                curd = curd_main
                Jobs.clear()
                window.close()
                return 1
                break

            del layout2, k, b, question


def past(n):
    file_good_times = open('tmp.txt', 'r')
    for i in range(0, len(n)):
        o = file_good_times.readline()
        if n[i] == True:
            file_manager('|' + o.split('~')[1])
    file_good_times.close()


def show_table():
    layout4 = [
        [sg.Text('Данные собранные за все время (начиная с ...):'), sg.Button('Показать')],
        [sg.Output(size=(130, 40))],
        [sg.Cancel(), sg.Button('справка')]
    ]
    table = sg.Window('Table', layout4)
    k = 0
    while True:
        t_event, t_values = table.read()
        if t_event == 'Показать':
            print(open('goodtime.txt').read())
        if t_event == 'Cancel':
            table.close()
            break


# Точка входа в приложение
if __name__ == "__main__":
    while True:
        out = frame()
        if out == 0:
            break