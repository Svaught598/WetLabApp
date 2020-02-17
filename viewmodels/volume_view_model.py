from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty

from models.solvent import Solvent
from models.material import Material
from settings import SOLUTION_TYPES

class VolumeViewModel(EventDispatcher):

    __events__ = (
        ''
    )

    solvents = ListProperty([])
    volume_needed = StringProperty()
    error = StringProperty()

    solvent_list = ListProperty([])
    material_list = ListProperty([])

    def calculate(self, context):
        self.context = context
        if self.verify_fields() == False:
            return

        if self.context["solution_type"] == '% Wt/Wt':
            concentration = float(self.context['concentration'])
            mass = float(self.context['mass'])
            density = float(self.context['density'])
            self.volume_needed = str(round(((1 - concentration) * mass)/(concentration * density), 3)) + ' ml' 
            return  

        if self.context["solution_type"] == '% Wt/Vol':
            concentration = float(self.context['concentration'])
            mass = float(self.context['mass'])
            self.volume_needed = str(round((mass/concentration), 3)) + 'ml'
            return

    def verify_fields(self):
        error_message = ''
        solution_type = self.context["solution_type"]
        solvent = self.context["solvent"]
        material = self.context["material"]
        mass = self.context["mass"]
        concentration = self.context["concentration"]
        
        # must check for every situation
        if concentration == '':
            error_message += 'Concentration field is blank!\n'
        if mass == '':
            error_message += 'Mass field is blank\n'
        if solution_type == 'Solution Type':
            error_message += 'Choose a Solution Type\n'
            return self.verify_error(error_message)

        # this is '% wt/wt' solution
        if solution_type == SOLUTION_TYPES[0]:
            if solvent == 'Solvent':
                error_message += 'Choose a Solvent!\n'
            else:
                self.get_solvent_density()
            if float(concentration) > 1:
                error_message += 'Concentration must be less than 1\n'
            if float(concentration) < 0:
                error_message += 'Concentration must be greater than 0\n'
            if float(mass) < 0:
                error_message += 'Mass must be greater than 0\n'
            return self.verify_error(error_message)
        
        # this is '% wt/vol' solution
        elif solution_type == SOLUTION_TYPES[1]:
            if float(concentration) > 1:
                error_message += 'Concentration must be less than 1\n'
            if float(concentration) < 0:
                error_message += 'Concentration must be greater than 0\n'
            if float(mass) < 0:
                error_message += 'Mass must be greater than 0\n'
            return self.verify_error(error_message)
        
    def verify_error(self, message):
        if message == '':
            return True
        else:
            self.error = message
            return False

    def get_solvents(self):
        self.solvent_list = Solvent.get_all()

    def get_materials(self):
        self.material_list = Material.get_all()

    def get_solvent_density(self):
        solvent = Solvent.get_solvent(self.context['solvent'])
        density = solvent[0].density
        self.context.update({'density': density})

# TODO: add more solution_types and logic.
# add conversion method for different solution types