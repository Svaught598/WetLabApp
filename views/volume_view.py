# KivyMD imports
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.menu import MDMenuItem
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd import factory_registers

# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.metrics import dp

# Local imports 
from models.solvent import Solvent
from settings import SOLUTION_TYPES, MASS_UNITS


class MDMenuItem(MDRectangleFlatButton):
    pass
        

class VolumeScreen(Screen):

    # Information pulled from database
    SOLVENT_NAMES = ListProperty([])
    MATERIAL_NAMES = ListProperty([])

    # Information pulled from settings
    _MASS_UNITS = ListProperty([])
    _SOLUTION_TYPES = ListProperty([])
    _MASS_UNIT_DEFAULT = MASS_UNITS[0]
    _SOLUTION_TYPE_DEFAULT = SOLUTION_TYPES[0]

    # Properties bound to dropdown selection. Upon change
    # they trigger an even that hides/displays widgets as needed
    _MOL_WEIGHT_FIELDS = BooleanProperty(False)
    _SOLVENT_DENSITY_FIELDS = BooleanProperty(True)

    def __init__(self, *args, **kwargs):
        super(VolumeScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self):
        """
        Bindings to corresponding viewmodel properties 
        and initialization of widget
        """
        app = MDApp.get_running_app()
        app.volume_view_model.bind(
            VOLUME = lambda x, y: self.show_volume_needed(y),
            ERROR = lambda x, y: self.error_popup(y),
            MOLECULAR_WEIGHT = lambda x, y: self.change_mol_weight(y),
            SOLVENT_DENSITY = lambda x, y: self.change_density(y),

            SOLVENT_LIST = lambda x, y: self.add_solvents(y),
            MATERIAL_LIST = lambda x, y: self.add_materials(y)
        )
        
        # Populate dropdowns from constants
        self.add_solution_types(SOLUTION_TYPES)
        self.add_mass_units(MASS_UNITS)

        # Populate dropdowns from database through viewmodel
        app.volume_view_model.get_solvents()
        app.volume_view_model.get_materials()
        self.create_dropdowns()

    def create_dropdowns(self):
        self.solvent_menu = MDDropdownMenu(
            caller=self.ids.solvent,
            items=self.SOLVENT_NAMES,
            position="bottom",
            callback=self.on_solvent, 
            width_mult=4,
        )
        self.material_menu = MDDropdownMenu(
            caller=self.ids.material,
            items=self.MATERIAL_NAMES,
            position="bottom",
            callback=self.on_material,
            width_mult=4,
        )
        self.types_menu = MDDropdownMenu(
            caller=self.ids.solution_types,
            items=self._SOLUTION_TYPES,
            position="bottom",
            callback=self.on_solution_types,
            width_mult=4,
        )
        self.mass_menu = MDDropdownMenu(
            caller = self.ids.mass_units,
            items=self._MASS_UNITS,
            position="bottom",
            callback=self.on_mass_unit,
            width_mult=4,
        )

    def on_solution_types(self, item):
        """
        Changes UI-bound properties as needed depending
        on dropdown selection.
        """
        text = item.text
        self.ids.solution_types.text = text

        # Solution Type is % w/w
        if text == SOLUTION_TYPES[0]:
            self._MOL_WEIGHT_FIELDS = False
            self._SOLVENT_DENSITY_FIELDS = True

        # Solution Type is any of (mol, mmol, umol, nmol)
        if any([
                text == SOLUTION_TYPES[3],
                text == SOLUTION_TYPES[4],
                text == SOLUTION_TYPES[5],
                text == SOLUTION_TYPES[6],
              ]):
            self._MOL_WEIGHT_FIELDS = True
            self._SOLVENT_DENSITY_FIELDS = True
        
        # Solution Type is any of (g/mL, mg/mL)
        elif any([
                text == SOLUTION_TYPES[1],
                text == SOLUTION_TYPES[2],
                ]):
            self._MOL_WEIGHT_FIELDS = False
            self._SOLVENT_DENSITY_FIELDS = False

        self.types_menu.dismiss()

    def on_solvent(self, item):
        """Bound to solvent dropdwn selection"""
        self.ids.solvent.text = item.text
        app = MDApp.get_running_app()
        app.volume_view_model.get_solvent_density(item.text)
        self.solvent_menu.dismiss()


    def on_material(self, item):
        """Bound to material dropdown selection"""
        self.ids.material.text = item.text
        app = MDApp.get_running_app()
        app.volume_view_model.get_mol_weight(item.text)
        self.material_menu.dismiss()

    def on_mass_unit(self, item):
        """Bound to mass unit dropdown selection"""
        self.ids.mass_units.text = item.text
        self.mass_menu.dismiss()

    def change_density(self, density):
        """Bound to solvent dropdown selection"""
        self.ids.solvent_density.text = f'{density}'

    def change_mol_weight(self, mol_weight):
        """Bound to material dropdown selection"""
        self.ids.molecular_weight.text = f'{mol_weight}'

    def clear(self):
        """clear input widgets on screen"""
        self.ids.mass.text = ''
        self.ids.concentration.text = ''
        self.ids.molecular_weight.text = ''

    def calculate_button_pressed(self):
        """
        Passes all input parameters from screen to viewmodel
        calculate method. These inputs take the form of a dictionary
        """
        app = MDApp.get_running_app()
        app.volume_view_model.calculate({
            'solution_type': self.ids.solution_types.text,
            'solvent': self.ids.solvent.text,
            'material': self.ids.material.text,
            'mass': self.ids.mass.text,
            'concentration': self.ids.concentration.text,
            'mass_unit': self.ids.mass_units.text,
            'mol_weight': self.ids.molecular_weight.text,
            'solvent_density': self.ids.solvent_density.text,})

    def add_mass_units(self, units):
        """Helper for constructing 'mass units' dropdown"""
        self._MASS_UNITS = [{
            'viewclass': 'MDMenuItem',
            'text': unit,
            'callback': self.on_mass_unit
        } for unit in units]

    def add_solution_types(self, types):
        """Helper for constructing 'solution types' dropdown"""
        self._SOLUTION_TYPES = [{
            'viewclass': 'MDMenuItem',
            'text': type,
            'callback': self.on_solution_types
            } for type in types]

    def add_materials(self, materials):
        """
        Helper for constructing 'materials' dropdown.
        Bound to 'MATERIAL_LIST' in volume_view_model
        """
        self.MATERIAL_NAMES = [{
            'text': material['name'],
        } for material in materials]

    def add_solvents(self, solvents):
        """
        Helper for constructing 'solvents' dropdown
        Bound to 'SOLVENT_LIST' in volume_view_model
        """
        self.SOLVENT_NAMES = [{
            'text': solvent['name']
        } for solvent in solvents]

    def show_volume_needed(self, volume_needed):
        """Bound to 'VOLUME' property in volume_view_viewmodel"""
        self.ids.volume.text = (
        f"You'll need [b][color=#ff3300]{volume_needed}[/color][/b] of the solvent to make a solution at this concentration")
    
    def error_popup(self, is_error):
        """Bound to 'ERROR' property in volume_view_model"""
        if is_error:
            self.dialog = MDDialog(
                title = 'Oops! Something went wrong!',
                text = "Please check that input fields are valid",
                size_hint = (0.8, None),
                height = dp(200), 
                on_dismiss = lambda x: self.close_error())
            self.dialog.open()

    def close_error(self):
        """closes error dialog"""
        app = MDApp.get_running_app()
        app.volume_view_model.close_error()
