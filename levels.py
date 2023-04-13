from random import randrange, getrandbits, randint
import functools

class D:
    def __init__(self, from_to, name = None, special = 0) -> None:
        self.from_to = from_to
        self.name = name if name else 'from %s to %s' % (from_to[0], from_to[1])
        self.special = special

def add(low, high, mod):
    def add_common(low, high):
        answer = randint(low, high)
        summand = randint(low, answer)
        augend = answer - summand
        return ('%s + %s = ?'%(summand, augend), str(answer))
    def add_neg(low, high):
        if bool(getrandbits(1)):
            low, high = -high, -low
        answer = randint(low, high)
        summand = randint(low, answer)
        augend = answer - summand
        return ('%s + %s = ?'%(summand, augend), str(answer))
    
    match (mod):
        case 'Common': return functools.partial(add_common, low, high)
        case 'Allow negatives': return functools.partial(add_neg, low, high)

    raise Exception('No such function')
    

    

levels = [
    ['Addition (+)',
        [
            D((0, 20)),
            D((0, 100)),
            D((0, 999)),
            D((0, 9999)),
            D((0, 99_999)),
            D((0, 9_999_999_999)),
        ],
        [
            'No carry',
            'Common',
            'Allow negatives',
        ],
        add,   
    ],
    ['Substraction (-)',]
]

