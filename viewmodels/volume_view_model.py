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
        if self.verify_fields(context):
            if context["solution_types"] == '%Wt/Wt':
                concentration = float(context['concentration'])
                mass = float(context['mass'])
                density = float(context['density'])
                self.volume_needed = str(round(((1 - concentration) * mass)/(concentration * density), 3)) + ' ml'   

            elif context["solution_types"] == '%Wt/V':
                concentration = float(context['concentration'])
                mass = float(context['mass'])
                self.volume_needed = str(round((mass/concentration), 3))
        else:
            return

    def verify_fields(self, context):

        error_message = ''
        
        # must check for every situation
        if context["solution_types"] == 'Solution Type':
            error_message.join("Choose a Solution Type\n")
        if context["solvent"] == 'Solvent':
            error_message.join('Choose a Solvent\n')
        if context["material"] == 'Material':
            error_message.join('Choose a Material\n')

        # TODO: add checks for empty inputs

        # All other verifications depend on previous selections
        if float(context["concentration"]) > 1:
            error_message.join("Concentration must be less than 1\n")
        if float(context["concentration"]) < 0:
            error_message.join("Concentration must be greater than 0\n")
        if float(context["mass"]) < 0:
            error_message.join("Mass must be greater than 0\n")

        # TODO: Add special verifications for each option

        self.error = error_message

        if error_message == '':
            return True
        else:
            return False
