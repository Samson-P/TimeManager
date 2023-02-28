import sys
import PySimpleGUI as sg
import datetime
import random
import subprocess
from sqlite_adapter import TMInterval

# Общая тема окон DarkGreen4
SimpleGUI.theme('DarkGreen3')

Jobs = []
curd_main = {
    'Time0': '00:00',
    'TimeEnd': '00:00',
    'Date0': '2020.10.17',
    'DateEnd': '2020.10.17',
    'Circle0': 1,
    'Circle': 1,
    'Jobs': ' ',
    'Notes': ' ',
    'Description': ' ',
    'Position': False,  # позиция переключателя пуск/стоп
}

A = {
    'Time': '00:00',
    'dTime': '00:00 - 00:00',
    'Date': '2020.10.17',
    'Circle0': 1,
    'Circle': 1,
    'Jobs': ' ',
    'Notes': ' ',
    'Description': ' ',
}

curd = curd_main
curd_save = A


def start_stop(demo):
    global curd
    curd['Position'] = not curd['Position']
    curd['Circle'] = round(0.51 * curd['Circle0'])
    curd['Circle0'] += 1

    if curd['Position']:
        curd['Time0'] = str(datetime.datetime.today().time()).split('.')[0][0:5]
        curd['Date0'] = str(datetime.date.today()).replace('-', '.')
    else:
        curd['TimeEnd'] = str(datetime.datetime.today().time()).split('.')[0][0:5]
        curd['DateEnd'] = str(datetime.date.today()).replace('-', '.')
        # сохранения рода деятельности:
        curd['Jobs'] = str(demo[2])
        if demo[0]:
            curd['Description'] = 'без перерывов'
        else:
            curd['Description'] = 'с перерывами'
        curd['Notes'] = demo[3]
        save(' ')
    if curd['Position']:
        print('пошло время')
    else:
        print('стоп машина')


def save(kindmem):
    if curd['DateEnd'] != curd['Date0']:  # если за круг дата поменялась, то
        curd_save['Date'] = curd['Date0'][0:8] + str(curd['Date0'].split('.')[2]) + '-' + str(
            curd['DateEnd'].split('.')[2])
    else:
        curd_save['Date'] = curd['Date0']
    # считаю время в чч:мм
    time = int(curd['TimeEnd'].split(':')[0]) - int(curd['Time0'].split(':')[0])
    time += (int(curd['TimeEnd'].split(':')[1]) - int(curd['Time0'].split(':')[1])) // 60
    time += abs(int(curd['Date0'].split('.')[2]) - int(curd['DateEnd'].split('.')[2])) * 24
    curd_save['Time'] = str(time)
    curd_save['Time'] += ':' + str((int(curd['TimeEnd'].split(':')[1]) - int(curd['Time0'].split(':')[1])) % 60)
    #
    Jobs.append(curd['Jobs'])
    #
    curd_save['dTime'] = curd['Time0'] + ' - ' + curd['TimeEnd']
    curd_save['Jobs'] = curd['Jobs']
    curd_save['Description'] = curd['Description']
    curd_save['Notes'] = curd['Notes']
    #
    mess = '|~\t' + curd_save['Time'] + '\t|\t' + curd_save['Jobs'] + '\t|\t' + curd_save['Description'] + '\t|\t'
    mess += curd_save['dTime'] + '\t|\t' + curd_save['Date'] + '\t|\t' + curd_save['Notes'] + '\n'
    if kindmem == 'long memory':
        file_manager(mess)  # сохранение последнего круга

    fm_tmp(mess)        # сохранение кругов


def save_frame():
    l = [[sg.Text("Выберите, какие круги вы хотите сохранить:")]]
    j = 0
    for i in Jobs:
        j += 1
        l.append([sg.Checkbox(str(j)), sg.Text(str(i))])
    l.append([sg.Button("Выбрать"), sg.Cancel()])
    swiped = sg.Window('сохранение...', l)
    while True:
        sev, salve = swiped.read()
        if sev == 'Cancel':
            swiped.close()
            break
        if sev == 'Выбрать':
            past(salve)
            swiped.close()
            break


def file_manager(a):
    file_m = open('№.txt', 'r')
    cnt = int(file_m.read()) + 1
    file_m.close()
    file_m = open('№.txt', 'w')
    file_m.write(str(cnt))
    file_m.close()
    file_m = open('goodtime.txt', 'a')
    file_m.write(str(cnt + 10000)[1:5] + a)
    file_m.close()
    del file_m


def fm_tmp(a):
    a = str(curd['Circle']/100).split('.')[1] + a
    file_m = open('tmp.txt', 'a')
    file_m.write(a)
    file_m.close()
    del file_m


def frame():
    layout = [
        [sg.Text('таймер'), sg.Button('пуск/стоп'), sg.Button('перезапуск')],
        [sg.Output(size=(88, 15))],
        [sg.Text('режим:'), sg.Radio('без перерывов', '', True), sg.Radio('с перерывами', '')],
        [sg.Text('род деятельности'), sg.InputText()],
        # sg.FileBrowse()
        [sg.Text('заметки')],
        [sg.InputText(size=(88, 1))],
        [sg.Button('сохранить'), sg.Cancel(), sg.Button('справка'), sg.Button('таблица')]
    ]
    window = sg.Window('полезное время', layout)
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


while True:
    open('tmp.txt', 'w').write('')
    curd = curd_main
    out = frame()
    if out == 0:
        break
