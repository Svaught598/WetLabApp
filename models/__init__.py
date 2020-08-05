from peewee import *

from .base import DB
from .solvent import Solvent
from .material import Material

def init_db():
    DB.connect()
    DB.create_tables([Solvent, Material])