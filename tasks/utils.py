import random
# from tasks import OpType, tbnames


def cum_weights(weights):
    cum_w = []
    current = 0.
    for w in weights:
        current += w
        cum_w.append(current)
    return cum_w


def randnum_len(n, m):
    low = 10 ** n
    high = 10 ** m
    return low, high


def randbool():
    return bool(random.getrandbits(1))


def randquarter():
    return bool(random.getrandbits(2))


def roundstr(value, digs):
    val_str = str(value)
    if dot_ind := val_str.find('.'):
        if len(val_str) - dot_ind > digs:
            last_dig = val_str[dot_ind + digs + 1]
            val_str = val_str[0:dot_ind + digs]
            if int(last_dig) > 4:
                val_str[-1] = int(val_str[-1])
    return val_str


def train_to_lists(data):
    probs = []
    questions = []
    for row in data:
        probs.append(row[0])
        questions.append((row[1], row[2]))
    return (probs, questions)
