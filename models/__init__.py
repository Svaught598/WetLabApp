from peewee import *

from .base import DB
from .solvent import Solvent

def init_db():
    DB.connect()
    DB.create_tables([Solvent])