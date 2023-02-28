import PySimpleGUI as SimpleGUI

# Общая тема окон DarkGreen4
SimpleGUI.theme('DarkGreen3')

layout_notes = [
    [SimpleGUI.Text('Похиленко Самсон')],
    [SimpleGUI.Text('По вопросам, связанным с технической поддержкой,')],
    [SimpleGUI.Text('можете обращаться на почту  europ108b@gmail.com')],
    [SimpleGUI.Cancel()]
]

question = SimpleGUI.Window('Обо мне', layout_notes)
while True:
    k, b = question.read()
    if k == 'Cancel':
        break

del layout_notes, k, b, question
