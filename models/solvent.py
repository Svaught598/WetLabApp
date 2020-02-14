from peewee import *
from kivy.properties import ListProperty
from .base import BaseModel

class Solvent(BaseModel):
    '''Peewee Model describing solvent'''
    solventID = IntegerField(primary_key = True)
    name = CharField(unique = True)
    density = CharField()
    formula = CharField()
    polarity = CharField()

    def __unicode__(self):
        return str(name)

