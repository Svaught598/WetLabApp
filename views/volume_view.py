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

from models.solvent import Solvent
from settings import SOLUTION_TYPES


class MDMenuItem(MDRectangleFlatButton):
    pass
        

class VolumeScreen(Screen):
    SOLVENT_NAMES = ListProperty([])
    SOLUTION_TYPES = ListProperty([])

    def __init__(self, *args, **kwargs):
        super(VolumeScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self):
        self.add_solution_types(SOLUTION_TYPES)
        app = MDApp.get_running_app()
        app.volume_view_model.bind(
            volume_needed = lambda x, y: self.show_volume_needed(y),
            error = lambda x, y: self.show_error_message(y),
            solvent_list = lambda x, y: self.add_solvents(y)
        )
        app.volume_view_model.get_solvents()

    def on_solution_types(self, text):
        self.ids.solution_types.text = text
        # if text == SOLUTION_TYPES[0]:
        #     self.ids.mass.size_hint_y = 0
        #     self.ids.mass_label.size_hint_y = 0
        # if text == SOLUTION_TYPES[1]:
        #     pass

    def on_solvent(self, text):
        self.ids.solvent.text = text

    def on_material(self, text):
        self.ids.material.text = text

    def calculate_button_pressed(self):
        app = MDApp.get_running_app()
        app.volume_view_model.calculate({
            'solution_type': self.ids.solution_types.text,
            'solvent': self.ids.solvent.text,
            'material': self.ids.material.text,
            'mass': self.ids.mass.text,
            'concentration': self.ids.concentration.text
        })

    def add_solvents(self, solvents):
        self.SOLVENT_NAMES = [{
            'viewclass': 'MDMenuItem',
            'text': solvent['name'],
            'callback': self.on_solvent
            } for solvent in solvents]

    def add_solution_types(self, types):
        self.SOLUTION_TYPES = [{
            'viewclass': 'MDMenuItem',
            'text': type,
            'callback': self.on_solution_types
            } for type in types]

    def show_error_message(self, error_message):
        self.ids.volume_needed.text = error_message

    def show_volume_needed(self, volume_needed):
        self.ids.volume_needed.text = volume_needed

