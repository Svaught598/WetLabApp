from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.menu import MDMenuItem
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.app import MDApp

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ListProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivymd import factory_registers

from settings import SOLUTION_TYPES


class MDMenuItem(MDRectangleFlatButton):
    pass
        

class FilmScreen(Screen):
    SOLVENT_NAMES = ListProperty([])
    MATERIAL_NAMES = ListProperty([])

    _SOLUTION_TYPES = ListProperty([])
    _SOLUTION_TYPE_DEFAULT = SOLUTION_TYPES[0]

    def __init__(self, *args, **kwargs):
        super(FilmScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self):
        app = MDApp.get_running_app()
        app.film_view_model.bind(
            film_thickness = lambda x, y: self.show_film_thickness(y),
            error = lambda x, y: self.show_error_message(y),

            SOLVENT_LIST = lambda x, y: self.add_solvents(y),
            MATERIAL_LIST = lambda x, y: self.add_materials(y)
        )

        self.add_solution_types(SOLUTION_TYPES)

        app.film_view_model.get_solvents()
        app.film_view_model.get_materials()
        

    def add_solution_types(self, types):
        self._SOLUTION_TYPES = [{
            'viewclass': 'MDMenuItem',
            'text': type,
            'callback': self.on_solution_types
            } for type in types]
    
    def add_materials(self, materials):
        self.MATERIAL_NAMES = [{
            'viewclass': 'MDMenuItem',
            'text': material['name'],
            'callback': self.on_material
        } for material in materials]

    def add_solvents(self, solvents):
        self.SOLVENT_NAMES = [{
            'viewclass': 'MDMenuItem',
            'text': solvent['name'],
            'callback': self.on_solvent
        } for solvent in solvents]

    def on_solvent(self, text):
        self.ids.solvent.text = text

    def on_material(self, text):
        self.ids.material.text = text

    def on_solution_types(self, text):
        self.ids.solution_types.text = text

    def on_mass(self, text):
        # text set automatically for input widgets
        pass

    def on_concentration(self, text):
        # text set automatically for input widgets
        pass

    def clear(self):
        self.ids.concentration.text = ''
        self.ids.volume.text = ''
        self.ids.area.text = ''

    def calculate_button_pressed(self):
        app = MDApp.get_running_app()
        app.film_view_model.calculate({
            'solvent': self.ids.solvent.text,
            'material': self.ids.material.text,
            'concentration': self.ids.concentration.text,
            'area': self.ids.area.text,
        })

    def show_error_message(self, error_message):
        self.ids.result.text = error_message

    def show_film_thickness(self, film_thickness):
        self.ids.result.text = film_thickness