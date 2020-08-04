from peewee import *
from settings import DATABASE

DB = SqliteDatabase(DATABASE)
class BaseModel(Model):
    class Meta:
        database = DB