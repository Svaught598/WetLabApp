from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock

from kivymd.uix.button import MDTextButton
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.app import MDApp

from models.solvent import Solvent


class UpdateScreen(Screen):
    
    solvents = StringProperty('')

    def __init__(self, *args, **kwargs):
        super(UpdateScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)
    
    def prepare(self):
        # Adding tabs to screen
        tab = SolventTab(text = 'Solvents')
        self.ids.update_tabs.add_widget(tab)
        tab = MaterialTab(text = 'Materials')
        self.ids.update_tabs.add_widget(tab)

        # Adding Subscreens to screenmanager
        screen = NewSolventScreen(name = 'Solvents')
        self.manager.add_widget(screen)
        screen = NewMaterialScreen(name = 'Materials')
        self.manager.add_widget(screen)

        app = MDApp.get_running_app()
        app.update_view_model.bind() 
        # TODO: bind view_model properties to view events above

    def plus_button_pressed(self):
        for tab in self.ids.update_tabs.ids.scrollview.children[0].children:
            if tab.state == 'down':
                self.manager.current = tab.text

    def on_exit(self):
        for screen in self.manager.children:
            if screen.name == 'Solvents':
                self.manager.remove_widget(screen)
            if screen.name == 'Materials':
                self.manager.remove_widget(screen)
        app = MDApp.get_running_app()
        app.get_main_screen()


class NewSolventScreen(Screen):

    def back(self):
        app = MDApp.get_running_app()
        app.root.ids.screens.current = 'update'

class NewMaterialScreen(Screen):
    
    def back(self):
        app = MDApp.get_running_app()
        app.root.ids.screens.current = 'update'


class SolventTab(BoxLayout, MDTabsBase):
    pass


class MaterialTab(BoxLayout, MDTabsBase):
    name = 'new_Materials'
    pass
