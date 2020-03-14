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
    
    # Properties that have to do with handling user input errors
    ERROR_MSG = StringProperty('')
    IS_ERROR = BooleanProperty()

    # Properties that store information from database queries
    SOLVENT_LIST = ListProperty([])
    MATERIAL_LIST = ListProperty([])

    def add_solvent(self, context):
        """method that attempts to add a solvent to the database"""
        is_error = self.check_solvent(context)
        if is_error:
            self.IS_ERROR = True
            return
        try:
            solvent = Solvent.create(
                name = context['name'],
                density = float(context['density']),
                formula = context['formula'],
                polarity = float(context['polarity']))
            solvent.save()
            self.IS_ERROR = False 
            self.get_solvents()
        except IntegrityError:
            self.ERROR_MSG = 'This Solvent is already in the system!'
            self.IS_ERROR = True

    def add_material(self, context):
        """method that attempts to add a material to the database"""
        is_error = self.check_material(context)
        if is_error:
            self.IS_ERROR = True
            return
        try:
            material = Material.create(
                name = context['name'],
                formula = context['formula'],
                molecular_weight = context['molecular_weight'],
                density = context['density'])
            material.save()
            self.IS_ERROR = False
            self.get_materials()
        except IntegrityError:
            self.ERROR_MSG = 'This Material is already in the system!'
            self.IS_ERROR = True

    def get_solvents(self):
        """method that gets all solvents from database"""
        self.SOLVENT_LIST = Solvent.get_all()

    def get_materials(self):
        """method that gets all materials from database"""
        self.MATERIAL_LIST = Material.get_all()
            
    def check_solvent(self, context):
        """
        helper method that checks validity of user inputs
        
        returns:
            - True if there is an error
            - False if there is no error
        """
        for key in context:
            if context[key] == '':
                self.ERROR_MSG = "One or more fields empty!"
                return True
        for char in context['formula']:
            if (char in string.whitespace) or (char in string.punctuation):
                self.ERROR_MSG = "Invalid chemical formula"
                return True
        if float(context['density']) < 0:
            self.ERROR_MSG = "Density must be positive!"
            return True
        if float(context['polarity']) < 0:
            self.ERROR_MSG = "Polarity must be positive!"
            return True
        return False

    def check_material(self, context):
        """
        helper method that checks validity of user inputs
        
        returns;
            - True if there is an error
            - False if there is no error
        """
        for key in context:
            if context[key] == '':
                self.ERROR_MSG = 'One or more fields empty!'
                return True
        for char in context['formula']:
            if (char in string.whitespace) or (char in string.punctuation):
                self.ERROR_MSG = 'Invalid chemical formula'
                return True
        if float(context['molecular_weight']) < 0:
            self.ERROR_MSG = "Molecular weight must be positive!"
            return True
        if float(context['density']) < 0:
            self.ERROR_MSG =  "Density must be positive!"
            return True
        return False

    def delete_solvent(self, name):
        """method that deletes selected solvent from database"""
        Solvent.delete_solvent(name)
        self.get_solvents()
    
    def delete_material(self, name):
        """method that deletes selected material from database"""
        Material.delete_material(name)
        self.get_materials()
