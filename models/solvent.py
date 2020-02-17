from peewee import *
from kivy.properties import ListProperty
from .base import BaseModel


class Solvent(BaseModel):
    '''Peewee Model describing solvent'''
    solventID = IntegerField(primary_key = True)
    name = CharField(unique = True)
    density = FloatField()
    formula = CharField()
    polarity = FloatField()

    def __unicode__(self):
        return str(name)

    @classmethod
    def get_all(cls):
        solvent_list = []
        for record in cls.select():
            solvent = {
                'name': str(record.name),
                'density': str(record.density),
                'formula': str(record.formula),
                'polarity': str(record.polarity)}
            solvent_list.append(solvent)
        return solvent_list

    @classmethod
    def get_solvent(cls, name):
        return cls.select().where(Solvent.name == name)