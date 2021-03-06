# Kivy imports
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty, BooleanProperty

# local imports
from models import Solvent, Material
from settings import SOLUTION_TYPES

class FilmViewModel(EventDispatcher):
    """
    This class accepts inputs from the corresponding view class and
    performs operations on those inputs unique to this class. 

    The primary responsibilty here is to ensure user input is valid, 
    and to calculate the THICKNESS of a film if it is. If the input is not 
    valid, the viewmodel will attempt to rectify this by either pulling 
    necesary data from the database or changing ERROR to True.
    (...which then triggers a UI dialog popup)
    """
    
    # These Properties are set by the calculate method
    THICKNESS = StringProperty('')
    ERROR = BooleanProperty('')

    # Properties that are bound to changes in 
    # solvent or material dropdown menu selection
    MOLECULAR_WEIGHT = StringProperty('')
    MATERIAL_DENSITY = StringProperty('')
    SOLVENT_DENSITY = StringProperty('')
    
    
    # Properties that are set by querying the database for 
    # all items in each table
    SOLVENT_LIST = ListProperty([])
    MATERIAL_LIST = ListProperty([])

    # context for calculate method. Usually reflects user inputs
    context = {}

    def calculate(self, context):
        """
        calculates THICKNESS based on user input
        
        context is a dictionary. The following keys are always submitted, 
        but may be '' if no input:

            - 'concentration':  string
            - 'volume':         string
            - 'solution_type':  string
            - 'area':           string

        The following keys may be present, and are set by the verify_fields 
        method through database query if not present:

            - 'material_density':   string
            - 'solvent_density':    string
        """
        self.context = context
        if self.verify_fields() == False:
            self.ERROR = True
            return 
        
        # Calculate for solution type 'Wt/Wt'
        if self.context["solution_type"] == SOLUTION_TYPES[0]:
            concentration = float(self.context['concentration'])
            volume = float(self.context['volume'])
            material_density = float(self.context['material_density'])
            solvent_density = float(self.context['solvent_density'])
            area = float(self.context['area'])
            thickness = (
                volume*solvent_density*concentration)/(
                material_density*area)
            self.THICKNESS = f'{thickness} cm'

        # Calculate for solution type 'mg/ml'
        if self.context["solution_type"] == SOLUTION_TYPES[1]:
            concentration = float(self.context['concentration'])
            volume = float(self.context['volume'])
            material_density = float(self.context['material_density'])
            area = float(self.context['area'])
            thickness = (
                concentration*volume)/(
                1e3*material_density*area)
            self.THICKNESS = f'{thickness} cm'

        # Calculate for solution type 'g/ml'
        if self.context["solution_type"] == SOLUTION_TYPES[2]:
            concentration = float(self.context['concentration'])
            volume = float(self.context['volume'])
            material_density = float(self.context['material_density'])
            area = float(self.context['area'])
            thickness = (
                concentration*volume)/(
                material_density*area)
            self.THICKNESS = f'{thickness} cm'

        # Calculate for solution type 'M'
        if self.context["solution_type"] == SOLUTION_TYPES[3]:
            concentration = float(self.context['concentration'])
            volume = float(self.context['volume'])
            mol_weight = float(self.context['mol_weight'])
            material_density = float(self.context['material_density'])
            area = float(self.context['area'])
            thickness = (
                concentration*volume*mol_weight)/(
                1e3*material_density*area)
            self.THICKNESS = f'{thickness} cm'

        # Calculate for solution type 'mM'
        if self.context["solution_type"] == SOLUTION_TYPES[4]:
            concentration = float(self.context['concentration'])
            volume = float(self.context['volume'])
            mol_weight = float(self.context['mol_weight'])
            material_density = float(self.context['material_density'])
            area = float(self.context['area'])
            thickness = (
                concentration*volume*mol_weight)/(
                1e6*material_density*area)
            self.THICKNESS = f'{thickness} cm'

        # Calculate for solution type '\u03BCM'
        if self.context["solution_type"] == SOLUTION_TYPES[5]:
            concentration = float(self.context['concentration'])
            volume = float(self.context['volume'])
            mol_weight = float(self.context['mol_weight'])
            material_density = float(self.context['material_density'])
            area = float(self.context['area'])
            thickness = (
                concentration*volume*mol_weight)/(
                1e9*material_density*area)
            self.THICKNESS = f'{thickness} cm'

        # Calculate for solution type 'nM'
        if self.context["solution_type"] == SOLUTION_TYPES[6]:
            concentration = float(self.context['concentration'])
            volume = float(self.context['volume'])
            mol_weight = float(self.context['mol_weight'])
            material_density = float(self.context['material_density'])
            area = float(self.context['area'])
            thickness = (
                concentration*volume*mol_weight)/(
                1e12*material_density*area
            )
            self.THICKNESS = f'{thickness} cm' 

    def verify_fields(self):
        solution_type = self.context['solution_type']
        solvent = self.context['solvent']
        material = self.context['material']
        concentration = self.context['concentration']
        volume =  self.context['volume']
        area = self.context['area']

        # must check for every situation
        if concentration == '':
            return False
        if area == '':
            return False
        if solution_type == 'Solution Type':
            return False

        # this is '% wt/wt' solution
        if solution_type == SOLUTION_TYPES[0]:
            if float(concentration) < 0:
                return False
            if float(volume) < 0:
                return False
            if float(area) < 0:
                return False
            if material == 'Material':
                return False
            else:
                self.get_material_density(material)
                self.context.update({'material_density': self.MATERIAL_DENSITY})
            if solvent == 'Solvent':
                return False
            else: 
                self.get_solvent_density(solvent)
                self.context.update({'solvent_density': self.SOLVENT_DENSITY})

        # this is 'mg/mL' & 'g/mL' solution
        elif any([
                solution_type == SOLUTION_TYPES[1],
                solution_type == SOLUTION_TYPES[2]
                ]):
            if float(concentration) < 0:
                return False
            if float(volume) < 0:
                return False
            if float(area) < 0:
                return False
            if material == 'Material':
                return False
            else: 
                self.get_material_density(material)
                self.context.update({'material_density': self.MATERIAL_DENSITY})

        # this is 'M', 'mM', 'uM', & 'nM' solution
        elif any([
                solution_type == SOLUTION_TYPES[3],
                solution_type == SOLUTION_TYPES[4],
                solution_type == SOLUTION_TYPES[5],
                solution_type == SOLUTION_TYPES[6],
                ]):
            if float(concentration) < 0:
                return False
            if float(volume) < 0:
                return False
            if float(area) < 0:
                return False
            if material == 'Material':
                return False
            else: 
                self.get_mol_weight(material)
                self.get_material_density(material)
                self.context.update({'mol_weight': self.MOLECULAR_WEIGHT})
                self.context.update({'material_density': self.MATERIAL_DENSITY})

    def close_error(self):
        """
        need this so that future ERRORs invoke a change in the state of
        the ERROR property. i.e, setting ERROR to True when its already True
        won't trigger an event on the UI side (no error popup)
        """
        self.ERROR = False 

    # The rest of these methods are just helper functions 
    # use the peewee model to query the database for specific
    # pieces of information
    def get_mol_weight(self, material):
        material = Material.get_material(material)
        mol_weight = material[0].molecular_weight
        self.MOLECULAR_WEIGHT = f'{mol_weight}'

    def get_material_density(self, material):
        material = Material.get_material(material)
        density = material[0].density
        self.MATERIAL_DENSITY = f'{density}'

    def get_solvent_density(self, solvent):
        solvent = Solvent.get_solvent(solvent)
        density = solvent[0].density
        self.SOLVENT_DENSITY = f'{density}'

    def get_solvents(self):
        self.SOLVENT_LIST = Solvent.get_all()

    def get_materials(self):
        self.MATERIAL_LIST = Material.get_all()
