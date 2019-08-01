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
import dropdownmenu
import inputs
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

<MainLayout>:
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
class Menu(BoxLayout):
    pass

class Header(BoxLayout):
    pass

class MainLayout(BoxLayout):
    """properties bound to dropdowns"""
    type_solution = StringProperty('')
    solvent = StringProperty('')
    solute = StringProperty('')
    """properties bound to inputs"""
    mass = StringProperty('')
    concentration = StringProperty('')
    solute_density = StringProperty('')
    volume = StringProperty('')
        
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        
    def calculate(self):
        if (
                self.concentration != '' and
                self.mass != '' and
                self.solute_density != ''
            ):
            self.result = (((1 - float(self.concentration)) * float(self.mass))/
                          (float(self.concentration) * float(self.solute_density)))
            if self.result < 0:
                self.volume = str('Solution not viable:')
            else: 
                self.volume = str(round(self.result, 3))
        else: 
            print('error')
            print(self.concentration, self.mass, self.solute_density)
    
class Inputs(BoxLayout):
    pass

class SolutionApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.screen1 = Screen()
        
        self.main = MainLayout()
        self.screen1.add_widget(self.main)
        
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