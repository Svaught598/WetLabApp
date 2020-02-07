from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty, NumericProperty

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

    solvents = ListProperty([])
    volume_needed = NumericProperty()
    error = StringProperty()

    def calculate(self, context):
        '''calculates volume needed based on view events
        
        context is a dict of key-value pairs
        '''
        return
        if self.verify(context):
            if context["type_concentration"] == '%Wt/Wt':
                # TODO write function to do this
                return volume_needed
            elif context["type_concentration"] == '%Wt/V':
                # TODO write function to do this
                return volume_needed
        else:
            self.error_check_fields() # TODO write this function
        
    
