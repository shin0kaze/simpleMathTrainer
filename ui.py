import PySimpleGUI as sg
from levels import levels
from game import start_quiz

fnt = 'Arial 30'
sg.theme('DarkBlue14')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Some text on Row 1', font=fnt)],
            [sg.Text('Enter something on Row 2'), sg.InputText(enable_events=True)],
            [sg.Button('Start')] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    print(event)
    if event == sg.WIN_CLOSED:
        break
    if event == 'Start':
        values = start_quiz('test', levels[0][3](0, 40, 'Common'), 10)

window.close()