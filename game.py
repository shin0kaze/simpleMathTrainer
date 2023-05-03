import PySimpleGUI as sg
import sys
import time

quiz_timer_dur = 180

def now_ms():
    return round(time.time() * 1000)

def qGen(question_func, count):
    for i in range(count):
        yield question_func()
    return

def start_quiz(caption, question_tuple, count, mod, op, *spec) -> None:
    
    func, diff = question_tuple
    q_gen = qGen(func, count)
    large_fnt = 'Arial 22'
    q_txt = 'question_text'
    a_it = 'answer_inputtext'
    answers = []
    save_results = True
    first_question = True
    quiz_start = 0
    quiz_end = 0
    slowest = 0
    fastest = sys.maxsize

    sg.theme('DarkBlue14')

    layout = [  [sg.Text('count n/N'), sg.Text('timer m:s')],
                [sg.Text('1 QUESTION', font=large_fnt, key=q_txt)],
                [sg.InputText(key=a_it, enable_events=True) ],
                [sg.Button('Stop and save')], [sg.Button('Cancel')] ]

    window = sg.Window(caption, layout, finalize=True)

    while quiz_end - quiz_start < quiz_timer_dur:
        print(f'ct:{round(time.time() - quiz_start)} < {quiz_timer_dur}')

        question, answer = next(q_gen)
        answered = False
        question_start = time.time()

        print('q:%s, a:%s'%(question, answer))
        while not answered:   
            window[q_txt].update(question)
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == 'Cancel':
                save_results = False
                break
            if event == 'Stop and save':
                break
            if values[a_it] == answer:
                if first_question:
                    first_question = False
                    quiz_start = time.time()
                else:
                    question_dur = time.time() - question_start
                    quiz_end = time.time()
                    slowest = max(question_dur, slowest)
                    fastest = min(question_dur, fastest)
                    answers.append((question, answer, 0, question_dur))
                window[a_it].update('')
                answered = True
        else:
            continue # if inner cycle not broken continue outer
        break

    window.close()

    if save_results and (count := len(answers)):
        print('save result')
        quiz_dur = quiz_end - quiz_start
#        count = len(answers)
        average = quiz_dur / count
        return (count, op, diff, mod, quiz_dur, quiz_timer_dur, fastest, slowest, average, 0, answers,)
    return None