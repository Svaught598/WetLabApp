# STandard Lib imports
import string

# kivy imports
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import (
    StringProperty, 
    ListProperty,
    BooleanProperty)

# peewee imports
from peewee import IntegrityError

# local imports
from models.solvent import Solvent
from models.material import Material


class UpdateViewModel(EventDispatcher):
    
    error = StringProperty('')
    solvent_list = ListProperty([])
    material_list = ListProperty([])

    error_added = BooleanProperty()

    def add_solvent(self, context):
        if self.check_solvent(context) == False:
            return
        try:
            solvent = Solvent.create(
                name = context['name'],
                density = float(context['density']),
                formula = context['formula'],
                polarity = float(context['polarity']))
            solvent.save()
            self.error_added = False 
            self.get_solvents()
        except IntegrityError:
            self.error = 'This Solvent is already in the system!'
            self.error_added = True

    def add_material(self, context):
        if self.check_material(context) == False:
            return
        try:
            material = Material.create(
                name = context['name'],
                formula = context['formula'],
                molecular_weight = context['molecular_weight'],
                density = context['density'])
            material.save()
            self.error_added = False
            self.get_materials()
        except IntegrityError:
            self.error = 'This Material is already in the system!'
            self.error_added = True

    def get_solvents(self):
        self.solvent_list = Solvent.get_all()

    def get_materials(self):
        self.material_list = Material.get_all()
            
    def check_solvent(self, context):
        for key in context:
            if context[key] == '':
                self.error = "One or more fields empty!"
                return False
        for char in context['formula']:
            if (char in string.whitespace) or (char in string.punctuation):
                self.error = "Invalid chemical formula"
                return False
        if float(context['density']) < 0:
            self.error = "Density must be positive!"
            return False
        if float(context['polarity']) < 0:
            self.error = "Polarity must be positive!"
            return False
        return True

    def check_material(self, context):
        for key in context:
            if context[key] == '':
                self.error = 'One or more fields empty!'
                return False
        for char in context['formula']:
            if (char in string.whitespace) or (char in string.punctuation):
                self.error = 'Invalid chemical formula'
                return False
        if float(context['molecular_weight']) < 0:
            self.error = "Molecular weight must be positive!"
            return False
        if float(context['density']) < 0:
            self.error =  "Density must be positive!"
            return False
        return True

    def delete_solvent(self, name):
        Solvent.delete_solvent(name)
        self.get_solvents()
    
    def delete_material(self, name):
        Material.delete_material(name)
        self.get_materials()
