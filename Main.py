import os 

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineAvatarListItem

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang.builder import Builder

from views import VolumeScreen, UpdateScreen, FilmScreen
from viewmodels import VolumeViewModel, UpdateViewModel, FilmViewModel
from settings import TEMPLATE_PATHS, MAIN_TEMPLATE_PATH


class ContentNavigationDrawer(BoxLayout):
    pass


class NavigationItem(OneLineAvatarListItem):
    icon = StringProperty()


class SolutionApp(MDApp):
    
    def build(self):
        for path in TEMPLATE_PATHS:
            Builder.load_file(path)
        return Builder.load_file(MAIN_TEMPLATE_PATH)

    def on_start(self):
        self.add_view_models()
        self.add_views()
        self.add_nav_drawer()
        self.load_changes()

    def add_views(self):
        self.screen1 = VolumeScreen(name = 'volumeneeded')
        self.root.ids.screens.add_widget(self.screen1)
        self.screen2 = UpdateScreen(name = 'update')
        self.root.ids.screens.add_widget(self.screen2)
        self.screen3 = FilmScreen(name = 'thickness')
        self.root.ids.screens.add_widget(self.screen3)

    def add_view_models(self):
        self.volume_view_model = VolumeViewModel()
        self.update_view_model = UpdateViewModel()
        self.film_view_model = FilmViewModel()

    def add_nav_drawer(self):
        context = [
            ['Home', 'home-circle-outline', self.get_main_screen()],
            ['Settings', 'settings-outline', self.get_settings_screen()],
            ['About', 'lambda', self.get_about_screen()],
            ['Developing', 'keyboard', self.get_developing_screen()],
            ['Exit', 'exit-to-app', self.exit_app()]
        ]
        for items in context:
            print(items[2])
            self.root.ids.content_drawer.ids.box_item.add_widget(
                NavigationItem(
                text=items[0],
                icon=items[1],
                on_press= lambda x: items[2]))
        return 

    def get_main_screen(self):
        self.root.ids.screens.current = 'menu'
        return 

    def get_settings_screen(self):
        pass

    def get_about_screen(self):
        pass

    def get_developing_screen(self):
        pass

    def exit_app(self):
        pass

    def load_changes(self):
        self.SOLUTION_TYPES = [
            {'viewclass': 'MDMenuItem',
            'text': '% Wt/Wt',
            'callback': self.screen1.on_solution_types},
            {'viewclass': 'MDMenuItem',
            'text': '% Wt/Vol',
            'callback': self.screen1.on_solution_types}]
        self.SOLVENTS = [
            {'viewclass': 'MDMenuItem',
            'text': 'Chloroform',
            'callback': self.screen1.on_solvent},
            {'viewclass': 'MDMenuItem',
            'text': 'Toluene',
            'callback': self.screen1.on_solvent}]
        self.MATERIALS = [
            {'viewclass': 'MDMenuItem',
            'text': 'MEH-PPV',
            'callback': self.screen1.on_material},
            {'viewclass': 'MDMenuItem',
            'text': 'BDMO-PPV',
            'callback': self.screen1.on_material}]
    
if __name__ == '__main__':
    SolutionApp().run()
