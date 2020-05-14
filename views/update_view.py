# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.metrics import dp

# KivyMD imports
from kivymd.uix.button import MDTextButton, MDRectangleFlatButton, MDFlatButton
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.boxlayout import MDBoxLayout

# Local imports
from models.solvent import Solvent
from models.material import Material



class Container(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


class UpdateScreen(Screen):

    # INformation pulled from Database
    SOLVENT_LIST = ListProperty([])
    MATERIAL_LIST = ListProperty([])

    def __init__(self, *args, **kwargs):
        super(UpdateScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)
    
    def prepare(self):
        """
        Bindings to corresponding viewmodel properties
        and initialization of widget
        """
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
        screen = UpdateSolventScreen(name = 'update_Solvents')
        self.manager.add_widget(screen)
        screen = UpdateMaterialScreen(name = 'update_Materials')
        self.manager.add_widget(screen)

        # Binding view_model properties to view events
        app = MDApp.get_running_app()
        app.update_view_model.bind(
            ERROR_MSG = lambda x, y: self.error_popup(y),

            SOLVENT_LIST = lambda x, y: self.refresh_solvent_rv(y),
            MATERIAL_LIST = lambda x, y: self.refresh_material_rv(y)
        ) 

        # Populate recycleview from database through viewmodel
        app.update_view_model.get_solvents()
        app.update_view_model.get_materials()

    def refresh_solvent_rv(self, solvent_list):
        """helper method bound to viewmodel property"""
        self.SOLVENT_LIST = solvent_list

    def refresh_material_rv(self, material_list):
        """helper method bound to viewmodel property"""
        self.MATERIAL_LIST = material_list

    def error_popup(self, error):
        """
        helper method bound to viewmodel property
        passes error-message to pertinent screen
        """
        screen = self.manager.current_screen
        screen.error_popup(error)

    def plus_button_pressed(self):
        """
        navigates to appropriate 'new item' screen by checking the state 
        of each tabbed item in the view. 
        
        The screen associated with 
        new solvent entry is called 'Solvent' and etc...
        """
        self.manager.transition.direction = 'left'
        for tab in self.ids.update_tabs.ids.scrollview.children[0].children:
            if tab.state == 'down':
                self.manager.current = tab.text

    def edit(self, context):
        self.manager.transition.direction = 'left'
        for tab in self.ids.update_tabs.ids.scrollview.children[0].children:
            if tab.state == 'down':
                screen_name = "update_" + tab.text
                screen = self.manager.get_screen(screen_name)
                for key in context:
                    setattr(screen, key, context[key])
                self.manager.current = screen_name

    def exit(self):
        """remove screens when leaving"""
        for screen in self.manager.children:
            if screen.name == 'Solvents':
                self.manager.remove_widget(screen)
            if screen.name == 'Materials':
                self.manager.remove_widget(screen)
        app = MDApp.get_running_app()
        app.get_main_screen()


class NewSolventScreen(Screen):

    # property bound to 'IS_ERROR' in viewmodel
    is_error = BooleanProperty()

    def __init__(self, *args, **kwargs):
        super(NewSolventScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self):
        """Bindings to corresponding viewmodel properties"""
        app = MDApp.get_running_app()
        app.update_view_model.bind(
            IS_ERROR = lambda x, y: self.change_error(y)
        )

    def change_error(self, is_error):
        """changes class 'is_error' to reflect viewmodel"""
        self.is_error = is_error

    def check_error(self):
        """
        checks is_error to determine whether to switch screens
        """
        if self.is_error == True:
            return
        else:
            self.back()

    def back(self):
        """navigates back to main update view screen"""
        app = MDApp.get_running_app()
        app.root.ids.screens.transition.direction = 'right'
        app.root.ids.screens.current = 'update'

    def on_leave(self):
        """clears inputs upon leaving screen"""
        self.ids.name.text = ''
        self.ids.density.text = ''
        self.ids.formula.text = ''
        self.ids.polarity.text = ''

    def submit(self):
        """sends inputs to viewmodel method to add solvent to database"""
        app = MDApp.get_running_app()
        app.update_view_model.add_solvent({
            'name': self.ids.name.text,
            'density': self.ids.density.text,
            'formula': self.ids.formula.text,
            'polarity': self.ids.polarity.text,})
        self.check_error()

    def error_popup(self, error):
        """Displays error message (if any)"""
        if error == '':
            return 
        else:
            self.dialog = MDDialog(
                title = 'Error',
                text = error,
                size_hint = (0.8, None),
                height = dp(200))
            self.dialog.open()

            # Change error message back to ""
            app = MDApp.get_running_app()
            app.update_view_model.ERROR_MSG = ''


class NewMaterialScreen(Screen):

    # Property bound to IS_ERROR in viewmodel
    is_error = BooleanProperty()

    # Other properties for editting entries
    material_name = StringProperty('')
    formula = StringProperty('')
    molecular_weight = StringProperty('')
    density = StringProperty('')

    def __init__(self, *args, **kwargs):
        super(NewMaterialScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self):
        """Bindings to corresponding viewmodel properties"""
        app = MDApp.get_running_app()
        app.update_view_model.bind(
            IS_ERROR = lambda x, y: self.change_error(y)
        )

    def change_error(self, is_error):
        """changes class 'is_error' to reflect viewmodel"""
        self.is_error = is_error

    def check_error(self):
        """
        checks is_error to determine whether to switch screens
        """
        if self.is_error == True:
            return
        else:
            self.back()

    def back(self):
        """navigates back to main update view screen"""
        app = MDApp.get_running_app()
        app.root.ids.screens.transition.direction = 'right'
        app.root.ids.screens.current = 'update'

    def on_leave(self):
        """clears all user input upon leaving screen"""
        self.ids.name.text = ''
        self.ids.formula.text = ''
        self.ids.molecular_weight.text = ''

    def submit(self):
        """sends inputs to viewmodel method to add material to database"""
        app = MDApp.get_running_app()
        app.update_view_model.add_material({
            'name': self.ids.name.text,
            'formula': self.ids.formula.text,
            'molecular_weight': self.ids.molecular_weight.text,
            'density': self.ids.density.text})
        self.check_error()

    def error_popup(self, error):
        """Displays error message (if any)"""
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
        """bindings to corresponding viewmodel properties"""
        app = MDApp.get_running_app()
        update_screen = app.root.ids.screens.get_screen(name = 'update')
        self.refresh_rv(update_screen.SOLVENT_LIST)
        update_screen.bind(
            SOLVENT_LIST = lambda inst, data: self.refresh_rv(data)
        )
        
    def refresh_rv(self, data):
        """updates data in recycleview"""
        self.ids.solvent_rv.data = data


class MaterialTab(BoxLayout, MDTabsBase):
    def __init__(self, *args, **kwargs):
        super(MaterialTab, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self, *args, **kwargs):
        """bindings to corresponding viewmodel properties"""
        app = MDApp.get_running_app()
        update_screen = app.root.ids.screens.get_screen(name = 'update')
        self.refresh_rv(update_screen.MATERIAL_LIST)
        update_screen.bind(
            MATERIAL_LIST = lambda inst, data: self.refresh_rv(data)
        )

    def refresh_rv(self, data):
        """updates data in recycleview"""
        self.ids.solvent_rv.data = data


class ButtonViewClass(OneLineAvatarIconListItem):

    # Class level constants
    CONFIRM = StringProperty('Yes')
    CANCEL = StringProperty('Maybe not...')

    # Nonetype if material, else Solvent
    polarity = None

    # Name of the solvent/material 
    name = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids._right_container.width = self.ids.container.width

    def delete_solvent(self):
        """calls viewmodel method to delete entry from database"""
        app = MDApp.get_running_app()
        app.update_view_model.delete_solvent(self.name)
        app.update_view_model.get_solvents()
        self.dialog.dismiss()

    def delete_material(self):
        """calls viewmodel method to delete entry from database"""
        app = MDApp.get_running_app()
        app.update_view_model.delete_material(self.name)
        app.update_view_model.get_materials()
        self.dialog.dismiss()

    def confirm_popup(self):
        """popup to confirm deletion of solvent/material"""
        self.dialog = MDDialog(
            title = 'Are you sure?',
            text = 'You are about to permanently delete this item. Continue?',
            type = 'confirmation',
            buttons = [
                MDFlatButton(
                    text = self.CANCEL, 
                    text_color = self.theme_cls.primary_color,
                    on_release = lambda x: self.dialog.dismiss()
                ),
                MDRectangleFlatButton(
                    text = self.CONFIRM,
                    text_color = self.theme_cls.primary_color,
                    on_release = lambda x: self.delete_solvent() if self.polarity else self.delete_material()
                ),
            ]
        )
        self.dialog.open()

    def edit(self):
        """Takes solvent/material & opens information to be editted"""
        if self.polarity == None:
            record = Material.get_material(self.name)
        else: 
            record = Solvent.get_solvent(self.name)
        app = MDApp.get_running_app()
        app.root.ids.screens.get_screen('update').edit(record)

    def handle_dialog(self, choice, inst):
        """helper method to handle dialog choice"""
        if choice == self.CONFIRM:
            self.delete_solvent() if self.polarity else self.delete_material()
        elif choice == self.CANCEL:
            return 


class UpdateMaterialScreen(Screen):

    # Property bound to IS_ERROR in viewmodel
    is_error = BooleanProperty()

    # Other properties for editting entries
    material_name = StringProperty('')
    formula = StringProperty('')
    molecular_weight = StringProperty('')
    density = StringProperty('')

    def __init__(self, *args, **kwargs):
        super(UpdateMaterialScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self):
        """Bindings to corresponding viewmodel properties"""
        app = MDApp.get_running_app()
        app.update_view_model.bind(
            IS_ERROR = lambda x, y: self.change_error(y)
        )

    def change_error(self, is_error):
        """changes class 'is_error' to reflect viewmodel"""
        self.is_error = is_error

    def check_error(self):
        """
        checks is_error to determine whether to switch screens
        """
        if self.is_error == True:
            return
        else:
            self.back()

    def back(self):
        """navigates back to main update view screen"""
        app = MDApp.get_running_app()
        app.root.ids.screens.transition.direction = 'right'
        app.root.ids.screens.current = 'update'

    def on_leave(self):
        """clears all user input upon leaving screen"""
        self.ids.name.text = ''
        self.ids.formula.text = ''
        self.ids.molecular_weight.text = ''

    def submit(self):
        """sends inputs to viewmodel method to add material to database"""
        app = MDApp.get_running_app()
        app.update_view_model.update_material({
            'name': self.ids.name.text,
            'formula': self.ids.formula.text,
            'molecular_weight': self.ids.molecular_weight.text,
            'density': self.ids.density.text})
        self.check_error()

    def error_popup(self, error):
        """Displays error message (if any)"""
        self.dialog = MDDialog(
            title = 'Error',
            text = error,
            size_hint = (0.8, None),
            height = dp(200))
        self.dialog.open()

class UpdateSolventScreen(Screen):

    # Property bound to IS_ERROR in viewmodel
    is_error = BooleanProperty()

    # Other properties for editting entries
    solvent_name = StringProperty('')
    formula = StringProperty('')
    polarity = StringProperty('')
    density = StringProperty('')

    def __init__(self, *args, **kwargs):
        super(UpdateSolventScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.prepare(), 0)

    def prepare(self):
        """Bindings to corresponding viewmodel properties"""
        app = MDApp.get_running_app()
        app.update_view_model.bind(
            IS_ERROR = lambda x, y: self.change_error(y)
        )

    def change_error(self, is_error):
        """changes class 'is_error' to reflect viewmodel"""
        self.is_error = is_error

    def check_error(self):
        """
        checks is_error to determine whether to switch screens
        """
        if self.is_error == True:
            return
        else:
            self.back()

    def back(self):
        """navigates back to main update view screen"""
        app = MDApp.get_running_app()
        app.root.ids.screens.transition.direction = 'right'
        app.root.ids.screens.current = 'update'

    def submit(self):
        """sends inputs to viewmodel method to add solvent to database"""
        app = MDApp.get_running_app()
        app.update_view_model.update_solvent({
            'name': self.ids.name.text,
            'density': self.ids.density.text,
            'formula': self.ids.formula.text,
            'polarity': self.ids.polarity.text,})
        self.check_error()

    def error_popup(self, error):
        """Displays error message (if any)"""
        if error == '':
            return 
        else:
            self.dialog = MDDialog(
                title = 'Error',
                text = error,
                size_hint = (0.8, None),
                height = dp(200))
            self.dialog.open()

            # Change error message back to ""
            app = MDApp.get_running_app()
            app.update_view_model.ERROR_MSG = ''
