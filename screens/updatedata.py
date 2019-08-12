# -*- coding: utf-8 -*-
"""

Updata Data Screen:
    
    - This file contains all necessary information for creating a screen 
    that can navigate through the information displayed in interactive 
    menus throughout the application and insert/delete/edit entries.
    
"""
"""importing kivy modules"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
"""importing local modules"""
from customwidgets import DropDownMenu
from bus import loader

###############################################################################
"""Update Screen Widget"""#####################################################
###############################################################################

class UpdateScreen(Screen):
    pass

###############################################################################
"""Drop-Down Widgets"""########################################################
###############################################################################

class SelectionDropDown(DropDownMenu):
    def __init__(self, **kwargs):
        super(SelectionDropDown).__init__(**kwargs)
        self.types = loader('data.json')
        
    def on_text(self, instance, value):
        return
        

###############################################################################
"""Input Widgets"""############################################################
###############################################################################
