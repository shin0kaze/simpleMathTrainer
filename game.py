import PySimpleGUI as sg
from threading import Thread, Event
import logging
import sys
import time



quiz_timer_dur = 10

def __run_timer(event, label, duration, start_time):
    while not event.is_set():
        label.update(f'timer: {round(duration - (time.time() - start_time), 1)}')

def __qGen(question_func, count):
    for i in range(count):
        yield question_func()
    return

def start_quiz(caption, question_tuple, count, mod, op) -> None:
    
    func, diff = question_tuple
    q_gen = __qGen(func, count)
    q_txt = 'question_text'
    a_it = 'answer_inputtext'
    answers = []
    save_results = True
    first_question = True
    quiz_start = 0
    quiz_end = 0
    slowest = 0
    fastest = sys.maxsize
    l_timer = 'label_timer'

    sg.theme('DarkBlue14')

    layout = [  [sg.Text('count n/N'), sg.Text(f'timer: {quiz_timer_dur}', key=l_timer)],
                [sg.Text('1 QUESTION', font='Arial 22', key=q_txt)],
                [sg.InputText(key=a_it, enable_events=True) ],
                [sg.Button('Stop and save')], [sg.Button('Cancel')] ]

    window = sg.Window(caption, layout, finalize=True)
    timer_event = Event()
    while quiz_end - quiz_start < quiz_timer_dur:

        question, answer = next(q_gen)
        window[q_txt].update(question)
        answered = False
        question_start = time.time()

        logging.debug(f'q:{question}, a:{answer}')
        while not answered:   
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
                    Thread(target = __run_timer, args = (timer_event, window[l_timer], quiz_timer_dur, quiz_start)).start()
                else:
                    question_dur = time.time() - question_start
                    quiz_end = time.time()
                    slowest = max(question_dur, slowest)
                    fastest = min(question_dur, fastest)
                    answers.append((question, answer, question_dur, 0,))
                window[a_it].update('')
                answered = True
      
        else:
            continue # if inner cycle not broken continue outer
        break
    
    timer_event.set()
    window.close()

    if save_results and (count := len(answers)):
        logging.debug('save result')
        quiz_dur = quiz_end - quiz_start
        average = quiz_dur / count
        return (count, op, diff, mod, quiz_dur, quiz_timer_dur, fastest, slowest, average, 0, answers,)
    return (None, None)