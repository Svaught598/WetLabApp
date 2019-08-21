# -*- coding: utf-8 -*-
"""
GUI for wetlab to help with making solutions with various 
concentrations/solvents/solutes.

Main Script
"""
"""importing kivy modules"""
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
"""importing local modules"""
from screens import *
"""importing python modules"""
import os

###############################################################################
"""Screen Manager"""###########################################################
###############################################################################
class Manager(ScreenManager):
    
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        
        self.menu = MenuScreen(name = 'menu')
        self.add_widget(self.menu)
        
        self.screen1 = VolumeScreen(name = 'volumeneeded')
        self.add_widget(self.screen1)
        
        self.screen2 = UpdateScreen(name = 'update')
        self.add_widget(self.screen2)

###############################################################################
"""Main Application Loop"""####################################################
###############################################################################
class SolutionApp(App):
    
    def build(self):       
        return Manager()
    
    def on_stop(self, **kwargs):
        
        """I was getting an assertion error for back-to-back runs 
        so this method resets the IPython kernel so I don't need to 
        manually reset it"""
        
        os._exit(00)
        return True

if __name__ == '__main__':
    SolutionApp().run()
    
###############################################################################