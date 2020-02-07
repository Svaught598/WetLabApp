import sqlite3 as SQL
import json

# TODO 
# I need this wrapper to be able to access the instance
# of the method call it is associated with. 
# Look into implementing a descriptor 
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


def loader():
    with open("data.json") as f:
        return json.load(f)


def dumper(dict):
    json.dump(dict, open("data.json", "w"))