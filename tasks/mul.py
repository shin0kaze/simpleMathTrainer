import random
from enum import Enum
import functools
from tasks.utils import cum_weights, randbool, randquarter

class Mod(Enum):
    COMMON = 'Common'
    TABLE = 'Table of mul'
    UPTEN = 'Up to 10...0'
    LONGA = 'Long x A'
    NEG = 'Allow negatives'
    FLOAT = 'Allow float'

def mul_get(mod, diff):
    def mul_table(cum_probs, questions):
        question, answer = random.choices(cum_weights=cum_probs, population=questions)[0]
        return question, answer
    
    def mul_long(low, high):
        a = random.randint(2,9)
        b = random.randint(low, high)
        if randbool():
            a, b = b, a
        return '{a} * {b} = ?', '%f'% a * b
    
    def mul_ten(cap):

        a = random.randint(2, cap//2)
        high = cap // a
        b = random.randint(2, high)
        return '{a} * {b} = ?', '%f'% a * b

    def mul_comm(low, high):
        a = random.randint(low, high)
        b = random.randint(low, high)
        return f'{a} * {b} = ?', f'{a*b}'

    def mul_neg(low, high):
        a = random.randint(low, high)
        b = random.randint(low, high)
        a = a if randbool() else -a
        b = a if randbool() else -b
        return '{a} * {b} = ?', '%f'% a * b

    def mul_float(low, high, digs):
        a = round(random.uniform(low, high), digs)
        b = round(random.uniform(low, high), digs)
        a = a if randbool() else -a
        b = a if randbool() else -b
        if randquarter():
            a = round(1/a, digs)
        if randquarter():
            b = round(1/b, digs)
        return '{a} * {b} = ?', '%f'% a * b
    
    match mod:
        case Mod.TABLE:
            weights, questions = db_get_multable_weights()
            return functools.partial(mul_table, cum_weights(weights), questions), mul['difficulty'][0]['name']
        case Mod.COMMON:
            return functools.partial(mul_comm, *diff['nums']), diff['name']
        case Mod.NEG:
            return functools.partial(mul_neg, *diff['nums']), diff['name']
        case Mod.UPTEN:
            ten_cap = 10 ** diff['lvl'] + 2
            return functools.partial(mul_ten, ten_cap), diff['name']
        case Mod.LONGA:
            low = 10 ** diff['lvl'] + 1
            high = 10 ** diff['lvl'] + 3
            if diff['lvl'] == 4:
                low = 1
                high = 10 ** 8
            return functools.partial(mul_long, low, high), diff['name']
        case Mod.FLOAT:
            return functools.partial(mul_float, *diff['fnums']), diff['name']

mul = {
    'name':'Multiplication',
    'hint':'AB x CD = EFGH',
    'difficulty': [
        {'name': 'kid', 'lvl': 0, 'nums': (2, 10), 'fnums':(1, 10, 1)},
        {'name': 'easy', 'lvl': 1,'nums': (11, 99), 'fnums':(1, 10, 2)},
        {'name': 'normal', 'lvl': 2,'nums': (101, 316), 'fnums':(1, 100, 2)},
        {'name': 'hard', 'lvl': 3,'nums': (400, 999), 'fnums':(1, 100, 3)},
        {'name': 'lunatic', 'lvl': 5,'nums': (1000, 9999), 'fnums':(1, 1000, 4)},
        {'name': 'random', 'lvl': 4,'nums': (0, 300), 'fnums':(1, 316, 3)},
    ],
    'mod': Mod,
    'get': mul_get,
}