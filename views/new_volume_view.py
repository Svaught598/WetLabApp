from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.menu import MDMenuItem
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.app import MDApp

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivymd import factory_registers


class MDMenuItem(MDRectangleFlatButton):
    pass
        

class VolumeScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(VolumeScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self):
        app = MDApp.get_running_app()
        app.volume_view_model.bind(
            volume_needed = lambda x, y: self.show_volume_needed(y),
            error = lambda x, y: self.show_error_message(y)
        )

    def on_solution_types(self, text):
        self.ids.solution_types.text = text

    def on_solvent(self, text):
        self.ids.solvent.text = text

    def on_material(self, text):
        self.ids.material.text = text

    def on_mass(self, text):
        # text set automatically for input widgets
        pass

    def on_concentration(self, text):
        # text set automatically for input widgets
        pass

    def calculate_button_pressed(self):
        app = MDApp.get_running_app()
        app.volume_view_model.calculate({
            'solution_types': self.ids.solution_types.text,
            'solvent': self.ids.solvent.text,
            'material': self.ids.material.text,
            'mass': self.ids.mass.text,
            'concentration': self.ids.concentration.text,
            'density': self.density.text,
        })

    def show_error_message(self, error_message):
        self.ids.volume_needed.text = error_message

    def show_volume_needed(self, volume_needed):
        self.ids.volume_needed.text = volume_needed

