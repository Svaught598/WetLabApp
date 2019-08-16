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
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.properties import BooleanProperty
"""importing local modules"""
from customwidgets import DropDownMenu
from bus import loader

###############################################################################
"""Update Screen Widget"""#####################################################
###############################################################################

class UpdateScreen(Screen):
    
    """data contains a list of all dicts displayed for a 
    selection in the dropdown"""
    disp_data = []
  
    
    def save(self):
        #save stuff here
        for item in self.rvlayout.children:
            print('%d is child.index for save method' % item.index)
        return 
    
    
    def clear(self):
        self.rv.data = []

    
    def add_entry(self):
        self.disp_data.append({'selection': str(self.input_1.text), 'pair': str(self.input_2.text)})
        self.rv.data = self.disp_data
        self.input_1.text = ''
        self.input_2.text = ''
        return
    
    
    def pair(self):
        #find pair to selection
        return
    
    
    def delete(self):
        for index, item in enumerate(reversed(self.rvlayout.children)):
            if bool(item.selected):
                self.disp_data.pop(index)
        self.clear()
        self.rv.data = self.disp_data
    
    
    def populate(self, key):
        data = loader()[key]
        self.clear()
        for item in data:
            self.disp_data.append({'selection': str(item), 'pair': str(data[item])})        
        self.rv.data = self.disp_data


Builder.load_string("""
                         
<UpdateScreen>:
    rv: rv
    rvlayout: rvlayout
    input_1: input_1
    input_2: input_2
    

    BoxLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        orientation: 'vertical'
        
        Button: 
            size_hint_y: None
            height: dp(56)
            text: "Back to Menu"
            on_press: root.manager.current = "menu"
    
        BoxLayout:
            canvas:
                Color:
                    rgba: 0.3, 0.3, 0.3, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(56)
            padding: dp(8)
            spacing: dp(16)
            
            SelectionDropDown:

            Button:
                text: "Delete"
                on_press: root.delete()
            
            Button: 
                text: "Save Changes"
                on_press: root.save()
            
        BoxLayout:
            canvas:
                Color:
                    rgba: 0.3, 0.3, 0.3, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(56)
            padding: dp(8)
            spacing: dp(16)
        
            TextInput:
                id: input_1
                hint_text: ''
                padding: dp(10), dp(10), 0, 0
                
            TextInput: 
                id: input_2
                hint_text: ''
                padding: dp(10), dp(10), 0, 0
        
            Button: 
                text: "Add Entry"
                on_press: root.add_entry()
            
        RecycleView:
            id: rv
            scroll_type: ['bars', 'content']
            scroll_wheel_distance: dp(114)
            bar_width: dp(10)
            viewclass: 'SelectableRow'
            SelectableRecycleBoxLayout:
                id: rvlayout
        
""")
###############################################################################
"""Supporting Widgets"""########################################################
###############################################################################

class SelectionDropDown(DropDownMenu):
    
    def __init__(self, **kwargs):
        super(SelectionDropDown, self).__init__(**kwargs)
        self.types = loader()
        self.default_text = "Choose category to edit"
        self.text = "Choose category to edit"
        self.name = "selection"
        
        
    def on_text(self, instance, value):
        if self.text == self.default_text:
            return
        else: 
            self.parent.parent.parent.clear()
            self.parent.parent.parent.populate(self.text)
            
            
Builder.load_string("""
                  
<SelectionDropDown>:    

""")
    
###############################################################################
"""Recycle View Components"""##################################################
###############################################################################
    
class SelectableRow(RecycleDataViewBehavior, BoxLayout):
    
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    
    
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableRow, self).refresh_view_attrs(
            rv, index, data)


    def on_touch_down(self, touch):
        if super(SelectableRow, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            if self.selected:
                self.parent.select_with_touch(self.index, touch)
                self.selected = False
                return True
            else: 
                return self.parent.select_with_touch(self.index, touch)


    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected


Builder.load_string("""
                    
<SelectableRow>:
    spacing: dp(2)
    selection: ''
    pair: ''
    
    Label: 
        id: val_1
        canvas.before:
            Color:
                rgba: (.8, .8, .8, .3) if root.selected else (0.3, 0.3, 0.8, 1)
            Rectangle:
                size: self.size
                pos: self.pos
            
        text: root.selection
        size: self.size
        pos_hint: {'center_x': 1}
        padding: dp(2), dp(2)
        
    Label: 
        id: val_2
        canvas.before:
            Color:
                rgba: (.8, .8, .8, .3) if root.selected else (0.3, 0.3, 0.8, 1)
            Rectangle:
                size: self.size
                pos: self.pos
            
        text: root.pair
        size: self.size
        pos_hint: {'center_x': 1}
        padding: dp(2), dp(2)
        
""")

class SelectableRecycleBoxLayout(FocusBehavior, 
                                 LayoutSelectionBehavior, 
                                 RecycleBoxLayout):
    pass
    
Builder.load_string("""
                    
<SelectableRecycleBoxLayout>:
    cols: 1
    default_size: None, dp(56)
    default_size_hint: 1, None
    size_hint_y: None
    height: self.minimum_height
    orientation: 'vertical'
    spacing: dp(2)
                
""")
        
###############################################################################
"""Input Widgets"""############################################################
###############################################################################

#class TestApp(App):
#    def build(self):
#        return UpdateScreen()
#
#
#if __name__ == '__main__':
#    TestApp().run()