""" Blended wing body (BWB) geometry parameterization.
"""

from openmdao.main.api import Component
from openmdao.main.datatypes.api import Float

def compute_mass():
    """ Used to estimate the empty mass of the plane. Should scale up with 
    surface area of body and wings in some principled manner. 
    """
    electronics = 0.3
    
    mass = electronics
    return mass