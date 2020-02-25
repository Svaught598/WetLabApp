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
    SOLVENT_DENSITY = StringProperty('')
    MOLECULAR_WEIGHT = StringProperty('')
    ERROR = BooleanProperty(False)

    SOLVENT_LIST = ListProperty([])
    MATERIAL_LIST = ListProperty([])

    context = {}

    def calculate(self, context):
        self.context = context
        if self.verify_fields() == False:
            self.ERROR = True
            return

        # Calculate for solution type 'Wt/Wt'
        if self.context["solution_type"] == SOLUTION_TYPES[0]:
            concentration = float(self.context['concentration'])
            mass_units = self.context['mass_unit']
            mass = float(self.context['mass'])
            density = float(self.context['solvent_density'])
            mass = convert_mass(mass, mass_units, 'g')
            self.VOLUME = str(round(((1 - concentration) * mass)/(concentration * density), 3)) + ' ml' 
            return  

        # Calculate for solution type 'mg/ml'
        if self.context["solution_type"] == SOLUTION_TYPES[1]:
            mass_units = self.context['mass_unit']
            concentration = float(self.context['concentration'])
            mass = float(self.context['mass'])
            mass = convert_mass(mass, mass_units, 'mg')
            self.VOLUME = str(round((mass/concentration), 3)) + ' mL'
            return

        # Calculate for solution type 'g/ml'
        if self.context["solution_type"] == SOLUTION_TYPES[2]:
            mass_units = self.context['mass_unit']
            concentration = float(self.context['concentration'])
            mass = float(self.context['mass'])
            mass = convert_mass(mass, mass_units, 'g')
            self.VOLUME = str(round((mass/concentration), 3)) + ' mL'
            return

        # Calculate for solution type 'M'
        if self.context["solution_type"] == SOLUTION_TYPES[3]:
            mass_units = self.context['mass_unit']
            concentration = float(self.context['concentration'])
            mol_weight = float(self.context['mol_weight'])
            mass = float(self.context['mass'])
            mass = convert_mass(mass, mass_units, 'g')
            self.VOLUME = f'{mass/mol_weight/concentration*1.e3}' + ' mL'
            return 

        # Calculate for solution type 'mM'
        if self.context["solution_type"] == SOLUTION_TYPES[4]:
            mass_units = self.context['mass_unit']
            concentration = float(self.context['concentration'])
            mol_weight = float(self.context['mol_weight'])
            mass = float(self.context['mass'])
            mass = convert_mass(mass, mass_units, 'g')
            self.VOLUME = f'{mass/mol_weight/concentration}' + ' mL'
            return 

        # Calculate for solution type '\u03BCM'
        if self.context["solution_type"] == SOLUTION_TYPES[5]:
            mass_units = self.context['mass_unit']
            concentration = float(self.context['concentration'])
            mol_weight = float(self.context['mol_weight'])
            mass = float(self.context['mass'])
            mass = convert_mass(mass, mass_units, 'g')
            self.VOLUME = f'{mass/mol_weight/concentration/1.e3}' + ' mL'
            return

        # Calculate for solution type 'nM'
        if self.context["solution_type"] == SOLUTION_TYPES[6]:
            mass_units = self.context['mass_unit']
            concentration = float(self.context['concentration'])
            mol_weight = float(self.context['mol_weight'])
            mass = float(self.context['mass'])
            mass = convert_mass(mass, mass_units, 'g')
            self.VOLUME = f'{mass/mol_weight/concentration/1.e6}' + ' mL'
            return

    def verify_fields(self):
        solution_type = self.context["solution_type"]
        material = self.context["material"]
        solvent = self.context["solvent"]
        mass = self.context["mass"]
        concentration = self.context["concentration"]
        mol_weight = self.context["mol_weight"]
        density = self.context["solvent_density"]
        
        # must check for every situation
        if concentration == '':
            return False
        if mass == '':
            return False
        if solution_type == 'Solution Type':
            return False

        # this is '% wt/wt' solution
        if solution_type == SOLUTION_TYPES[0]:
            if (density == '' and solvent == 'Solvent'):
                return False
            elif (density == ''):
                self.get_solvent_density(solvent)
                self.context.update({'solvent_density': self.SOLVENT_DENSITY})
            if float(concentration) > 1:
                return False
            if float(concentration) < 0:
                return False
            if float(mass) < 0:
                return False
        
        # this is 'mg/mL' & 'g/mL' solution
        elif any([
                solution_type == SOLUTION_TYPES[1],
                solution_type == SOLUTION_TYPES[2]
                ]):
            if float(concentration) < 0:
                return False
            if float(mass) < 0:
                return False

        # this is 'M', 'mM', 'uM', & 'nM' solution
        elif any([
                solution_type == SOLUTION_TYPES[3],
                solution_type == SOLUTION_TYPES[4],
                solution_type == SOLUTION_TYPES[5],
                solution_type == SOLUTION_TYPES[6],
                ]):
            if float(concentration) < 0:
                return False
            if float(mass) < 0:
                return False
            if (mol_weight == '' and material == 'Material'):
                return False
            elif (mol_weight == ''):
                self.get_mol_weight(material)
                self.context.update({'mol_weight': self.MOLECULAR_WEIGHT})
                mol_weight = self.context['mol_weight']
            if mol_weight < 0:
                return False
            
    def get_solvents(self):
        self.SOLVENT_LIST = Solvent.get_all()

    def get_materials(self):
        self.MATERIAL_LIST = Material.get_all()

    def get_solvent_density(self, solvent):
        solvent = Solvent.get_solvent(solvent)
        density = solvent[0].density
        self.SOLVENT_DENSITY = f'{density}'

    def get_mol_weight(self, material):
        material = Material.get_material(material)
        mol_weight = material[0].molecular_weight
        self.MOLECULAR_WEIGHT = f'{mol_weight}'

    def close_error(self):
        self.ERROR = False

# TODO: add more solution_types and logic.
# add conversion method for different solution types