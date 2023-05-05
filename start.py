import PySimpleGUI as sg
import logging
import calc


sg.theme('DarkBlue14')
logging.basicConfig(level=logging.DEBUG,)

calc.open_traincalc_window()
