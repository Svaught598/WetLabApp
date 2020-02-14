from peewee import *
from settings import DATABASE


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(DATABASE)