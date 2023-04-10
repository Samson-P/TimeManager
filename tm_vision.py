import pandas
import PySimpleGUI as SimpleGUI
from sqlite_adapter import TMInterval


def show_table(limit=20):
    headers = [
        'Род деятельности', 'Описание', 'Количество времени'
    ]

    cur_query = TMInterval.select().limit(limit)
    table = []

    for item in cur_query.dicts().execute():
        table.append([item['title'], item['description'], item['interval']])

    SimpleGUI.theme("DarkBlue3")
    SimpleGUI.set_options(font=("Courier New", 12))

    layout = [
        [
            SimpleGUI.Table(
                values=table,
                headings=headers,
                auto_size_columns=False,
                col_widths=[20, 30, 20])
        ],
        [
            SimpleGUI.Cancel(), SimpleGUI.Button('Справка'),
        ]
    ]

    # list(map(lambda x:len(x)+1, headers))

    window = SimpleGUI.Window('TMv5 Таблица сохраненных кругов', layout)
    event, value = window.read()


if __name__ == "__main__":
    show_table()
