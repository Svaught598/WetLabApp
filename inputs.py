# -*- coding: utf-8 -*-
"""

Inputs

"""
"""importing kivy modules"""
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.bubble import Bubble
from kivy.properties import NumericProperty, StringProperty, BooleanProperty


"""Custom Inputs"""############################################################
class C_Input(BoxLayout):
    
    concentration = StringProperty('')
    
    def __init__(self, **kwargs):
        orientation = 'horizontal'
        super(C_Input, self).__init__(**kwargs)
        self.label = Label(text = 'Concentration:')
        self.input = TextInput(input_type = 'number', input_filter = 'float')
        
        self.add_widget(self.label)
        self.add_widget(self.input)
        self.input.bind(text = self.set_concentration)
        
    def set_concentration(self, instance, value):
        self.concentration = value
        self.parent.parent.parent.concentration = value 
            
        
class M_Input(BoxLayout):
     
    mass = StringProperty('')
    
    def __init__(self, **kwargs):
        super(M_Input, self).__init__(**kwargs)
        self.label = Label(text = 'Mass:')
        self.input = TextInput(input_type = 'number', input_filter = 'float')
        
        self.add_widget(self.label)
        self.add_widget(self.input)
        self.input.bind(text = self.set_mass)
        
    def set_mass(self, instance, value):
        self.mass = value
        self.parent.parent.parent.mass = value 

class D_Input(BoxLayout):
    
    density = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(D_Input, self).__init__(**kwargs)
        self.label = Label(text = 'Density:')
        self.dens  = Label(text = '')
        
        self.add_widget(self.label)
        self.add_widget(self.dens)

    def on_parent(self, instance, value):
        self.parent.parent.parent.bind(solvent = self.set_text)
        
    def set_text(self, instance, value):
        self.dens.text = value
        self.parent.parent.parent.solute_density = value
        


