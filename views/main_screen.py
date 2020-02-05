import os

from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.clock import Clock


class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.start(), 0)
        
    def start(self):
        self.name = 'menu'
        
