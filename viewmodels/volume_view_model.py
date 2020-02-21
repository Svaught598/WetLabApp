from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty, BooleanProperty

from models.solvent import Solvent
from models.material import Material
from settings import SOLUTION_TYPES, MASS_UNITS
from utils import convert_mass

class VolumeViewModel(EventDispatcher):

    __events__ = (
        ''
    )

    VOLUME = StringProperty()
    ERROR = BooleanProperty(False)

    SOLVENT_LIST = ListProperty([])
    MATERIAL_LIST = ListProperty([])

    def calculate(self, context):
        self.context = context
        if self.verify_fields() == False:
            self.ERROR = True
            return

        # Calculate for solution type 'Wt/Wt'
        if self.context["solution_type"] == SOLUTION_TYPES[0]:
            concentration = float(self.context['concentration'])
            mass = float(self.context['mass'])
            density = float(self.context['density'])
            self.VOLUME = str(round(((1 - concentration) * mass)/(concentration * density), 3)) + ' ml' 
            return  

        # Calculate for solution type 'mg/ml'
        if self.context["solution_type"] == SOLUTION_TYPES[1]:
            mass_units = self.context['mass_unit']
            concentration = float(self.context['concentration'])
            mass = float(self.context['mass'])
            mass = convert_mass(mass, mass_units, 'mg')
            self.VOLUME = str(round((mass/concentration), 3)) + 'ml'
            return

        # Calculate for solution type 'g/ml'
        if self.context["solution_type"] == SOLUTION_TYPES[2]:
            mass_units = self.context['mass_unit']
            concentration = float(self.context['concentration'])
            mass = float(self.context['mass'])
            mass = convert_mass(mass, mass_units, 'g')
            self.VOLUME = str(round((mass/concentration), 3)) + 'ml'
            return

    def verify_fields(self):
        solution_type = self.context["solution_type"]
        solvent = self.context["solvent"]
        material = self.context["material"]
        mass = self.context["mass"]
        concentration = self.context["concentration"]
        
        # must check for every situation
        if concentration == '':
            return False
        if mass == '':
            return False
        if solution_type == 'Solution Type':
            return False

        # this is '% wt/wt' solution
        if solution_type == SOLUTION_TYPES[0]:
            if solvent == 'Solvent':
                return False
            else:
                self.get_solvent_density()
            if float(concentration) > 1:
                return False
            if float(concentration) < 0:
                return False
            if float(mass) < 0:
                return False
        
        # this is 'mg/mL' solution
        elif solution_type == SOLUTION_TYPES[1]:
            if float(concentration) < 0:
                return False
            if float(mass) < 0:
                return False

        # this is 'g/mL' solution
        elif solution_type == SOLUTION_TYPES[2]:
            if float(concentration) < 0:
                return False
            if float(mass) < 0:
                return False

    def get_solvents(self):
        self.SOLVENT_LIST = Solvent.get_all()

    def get_materials(self):
        self.MATERIAL_LIST = Material.get_all()

    def get_solvent_density(self):
        solvent = Solvent.get_solvent(self.context['solvent'])
        density = solvent[0].density
        self.context.update({'density': density})

    def close_error(self):
        self.ERROR = False

# TODO: add more solution_types and logic.
# add conversion method for different solution types