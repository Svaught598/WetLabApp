from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.metrics import dp

from kivymd.uix.button import MDTextButton
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp

from models.solvent import Solvent

# class SolventViewClass(Label):
#     pass


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

        # Binding view_model properties to view events
        app = MDApp.get_running_app()
        app.update_view_model.bind(
            error = lambda x, y: self.error_popup(y),
            solvent_list = lambda x, y: self.refresh_solvent_rv(y)
        ) 
        app.update_view_model.get_solvents()

    def refresh_solvent_rv(self, solvent_list):
        # for tab in self.ids.update_tabs.ids.scrollview.children[0].children:
        #     if tab.state == 'down':
        #         tab.

    def error_popup(self, error):
        screen = self.manager.current_screen
        screen.error_popup(error)

    def plus_button_pressed(self):
        # Screen manager navigation to appropriate 'new item' screen
        for tab in self.ids.update_tabs.ids.scrollview.children[0].children:
            if tab.state == 'down':
                self.manager.current = tab.text

    def exit(self):
        # remove screens when leaving
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

    def submit(self):
        app = MDApp.get_running_app()
        app.update_view_model.add_solvent({
            'name': self.ids.name.text,
            'density': self.ids.density.text,
            'formula': self.ids.formula.text,
            'polarity': self.ids.polarity.text,})

    def error_popup(self, error):
        self.dialog = MDDialog(
            title = 'Error',
            text = error,
            size_hint = (0.8, None),
            height = dp(200))
        self.dialog.open()


class NewMaterialScreen(Screen):
    
    def back(self):
        app = MDApp.get_running_app()
        app.root.ids.screens.current = 'update'


class SolventTab(BoxLayout, MDTabsBase):
    pass


class MaterialTab(BoxLayout, MDTabsBase):
    name = 'new_Materials'
    pass


        
# TODO: find way to push data to RV. trouble is in finding
# a way to reference the RV from the parent screen.
# probably need to bind a few properties to transport the data.
# sucks, but that seems to be the only way.