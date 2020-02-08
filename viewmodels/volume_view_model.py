from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty


class VolumeViewModel(EventDispatcher):

    __events__ = (
        ''
    )

    solvents = ListProperty([])
    volume_needed = StringProperty()
    error = StringProperty()

    def calculate(self, context):
        if self.verify_fields(context):
            # TODO: check these formulas again 
            if context["solution_types"] == '% Wt/Wt':
                concentration = float(context['concentration'])
                mass = float(context['mass'])
                density = float(context['density'])
                self.volume_needed = str(round(((1 - concentration) * mass)/(concentration * density), 3)) + ' ml'   
            # TODO: check these formulas again
            elif context["solution_types"] == '% Wt/Vol':
                print('we/v function')
                concentration = float(context['concentration'])
                mass = float(context['mass'])
                self.volume_needed = str(round((mass/concentration), 3)) + 'ml'
        else:
            # TODO: rearrange logic so that solution type is called before
            # verify method. This will ensure that the verify method only 
            # checks fields needed for that specific formula. Just create 
            # a new verify method that takes the solution type as an argument
            # and uses it to direct logic flow accordingly
            return
            # TODO: This return is goin to hide some errors in the 
            # calculation blocks above. Fix this somehow.
            # It may sort itself out with the implementation of 
            # the above TODO

    def verify_fields(self, context):

        error_message = ''
        
        # must check for every situation
        if context["solution_types"] == 'Solution Type':
            error_message += 'Choose a Solution Type\n'
        if context["solvent"] == 'Solvent':
            error_message += 'Choose a Solvent\n'
        if context["material"] == 'Material':
            error_message += 'Choose a Material\n'

        # All other verifications depend on previous selections
        try:
            if float(context["concentration"]) > 1:
                error_message += "Concentration must be less than 1\n"
            elif float(context["concentration"]) < 0:
                error_message += "Concentration must be greater than 0\n"
        except ValueError:
            error_message+="Concentration field empty\n"
        try:
            if float(context["mass"]) < 0:
                error_message += "Mass must be greater than 0\n"
        except ValueError:
            error_message += "Mass field empty\n"

        # Return True if no errors, False and errors if any
        finally:
            if error_message == '':
                return True
            else:
                self.error = error_message
                return False
