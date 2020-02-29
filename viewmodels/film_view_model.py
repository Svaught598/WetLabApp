from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty

from models import Solvent, Material

class FilmViewModel(EventDispatcher):
    
    film_thickness = StringProperty('')
    error = StringProperty('')

    SOLVENT_LIST = ListProperty([])
    MATERIAL_LIST = ListProperty([])

    def calculate(self, context):
        # TODO: write method that accepts context 
        # and calculates film thickness from parameters
        pass

    def verify_fields(self, context):
        # TODO: write method that accepts context
        # and checks validity of passed data
        pass

    def get_solvents(self):
        self.SOLVENT_LIST = Solvent.get_all()

    def get_materials(self):
        self.MATERIAL_LIST = Material.get_all()