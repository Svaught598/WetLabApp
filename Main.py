# KivyMD imports
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineAvatarListItem

# Kivy imports
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang.builder import Builder

# Local imports
from models import init_db
from views import (
    VolumeScreen,
    UpdateScreen,
    FilmScreen,
    AboutScreen,
    DevelopingScreen,
    DilutionScreen,
)
from viewmodels import (
    VolumeViewModel,
    UpdateViewModel,
    FilmViewModel,
    DilutionViewModel,
)
from settings import TEMPLATE_PATHS, MAIN_TEMPLATE_PATH


class ContentNavigationDrawer(BoxLayout):
    """
    Empty class for custom .kv structure

    markup in 'navigation_drawer.kv' in templates directory
    """
    pass


class NavigationItem(OneLineAvatarListItem):
    """
    Empty class for custom .kv structure
    
    markup in 'navigation_drawer.kv' in templates directory
    """
    icon = StringProperty()


class SolutionApp(MDApp):
    """
    When app the run() method is called, the following 
    methods are called in this order:
        
        1. build()
        2. add_view_models()
        3. add_views()
        4. add_nav_drawer()

    The templates & viewmodels are reference in the views, 
    so it is imperative that they are constructed first. 
    changing order of template builds and viewmodel instantiation
    shouldn't affect anything, since those layers don't communicate directly

    The return statement of the 'build' method triggers the 'on_start' 
    method by default through kivy internals.
    """
    def build(self):
        for path in TEMPLATE_PATHS:
            Builder.load_file(path)
        return Builder.load_file(MAIN_TEMPLATE_PATH)

    def on_start(self):
        self.add_view_models()
        self.add_views()
        self.add_nav_drawer()

    def add_views(self):
        """adding screens to widget tree"""
        self.screen1 = VolumeScreen(name = 'volumeneeded')
        self.root.ids.screens.add_widget(self.screen1)
        self.screen2 = UpdateScreen(name = 'update')
        self.root.ids.screens.add_widget(self.screen2)
        self.screen3 = FilmScreen(name = 'thickness')
        self.root.ids.screens.add_widget(self.screen3)
        self.screen4 = DilutionScreen(name = 'dilution')
        self.root.ids.screens.add_widget(self.screen4)

        """adding nav drawer screens"""
        self.root.ids.screens.add_widget(AboutScreen(name = 'about'))
        self.root.ids.screens.add_widget(DevelopingScreen(name = 'developing'))

    def add_view_models(self):
        """
        addding viewmodels to app directly, so that 
        they are easily usable. no need for overly verbose calling 
        in views like:

        viewmodel = self.manager.parent.ids.root.ids.something.somethingelse.ids.bullshit.and.finally.viewmodel
        viewmodel.do_stuff()
        """
        self.volume_view_model = VolumeViewModel()
        self.update_view_model = UpdateViewModel()
        self.film_view_model = FilmViewModel()
        self.dilution_view_model = DilutionViewModel()

    def add_nav_drawer(self):
        """
        populates the navigation drawer on the side and declares the function to 
        be called when the object is selected.
        """
        context = [
            ['Home', 'home-circle-outline', lambda x: self.get_main_screen()],
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
        self.root.ids.screens.transition.direction = 'right'
        self.root.ids.screens.current = 'menu'

    def get_about_screen(self):
        self.root.ids.screens.transition.direction = 'left'
        self.root.ids.screens.current = 'about'
        self.root.ids.nav_drawer.toggle_nav_drawer()

    def get_developing_screen(self):
        self.root.ids.screens.transition.direction = 'left'
        self.root.ids.screens.current = 'developing'
        self.root.ids.nav_drawer.toggle_nav_drawer()

    def solvent_refresh(self):
        """
        calls all 'get_solvents' methods from
        each viewmodel to reflect changes in database
        """
        self.volume_view_model.get_solvents()
        self.update_view_model.get_solvents()
        self.film_view_model.get_solvents()

    def material_refresh(self):
        """
        calls all 'get_materials' methods from
        each viewmodel to reflect changes in database
        """
        self.volume_view_model.get_materials()
        self.update_view_model.get_materials()
        self.film_view_model.get_materials()

    def exit_app(self):
        """
        called by kivy when the app closes. I have 
        it here in case I need that functionality at some point
        since i'm sure I won't remember which method name to use
        """
        return 'exit'

"""Starting the application but first initializing the database"""
if __name__ == '__main__':
    init_db()
    SolutionApp().run()
