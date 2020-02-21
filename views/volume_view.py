from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.menu import MDMenuItem
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd import factory_registers

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.metrics import dp

from models.solvent import Solvent
from settings import SOLUTION_TYPES, MASS_UNITS


class MDMenuItem(MDRectangleFlatButton):
    pass
        

class VolumeScreen(Screen):
    SOLVENT_NAMES = ListProperty([])
    MATERIAL_NAMES = ListProperty([])

    _MASS_UNITS = ListProperty([])
    _SOLUTION_TYPES = ListProperty([])
    _MASS_UNIT_DEFAULT = MASS_UNITS[0]
    _SOLUTION_TYPE_DEFAULT = SOLUTION_TYPES[0]

    _MOL_WEIGHT_FIELDS = BooleanProperty(True)
    _SOLVENT_DENSITY_FIELDS = BooleanProperty(True)

    def __init__(self, *args, **kwargs):
        super(VolumeScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self):
        self.add_solution_types(SOLUTION_TYPES)
        app = MDApp.get_running_app()
        app.volume_view_model.bind(
            VOLUME = lambda x, y: self.show_volume_needed(y),
            ERROR = lambda x, y: self.error_popup(y),

            SOLVENT_LIST = lambda x, y: self.add_solvents(y),
            MATERIAL_LIST = lambda x, y: self.add_materials(y)
        )
        
        # populate dropdowns from consts
        self.add_solution_types(SOLUTION_TYPES)
        self.add_mass_units(MASS_UNITS)

        # populate dropdowns from database through viewmodel
        app.volume_view_model.get_solvents()
        app.volume_view_model.get_materials()

    def on_solution_types(self, text):
        self.ids.solution_types.text = text
        if text == SOLUTION_TYPES[0]:
            self._MOL_WEIGHT_FIELDS = True
            self._SOLVENT_DENSITY_FIELDS = True
        elif text == SOLUTION_TYPES[1]:
            self._MOL_WEIGHT_FIELDS = False
            self._SOLVENT_DENSITY_FIELDS = False
        elif text == SOLUTION_TYPES[2]:
            self._MOL_WEIGHT_FIELDS = False
            self._SOLVENT_DENSITY_FIELDS = False

    def on_solvent(self, text):
        self.ids.solvent.text = text

    def on_material(self, text):
        self.ids.material.text = text

    def on_mass_unit(self, text):
        self.ids.mass_units.text = text

    def clear(self):
        self.ids.mass.text = ''
        self.ids.concentration.text = ''
        self.ids.molecular_weight.text = ''

    def calculate_button_pressed(self):
        app = MDApp.get_running_app()
        app.volume_view_model.calculate({
            'solution_type': self.ids.solution_types.text,
            'solvent': self.ids.solvent.text,
            'material': self.ids.material.text,
            'mass': self.ids.mass.text,
            'concentration': self.ids.concentration.text,
            'mass_unit': self.ids.mass_units.text,
        })

    def add_mass_units(self, units):
        self._MASS_UNITS = [{
            'viewclass': 'MDMenuItem',
            'text': unit,
            'callback': self.on_mass_unit
        } for unit in units]

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

    def show_error_message(self, error_message):
        self.ids.volume_needed.text = error_message

    def show_volume_needed(self, volume_needed):
        self.ids.volume_needed.text = volume_needed
    
    def error_popup(self, is_error):
        print(is_error)
        if is_error:
            self.dialog = MDDialog(
                title = 'Oops! Something went wrong!',
                text = "Please check that input fields are valid",
                size_hint = (0.8, None),
                height = dp(200), 
                on_dismiss = lambda x: self.close_error())
            self.dialog.open()

    def close_error(self):
        app = MDApp.get_running_app()
        app.volume_view_model.close_error()
