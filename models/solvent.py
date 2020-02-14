from peewee import *
from kivy.properties import ListProperty

class Solvent(Model):
    '''Peewee Model describing solvent'''
    solventID = IntegerField(primary_key = True)
    name = CharField()
    density = CharField()
    formula = CharField()
    polarity = CharFiel()

    class Meta:
        database = SqliteDatabase('db.sqlite3')
