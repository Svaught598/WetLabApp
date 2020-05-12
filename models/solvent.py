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
        solvent_list = [{
            'name': str(record.name),
            'density': str(record.density),
            'formula': str(record.formula),
            'polarity': str(record.polarity)
            } for record in cls.select()]
        return solvent_list

    @classmethod
    def get_solvent(cls, name):
        """Since name is a unique field, this query should only return
        one record in the list, so we use the primary index 0"""
        record = cls.select().where(Solvent.name == name)[0]
        solvent = {
            'solvent_name': str(record.name),
            'density': str(record.density),
            'formula': str(record.formula),
            'polarity': str(record.polarity)}
        return solvent
        

    @classmethod
    def delete_solvent(cls, name):
        solvent = cls.get(Solvent.name == name)
        return solvent.delete_instance()

    @classmethod
    def update_solvent(cls, name, context):
        query = cls.update(context).where(cls.name == name)
        query.execute()
