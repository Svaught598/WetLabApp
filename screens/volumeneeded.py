# -*- coding: utf-8 -*-
"""

Volume Needed Screen:
    
    - This file contains all necessary information for calculating the 
    volume needed to make a solution matching given criteria
    
    
"""
"""importing kivy modules"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.lang.builder import Builder
"""Importing Local Modules"""
from customwidgets import DropDownMenu
from bus import loader

###############################################################################
"""Main Screen Widget"""#######################################################
###############################################################################
class VolumeNeededScreen(Screen):
    
    """properties bound to dropdown selection"""
    type_solution = StringProperty('')
    solvent = StringProperty('')
    solute = StringProperty('')
    
    
    """properties bound to inputs"""
    mass = StringProperty('')
    concentration = StringProperty('')
    solvent_density = StringProperty('')
    volume = StringProperty('')
    
    
####"""Calculation Methods"""##################################################
    def calculate(self):
        
        """checks dropdown menu selection to call 
        appropriate calculation function"""
        
        if self.type_solution == '% Wt/Wt':
            return self.calculate_wtwt()
        elif self.type_solution == '% Wt/V':
            return self.calculate_wtv()
        else: 
            self.volume = "Type of solution not specified"



    def calculate_wtwt(self):
        if self.verify() == '':
            self.volume = str(round(((1 - float(self.concentration)) * float(self.mass))/
                          (float(self.concentration) * float(self.solvent_density)), 3)) + ' ml'
        else: 
            self.volume = 'Error:\n' + self.verify()
            
            
            
    def calculate_wtv(self):
        if (self.verify() == '' or self.verify == "One or more fields is blank"):
            try:
                self.volume = str(round((float(self.mass)/float(self.concentration)), 3))
            except:
                self.volume = "Error: \nOne or more fields is blank"
        else:
            self.volume = self.verify()
        
        
        
####"""Verification Method"""##################################################
    def verify(self):
        message = ''
        if (self.concentration != '' and self.mass != '' and self.solvent_density != ''):
            if float(self.concentration) > 1:
                message += "Concentration is too high\n"
            if float(self.mass) < 0:
                message += "Mass must be positive\n"
            return message
        return "One or more fields is blank"
    
###############################################################################
Builder.load_string("""
                    
<VolumeNeededScreen>:
    BoxLayout:
        orientation: 'vertical'
        id: main
        
        BoxLayout:
            height: '20sp'
            Button:
                text: 'Back'
                on_press: root.manager.current = 'menu'
        Header:
        BoxLayout: 
            Button:
                text: 'Calculate volume needed'
                on_press: str(root.calculate())
            Label: 
                text: str(root.volume)
""")
    
###############################################################################
"""Drop-Down Widgets"""########################################################
###############################################################################


class DropTypes(DropDownMenu):
    
    """Dropdown menu for solution type selection"""
    
    def __init__(self, **kwargs):
        super(DropTypes, self).__init__(**kwargs)
        self.types = loader('data.json')['Types']
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
        self.types = loader('data.json')['Solvents']
        self.default_text = "Solvent"
        self.text = "Solvent"
        self.name = "solvent"
        
    def set_parent_screen(self, instance, value):
        try:
            setattr(self.parent.parent.parent.parent, self.name, str(self.types[str(value)]))
        except:
            setattr(self.parent.parent.parent.parent, self.name, "No solvent selected")
        
    def on_parent(self, instance, parent):
        self.bind(text = self.set_parent_screen)
        
class DropSolutes(DropDownMenu):
    
    """Dropdown menu for solute selection"""
    
    def __init__(self, **kwargs):
        super(DropSolutes, self).__init__(**kwargs)
        self.types = loader('data.json')['Solutes']
        self.default_text = "Solute"
        self.text = "Solute"
        self.name = "solute"

    def set_parent_screen(self, instance, value):
        setattr(self.parent.parent.parent.parent, self.name, value)
        
    def on_parent(self, instance, parent):
        self.bind(text = self.set_parent_screen)
        
Builder.load_string("""
                    
<DropTypes, DropSolvents, DropSolutes>:
    size_hint: [0.8, 0.2]
	pos_hint: {'center_x': 0.5 , 'center_y': 0.5}
    
""")
        
###############################################################################
"""Input Widgets"""############################################################
###############################################################################

class Concentration_Input(BoxLayout):
    
    """This input is for concentration. It takes a numeric value 
    and passes it to the MainScreen.concentration"""
    
    concentration = StringProperty('')
    
    def __init__(self, **kwargs):
        super(Concentration_Input, self).__init__(**kwargs)
        self.label = Label(text = 'Concentration:\n(as fraction)')
        self.input = TextInput(input_type = 'number', input_filter = 'float')
        
        self.add_widget(self.label)
        self.add_widget(self.input)
        self.input.bind(text = self.set_concentration)
        
    def set_concentration(self, instance, value):
        self.concentration = value
        self.parent.parent.parent.parent.concentration = value 
            
        
class Mass_Input(BoxLayout):
    
    """This input is for mass. It takes a numeric value and 
    passes it to the MainScreen.mass"""
     
    mass = StringProperty('')
    
    def __init__(self, **kwargs):
        super(Mass_Input, self).__init__(**kwargs)
        self.label = Label(text = 'Mass:\n(in grams)')
        self.input = TextInput(input_type = 'number', input_filter = 'float')
        
        self.add_widget(self.label)
        self.add_widget(self.input)
        self.input.bind(text = self.set_mass)
        
    def set_mass(self, instance, value):
        self.mass = value
        self.parent.parent.parent.parent.mass = value 


class Density_Input(BoxLayout):
    
    """This input is for density. It shows the density of the 
    solvent chosen on the solvents dropwdown menu"""

    def __init__(self, **kwargs):
        super(Density_Input, self).__init__(**kwargs)
        self.label = Label(text = 'Density:\n(in g/ml)')
        self.dens  = Label(text = 'No solvent selected')
        
        self.add_widget(self.label)
        self.add_widget(self.dens)

    def on_parent(self, instance, value):
        self.parent.parent.parent.parent.bind(solvent = self.set_text)
        
    def set_text(self, instance, value):
        self.dens.text = value
        self.parent.parent.parent.parent.solvent_density = value
        
###############################################################################
"""Blank Widgets"""############################################################
###############################################################################

class SelectionMenu(BoxLayout):
    pass

Builder.load_string("""
                    
<SelectionMenu>:
    orientation: 'vertical'
    DropTypes:
    DropSolvents:
    DropSolutes:
        
""")

###############################################################################
class Header(BoxLayout):
    pass

Builder.load_string("""
                    
<Header>:
    SelectionMenu:
    BoxLayout:
        orientation: 'vertical'
        Concentration_Input:
        Mass_Input:
        Density_Input:
            
""")

###############################################################################
