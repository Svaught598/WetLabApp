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

    def on_press(self):
        app = MDApp.get_running_app()
        print(self.text)
        app.root.ids.solution_types.text = self.text
        print(app.root.ids.solution_types.text)
        self.parent.close()
        

class VolumeScreen(Screen):

    def on_solution_types(self, text):
        self.ids.solution_types.text = text

    def on_solvent(self, text):
        self.ids.solvent.text = text

    def on_material(self, text):
        self.ids.material.text = text

    def on_mass(self, text):
        # TODO: write
        pass

    def on_concentration(self, text):
        pass

