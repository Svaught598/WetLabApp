import os 

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineAvatarListItem

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang.builder import Builder

from models import init_db
from views import VolumeScreen, UpdateScreen, FilmScreen
from viewmodels import VolumeViewModel, UpdateViewModel, FilmViewModel
from settings import TEMPLATE_PATHS, MAIN_TEMPLATE_PATH


class ContentNavigationDrawer(BoxLayout):
    pass


class NavigationItem(OneLineAvatarListItem):
    icon = StringProperty()


class SolutionApp(MDApp):
    '''When app the run() method is called, the following 
        methods are called in order:
        
        1. build()
        2. add_view_models()
        3. add_views()
        4. add_nav_drawer()
    '''
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
            ['Home', 'home-circle-outline', lambda x: self.get_main_screen()],
            ['Settings', 'settings-outline', lambda x:self.get_settings_screen()],
            ['About', 'lambda', lambda x: self.get_about_screen()],
            ['Developing', 'keyboard', lambda x: self.get_developing_screen()],
            ['Exit', 'exit-to-app', lambda x: self.exit_app()]
        ]
        for items in context:
            self.root.ids.content_drawer.ids.box_item.add_widget(
                NavigationItem(
                text=items[0],
                icon=items[1],
                on_press= items[2]))
        return 

    def get_main_screen(self):
        self.root.ids.screens.current = 'menu'
        return 'menu'

    def get_settings_screen(self):
        return 'settings'

    def get_about_screen(self):
        return 'about'

    def get_developing_screen(self):
        return 'development'

    def exit_app(self):
        return 'exit'

    def load_changes(self):
        self.MATERIALS = [
            {'viewclass': 'MDMenuItem',
            'text': 'MEH-PPV',
            'callback': self.screen1.on_material},
            {'viewclass': 'MDMenuItem',
            'text': 'BDMO-PPV',
            'callback': self.screen1.on_material}]
    
if __name__ == '__main__':
    init_db()
    SolutionApp().run()
