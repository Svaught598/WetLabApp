from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.metrics import dp

from kivymd.uix.button import MDTextButton, MDRectangleFlatButton
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp

from models.solvent import Solvent


class UpdateScreen(Screen):
    solvent_list = ListProperty([])
    material_list = ListProperty([])

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

            solvent_list = lambda x, y: self.refresh_solvent_rv(y),
            material_list = lambda x, y: self.refresh_material_rv(y)
        ) 
        app.update_view_model.get_solvents()
        app.update_view_model.get_materials()

    def refresh_solvent_rv(self, solvent_list):
        self.solvent_list = solvent_list

    def refresh_material_rv(self, material_list):
        self.material_list = material_list

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
    def __init__(self, *args, **kwargs):
        super(NewSolventScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self):
        app = MDApp.get_running_app()
        app.update_view_model.bind(
            error_added = lambda x, y: self.error_added(y))

    def error_added(self, error_bool):
        if error_bool == True:
            return
        else:
            self.back()

    def back(self):
        app = MDApp.get_running_app()
        app.root.ids.screens.current = 'update'

    def on_leave(self):
        self.ids.name.text = ''
        self.ids.density.text = ''
        self.ids.formula.text = ''
        self.ids.polarity.text = ''

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
    def __init__(self, *args, **kwargs):
        super(NewMaterialScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self):
        app = MDApp.get_running_app()
        app.update_view_model.bind(
            error_added = lambda x, y: self.error_added(y))

    def error_added(self, error_bool):
        if error_bool == True:
            return
        else:
            self.back()

    def back(self):
        app = MDApp.get_running_app()
        app.root.ids.screens.current = 'update'

    def on_leave(self):
        self.ids.name.text = ''
        self.ids.formula.text = ''
        self.ids.molecular_weight.text = ''

    def submit(self):
        app = MDApp.get_running_app()
        app.update_view_model.add_material({
            'name': self.ids.name.text,
            'formula': self.ids.formula.text,
            'molecular_weight': self.ids.molecular_weight.text,})

    def error_popup(self, error):
        self.dialog = MDDialog(
            title = 'Error',
            text = error,
            size_hint = (0.8, None),
            height = dp(200))
        self.dialog.open()


class SolventTab(BoxLayout, MDTabsBase):
    def __init__(self, *args, **kwargs):
        super(SolventTab, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self):
        app = MDApp.get_running_app()
        update_screen = app.root.ids.screens.get_screen(name = 'update')
        self.refresh_rv(update_screen.solvent_list)
        update_screen.bind(
            solvent_list = lambda inst, data: self.refresh_rv(data)
        )
        
    def refresh_rv(self, data):
        self.ids.solvent_rv.data = data


class MaterialTab(BoxLayout, MDTabsBase):
    def __init__(self, *args, **kwargs):
        super(MaterialTab, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self, *args, **kwargs):
        app = MDApp.get_running_app()
        update_screen = app.root.ids.screens.get_screen(name = 'update')
        self.refresh_rv(update_screen.material_list)
        update_screen.bind(
            material_list = lambda inst, data: self.refresh_rv(data)
        )

    def refresh_rv(self, data):
        self.ids.solvent_rv.data = data


class ButtonViewClass(BoxLayout):
    name = StringProperty('')
    polarity = None

    def delete_solvent(self):
        app = MDApp.get_running_app()
        app.update_view_model.delete_solvent(self.name)

    def delete_material(self):
        app = MDApp.get_running_app()
        app.update_view_model.delete_material(self.name)