import webbrowser
import PySimpleGUI as SimpleGUI
import configparser
import base64


setup_steps = {
    'Welcome': 1,
    'Interface personalization': 2,
    'Confirm the selected settings': 3,
}


config = configparser.ConfigParser()  # создаём объекта парсера
config.read("cnf/ui_configuration.ini")  # читаем конфиг

# Достает цветовую схему из конфигурационного файла
# SimpleGUI.theme(config["UI"]["theme"])
SimpleGUI.set_options(font=("Courier Mono", 12))

source_url_font = ('Courier Mono', 14, 'underline')
title_font = ('Courier Mono', 14)


def confirm():
    return 'cancel confirm'


def personalization():
    # Шаблон окна персонализации
    Ru_locale = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAWCAYAAACG9x+sAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAu5JREFUWIW9l99LU2EYx7/ve7blpm6w3cTOYnVT7hwiBJMudHVR4KQUr7qOgYhehPbjf0hIBXG7OgXdBSEyyB90UxNyIIjhPBoNodzcjWexoSic7bxdOEPKzene7XP58vDh+/A+h/c8BCUIBoNOYjL1EUJ6CHCDEeIBY42l6rlCyD5hLMmATQARQ9dnFEXJnFr670F/f7+NCcKISRBeyJJkl3w+iKIIh90OAMjmckilUlhXVagbG8jn87Vt5ogcAUYbrdax8fHxg5INDAwMiHlg5qYst3UHAnA5nWWtmqZhbmEBa/F4DTKfyjdDEHqVqamfxwd/G3gyOHjlEhALdHW5Ozs6zmWNLi5idn4ejDGOWUuyk6f0zttQaBsABOBobATgU3cgcP284QHA6/XCbDbjRyLBOeupNAuM3fN3dr6LxWJ5CgCMkOeyLLdeJPwxd/1+yJLELWU5GNC6d3j4DADI0NCQyyBka+TpU7vL5apKnMlk8Hpiom4ftqHr16huGH2yJFUdHgCcTid8LS0cslWEnVgsvZQx9pDn1ddrjACAMPaIApBFt5ub1OPxcHOdBQEkCuCyvfhI8cDB0XUWDBApd2l93oJjDAogncvluBl5uipghwJQk6kUN+M2R1cFbFAAkXVV5WZUOboqIEINXZ9ZV9XcrqZVbdMyGWxsbnLIVRFZQ9cjVFGUjFEojM4vLFRt/Dg7W69XGGDslaIoGQoAjVbr2Fo8vhJdXLyw73M0Cp6jeAYrTTbbBFD8G43FYvlb7e1zW4nEY7PF0nzV6z2X7Us0Ch43WCE7eUrvhycnNaDYAACsLi/nbre1vf+eSPjT6bRbFEXYbLaypl1Nw4fpaXxdWqpx5iKMrRom04M3odCv46P/Vsrh4WHr/sHBCBWEl5LPZ5clCR5RhMPhAABks1kkT6yUhUKhHtGzjJDR5oaG8bIr5UmCwaCTWCy9xDB6QEgLAA+AplonLbIHIAnGNhmlETMwEw6Hf59W+AeEBxzSTJhqkQAAAABJRU5ErkJggg=='
    En_locale = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAWCAYAAACG9x+sAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAr9JREFUWIXFl0tPE1EYhp9v5syAiCwgXgItiXEhlxXEhTvBtXKJW417NZoU9T9IYkE0Ju68bF1gf4CAKzcWXXDZqLEdMF7AWBBs50yPixY1Ci3SoT7LM9955/2Sc2a+V9iCSNw0OpY/iCV9GI4CEWDvVvUh8w3wgHkRk8hpZ9yLyfJmhfLnQvM9U1eT1TEM14CGXTaKY0Nv1KcnGtDWGHCgzgDwcU2YX7aZSNlMek7GDxj2AxX3YrK+ZQORuGlxLD2OcGy3jQOcbPW50p0lss+UrPNWhFvJWp6m1Cts1f/2krzbePazgSM3TTSv9HOgefcsF7AFLndnOduR+6d9j2ZdbidrFo2vjr8ekjSABYVjk1f6CVUwDzszD3CuI8fFrmxzXuknkbjZA8UG3Ky+CnSFa3NzTrb6OzK/wfnOHL2tustReghAWu6YJjfQb6jShX18erXsmS/HwqpwJlGfWcupw5Yb+INUwTwUvjaVmgdoqTeciPgNru33WyCnQvC2LXqiQchactpCpDM01TK0N+rQtDqaAgx0WBhzKDTVMuyvC0+r+MNrscKTrC75wlXKW8D7ar300/pfk0ulWosWMBuaahnmluzQtGY/2wjMWSImEZpqGSZS4TUwmbbJi0lYOe2MA5nQlEswkXZIZyo/Rt6K8GzB+aq1k7CKc/Zw5fbKo/MwNl1bsc7Ii1p0wA0vJssWgB+ouAjJipW3wdOU4tGsu+P992dcpjyVzAVqFIrDnBeTdfHVALAYjs3SjCVreLiDJh7MuNydrlkUXw1sBJv/Gmh6WzVXur4TbSg9H6Uzwmiylsm0eomtBjYNNBtE4maPY+sYcJ0qDHnKgp5ipGxvCjhYjJQf1oS5pUKknPKcrzpg2M+rkZKR8ncicdPo2n4/In3G0EYh1Nfvaje/WAU8EeYxJqEdZzx1Qb5sVvgDAJEFQLjoGwcAAAAASUVORK5CYII='
    layout = [
        [SimpleGUI.Text('Настройте внешний вид приложения на свой вкус')],
        [SimpleGUI.Frame('Выберите тему приложения:', [[
            SimpleGUI.Button('', image_filename='ico/themes/DarkBlue13.png', key='DarkBlue13'),
            SimpleGUI.Button('', image_filename='ico/themes/DarkGrey.png', key='DarkGrey'),
            SimpleGUI.Button('', image_filename='ico/themes/Default1.png', key='Default1'),
            SimpleGUI.Button('', image_filename='ico/themes/LightBlue5.png', key='LightBlue5'),
            ],
            [SimpleGUI.Combo(SimpleGUI.theme_list(), default_value='Выбрать другую тему...',
                             enable_events=True, key='More themes')],
        ],
            border_width=2)
         ],


        [SimpleGUI.Frame('Язык:', [
            [SimpleGUI.Text('Ru'),
             SimpleGUI.Button(image_data=((En_locale, En_locale)[False]),
                              button_color=(SimpleGUI.theme_background_color(), SimpleGUI.theme_background_color()),
                              border_width=0,
                              key='Locale'),
             SimpleGUI.Text('En')]
        ],
                         border_width=0)
         ],


        [SimpleGUI.Button('Выйти', key='Cancel'),
         SimpleGUI.Button('Далее', key='Next'),
         SimpleGUI.Button('Пропустить с настройками по умолчанию', key='Skip')],
    ]

    window = SimpleGUI.Window('TimeManager 5, personalization', layout, icon='ico/main.ico')

    db13_btn = window['DarkBlue13']
    dg_btn = window['DarkGrey']
    default_btn = window['Default1']
    lb5_btn = window['LightBlue5']
    default_themes = ['DarkBlue13', 'DarkGrey', 'Default1', 'LightBlue5']
    locale_state = True

    while True:
        event, value = window.read()
        locale_state = not locale_state
        match event:
            case 'Cancel':
                window.close()
                return 'cancel personalization'
            case 'Next':
                # Изменение настроек в конфигурационном файле согласно заданным пользователем
                with open('cnf/ui_configuration.ini', 'w') as configfile:
                    config.write(configfile)

                # save and execute preferences, close
                window.close()
                return 'next personalization'
            case 'Skip':
                # close and execute default preferences
                window.close()
                return 'skip personalization'
            case 'More themes':
                # Делаем доступными все кнопки тем
                for theme in default_themes:
                    window[theme].update(disabled=False)
                # Если выбранная тема находится среди дефолтных
                if value['More themes'] in default_themes:
                    # Дефолтную выделяем
                    window[value['More themes']].update(disabled=True)

                # Изменение настроек темы
                config.set('UI', 'theme', value['More themes'])

            case 'Locale':
                window['Locale'].update(image_data=((Ru_locale, En_locale)[locale_state]))

                config.set('UI', 'locale', ('Ru', 'En')[locale_state])

            case SimpleGUI.WIN_CLOSED:
                window.close()
                break
            case 'DarkBlue13':
                # change focus button
                db13_btn.update(disabled=True)
                dg_btn.update(disabled=False)
                default_btn.update(disabled=False)
                lb5_btn.update(disabled=False)
            case 'DarkGrey':
                # change focus button
                db13_btn.update(disabled=False)
                dg_btn.update(disabled=True)
                default_btn.update(disabled=False)
                lb5_btn.update(disabled=False)
            case 'Default1':
                # change focus button
                db13_btn.update(disabled=False)
                dg_btn.update(disabled=False)
                default_btn.update(disabled=True)
                lb5_btn.update(disabled=False)
            case 'LightBlue5':
                # change focus button
                db13_btn.update(disabled=False)
                dg_btn.update(disabled=False)
                default_btn.update(disabled=False)
                lb5_btn.update(disabled=True)
            case _:
                pass
        if event.startswith("URL "):
            url = event.split(' ')[1]
            webbrowser.open(url)


