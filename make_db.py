import sqlite3 as SQL


db = SQL.connect('db.sqlite3')


try:
    cur=db.cursor()
    cur.execute('''
        CREATE TABLE solvents (
            SolventID    INTEGER    PRIMARY KEY    AUTOINCREMENT,
            name         TEXT (20)  NOT NULL,
            density      TEXT (20)  NOT NULL,
            formula      TEXT (20)  NOT NULL,
            polarity     REAL       NOT NULL
        );
    ''')
    db.commit()
    print ("success message")
except:
    print ("error")
    db.rollback()
finally:
    db.close()