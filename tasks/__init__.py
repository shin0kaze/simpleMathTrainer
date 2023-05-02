from tasks.mul import mul
from enum import Enum

class OpType(Enum):
    MUL = 'Multiplication'

def EToList(OpType):
    lst = []
    for e in OpType:
        lst.append(e)
    return lst

def choose(optype):
    match optype:
        case OpType.MUL:
            return mul