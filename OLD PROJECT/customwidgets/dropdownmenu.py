# -*- coding: utf-8 -*-
"""

Custom Widgets

"""
"""importing kivy modules"""
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.properties import DictProperty

###############################################################################
"""Dropdown Menu Widget"""#####################################################
###############################################################################
class DropDownMenu(Button):
    
    types = DictProperty()
       
    def __init__(self, default_text = '', **kwargs):
        super(DropDownMenu, self).__init__(**kwargs)
        self.drop_list = None
        self.drop_list = DropDown()
        self.text = default_text
        self.name = ''
        
        """Button bindings"""
        self.bind(on_release = self.drop_list.open)
        
        """Dropdown bindings"""
        self.drop_list.bind(on_select = self.set_text)
        
        
    """generates a button for each type in types"""
    def on_types(self, instance, value):
        self.clear_widgets()
        for type in self.types:
            btn = Button(text = type, size_hint_y = None, height = 50)
            btn.bind(on_release = lambda btn: self.drop_list.select(btn.text))
            self.drop_list.add_widget(btn)
    
        
    def set_text(self, instance, value):
        setattr(self, 'text', value)
        


###############################################################################       

