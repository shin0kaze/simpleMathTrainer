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


if __name__ == '__main__':
    from mul import mul
    import os
    import sys
    import inspect
    currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)
    import db
    diff = mul['difficulty'][1]
    mods = mul['mod']
    for mod in mods:
        tbname = mul['db'].get(mod.value)
        datas = db.db_get_traintable(tbname) if tbname else None
        qfunc, actual_diff = mul['get'](mod.value, diff, datas)
        print(f'mod: {mod}, diff: {actual_diff}, tb: {tbname}')
        for i in range(5):
            print(qfunc())
