import PySimpleGUI as sg
import sys
import time
import datetime

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
    question = ''
    answered = False
    answers = []
    answer = 0
    save_results = True
    sg.theme('DarkBlue14')

    layout = [  [sg.Text('count n/N'), sg.Text('timer m:s')],
                [sg.Text('1 QUESTION', font=large_fnt, key=q_txt)],
                [sg.InputText(key=a_it, enable_events=True) ],
                [sg.Button('Stop and save')], [sg.Button('Cancel')] ]

    window = sg.Window(caption, layout, finalize=True)

    quiz_dur = 0
    first_question = True
    slowest = 0
    fastest = sys.maxsize

    while time.time() - quiz_dur < quiz_timer_dur * 1000 * 10000:
        print(f'ct:{round(time.time() - quiz_dur)} < {quiz_timer_dur}')
        q = next(q_gen)
        question, answer = q
        answered = False
        

        print('q:%s, a:%s'%(question, answer))
        while not answered:   
            start_time = time.time()
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
                    quiz_dur = time.time()
                else:
                    dur = time.time() - start_time
                    slowest = max(dur, slowest)
                    fastest = min(dur, fastest)
                    answers.append((question, answer, 0, dur))
                window[a_it].update('')
                answered = True
        else:
            continue
        break

    window.close()

    if save_results:
        print('save result')
        quiz_dur = time.time() - quiz_dur
        average = count / quiz_dur
        return (len(answers), op.value, diff['name'], mod.value, quiz_dur, quiz_timer_dur, fastest, slowest, average, 0, answers,)
    return None