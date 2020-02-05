import os 

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from screens import VolumeScreen, UpdateScreen, FilmThicknessScreen
from views.main_screen import MainScreen

from settings import TEMPLATE_PATHS

for path in TEMPLATE_PATHS:
    Builder.load_file(path)

class Manager(ScreenManager):
    """Screenmanager for all children screens"""
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.menu = MainScreen(name = 'menu')
        self.add_widget(self.menu)
        self.screen1 = VolumeScreen(name = 'volumeneeded')
        self.add_widget(self.screen1)
        self.screen2 = UpdateScreen(name = 'update')
        self.add_widget(self.screen2)
        self.screen3 = FilmThicknessScreen(name = 'thickness')
        self.add_widget(self.screen3)
        


class SolutionApp(App):
    
    def build(self):
        return Manager()

    
if __name__ == '__main__':
    SolutionApp().run()
