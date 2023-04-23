import os.path
import sqlite3



if not os.path.isfile('sqlite3.db'):
    pass

def dbconnect():
    con = sqlite3.connect('sqlite3.db')
    cur = con.cursor()
    return con, cur


def save():
    pass

def read():
    pass

def db_get_probtable(tbname):
    conn, cursor = dbconnect()
    # drop_q = 'DROP TABLE multable'
    # cursor.execute(drop_q)
    select_q = 'SELECT prob, question, answer FROM %s'% tbname
    try:
        cursor.execute(select_q)
        data = cursor.fetchall()
    except:
        create_q = 'CREATE TABLE %s (id INT PRIMARY KEY, prob real, question text, answer text)'% tbname
        insert_q = 'INSERT INTO %s (prob, question, answer) VALUES (?,?,?)'% tbname
        cursor.execute(create_q)
        init_data = []
        match tbname:
            case 'multable': 
                init_data = init_multable_data()
            case 'subtable':
                init_data = init_subtable_data()
        cursor.executemany(insert_q, init_data)
        cursor.execute(select_q)
        data = cursor.fetchall()
        conn.close()
    return data

def db_upd_multable(tbname, db_entities, entities):
    cursor = sqlite3.connect().cursor()
    db_upd_ents = upd_probtable_data(db_entities, entities)
    update_q = 'UPDATE %s VALUES (id, question, answer) VALUES (?,?,?)'% tbname
    cursor.executemany(update_q, db_upd_ents)     

def upd_probtable_data(db_entities, entitties):
    db_upd_ents = []
    for e in entitties:
        for db_e in db_entities:
            if e[1] == db_e[1]:
                coeff = 100.
                upd_prob = (db_e[0] * (coeff-1) + e[0]) // coeff
                db_upd_ents.append((upd_prob, *db_e[1:]))
    return db_upd_ents

def init_multable_data():
    entities = []
    for n in range(1,10):
        m = 1
        while n * m <= 100:
            entities.append([0,'%s * %s'%(n, m),'%i'% (n * m)])
            m+=1
    prob = 1. / len(entities)
    for e in entities:
        e[0] = prob
    return entities

def init_subtable_data():
    entities = []
    for n in range(0,100):
        entities.append([0,'100 - %s'%n, '%i'% (100 - n)])
    prob = 1. / len(entities)
    for e in entities:
        e[0] = prob
    return entities

all = db_get_probtable('subtable')


print(all)