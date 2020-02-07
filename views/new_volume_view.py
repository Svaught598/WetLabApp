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

    def on_solution_types(self, text):
        self.ids.solution_types.text = text

    def on_solvent(self, text):
        self.ids.solvent.text = text

    def on_material(self, text):
        self.ids.material.text = text

    def on_mass(self, text):
        pass

    def on_concentration(self, text):
        pass

    def calculate_button_pressed(self):
        app = MDApp.get_running_app()
        app.volume_view_model.calculate(
            self.solution_types.text,
            self.solvent.text,
            self.material.text,
            self.mass.text,
            self.concentration.text
        )

"""
class VolumeScreen(Screen):
    types = StringProperty('')
    solvs = StringProperty('')
    solts = StringProperty('')
    mass = StringProperty('')
    conc = StringProperty('')
    dens = StringProperty('')
    volume = StringProperty('')

    def __init__(self, **kwargs):
        super(VolumeScreen, self).__init__(**kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self):
        app = App.get_running_app()
        self.view_model = app.volume_view_model
        self.view_model.bind(
            volume = lambda instance, volume: self.display_volume(volume)
        )

    def display_volume(self, volume):
        app = App.get_running_app()
        app.root.ids.volume.text = volume
        
    def calculate(self):
        print(self.conc)
        if self.types == '% Wt/Wt':
            if self.verify(check_density = True) == True:
                self.volume = self.calculate_wtwt()
            else: 
                _, message = self.verify(check_density = True)
                self.volume = self.error_message(message)
        elif self.types == '% Wt/V':
            if self.verify() == True:
                self.volume = self.calculate_wtv()
            else: 
                _, message = self.verify()
                self.volume = self.error_message(message)
        else: 
            self.volume = "Type of solution not specified"

    def calculate_wtwt(self):
        conc = float(self.conc)
        mass = float(self.mass)
        sdens= float(self.dens)
        return str(round(((1 - conc) * mass)/(conc * sdens), 3)) + ' ml'            
            
    def calculate_wtv(self):
        conc = float(self.conc)
        mass = float(self.mass)
        return str(round((mass/conc), 3))
        
    def verify(self, check_density = False):
        message = []
        if self.conc == '':
            message.append("Concentration field is empty\n")
        else: 
            try: 
                if float(self.conc) > 1:
                    message.append("Concentration must be less than 1\n")
            except:
                message.append("Concentration must be greater than 0\n")
    
        if self.mass == '':
            message.append("Mass field is empty\n")
        else: 
            try:
                if float(self.mass) < 0:
                    message.append("Mass must be greater than 0\n")
            except:
                pass
        
        if (self.dens == '' and check_density == True):
            message.append("Density field is empty\n")        
        
        if message == []:
            return True
        else:
            return False, message
        
    def error_message(self, messages):
        err = 'Error:\n'
        for message in messages:
            err += message 
        return err

"""