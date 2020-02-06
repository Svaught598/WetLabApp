from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.lang.builder import Builder

from customwidgets import DropDownMenu
from utils import loader


class VolumeScreen(Screen):
    types = StringProperty('')
    solvs = StringProperty('')
    solts = StringProperty('')
    mass = StringProperty('')
    conc = StringProperty('')
    dens = StringProperty('')
    volume = StringProperty('')
    
    def calculate(self):
        """checks dropdown menu selection to call 
        appropriate calculation function"""
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
        """checking concentration field"""
        if self.conc == '':
            message.append("Concentration field is empty\n")
        else: 
            try: 
                if float(self.conc) > 1:
                    message.append("Concentration must be less than 1\n")
            except:
                message.append("Concentration must be greater than 0\n")
    
        """checking mass field"""
        if self.mass == '':
            message.append("Mass field is empty\n")
        else: 
            try:
                if float(self.mass) < 0:
                    message.append("Mass must be greater than 0\n")
            except:
                pass
        
        """checking density field"""
        if (self.dens == '' and check_density == True):
            message.append("Density field is empty\n")        
        
        """Here we return messages only if False, for use with error_message()"""
        if message == []:
            return True
        else:
            return False, message
        
    def error_message(self, messages):
        err = 'Error:\n'
        for message in messages:
            err += message 
        return err
        

class DropTypes(DropDownMenu):
    """Dropdown menu for solution type selection"""
    def __init__(self, **kwargs):
        super(DropTypes, self).__init__(**kwargs)
        self.types = loader()['Types']
        self.default_text = "Type of Solution"
        self.text = "Type of Solution"
        self.name = "type_solution"
        
    def set_parent_screen(self, instance, value):
        setattr(self.parent.parent.parent.parent, self.name, value)
        
    def on_parent(self, instance, parent):
        self.bind(text = self.set_parent_screen)


class DropSolvents(DropDownMenu):
    """Dropdown menu for solvent selection"""
    def __init__(self, **kwargs):
        super(DropSolvents, self).__init__(**kwargs)
        self.types = loader()['Solvents']
        self.default_text = "Solvent"
        self.text = "Solvent"
        self.name = "dens"
        
    def set_parent_screen(self, instance, value):
        try:
            setattr(self.parent.parent.parent, self.name, str(self.types[str(value)]))
        except:
            setattr(self.parent.parent.parent, self.name, "No solvent selected")
        
    def on_parent(self, instance, parent):
        self.bind(text = self.set_parent_screen)
        

class DropSolutes(DropDownMenu):
    """Dropdown menu for solute selection"""
    def __init__(self, **kwargs):
        super(DropSolutes, self).__init__(**kwargs)
        self.types = loader()['Solutes']
        self.default_text = "Solute"
        self.text = "Solute"
        self.name = "solts"

    def set_parent_screen(self, instance, value):
        setattr(self.parent.parent.parent.parent, self.name, value)
        
    def on_parent(self, instance, parent):
        self.bind(text = self.set_parent_screen)
        
        

