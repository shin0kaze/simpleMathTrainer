import PySimpleGUI as sg
# from levels import levels
from game import start_quiz
import tasks
import db
import plots


def __start_game(quiz_data, operation, difficulty, modification):
    tbname = quiz_data['db'].get(modification)
    datas = db.db_get_traintable(tbname) if tbname else None

    qfunc = quiz_data['get'](modification, difficulty, datas)
    *data_to_save, answers = start_quiz(f'{quiz_data["name"]}:{modification}:{difficulty}',
                                        120, qfunc, 1000, modification, operation)
    if answers:
        db.save(*data_to_save)
        if tbname:
            db.db_upd_traintable(tbname, datas, answers)


def __draw_scores_plot(operation, difficulty, modification, is_complete):
    data = db.read(operation, difficulty, modification, is_complete)
    if data:
        plots.draw_scores(data)


def open_traincalc_window():
    quiz_op_type = tasks.EToList(tasks.OpType)
    quiz_data = tasks.choose(quiz_op_type[0])
    quiz_mod = quiz_data['mod']
    quiz_difficulty = quiz_data['difficulty']

    c_quiz = 'combo_quiz_optype'
    c_diff = 'combo_quiz_diff'
    c_mod = 'combo_quiz_mod'
    cb_full = 'checkbox_complete'

    layout = [
        [sg.Text('Some text on Row 1', font='Arial 30')],
        [sg.Combo(quiz_op_type, key=c_quiz, default_value=quiz_op_type[0]),
            sg.Combo(tasks.EToList(quiz_mod), key=c_mod,
                     default_value=tasks.EToList(quiz_mod)[0]),
            sg.Combo(tasks.diff_get(), key=c_diff, default_value=tasks.diff_get()[0])],
        [sg.Checkbox(key=cb_full, text='Complete only')],
        [sg.Button('Start'), sg.Button('Scores')],
    ]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        operation = values[c_quiz].value
        difficulty = quiz_difficulty[tasks.diff_get(values[c_diff])]
        mod = values[c_mod].value

        if event == 'Start':
            __start_game(quiz_data, operation, difficulty, mod)

        if event == 'Scores':
            is_complete_only = values[cb_full]
            __draw_scores_plot(
                operation, difficulty['name'], mod, is_complete_only)

    window.close()
