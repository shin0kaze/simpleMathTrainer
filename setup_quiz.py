import sqlite3
from string import Template
import logging
from db import dbconnect

template_tables = ['multable', 'subtable']
create_template_q = Template(
    'CREATE TABLE $tbname (id INTEGER PRIMARY KEY, prob real, question text, answer text)')
insert_template_q = Template(
    'INSERT INTO $tbname (prob, question, answer) VALUES (?,?,?)')
create_quiz_q = ('CREATE TABLE quiztable (id INTEGER PRIMARY KEY,'
                 'count INT, operation TEXT, difficulty TEXT, modification TEXT, time INT, timer INT, speed REAL, min INT, max INT, errors INT, date TIMESTAMP)')
select_quiz_q = 'SELECT * FROM quiztable'
select_template_q = Template('SELECT * FROM $tbname')


def init_multable_data():
    entities = []
    for n in range(1, 10):
        m = 1
        while n * m <= 100:
            entities.append([0, '%s * %s' % (n, m), '%i' % (n * m)])
            m += 1
    prob = 1. / len(entities)
    for e in entities:
        e[0] = prob
    return entities


def init_subtable_data():
    entities = []
    for n in range(0, 100):
        entities.append([0, '100 - %s' % n, '%i' % (100 - n)])
    prob = 1. / len(entities)
    for e in entities:
        e[0] = prob
    return entities


def init_traintable_data(tablename):
    match tablename:
        case 'multable': return init_multable_data()
        case 'subtable': return init_subtable_data()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,)
    with dbconnect() as conn:  # sqlite3.connect('sqlite3.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(create_quiz_q)
        except:
            logging.debug('quiz table exists')
        else:
            logging.debug('quiz table created')
        for tn in template_tables:
            try:
                cursor.execute(create_template_q.substitute(tbname=tn))
            except:
                logging.debug(f'{tn} table exists')
                continue
            else:
                initial_data = init_traintable_data(tn)
                cursor.executemany(
                    insert_template_q.substitute(tbname=tn), initial_data)
                logging.debug(f'{tn} table created')

        if True:
            cursor.execute(select_quiz_q)
            print(cursor.fetchall())
            # for tn in template_tables:
            #     cursor.execute(select_template_q.substitute(tbname=tn))
            #     print(cursor.fetchall())
