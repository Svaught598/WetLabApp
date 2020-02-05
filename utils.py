import sqlite3 as SQL


def querify(method, *args, **kwargs):
    client = SQL.connect('db.sqlite3')
    query, info = method()
    try:
        cur=db.cursor()
        cur.execute(query, info)
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()