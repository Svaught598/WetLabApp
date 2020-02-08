from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import StringProperty


class FilmViewModel(EventDispatcher):
    
    film_thickness = StringProperty('')
    error = StringProperty('')

    def calculate(self, context):
        # TODO: write method that accepts context 
        # and calculates film thickness from parameters
        pass

    def verify_fields(self, context):
        # TODO: write method that accepts context
        # and checks validity of passed data
        pass