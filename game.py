import PySimpleGUI as sg
import time

def now_ms():
    return round(time.time() * 1000)

def qGen(question_func, count):
    for i in range(count):
        yield question_func()
    return

def start_quiz(caption, question_func, count) -> None:
    
    q_gen = qGen(question_func, count)
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

    while q := next(q_gen):
        question, answer = q
        answered = False
        print('q:%s, a:%s'%(question, answer))
        while not answered:
            
            
            start_time = now_ms()
            window[q_txt].update(question)
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == 'Cancel':
                save_results = False
                break
            if event == 'Stop and save':
                break
            print(values[a_it])
            if values[a_it] == answer:
                answers.append((question, answer, 0, now_ms() - start_time))
                window[a_it].update('')
                answered = True
        else:
            continue
        break

    window.close()

    if save_results:
        return answers
    return []