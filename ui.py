import PySimpleGUI as sg
#from levels import levels
from game import start_quiz
import tasks
import db
import plots

# TODO: refactoring

fnt = 'Arial 30'
sg.theme('DarkBlue14')   # Add a touch of color
# All the stuff inside your window.

qtype = tasks.EToList(tasks.OpType)
qdata = tasks.choose(qtype[0])
qmod = qdata['mod']
qdiff = qdata['difficulty']

c_quiz = 'combo_quiz_optype'
c_diff = 'diff'
c_mod = 'mod'
cb_full = 'checkbox_complete_only'


layout = [  
    [sg.Text('Some text on Row 1', font=fnt)],
    [sg.Combo(qtype, key = c_quiz, default_value=qtype[0]),
        sg.Combo(tasks.EToList(qmod), key = c_mod, default_value=tasks.EToList(qmod)[0]),
        sg.Combo(tasks.diff_get(), key = c_diff, default_value=tasks.diff_get()[0])], 
    [sg.Checkbox(key = cb_full, text='Complete only')],
    [sg.Button('Start'), sg.Button('Scores')], 
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
        cur_diff = qdiff[tasks.diff_get(values[c_diff])]
        print(cur_diff)
        qfunc = qdata['get'](values[c_mod], cur_diff)
        *data_to_save, answers = start_quiz('test', qfunc, 1000, values[c_mod].value, values[c_quiz].value)
        print(data_to_save)
        print(answers)
        db.save(*data_to_save)
    if event == 'Scores':
        data = db.read(values[c_quiz].value, values[c_diff], values[c_mod].value, values[cb_full])
        if data:
            #print(data)
            plots.draw_scores(data)

window.close()