import sqlite3 as SQL
#from utils import querify

class Solvent(object):
    '''Model describing solvent
    
    kwargs:
        - name
        - density
        - chemical formula
        - relative polarity
    '''
    def __init__(self, *args, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    #@querify
    def save(self):
        query = "INSERT INTO Solvents (name, density, formula, polarity) VALUES(?,?,?,?);"
        info = (self.name, self.density, self.formula, self.polarity,)
        return query, info
        
    #@querify
    def delete(self):
        query = "DELETE FROM Solvents WHERE name=?;"
        info = (self.name,)
        return query, info

    
