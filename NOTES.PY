import PySimpleGUI as sg
import datetime
import random
import sys, subprocess

layout_notes = [
        [sg.Text('моя почта europioid108000000000@gmail.com')],
        [sg.Text('89165584923')],
        [sg.Cancel()]
]

question = sg.Window('', layout_notes)
while True:
    k, b = question.read()
    if k == 'Cancel':
        break

del layout_notes, k, b, question