# -*- coding: utf-8 -*-
"""






"""
"""importing kivy modules"""
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
"""importing local modules"""
from customwidgets import DropDownMenu
from utils import loader
"""importing python modules"""
import os


###############################################################################
"""Screen Manager"""###########################################################
###############################################################################
class FilmThicknessScreen(Screen):
    
    """properties bound to dropdown selection"""
    solvs = StringProperty('')
    solts = StringProperty('')
    
    
    """properties bound to inputs"""
    vol = StringProperty('')
    conc = StringProperty('')
    sden = StringProperty('')
    mden = StringProperty('')
    area = StringProperty('')
    
    """properties bound to output"""
    thickness = StringProperty('')
    
    
    def calculate(self):
        if self.verify() == True:
            conc = float(self.conc)
            vol = float(self.vol)
            sden = float(self.sden)
            mden = float(self.mden)
            area = float(self.area)
            
            """computing the mass in on ml of solution"""
            a = (1 - conc) / (conc * sden)
            b = 1 / (mden)
            mass = vol * (a + b)**(-1)
            
            """finding the volume of the film"""
            film_vol = mass / mden
            
            """using area guess to estimate film thickness"""
            self.thickness = str(round(film_vol / area * 10000, 4)) + " Microns"    
        else: 
            _, message = self.verify()
            self.thickness = self.error_message(message)
        
        
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
        
        
        """checking volume field"""
        if self.vol == '':
            message.append("Volume field is empty\n")
        else: 
            try:
                if float(self.vol) < 0:
                    message.append("Volume must be greater than 0\n")
            except:
                pass
        
        
        """checking density fields"""
        if (self.sden == ''):
            message.append("Solvent density field is empty\n")        
        if (self.mden == ''):
            message.append("Material density field is empty\n")      
        
        
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
    
    
###############################################################################
"""Drop-Down Widgets"""########################################################
###############################################################################
class DropSolvents(DropDownMenu):
    
    """Dropdown menu for solvent selection"""
    
    def __init__(self, **kwargs):
        super(DropSolvents, self).__init__(**kwargs)
        self.types = loader()['Solvents']
        self.default_text = "Solvent"
        self.text = "Solvent"
        self.name = "sden"
        
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
        self.name = "mden"

    def set_parent_screen(self, instance, value):
        try:
            setattr(self.parent.parent.parent, self.name, str(self.types[str(value)]))
        except:
            setattr(self.parent.parent.parent, self.name, "No solvent selected")
        
    def on_parent(self, instance, parent):
        self.bind(text = self.set_parent_screen)
        
###############################################################################

###############################################################################
"""Main Application Loop"""####################################################
###############################################################################
class SolutionApp(App):
    
    def build(self):       
        return FilmThicknessScreen()
    
    def on_stop(self, **kwargs):
        
        """I was getting an assertion error for back-to-back runs 
        so this method resets the IPython kernel so I don't need to 
        manually reset it"""
        
        os._exit(00)
        return True

if __name__ == '__main__':
    SolutionApp().run()
    
###############################################################################
