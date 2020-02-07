from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import StringProperty

from models.solvent import Solvent


class VolumeViewModel(EventDispatcher):
    type_concentration = StringProperty('')
    solvent = StringProperty('')
    material = StringProperty('')
    mass = StringProperty('')
    concentration = StringProperty('')
    density = StringProperty('')
    volume = StringProperty('')

    __events__ = (
        ''
    )

    def calculate(self, context):
        '''calculates volume needed based on view events
        
        context is a dict of key-value pairs
        '''
        if self.verify(context):
            if context["type_concentration"] == '%Wt/Wt':
                # TODO write function to do this
                return volume_needed
            elif context["type_concentration"] == '%Wt/V':
                # TODO write function to do this
                return volume_needed
        else:
            self.error_check_fields() # TODO write this function
        
    def on_solution_type(self, solution_type):
        '''watches for changes in solutions dropdown'''
        pass

    def on_solvent(self, solvent):
        '''watches for changes in solvents dropdown'''
        pass

    def on_material(self, material):
        '''watches for changes in materials dropdown'''
        pass

    def on_concentration(self, concentration):
        '''watches for changes in concentration input'''
        pass

    def on_mass(self, mass):
        '''watches for changes in mass input'''
        pass
