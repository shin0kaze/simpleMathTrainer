import os.path
import sqlite3
import datetime
from db_utils import upd_traintable_data


dbpath = 'sqlite3.db'


def dbconnect():
    return sqlite3.connect(dbpath, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)


def save(count, operation, difficulty, modification, time, timer, min, max, avg, errors=0,):
    with dbconnect() as conn:
        cur = conn.cursor()
        row = (count, operation, difficulty, modification, time,
               timer, avg, min, max, errors, datetime.datetime.now())
        insert_q = 'INSERT INTO quiztable' \
            '(count, operation, difficulty, modification, time, timer, speed, min, max, errors, date)' \
            'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
        cur.execute(insert_q, row)


def read(operation, difficulty, modification, full, timer=180):
    with dbconnect() as conn:
        cur = conn.cursor()
        complete_only = 'and time >= timer' if full else ''
        condition = f"operation == '{operation}' and difficulty == '{difficulty}' and modification == '{modification}' and timer == {timer} {complete_only}"
        select_q = f'SELECT id, speed, min, max FROM quiztable WHERE {condition}'
        print(select_q)
        cur.execute(select_q)
        return cur.fetchall()


def db_get_traintable(tbname):
    with dbconnect() as conn:
        cur = conn.cursor()
        select_q = f'SELECT prob, question, answer FROM {tbname}'
        try:
            cur.execute(select_q)
            data = cur.fetchall()
        except:
            pass
        return data


def db_upd_traintable(tbname, db_entities, entities):
    with dbconnect() as conn:
        cur = conn.cursor()
        print(entities)
        db_upd_ents = upd_traintable_data(db_entities, entities)
        print(db_upd_ents)
        update_q = f'UPDATE {tbname} SET prob = ? WHERE question == ?'
        print(update_q)
        cur.executemany(update_q, db_upd_ents)


if __name__ == "__main__":
    cursor = dbconnect().cursor()
