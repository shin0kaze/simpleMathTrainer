from tasks.mul import mul
from enum import Enum

class OpType(Enum):
    MUL = 'Multiplication'

tbnames = { OpType.MUL.value: 'multable'}


def EToList(OpType):
    lst = []
    for e in OpType:
        lst.append(e)
    return lst

def choose(optype):
    match optype:
        case OpType.MUL:
            return mul

def diff_get(val=None):
    if val:
        for i, diff in enumerate(mul['difficulty']):
            if diff['name'] == val:
                 return i
    diffs = []
    for diff in mul['difficulty']:
        diffs.append(diff['name'])
    return diffs

