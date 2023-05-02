import PySimpleGUI as sg
#from levels import levels
from game import start_quiz
import tasks
import db

fnt = 'Arial 30'
sg.theme('DarkBlue14')   # Add a touch of color
# All the stuff inside your window.

qtype = tasks.EToList(tasks.OpType)
qdata = tasks.choose(qtype[0])
qmod = qdata['mod']
qdiff = qdata['difficulty']

layout = [  
    [sg.Text('Some text on Row 1', font=fnt)],
    [sg.Combo(qtype, key = 'quiz', default_value=qtype[0])], 
    [sg.Combo(tasks.EToList(qmod), key = 'mod', default_value=tasks.EToList(qmod)[0])],
    [sg.Combo(qdata['diff'](), key = 'diff', default_value=qdata['diff']()[0])],
    [sg.Button('Start')], 
]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    print(event)
    if event == sg.WIN_CLOSED:
        break
    if event == 'Start':
        cur_diff = qdiff[qdata['diff'](values['diff'])]
        print(cur_diff)
        qfunc = qdata['get'](values['mod'], cur_diff)
        *data_to_save, answers = start_quiz('test', qfunc, 1000, values['mod'], values['quiz'])
        print(data_to_save)
        print(answers)
        db.save(*data_to_save)
window.close()