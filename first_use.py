import PySimpleGUI as SimpleGUI
from conf_creator import ConfManager
import base64
from sqlite_adapter import FirstUseModel


config = ConfManager()

# Дефолтная тема приложения
SimpleGUI.set_options(font=("Courier Mono", 12))

# event.startswith("URL ")

source_url_font = ('Courier Mono', 14, 'underline')
title_font = ('Courier Mono', 14)


# Подтверждение выбранных настроек
def confirm():
    # Шаблон приветственного окна
    layout = [
        [SimpleGUI.Text('Хотите применить введенные настройки?', font=title_font, justification='center', size=(70, 1))],
        [SimpleGUI.Text(
            'Вы внесли настройки в конфигурацию по умолчанию! Сохранить их?')],

        [SimpleGUI.Button('Вернуться к началу', key='cancel'),
         SimpleGUI.Button('Далее', key='next')
         ]
    ]

    window = SimpleGUI.Window('Подтверждение', layout, icon='ico/save.ico')

    while True:
        event, _ = window.read()
        match event:
            case 'cancel':
                window.close()
                return 'cancel confirm'
            case 'next':
                window.close()
                return 'next confirm'
            case SimpleGUI.WIN_CLOSED:
                window.close()
                return 'cancel confirm'


# Персонализация настроек
def personalization():

    first_use_model = FirstUseModel()

    # Шаблон окна персонализации
    Ru_locale = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAWCAYAAACG9x+sAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAu5JREFUWIW9l99LU2EYx7/ve7blpm6w3cTOYnVT7hwiBJMudHVR4KQUr7qOgYhehPbjf0hIBXG7OgXdBSEyyB90UxNyIIjhPBoNodzcjWexoSic7bxdOEPKzene7XP58vDh+/A+h/c8BCUIBoNOYjL1EUJ6CHCDEeIBY42l6rlCyD5hLMmATQARQ9dnFEXJnFr670F/f7+NCcKISRBeyJJkl3w+iKIIh90OAMjmckilUlhXVagbG8jn87Vt5ogcAUYbrdax8fHxg5INDAwMiHlg5qYst3UHAnA5nWWtmqZhbmEBa/F4DTKfyjdDEHqVqamfxwd/G3gyOHjlEhALdHW5Ozs6zmWNLi5idn4ejDGOWUuyk6f0zttQaBsABOBobATgU3cgcP284QHA6/XCbDbjRyLBOeupNAuM3fN3dr6LxWJ5CgCMkOeyLLdeJPwxd/1+yJLELWU5GNC6d3j4DADI0NCQyyBka+TpU7vL5apKnMlk8Hpiom4ftqHr16huGH2yJFUdHgCcTid8LS0cslWEnVgsvZQx9pDn1ddrjACAMPaIApBFt5ub1OPxcHOdBQEkCuCyvfhI8cDB0XUWDBApd2l93oJjDAogncvluBl5uipghwJQk6kUN+M2R1cFbFAAkXVV5WZUOboqIEINXZ9ZV9XcrqZVbdMyGWxsbnLIVRFZQ9cjVFGUjFEojM4vLFRt/Dg7W69XGGDslaIoGQoAjVbr2Fo8vhJdXLyw73M0Cp6jeAYrTTbbBFD8G43FYvlb7e1zW4nEY7PF0nzV6z2X7Us0Ch43WCE7eUrvhycnNaDYAACsLi/nbre1vf+eSPjT6bRbFEXYbLaypl1Nw4fpaXxdWqpx5iKMrRom04M3odCv46P/Vsrh4WHr/sHBCBWEl5LPZ5clCR5RhMPhAABks1kkT6yUhUKhHtGzjJDR5oaG8bIr5UmCwaCTWCy9xDB6QEgLAA+AplonLbIHIAnGNhmlETMwEw6Hf59W+AeEBxzSTJhqkQAAAABJRU5ErkJggg=='
    En_locale = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAWCAYAAACG9x+sAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAr9JREFUWIXFl0tPE1EYhp9v5syAiCwgXgItiXEhlxXEhTvBtXKJW417NZoU9T9IYkE0Ju68bF1gf4CAKzcWXXDZqLEdMF7AWBBs50yPixY1Ci3SoT7LM9955/2Sc2a+V9iCSNw0OpY/iCV9GI4CEWDvVvUh8w3wgHkRk8hpZ9yLyfJmhfLnQvM9U1eT1TEM14CGXTaKY0Nv1KcnGtDWGHCgzgDwcU2YX7aZSNlMek7GDxj2AxX3YrK+ZQORuGlxLD2OcGy3jQOcbPW50p0lss+UrPNWhFvJWp6m1Cts1f/2krzbePazgSM3TTSv9HOgefcsF7AFLndnOduR+6d9j2ZdbidrFo2vjr8ekjSABYVjk1f6CVUwDzszD3CuI8fFrmxzXuknkbjZA8UG3Ky+CnSFa3NzTrb6OzK/wfnOHL2tustReghAWu6YJjfQb6jShX18erXsmS/HwqpwJlGfWcupw5Yb+INUwTwUvjaVmgdoqTeciPgNru33WyCnQvC2LXqiQchactpCpDM01TK0N+rQtDqaAgx0WBhzKDTVMuyvC0+r+MNrscKTrC75wlXKW8D7ar300/pfk0ulWosWMBuaahnmluzQtGY/2wjMWSImEZpqGSZS4TUwmbbJi0lYOe2MA5nQlEswkXZIZyo/Rt6K8GzB+aq1k7CKc/Zw5fbKo/MwNl1bsc7Ii1p0wA0vJssWgB+ouAjJipW3wdOU4tGsu+P992dcpjyVzAVqFIrDnBeTdfHVALAYjs3SjCVreLiDJh7MuNydrlkUXw1sBJv/Gmh6WzVXur4TbSg9H6Uzwmiylsm0eomtBjYNNBtE4maPY+sYcJ0qDHnKgp5ipGxvCjhYjJQf1oS5pUKknPKcrzpg2M+rkZKR8ncicdPo2n4/In3G0EYh1Nfvaje/WAU8EeYxJqEdZzx1Qb5sVvgDAJEFQLjoGwcAAAAASUVORK5CYII='
    default_layout = [
        [SimpleGUI.Text('Настройте внешний вид приложения на свой вкус')],
        [SimpleGUI.Frame('Выберите тему приложения:', [
            [SimpleGUI.Button('', image_filename='ico/themes/DarkBlue13.png', key='DarkBlue13'),
             SimpleGUI.Button('', image_filename='ico/themes/DarkGrey.png', key='DarkGrey'),
             ],
            [SimpleGUI.Button('', image_filename='ico/themes/Default1.png', key='Default1'),
             SimpleGUI.Button('', image_filename='ico/themes/LightBlue5.png', key='LightBlue5')
             ],
            [SimpleGUI.Combo(SimpleGUI.theme_list(), default_value='Выбрать другую тему...',
                             enable_events=True, key='more themes')],
        ],
            border_width=2)
         ],


        [SimpleGUI.Frame('Язык:', [
            [SimpleGUI.Text('Ru'),
             SimpleGUI.Button(image_data=((En_locale, En_locale)[False]),
                              button_color=(SimpleGUI.theme_background_color(), SimpleGUI.theme_background_color()),
                              border_width=0,
                              key='locale'),
             SimpleGUI.Text('En')]
        ],
                         border_width=0)
         ],


        [SimpleGUI.Button('Выйти', key='cancel'),
         SimpleGUI.Button('Назад', key='back'),
         SimpleGUI.Button('Далее', key='next'),
         SimpleGUI.Button('Дополнительные настройки', key='advanced-settings'),
         ],
    ]
    advanced_settings_layout = [
        [
            SimpleGUI.Frame('UI:', [
                [SimpleGUI.Text('Имя пользователя:')],
            ],
                         border_width=0),

            SimpleGUI.Frame('Данные о пользователе', [
                [SimpleGUI.InputText(default_text=first_use_model.uname, key='uname')],
            ],
                            border_width=1),
        ],

        [
            SimpleGUI.Frame('DataBase:', [
                [SimpleGUI.Text('Название файла базы данных:')],
                [SimpleGUI.Text('Название таблицы базы данных:')],
                [SimpleGUI.Text('Поля таблицы:')]
            ],
                            border_width=0),

            SimpleGUI.Frame('Описание конфигурации БД', [
                [SimpleGUI.InputText(
                    default_text=first_use_model.database_db_name, key='db_name')],
                [SimpleGUI.InputText(
                    default_text=first_use_model.database_table_name, key='table_name')],
                [SimpleGUI.InputText(
                    default_text=first_use_model.database_fields, key='fields')],
            ],
                            border_width=1),
        ],

        [
            SimpleGUI.Frame('SuperUser:', [
                [SimpleGUI.Text('Администратор:')],
                [SimpleGUI.Text('Пароль:')]
            ],
                            border_width=0),

            SimpleGUI.Frame('Учетные данные администратора БД', [
                [SimpleGUI.InputText(
                    default_text=first_use_model.superuser_login, key='login')],
                [SimpleGUI.InputText(
                    default_text=first_use_model.superuser_password, key='password')],
            ],
                            border_width=1),
        ],

        [SimpleGUI.Button('Назад', key='advanced-back'),
         SimpleGUI.Button('Далее', key='advanced-next'),
         ],

    ]

    layout = [
        [SimpleGUI.Column(default_layout, key='default'),
         SimpleGUI.Column(advanced_settings_layout, visible=False, key='advanced'),
         ]
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
            case 'advanced-settings':
                window['default'].update(visible=False)
                window['advanced'].update(visible=True)
            case 'advanced-back':
                window['default'].update(visible=True)
                window['advanced'].update(visible=False)
            case 'cancel':
                window.close()
                return 'cancel personalization', None
            case SimpleGUI.WIN_CLOSED:
                window.close()
                return 'cancel personalization', None
            case 'next':
                # Закрываем окно
                window.close()
                first_use_model.ui_locale = ('Ru', 'En')[locale_state]
                # Передаем в точку входа в приложение первого использования данные с окна
                return 'next personalization', first_use_model
            case 'advanced-next':
                # Закрываем окно
                window.close()
                # Передаем в точку входа в приложение первого использования данные с окна
                first_use_model.uname = value['uname']
                first_use_model.database_db_name = value['db_name']
                first_use_model.database_table_name = value['table_name']
                first_use_model.database_fields = value['fields']
                first_use_model.superuser_login = value['login']
                first_use_model.superuser_password = value['password']
                return 'next personalization', first_use_model
            case 'back':
                # close and execute default preferences
                window.close()
                return 'back personalization', None
            case 'more themes':
                # Делаем доступными все кнопки тем
                for theme in default_themes:
                    window[theme].update(disabled=False)
                # Если выбранная тема находится среди дефолтных
                if value['more themes'] in default_themes:
                    # Дефолтную выделяем
                    window[value['more themes']].update(disabled=True)

                first_use_model.ui_theme = value['more themes']

            case 'locale':
                window['locale'].update(image_data=((Ru_locale, En_locale)[locale_state]))

                # config.set('UI', 'locale', ('Ru', 'En')[locale_state])
                first_use_model.ui_locale = ('Ru', 'En')[locale_state]

            case SimpleGUI.WIN_CLOSED:
                window.close()
                break
            case 'DarkBlue13':
                # change focus button
                db13_btn.update(disabled=True)
                dg_btn.update(disabled=False)
                default_btn.update(disabled=False)
                lb5_btn.update(disabled=False)

                first_use_model.ui_theme = 'DarkBlue13'

            case 'DarkGrey':
                # change focus button
                db13_btn.update(disabled=False)
                dg_btn.update(disabled=True)
                default_btn.update(disabled=False)
                lb5_btn.update(disabled=False)

                first_use_model.ui_theme = 'DarkGrey'

            case 'Default1':
                # change focus button
                db13_btn.update(disabled=False)
                dg_btn.update(disabled=False)
                default_btn.update(disabled=True)
                lb5_btn.update(disabled=False)

                first_use_model.ui_theme = 'Default1'

            case 'LightBlue5':
                # change focus button
                db13_btn.update(disabled=False)
                dg_btn.update(disabled=False)
                default_btn.update(disabled=False)
                lb5_btn.update(disabled=True)

                first_use_model.ui_theme = 'LightBlue5'

            case _:
                pass


# Приветствие
def welcome():
    # Шаблон приветственного окна
    layout = [
        [SimpleGUI.Text(f'Привет, {config.uname}. Я Time Manager версии 5', font=title_font, justification='center',
                        size=(70, 1))],
        [SimpleGUI.Text(
            'Приложение для подсчета времени, затраченного на определенный вид деятельности с возможностью\n'
            'первичного анализа, демонстрации и экспорта статистики')],
        [SimpleGUI.Image('ico/first_use.png', expand_x=True, expand_y=True, subsample=2)],
        [SimpleGUI.Text('Samson-P 2023', tooltip='Исходники', enable_events=True, font=source_url_font,
                        key='source', justification='center', size=(70, 1))],
        [SimpleGUI.Button('Выйти', key='cancel'),
         SimpleGUI.Button('Далее', key='next'),
         SimpleGUI.Button('Пропустить с настройками по умолчанию', key='skip')]
    ]

    window = SimpleGUI.Window('Добро пожаловать!', layout, icon='ico/main.ico')

    while True:
        event, _ = window.read()
        match event:
            case 'cancel':
                window.close()
                return 'cancel welcome'
            case 'next':
                window.close()
                return 'next welcome'
            case SimpleGUI.WIN_CLOSED:
                window.close()
                return 'cancel welcome'
            case 'source':
                config.open_source()
            case 'skip':
                window.close()
                return 'skip welcome'
            case _:
                pass


# Точка входа
def main():
    next_chapter = welcome()
    model = ConfManager()

    while True:
        # Возьмем отдельно: нажатая кнопка,
        button_preset, subchapter = next_chapter.split()

        # Отработка кнопки ДАЛЕЕ
        if 'next' == button_preset:
            match subchapter:
                case 'welcome':
                    next_chapter, model = personalization()
                    print(model.uname, model.superuser_login, model.superuser_password)
                case 'personalization':
                    next_chapter = confirm()
                case 'confirm':
                    print(model.uname, model.superuser_login, model.superuser_password)
                    config.create(mode='personal',
                                  uname=model.uname,
                                  theme=model.ui_theme,
                                  locale=model.ui_locale,
                                  db_name=model.database_db_name,
                                  table_name=model.database_table_name,
                                  fields=model.database_fields,
                                  login=model.superuser_login,
                                  password=model.superuser_password,
                                  )
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
                    next_chapter, model = personalization()

        # Отработка кнопки ПРОПУСТИТЬ, ПОСТАВИТЬ ПО УМОЛЧ.
        if 'skip' == button_preset:
            match subchapter:
                case 'welcome':
                    config.create()
                    return 'default'
                case 'personalization':
                    config.create()
                    return 'default'


if __name__ == "__main__":
    chapter = 'Welcome'
    # welcome()
    personalization()
