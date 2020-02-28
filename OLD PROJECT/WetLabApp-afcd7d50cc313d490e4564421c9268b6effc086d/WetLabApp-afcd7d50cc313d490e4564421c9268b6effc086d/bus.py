# -*- coding: utf-8 -*-
"""

This module contains common functions used throughout 
the app to transfer data.

"""
"""importing standard modules"""
import json

"""function loads data from .json files"""#####################################
def loader():
    with open("data.json") as f:
        return json.load(f)

def dumper(dict):
    json.dump(dict, open("data.json", "w"))
    