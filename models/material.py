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
        """Since name is a unique field, this query should only return
        one record in the list, so we use the primary index 0"""
        record = cls.select().where(cls.name == name)[0]
        material = {
            'material_name': str(record.name),
            'formula': str(record.formula),
            'molecular_weight': str(record.molecular_weight),
            'density': str(record.density)}
        return material

    @classmethod
    def delete_material(cls, name):
        material = cls.get(Material.name == name)
        return material.delete_instance()

    @classmethod
    def update_material(cls, name, context):
        query = cls.update(context).where(cls.name == name)
        query.execute()

