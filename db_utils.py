

def upd_traintable_data(db_entities, entities):
    db_upd_ents = []
    for e in entities:
        for db_e in db_entities:
            if e[1] == db_e[1]:
                coeff = 100.
                upd_prob = (db_e[0] * (coeff-1) + e[0]** 3) / coeff
                db_upd_ents.append((upd_prob, *db_e[1:]))
    return db_upd_ents