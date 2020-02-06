from pprint import pprint

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

from customwidgets import DropDownMenu
from utils import loader, dumper


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


class SelectableRecycleBoxLayout(FocusBehavior, 
                                 LayoutSelectionBehavior, 
                                 RecycleBoxLayout):
    pass


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
    
