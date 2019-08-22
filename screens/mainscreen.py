# -*- coding: utf-8 -*-
"""

Menu Screen:
    
    This screen serves as a means navigate to each of the subroutines 
    outlined in their corresponding screen module.

"""
"""importing kivy modules"""
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder

###############################################################################
"""Menu Screen"""##############################################################
###############################################################################
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.name = 'menu'
        
Builder.load_string("""
                    
<MenuScreen>:
    BoxLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        orientation: 'vertical'
    
        BoxLayout: 
            orientation: 'vertical'
            
            Button:
                text: "Calculate Volume for Solution"
                on_press: root.manager.current = 'volumeneeded'
                
            Button:
                text: "Update data"
                on_press: root.manager.current = 'update'
                
            Button: 
                text: "Calculate Film Thickness"
                on_press: root.manager.current = 'thickness'
            
""")
    
###############################################################################