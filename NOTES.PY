import PySimpleGUI as SimpleGUI

layout_notes = [
        [sg.Text('моя почта europioid108000000000@gmail.com')],
        [sg.Text('89165584923')],
        [sg.Cancel()]
]

question = SimpleGUI.Window('Обо мне', layout_notes)
while True:
    k, b = question.read()
    if k == 'Cancel':
        break

del layout_notes, k, b, question