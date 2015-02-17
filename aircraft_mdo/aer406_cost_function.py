""" Cost function for AER406 competition. This serves as the objective function
for BWB design.
"""
from openmdao.main.api import Component
from openmdao.main.datatypes.api import Float
from openmdao.main.datatypes.api import Bool
import numpy as np

class FlightScore(Component):
    """ Taken from AER406 "Introduction" slide, 2015.
    """
    
    # Inputs
    t_balls = Float(0.0, iotype='in', desc='Number of tennis balls')
    g_balls = Float(0.0, iotype='in', desc='Number of golf balls')
    p_balls = Float(0.0, iotype='in', desc='Number of ping pong balls')
    v = Float(0.1, iotype='in', desc='Velocity (m/s)')
    empty_mass = Float(0.1, iotype='in', desc='Empty mass (kg)')
    turn_time = Float(0.1, iotype='in', desc='Turn time (s)')
    takeoff_bonus = Bool(True, iotype='in', desc='Take off bonus (boolean)')
    stability_bonus = Float(1.0, iotype='in', desc='Stability bonus') 
    
    # Output
    flight_score = Float(iotype='out', desc='AER406 flight score')

    def execute(self):
        """ 
        """
        CU = cargo_units(self.t_balls, self.g_balls, self.p_balls)
        time_score = time_cost(self.v, self.turn_time)
        PF = payload_fraction(self.t_balls, self.g_balls, 
                                         self.p_balls, self.empty_mass)
                                         
        self.flight_score = 

def time_cost(v, turn_t):
    """ v: velocity (m/s)
        turn_t: turn time (s)
    """
    return np.exp(1.5*(1.0 - t/58.0))

def cargo_units(t_balls, g_balls, p_balls):
    return p_balls*10.0 + g_balls*50.0 + t_balls*120.0

def payload_fraction(p_balls, g_balls, t_balls, empty_weight):
    payload = 0.0027*p_balls + 0.046*g_balls + 0.06*t_balls
    return payload/(payload + empty_weight)

def stability_bonus(t):
    """ TODO: vectorize.
    """
    return 1.0 + 0.025*np.min(t, 8.0)


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    