# Приветствие
def welcome():
    # Шаблон приветственного окна
    layout = [
        [SimpleGUI.Text('Привет, я Time Manager версии 5', font=title_font, justification='center', size=(70, 1))],
        [SimpleGUI.Text(
            'Приложение для подсчета времени, затраченного на определенный вид деятельности с возможностью\n'
            'первичного анализа, демонстрации и экспорта статистики')],
        [SimpleGUI.Image('ico/first_use.png', expand_x=True, expand_y=True, subsample=2)],
        [SimpleGUI.Text('Samson-P 2023', tooltip='Исходники', enable_events=True, font=source_url_font,
                        key='Source', justification='center', size=(70, 1))],
        [SimpleGUI.Button('Выйти', key='Cancel'),
         SimpleGUI.Button('Далее', key='Next'),
         SimpleGUI.Button('Пропустить с настройками по умолчанию', key='Skip')]
    ]

    window = SimpleGUI.Window('Добро пожаловать!', layout, icon='ico/main.ico')

    while True:
        event, _ = window.read()
        match event:
            case 'Cancel':
                window.close()
                return 'cancel welcome'
            case 'Next':
                window.close()
                return 'next welcome'
            case SimpleGUI.WIN_CLOSED:
                window.close()
                break
            case 'Source':
                # if event.startswith("URL "):
                webbrowser.open(config['Global']['source'])
            case 'Skip':
                window.close()
                return 'skip welcome'
            case _:
                pass

    return 'Cancel'


