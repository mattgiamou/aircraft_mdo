"""
Top level analysis functions for BWB design.
"""

from avl_bridge import avl_analysis
from bwb_geometry import write_avl_files
from openmdao.main.api import Component
from openmdao.main.datatypes.api import Float

class AeroStab(Component):
    """ Aerodynamic and stability analysis using AVL.
    """
    
    # Inputs
    body_chord = Float(0.8, iotype='in', desc='Body root chord')
    body_span = Float(0.25, iotype='in', 
                      desc='Half span of body (including transition)')
    body_sweep = Float(15.0, iotype='in', 
                       desc='Sweep (degrees) of body section')
    wing_chord = Float(0.35, iotype='in', desc='Wing base chord')
    wing_span = Float(0.4, iotype='in', desc='Wing half span')
    wing_x_offset = Float(0.35, iotype='in', 
                    desc='Offset from nose of the start of the wing section')
    wing_sweep = Float(0.8, iotype='in', desc='Wing section sweep in degrees')
    wing_taper = Float(0.5, iotype='in', desc='Wing taper (ratio)')
    wing_twist = Float(-2.0, iotype='in', 
                       desc='Geometric twist of wing section')
    transition = Float(0.1, iotype='in', desc='Transition region length')
    
    # Output
    s_ref = Float(iotype='out', desc='Reference surface area (planiform)')
    c_ref = Float(iotype='out', desc='Mean chord length')
    m_total = Float(iotype='out', desc='Total mass')
    cl0 = Float(iotype='out', desc='CL at alpha = 0')
    cla = Float(iotype='out', desc='CL_alpha')
    cm0 = Float(iotype='out', desc='Cm at alpha = 0')
    cma = Float(iotype='out', desc='Cm_alpha')
    
    def execute(self):
        """ 
        Creates AVL input files and executes. Assumes AVL and AVL file inputs
        are on the path.
        """
        
        (s, c, M) = write_avl_files(self.body_chord, self.body_span, 
                                    self.body_sweep, self.wing_chord, 
                                    self.wing_span, self.wing_x_offset, 
                                    self.wing_sweep, self.wing_taper, 
                                    self.wing_twist, self.transition)
                                    
        self.s_ref = s
        self.c_ref = c
        self.m_total = M
        
        
                                    
        self.flight_score = CU*PF*time_score*self.stability_bonus \
                            *self.takeoff_bonus
                            