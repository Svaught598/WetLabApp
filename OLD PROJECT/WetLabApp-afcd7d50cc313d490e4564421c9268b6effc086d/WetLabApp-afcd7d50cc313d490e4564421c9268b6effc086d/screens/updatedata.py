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
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.factory import Factory
"""importing local modules"""
from customwidgets import DropDownMenu
from bus import loader, dumper
from pprint import pprint

###############################################################################
"""Update Screen Widget"""#####################################################
###############################################################################

class UpdateScreen(Screen):
    
    """data contains a list of all dicts displayed for a 
    selection in the dropdown"""
    disp_data = []
    json_data = loader()
    key       = ''
    
    
    hint_text_1 = StringProperty('')
    hint_text_2 = StringProperty('')
    
    
    def save(self):
        Factory.VerifyPopup(data = self.json_data).open()
        
    
    def clear(self):
        self.rv.data = []
        self.disp_data = []

    
    def add_entry(self):
        try:
            self.disp_data.append({'selection': str(self.input_1.text), 'pair': str(self.input_2.text)})
            self.json_data[self.key].update({self.input_1.text: self.input_2.text})
            self.rv.data = self.disp_data
            self.input_1.text = ''
            self.input_2.text = ''
        except: 
            Factory.ErrorPopup().open()
            
 
    def delete(self):
        temp = self.disp_data
        for index, item in enumerate(reversed(self.rvlayout.children)):
            if item.selected:
                self.json_data[self.key].pop(item.selection)
                i = temp.index({'selection': item.selection, 'pair': item.pair})
                temp.pop(i)
                print(temp.pop(index))
        self.clear()
        self.disp_data = temp
        self.rv.data = temp
    
    
    def populate(self, key):
        data = self.json_data[key]
        self.clear()
        for item in data:
            self.disp_data.append({'selection': str(item), 'pair': str(data[item])})        
        self.rv.data = self.disp_data
        self.key = key

class Content(BoxLayout):
    pass

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
        canvas.before: 
            Color: 
                rgba: 0.3, 0.3, 0.3, 1
            Rectangle:
                size: self.size
                pos: self.pos
        
        Button: 
            background_color: (0.3, 0.3, 0.3, .5)
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
                text: "Save"
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
                hint_text: root.hint_text_1
                padding: dp(10), dp(10), 0, 0
                
            TextInput: 
                id: input_2
                hint_text: root.hint_text_2
                padding: dp(10), dp(10), 0, 0
        
            Button: 
                text: "Add Entry"
                on_press: root.add_entry()
                
        BoxLayout:
            canvas:
                Color:
                    rgba: 0, 0, 0, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(56)
            padding: dp(2)
            spacing: dp(2)
            
            
            BoxLayout:
                color: [0.8, 0.8, 0.8, .3]
                canvas.before: 
                    Color: 
                        rgba: [0, 0, 0, 1] if root.hint_text_1 == '' else self.color
                    Rectangle:
                        size: self.size
                        pos: self.pos
                Label: 
                    id: label_1
                    text: root.hint_text_1
                    
            BoxLayout:
                color: [0.8, 0.8, 0.8, .3]
                canvas.before: 
                    Color: 
                        rgba: [0, 0, 0, 1] if root.hint_text_2 == '' else self.color
                    Rectangle:
                        size: self.size
                        pos: self.pos        
                Label:  
                    id: label_2
                    text: root.hint_text_2
            
        BoxLayout: 
            canvas.before: 
                Color: 
                    rgba: 0, 0, 0, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
                    
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
        
        
    def on_parent(self, instance, value):
        self.bind(text = self.populate_rv)
        
    def populate_rv(self, instance, value):
        if self.text == self.default_text:
            
            self.parent.parent.parent.hint_text_1 = ''
            self.parent.parent.parent.hint_text_2 = ''
            return
        
        else: 
            
            if self.text == "Solvents":
                self.parent.parent.parent.hint_text_1 = "Solvent"
                self.parent.parent.parent.hint_text_2 = "Density"
                
            elif self.text == "Solutes":
                self.parent.parent.parent.hint_text_1 = "Material"
                self.parent.parent.parent.hint_text_2 = "Material"
                
            elif self.text == "Types":
                self.parent.parent.parent.hint_text_1 = "Solution Type"
                self.parent.parent.parent.hint_text_2 = "Solution Type"
            
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
                rgba: (.3, .3, .8, 1) if root.selected else (0.3, 0.3, 0.3, .5)
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
                rgba: (.3, .3, .8, 1) if root.selected else (0.3, 0.3, 0.3, .5)
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
"""Popups"""###################################################################
###############################################################################
    
class ErrorPopup(Popup):
    
    def __init__(self, **kwargs):
        super(ErrorPopup, self).__init__(**kwargs)
        self.title = "No category selected"
        self.layout = BoxLayout(orientation = 'vertical')
        self.label = Label(text = "Please select a category\nfrom the dropdown menu\nabove",
                           size_hint_y = 0.8)
        self.button = Button(text = "Ok", size_hint_y = 0.2)
        
        
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)
        
        
        self.content = self.layout
        
        self.button.bind(on_press = self.dismiss)

Builder.load_string("""
                    
<ErrorPopup>:
    size_hint: None, None
    size: dp(256), dp(256)

""")
    
class VerifyPopup(Popup):
    
    def __init__(self, data = None, **kwargs):
        super(VerifyPopup, self).__init__(**kwargs)
        self.data = data
        self.title = "Are you sure?"
        self.layout = BoxLayout(orientation = 'vertical')
        
        self.label = Label(text = "Are you sure you'd like\nto save your changes?",
                           size_hint_y = 0.8)
        
        self.buttons = BoxLayout(size_hint_y = 0.2)
        self.cancel = Button(text = "Cancel")
        self.verify = Button(text = "I'm sure")
        
        self.buttons.add_widget(self.cancel)
        self.buttons.add_widget(self.verify)
        
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.buttons)
        
        self.content = self.layout
        
        self.cancel.bind(on_press = self.dismiss)
        self.verify.bind(on_press = self.save)

    def save(self, instance):
        dumper(self.data)
        self.dismiss()
        
    
Builder.load_string("""
                    
<VerifyPopup>:
    size_hint: None, None
    size: dp(256), dp(256)

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