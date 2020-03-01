from peewee import *
from .base import BaseModel


class Material(BaseModel):
    '''Peewee Model describing matrial'''
    materialID = IntegerField(primary_key=True)
    name = CharField(unique=True)
    formula = CharField()
    molecular_weight = FloatField()
    density = FloatField()

    def __unicode__(self):
        return str(name)

    @classmethod
    def get_all(cls):
        material_list = [{
            'name': str(record.name),
            'formula': str(record.formula),
            'molecular_weight': str(record.molecular_weight),
            'density': str(record.density),
            } for record in cls.select()]
        return material_list

    @classmethod
    def get_material(cls, name):
        return cls.select().where(Material.name == name)

    @classmethod
    def delete_material(cls, name):
        material = cls.get(Material.name == name)
        return material.delete_instance()