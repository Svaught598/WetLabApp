# KivyMD imports
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.menu import MDMenuItem
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd import factory_registers

# kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ListProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.metrics import dp

# local imports
from settings import SOLUTION_TYPES


class MDMenuItem(MDRectangleFlatButton):
    pass
        

class FilmScreen(Screen):

    # Information pulled from database
    SOLVENT_NAMES = ListProperty([])
    MATERIAL_NAMES = ListProperty([])

    # INformation pulled form settings
    _SOLUTION_TYPES = ListProperty([])
    _SOLUTION_TYPE_DEFAULT = SOLUTION_TYPES[0]

    def __init__(self, *args, **kwargs):
        super(FilmScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self):
        """
        Bindings to corresponding viewmodel properties 
        and initialization of widget
        """
        app = MDApp.get_running_app()
        app.film_view_model.bind(
            THICKNESS = lambda x, y: self.show_film_thickness(y),
            ERROR = lambda x, y: self.error_popup(y),

            SOLVENT_LIST = lambda x, y: self.add_solvents(y),
            MATERIAL_LIST = lambda x, y: self.add_materials(y)
        )

        # Dropdown construction from settings const.
        self.add_solution_types(SOLUTION_TYPES)

        # Dropdown construction from viewmodel querying
        # that triggers bound method in view 'add_solvents' or 'add_materials'
        app.film_view_model.get_solvents()
        app.film_view_model.get_materials()
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


    def add_solution_types(self, types):
        """Helper for constructing 'solution types' dropdown"""
        self._SOLUTION_TYPES = [{
            'viewclass': 'MDMenuItem',
            'text': type,
            'callback': self.on_solution_types
            } for type in types]
    
    def add_materials(self, materials):
        """Helper for constructing 'materials' dropdown"""
        self.MATERIAL_NAMES = [{
            'viewclass': 'MDMenuItem',
            'text': material['name'],
            'callback': self.on_material
        } for material in materials]

    def add_solvents(self, solvents):
        """Helper for constructing 'solvents' dropdown"""
        self.SOLVENT_NAMES = [{
            'viewclass': 'MDMenuItem',
            'text': solvent['name'],
            'callback': self.on_solvent
        } for solvent in solvents]

    def on_solvent(self, item):
        """boudn to solvent dropdown selection"""
        self.ids.solvent.text = item.text
        self.solvent_menu.dismiss()

    def on_material(self, item):
        """Boudn to material dropdown selection"""
        self.ids.material.text = item.text
        self.material_menu.dismiss()

    def on_solution_types(self, item):
        """Bound to solution type dropdown selection"""
        self.ids.solution_types.text = item.text
        self.types_menu.dismiss()

    def on_mass(self, text):
        """
        Not used, but kept in case I need to set events based 
        on input state change
        """
        # text set automatically for input widgets
        pass

    def on_concentration(self, text):
        """
        Not used, but kept in case I need to set events based 
        on input state change
        """
        # text set automatically for input widgets
        pass

    def clear(self):
        """Clears all inputs on view UI"""
        self.ids.concentration.text = ''
        self.ids.volume.text = ''
        self.ids.area.text = ''

    def calculate_button_pressed(self):
        """
        Passes all input parameters from screen to viewmodel
        calculate method. These inputs take the form of a dictionary
        """
        app = MDApp.get_running_app()
        app.film_view_model.calculate({
            'solution_type': self.ids.solution_types.text,
            'solvent': self.ids.solvent.text,
            'material': self.ids.material.text,
            'concentration': self.ids.concentration.text,
            'volume': self.ids.volume.text,
            'area': self.ids.area.text,
        })

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
        app.film_view_model.close_error()

    def show_film_thickness(self, film_thickness):
        """Bound to 'THICKNESS' property in volume_view_model"""
        self.ids.result.text = (
        f'Film Thickness is approximately [b][color=#ff3300]{film_thickness}[/color][/b]'
        )