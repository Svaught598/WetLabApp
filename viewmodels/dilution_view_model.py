# Kivy imports
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty, BooleanProperty

# local imports
from models import Solvent, Material
from settings import SOLUTION_TYPES


class DilutionViewModel(EventDispatcher):

    # Properties set by calculate method
    VOLUME = StringProperty('')
    ERROR = BooleanProperty()

    # Properties that are set by querying the database for 
    # all items in each table
    SOLVENT_LIST = ListProperty([])
    MATERIAL_LIST = ListProperty([])

    # context for calculate method. Usually reflects user inputs
    context = {}

    def calculate(self, context):
        """
        Uses target solution type and stock solution type to direct calculation
        to appropriate method. That method then calculates VOLUME from user
        input (stored in context dictionary)
        
        The following keys are always submitted to context,
        but may be '' if no input is entered:

            - 'concentration':          string
            - 'target_concentration':   string
            - 'solution_type':          string
            - 'target_solution_type':   string

        The following keys may be present, and are set by the verify_fields 
        method through database query if not present:

            - 'mol_weight':         string
            - 'solvent_density':    string
        """
        self.context = context
        if self.verify_fields() == False:
            self.ERROR = True
            return

        # Calculate for solution type '%w/w'
        if self.context["solution_type"] == SOLUTION_TYPES[0]:
            self.calculate_from_wt()
            return 

        # Calculate for solution type 'mg/ml'
        if self.context["solution_type"] == SOLUTION_TYPES[1]:
            self.calculate_from_mgml()
            return 

        # Calculate for solution type 'g/ml'
        if self.context["solution_type"] == SOLUTION_TYPES[2]:
            self.calculate_from_gml()
            return 

        # Calculate for solution type 'M'
        if self.context["solution_type"] == SOLUTION_TYPES[3]:
            self.calculate_from_M()
            return 

        # Calculate for solution type 'mM'
        if self.context["solution_type"] == SOLUTION_TYPES[4]:
            self.calculate_from_mM()
            return
            
        # Calculate for solution type '\u03BCM'
        if self.context["solution_type"] == SOLUTION_TYPES[5]:
            self.calculate_from_uM()
            return

        # Calculate for solution type 'nM'
        if self.context["solution_type"] == SOLUTION_TYPES[6]:
            self.calculate_from_nM()
            return

    def verify_fields(self):
        # TODO: Write verify method
        # Need to write method that checks validity of user input
        # (context dictionary)
        pass

    def close_error(self):
        """
        need this so that future ERRORs invoke a change in the state of
        the ERROR property. i.e, setting ERROR to True when its already True
        won't trigger an event on the UI side (no error popup)
        """
        self.ERROR = False

    def calculate_from_wt(self):
        # TODO: calculate from %w/w solution

        # Calculate for target solution type '%w/w'
        if self.context["target_solution_type"] == SOLUTION_TYPES[0]:
            pass

        # Calculate for target solution type 'mg/ml'
        if self.context["target_solution_type"] == SOLUTION_TYPES[1]:
            pass

        # Calculate for target solution type 'g/ml'
        if self.context["target_solution_type"] == SOLUTION_TYPES[2]:
            pass

        # Calculate for target solution type 'M'
        if self.context["target_solution_type"] == SOLUTION_TYPES[3]:
            pass

        # Calculate for target solution type 'mM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[4]:
            pass
            
        # Calculate for target solution type '\u03BCM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[5]:
            pass

        # Calculate for target solution type 'nM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[6]:
            pass

    def calculate_from_mgml(self):
        # TODO: calculate from mg/ml solution

        # Calculate for target solution type '%w/w'
        if self.context["target_solution_type"] == SOLUTION_TYPES[0]:
            pass

        # Calculate for target solution type 'mg/ml'
        if self.context["target_solution_type"] == SOLUTION_TYPES[1]:
            pass

        # Calculate for target solution type 'g/ml'
        if self.context["target_solution_type"] == SOLUTION_TYPES[2]:
            pass

        # Calculate for target solution type 'M'
        if self.context["target_solution_type"] == SOLUTION_TYPES[3]:
            pass

        # Calculate for target solution type 'mM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[4]:
            pass
            
        # Calculate for target solution type '\u03BCM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[5]:
            pass

        # Calculate for target solution type 'nM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[6]:
            pass

    def calculate_from_gml(self):
        # TODO: calculate from g/ml solution

        # Calculate for target solution type '%w/w'
        if self.context["target_solution_type"] == SOLUTION_TYPES[0]:
            pass

        # Calculate for target solution type 'mg/ml'
        if self.context["target_solution_type"] == SOLUTION_TYPES[1]:
            pass

        # Calculate for target solution type 'g/ml'
        if self.context["target_solution_type"] == SOLUTION_TYPES[2]:
            pass

        # Calculate for target solution type 'M'
        if self.context["target_solution_type"] == SOLUTION_TYPES[3]:
            pass

        # Calculate for target solution type 'mM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[4]:
            pass
            
        # Calculate for target solution type '\u03BCM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[5]:
            pass

        # Calculate for target solution type 'nM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[6]:
            pass

    def calculate_from_M(self):
        # TODO: calculate from M solution

        # Calculate for target solution type '%w/w'
        if self.context["target_solution_type"] == SOLUTION_TYPES[0]:
            pass

        # Calculate for target solution type 'mg/ml'
        if self.context["target_solution_type"] == SOLUTION_TYPES[1]:
            pass

        # Calculate for target solution type 'g/ml'
        if self.context["target_solution_type"] == SOLUTION_TYPES[2]:
            pass

        # Calculate for target solution type 'M'
        if self.context["target_solution_type"] == SOLUTION_TYPES[3]:
            pass

        # Calculate for target solution type 'mM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[4]:
            pass
            
        # Calculate for target solution type '\u03BCM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[5]:
            pass

        # Calculate for target solution type 'nM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[6]:
            pass

    def calculate_from_mM(self):
        # TODO: calculate from mM solution

        # Calculate for target solution type '%w/w'
        if self.context["target_solution_type"] == SOLUTION_TYPES[0]:
            pass

        # Calculate for target solution type 'mg/ml'
        if self.context["target_solution_type"] == SOLUTION_TYPES[1]:
            pass

        # Calculate for target solution type 'g/ml'
        if self.context["target_solution_type"] == SOLUTION_TYPES[2]:
            pass

        # Calculate for target solution type 'M'
        if self.context["target_solution_type"] == SOLUTION_TYPES[3]:
            pass

        # Calculate for target solution type 'mM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[4]:
            pass
            
        # Calculate for target solution type '\u03BCM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[5]:
            pass

        # Calculate for target solution type 'nM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[6]:
            pass

    def calculate_from_uM(self):
        # TODO: calculate from uM solution

        # Calculate for target solution type '%w/w'
        if self.context["target_solution_type"] == SOLUTION_TYPES[0]:
            pass

        # Calculate for target solution type 'mg/ml'
        if self.context["target_solution_type"] == SOLUTION_TYPES[1]:
            pass

        # Calculate for target solution type 'g/ml'
        if self.context["target_solution_type"] == SOLUTION_TYPES[2]:
            pass

        # Calculate for target solution type 'M'
        if self.context["target_solution_type"] == SOLUTION_TYPES[3]:
            pass

        # Calculate for target solution type 'mM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[4]:
            pass
            
        # Calculate for target solution type '\u03BCM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[5]:
            pass

        # Calculate for target solution type 'nM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[6]:
            pass

    def calculate_from_nM(self):
        # TODO: calculate from nM solution

        # Calculate for target solution type '%w/w'
        if self.context["target_solution_type"] == SOLUTION_TYPES[0]:
            pass

        # Calculate for target solution type 'mg/ml'
        if self.context["target_solution_type"] == SOLUTION_TYPES[1]:
            pass

        # Calculate for target solution type 'g/ml'
        if self.context["target_solution_type"] == SOLUTION_TYPES[2]:
            pass

        # Calculate for target solution type 'M'
        if self.context["target_solution_type"] == SOLUTION_TYPES[3]:
            pass

        # Calculate for target solution type 'mM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[4]:
            pass
            
        # Calculate for target solution type '\u03BCM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[5]:
            pass

        # Calculate for target solution type 'nM'
        if self.context["target_solution_type"] == SOLUTION_TYPES[6]:
            pass
