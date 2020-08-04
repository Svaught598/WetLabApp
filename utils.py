import json
from settings import MASS_UNITS


def convert_mass(mass, from_unit, to_unit):
    if from_unit == to_unit:
        return mass

    # from kg to ...
    if from_unit == MASS_UNITS[0]:
        if to_unit == MASS_UNITS[1]:
            return mass * 1.e3
        elif to_unit == MASS_UNITS[2]:
            return mass * 1.e6
        elif to_unit == MASS_UNITS[3]:
            return mass * 1.e9
        elif to_unit == MASS_UNITS[4]:
            return mass * 1.e12

    # from g to ...
    if from_unit == MASS_UNITS[1]:
        if to_unit == MASS_UNITS[0]:
            return mass * 1.e-3
        elif to_unit == MASS_UNITS[2]:
            return mass * 1.e3
        elif to_unit == MASS_UNITS[3]:
            return mass * 1.e6
        elif to_unit == MASS_UNITS[4]:
            return mass * 1.e9

    # from mg to ...
    if from_unit == MASS_UNITS[2]:
        if to_unit == MASS_UNITS[0]:
            return mass * 1.e-6
        elif to_unit == MASS_UNITS[1]:
            return mass * 1.e-3
        elif to_unit == MASS_UNITS[3]:
            return mass * 1.e3
        elif to_unit == MASS_UNITS[4]:
            return mass * 1.e6

    # from ug to ...
    if from_unit == MASS_UNITS[3]:
        if to_unit == MASS_UNITS[0]:
            return mass * 1.e-9
        elif to_unit == MASS_UNITS[1]:
            return mass * 1.e-6
        elif to_unit == MASS_UNITS[2]:
            return mass * 1.e-3
        elif to_unit == MASS_UNITS[4]:
            return mass * 1.e3

    # from ng to ...
    if from_unit == MASS_UNITS[4]:
        if to_unit == MASS_UNITS[0]:
            return mass * 1.e-12
        elif to_unit == MASS_UNITS[1]:
            return mass * 1.e-9
        elif to_unit == MASS_UNITS[2]:
            return mass * 1.e-6
        elif to_unit == MASS_UNITS[3]:
            return mass * 1.e-3