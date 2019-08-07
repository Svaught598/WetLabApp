# -*- coding: utf-8 -*-
"""

This module contains common functions used throughout 
the app to transfer data.

"""
"""importing standard modules"""
import json

"""function loads data from .json files"""#####################################
def loader(filename):
    
    """returns a dictionary"""
    
    with open(filename) as f:
        return json.load(f)

x = loader('data.json')['Solvents']