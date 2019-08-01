# -*- coding: utf-8 -*-
"""
GUI for wetlab to help with making solutions with various 
concentrations/solvents/solutes.

Main Script
"""
"""importing kivy modules"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty
"""importing local modules"""
import screen1
"""importing python modules"""
import os

Builder.load_string("""

<DropTypes, DropSolvents, DropSolutes>:
    size_hint: [0.8, 0.2]
	pos_hint: {'center_x': 0.5 , 'center_y': 0.5}
    
<Menu>:
    orientation: 'vertical'
    DropTypes:
    DropSolvents:
    DropSolutes:
    
<Header>:
    Menu:
    BoxLayout:
        orientation: 'vertical'
        C_Input:
        M_Input:
        D_Input:

<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        id: main
        Header:
        BoxLayout: 
            Button:
                text: 'Calculate volume needed'
                on_press: str(root.calculate())
            Label: 
                text: str(root.volume)

""")

class SolutionApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.screen1 = screen1.MainScreen()

        self.sm.add_widget(self.screen1)
        
        return self.sm
    
    def on_stop(self, **kwargs):
        """I was getting an assertion error for back-to-back runs 
        so this method resets the IPython kernel so I don't need to 
        manually reset it"""
        os._exit(00)
        return True

if __name__ == '__main__':
    SolutionApp().run()