# Точка входа
def main():
    next_chapter = welcome()

    while True:
        # Возьмем отдельно: нажатая кнопка,
        button_preset, subchapter = next_chapter.split()

        # Отработка кнопки ДАЛЕЕ
        if 'next' == button_preset:
            match subchapter:
                case 'welcome':
                    next_chapter = personalization()
                case 'personalization':
                    next_chapter = confirm()
                case 'confirm':
                    return 'ПРИМЕНЕНИЕ ВЫБРАННЫХ НАСТРОЕК'

        # Отработка кнопки ВЫЙТИ
        if 'cancel' == button_preset:
            match subchapter:
                case 'welcome':
                    return 'logout'
                case 'personalization':
                    return 'logout'
                case 'confirm':
                    next_chapter = welcome()

        # Отработка кнопки НАЗАД
        if 'back' == button_preset:
            match subchapter:
                case 'welcome':
                    return 'logout'
                case 'personalization':
                    next_chapter = welcome()
                case 'confirm':
                    next_chapter = personalization()

        # Отработка кнопки ПРОПУСТИТЬ, ПОСТАВИТЬ ПО УМОЛЧ.
        if 'skip' == button_preset:
            match subchapter:
                case 'welcome':
                    return 'default'
                case 'personalization':
                    return 'default'


if __name__ == "__main__":
    chapter = 'Welcome'
    # welcome()
    personalization()
