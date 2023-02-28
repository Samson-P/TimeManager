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


# Точка входа в оконное приложение
def frame():
    jobs: list = []
    window = master_frame()
    # Забираем экземпляры кнопок пуск и стоп
    stop_button = window['Стоп']
    start_button = window['Пуск']
    save_button = window['Сохранить']
    # И экземпляр модели БД
    tm: TMInterval
    while True:
        event, values = window.read()
        match event:
            case 'Таблица':
                # show_table()
                pass
            case 'Пуск':
                if values[4] == '':
                    print('Введите данные в поле "Род деятельности"!')
                tm = TMInterval(title=values[4])
                # Обновляем состояние кнопок
                start_button.update(disabled=True)
                stop_button.update(disabled=False)
                save_button.update(disabled=False)
            case 'Стоп':
                tm.description = values[5]
                # Вычислим интервал времени
                tm.stop()
                jobs.append(tm)
                tm.delete()
                # Обновляем состояние кнопок
                start_button.update(disabled=False)
                stop_button.update(disabled=True)
            case 'Сохранить' | 'Сохранить круги':
                print(jobs)
                # Создаем шаблон формы с Checkbox-сами кругов, которые хотим сохранить
                SAVE_FORM = [
                    [SimpleGUI.Checkbox(f'{job.title}', default=True)] for job in jobs
                ]
                # Добавляем кнопки "Сохранить" и "Выйти"
                SAVE_FORM.append(
                    [SimpleGUI.Button('Сохранить'), SimpleGUI.Cancel()]
                )
                # Инициализируем окно как экземпляр класса SimpleGUI.Window, подгоняем по размеру к содержимому
                save_frames = SimpleGUI.Window('Выберите круги для сохранения',
                                               layout=SAVE_FORM, size=(300, 30*len(jobs) + 40)
                                               )
                # Отображаем окно, отслеживаем нажатия
                save_frame_event, save_frame_values = save_frames.read()
                # Закрываем окно сохранения
                save_frames.close()
                match save_frame_event:
                    case 'Сохранить':
                        tmp_jobs = jobs
                        jobs = []
                        for job in tmp_jobs:
                            # Сохраняем только выбранные в save_frame_values
                            if save_frame_values[tmp_jobs.index(job)]:
                                job.save()
                        for job in tmp_jobs:
                            if not save_frame_values[tmp_jobs.index(job)]:
                                # В памяти остаются только не сохраненные круги
                                jobs.append(job)
                        del tmp_jobs
                    case _:
                        pass
            case 'Справка':
                # Открываем справку в отдельном потоке
                subprocess.Popen([sys.executable, 'notes.py'])
            case 'Cancel' | 'Выйти':
                cancel_event = cancel_frame()
                match cancel_event:
                    case 'Да':
                        # Выход без сохранения сессии
                        # open('tmp.txt', 'w').write('')
                        window.close()
                        return 0
                    case 'Сохранить сессию и выйти':
                        # Выход с сохранением сессии в tmp файле
                        # open('tmp.txt', 'w').write('')
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
                # Сохраняем сессию
                # ...
                # и закрываем окно
                window.close()
                fm_tmp(jobs)
                jobs.clear()
                return 0
            case _:
                pass


def show_table():
    layout4 = [
        [SimpleGUI.Text('Данные собранные за все время (начиная с ...):'), SimpleGUI.Button('Показать')],
        [SimpleGUI.Output(size=(130, 40))],
        [SimpleGUI.Cancel(), SimpleGUI.Button('справка')]
    ]
    table = SimpleGUI.Window('Table', layout4)
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