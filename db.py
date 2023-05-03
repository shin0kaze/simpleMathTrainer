import os.path
import sqlite3
import datetime
from db_utils import upd_traintable_data

dbpath = 'sqlite3.db'

if not os.path.isfile('sqlite3.db'):
    pass

def dbconnect():
    return sqlite3.connect(dbpath, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

def save(count, operation, difficulty, modification, time, timer, min, max, avg, errors=0,):
    with dbconnect() as conn:
        cur = conn.cursor()
        row = (count, operation, difficulty, modification, time, timer, avg, min, max, errors, datetime.datetime.now())
        insert_q = 'INSERT INTO quiztable' \
                '(count, operation, difficulty, modification, time, timer, speed, min, max, errors, date)' \
                'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
        cur.execute(insert_q, row)

def read(operation, difficulty, modification, full, timer = 180):
    with dbconnect() as conn:
        cur = conn.cursor()
        complete_only = ' and time >= timer' if full else ''
        condition = f"operation == '{operation}' and difficulty == '{difficulty}' and modification == '{modification}' and timer == {timer} {complete_only}"
        select_q = f'SELECT id, speed, min, max FROM quiztable WHERE {condition}'
        cur.execute(select_q)
        return cur.fetchall()

def db_get_traintable(tbname):
    conn, cursor = dbconnect()
    # drop_q = 'DROP TABLE multable'
    # cursor.execute(drop_q)
    select_q = f'SELECT prob, question, answer FROM {tbname}'
    try:
        cursor.execute(select_q)
        data = cursor.fetchall()
    except:
        pass
        # create_q = 'CREATE TABLE %s (id INT PRIMARY KEY, prob real, question text, answer text)'% tbname
        # insert_q = 'INSERT INTO %s (prob, question, answer) VALUES (?,?,?)'% tbname
        # cursor.execute(create_q)
        # initial_data = init_traintable_data(tbname)
        # cursor.executemany(insert_q, initial_data)
        # cursor.execute(select_q)
        # data = cursor.fetchall()
        # conn.close()
    return data

def db_upd_traintable(tbname, db_entities, entities):
    cursor = dbconnect().cursor()
    db_upd_ents = upd_traintable_data(db_entities, entities)
    update_q = f'UPDATE {tbname} VALUES (id, question, answer) VALUES (?,?,?)'
    cursor.executemany(update_q, db_upd_ents)
