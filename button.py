from time import sleep

import PySimpleGUI as SimpleGUI
from PySimpleGUI import Column, Button, Frame, Image
from pygame import mixer


import keyboard
from threading import Thread, Event

keyboard.get_hotkey_name()

SimpleGUI.set_options(font=('Natasha', 14))

SimpleGUI.Window._move_all_windows = True

# SimpleGUI.theme('Default')
background_image = open("ico/buttons/background.png", 'rb').read()


def keyboard_mngr():
    mixer.init()
    while True:
        if keyboard.is_pressed('enter'):
            mixer.music.load('eff/press-enter.wav')
            mixer.music.play(0)
            sleep(0.1)
        if keyboard.is_pressed('space'):
            mixer.music.load('eff/press-button.wav')
            mixer.music.play(0)
            sleep(0.1)
        if keyboard.is_pressed('backspace'):
            mixer.music.load('eff/press-button.wav')
            mixer.music.play(0)
            sleep(0.1)
        if keyboard.read_key() in \
                "йцукенгшщзхъфывапроолджэячсмитьбюqwertyuiopasdfghjklzxcvbnm1234567890:;.,/?|[{]}-+<>'_=":
            mixer.music.load('eff/press-button.wav')
            mixer.music.play(0)
            sleep(0.1)


def title_bar(title, text_color, background_color):
    """
    Creates a "row" that can be added to a layout. This row looks like a titlebar
    :param title: The "title" to show in the titlebar
    :type title: str
    :param text_color: Text color for titlebar
    :type text_color: str
    :param background_color: Background color for titlebar
    :type background_color: str
    :return: A list of elements (i.e. a "row" for a layout)
    :rtype: List[sg.Element]
    """
    bc = background_color
    tc = text_color
    font = 'Natasha'

    return [SimpleGUI.Col([[SimpleGUI.T(title, text_color=tc, background_color=bc, font=font, grab=True)]], pad=(0, 0),
                          background_color=bc),
            SimpleGUI.Col([
                [SimpleGUI.T('_', text_color=tc, background_color=bc, enable_events=True, font=font, key='-MINIMIZE-'),
                 SimpleGUI.Text('❎', text_color=tc, background_color=bc, font=font, enable_events=True, key='Exit')]],
                          element_justification='r', key='-C-', grab=True,
                          pad=(0, 0), background_color=bc)]


def button():
    colors = ("#000000", "#BDB76B")

    background_layout = [title_bar('Стиль кнопки', SimpleGUI.theme_text_color(), SimpleGUI.theme_background_color()),
                         [SimpleGUI.Image(data=background_image)]]
    window_background = SimpleGUI.Window('Background', background_layout, no_titlebar=True, finalize=True, margins=(0, 0),
                                         element_padding=(0, 0), right_click_menu=[[''], ['Exit', ]])

    window_background['-C-'].expand(True, False,
                                    False)  # expand the titlebar's rightmost column so that it resizes correctly

    layout_center = [
        [SimpleGUI.Text('Смотрим разные стили кнопок', justification='center', text_color="#000000",
                        size=(60, 1))],
        [Frame('Actions:', [[Column([
            # image_filename='ico/buttons/del.png',
            [
                Button('старт', key='start', button_color=colors, border_width=1, size=(10, 2)),
                Button('стоп', key='stop', button_color=colors, border_width=1, size=(10, 2))
             ],
            [SimpleGUI.MLine(default_text='This is the default Text', size=(35, 3), font=("UbuntuMono", 12, "bold"))],
        ], size=(500, 300), pad=(0, 0))]])],

        [Button('выйти', key='cancel')],
    ]

    layout = [[SimpleGUI.VPush()],
              [SimpleGUI.Push(), SimpleGUI.Column(layout_center, element_justification='c'), SimpleGUI.Push()],
              [SimpleGUI.VPush()]]


    # window = SimpleGUI.Window('Стиль кнопки', layout, finalize=True, margins=(0, 0), element_padding=(0, 0))
    top_window = SimpleGUI.Window('Everything bagel', layout, finalize=True, keep_on_top=True, grab_anywhere=False,
                                  transparent_color=SimpleGUI.theme_background_color(), no_titlebar=True)

    while True:
        window, event, _ = SimpleGUI.read_all_windows()

        match event:
            case 'cancel':
                return 'cancel'
            case 'start':
                pass
            case SimpleGUI.WIN_CLOSED:
                return 'cancel'


    top_window.close()
    window_background.close()


if __name__ == "__main__":
    ev = Event()


    th1 = Thread(target=button)
    th2 = Thread(target=keyboard_mngr)

    th1.start()
    th2.start()

    ev.set()
