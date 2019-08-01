# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 10:50:18 2019

@author: Steven
"""
"""importing kivy modules"""
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
"""importing other modules"""
import json


def loader(json_filename):
    with open(json_filename) as f:
        return_dict = json.load(f)
    return return_dict


"""DropDown menu for solution type"""##########################################
class DropTypes(Button):
    
    types = loader('data.json')['Types']
    
    def __init__(self, **kwargs):
        super(DropTypes, self).__init__(**kwargs)
        self.drop_list = None
        self.drop_list = DropDown()
        self.text = "Type of Solution"

        """generates a button for each type in types"""
        for type in DropTypes.types:
            btn = Button(text = type, size_hint_y = None, height = 50)
            btn.bind(on_release = lambda btn: self.drop_list.select(btn.text))
            self.drop_list.add_widget(btn)

        """bind parent button release to dropdown opening
           bind opening of menu to desired parent button text"""
        self.bind(on_release = self.drop_list.open)
        self.bind(on_release = lambda instance: setattr(self, 'text', 'Type of Solution'))
       
        """bind dropdown selection to parent button text"""
        self.drop_list.bind(on_select = lambda instance, x: setattr(self, 'text', x))
        
    def on_parent(self, instance, parent):
        self.drop_list.bind(on_select = lambda instance, x: setattr(self.parent.parent.parent, 'type_solution', x))
        
"""DropDown menu for solvent type"""###########################################
class DropSolvents(Button):
    
    types = loader('data.json')['Solvents']
       
    def __init__(self, **kwargs):
        super(DropSolvents, self).__init__(**kwargs)
        self.drop_list = None
        self.drop_list = DropDown()
        self.text = "Solvent"
        
        """generates a button for each type in types"""
        for type in DropSolvents.types:
            btn = Button(text = type, size_hint_y = None, height = 50)
            btn.bind(on_release = lambda btn: self.drop_list.select(btn.text))
            self.drop_list.add_widget(btn)
            
        """bind parent button release to dropdown opening
           bind opening of menu to desired parent button text"""
        self.bind(on_release = self.drop_list.open)
        self.bind(on_release = lambda instance: setattr(self, 'text', 'Solvent'))
        
        """bind dropdown selection to parent button text"""
        self.drop_list.bind(on_select = lambda instance, x: setattr(self, 'text', x))
        
    def on_parent(self, instance, parent):
        self.drop_list.bind(on_select = lambda instance, x: setattr(self.parent.parent.parent, 'solvent', str(self.types[x])))
        
"""DropDown menu for solute type"""############################################
class DropSolutes(Button):
    
    types = loader('data.json')['Solutes']
       
    def __init__(self, **kwargs):
        super(DropSolutes, self).__init__(**kwargs)
        self.drop_list = None
        self.drop_list = DropDown()
        self.text = "Solute"
        
        """generates a button for each type in types"""
        for type in DropSolutes.types:
            btn = Button(text = type, size_hint_y = None, height = 50)
            btn.bind(on_release = lambda btn: self.drop_list.select(btn.text))
            self.drop_list.add_widget(btn)
            
        """bind parent button release to dropdown opening
           bind opening of menu to desired parent button text"""
        self.bind(on_release = self.drop_list.open)
        self.bind(on_release = lambda instance: setattr(self, 'text', 'Solute'))
        
        """bind dropdown selection to parent button text"""
        self.drop_list.bind(on_select = lambda instance, x: setattr(self, 'text', x))
        
    def on_parent(self, instance, parent):
        self.drop_list.bind(on_select = lambda instance, x: setattr(self.parent.parent.parent, 'solute', x))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        