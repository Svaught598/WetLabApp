from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import (
    StringProperty, 
    ListProperty,
    BooleanProperty)

from models.solvent import Solvent

import string


class UpdateViewModel(EventDispatcher):
    
    error = StringProperty('')
    solvent_list = ListProperty()

    error_added = BooleanProperty()

    def add_solvent(self, context):
        print('solvent data added! ... not really though')
        if self.check_solvent(context):
            solvent = Solvent.create(
                name = context['name'],
                density = float(context['density']),
                formula = context['formula'],
                polarity = float(context['polarity']))
            solvent.save()
            self.error_added = False 
        self.get_solvents()

    def get_solvents(self):
        solvent_list = []
        for record in Solvent.select():
            solvent = {
                'name': str(record.name),
                'density': str(record.density),
                'formula': str(record.formula),
                'polarity': str(record.polarity)}
            solvent_list.append(solvent)
        self.solvent_list = solvent_list
            

    def check_solvent(self, context):
        for key in context:
            if context[key] == '':
                self.error = "One or more fields empty!"
                return False
        if float(context['density']) < 0:
            self.error = "Density must be positive!"
            return False
        elif float(context['polarity']) < 0:
            self.error = "Polarity must be positive!"
            return False
        for char in context['formula']:
            if char in string.whitespace:
                self.error = "Invalid chemical formula"
                return False
            elif char in string.punctuation:
                self.error = "Invalid chemcial formula"
                return False
        return True

    def add_material(self, context):
        print('material added! ... not really though')