"""
Top level analysis functions for BWB design.
"""
from avl_bridge import avl_analysis
from bwb_geometry import write_avl_files
from cruise_analysis import alpha_cruise, maxSpeedWithThrust
from openmdao.main.api import Component
from openmdao.main.datatypes.api import Float
from openmdao.lib.drivers.api import CaseIteratorDriver
from openmdao.main.api import Assembly
from openmdao.lib.drivers.api import FixedPointIterator

class BWBIterator(Assembly):
    """ Iterates over BWB designs.
    """

    def configure(self):
        """ Creates a new Assembly with this problem
        """
        
        self.add('aero', AeroStab())
        self.add('cruiseAlpha', CruiseAlpha())
        self.add('thrustVelocity', ThrustVelocity())
        # create Optimizer instance
        self.add('driver', CaseIteratorDriver())
        
        # Set input parameters
        self.driver.add_parameter('aero.body_chord', low=0.6, high=0.9)
        self.driver.add_parameter('aero.body_span', low=0.20, high=0.30)
        self.driver.add_parameter('aero.body_sweep', low=5.0, high=30.0)
        self.driver.add_parameter('aero.wing_chord', low=0.20, high=0.40)
        self.driver.add_parameter('aero.wing_span', low=0.30, high=0.50)
        self.driver.add_parameter('aero.wing_x_offset', low=0.10, high=0.35)
        self.driver.add_parameter('aero.wing_sweep', low=0.0, high=45.0)
        self.driver.add_parameter('aero.wing_taper', low=0.2, high=1.0)
        self.driver.add_parameter('aero.wing_twist', low=-5.0, high=0.0)
        self.driver.add_parameter('aero.transition', low=0.1, high=0.15)
        # Set "responses"
        self.driver.add_response('aero.s_ref')
        self.driver.add_response('aero.c_ref')
        self.driver.add_response('aero.m_total')
        self.driver.add_response('aero.cl0')
        self.driver.add_response('aero.cla')
        self.driver.add_response('aero.cm0')
        self.driver.add_response('aero.cma')
        
        # Outer Loop - Global Optimization
        self.add('solver', FixedPointIterator())
        self.driver.workflow.add(['solver'])

        # Inner Loop - Full Multidisciplinary Solve via fixed point iteration
        self.solver.workflow.add(['cruiseAlpha', 'thrustVelocity'])

        # Add Parameters to optimizer
        self.driver.add_parameter(('c.z1','dis2.z1'), low = -10.0, high = 10.0)
        self.driver.add_parameter('dis1.x1', low = 0.0,   high = 10.0)

        # Make all connections
        self.connect('cruiseAlpha.a_cruise','thrustVelocity.a_cruise')
        self.connect('aero.s_ref','cruiseAlpha.s_ref')
        self.connect('aero.s_ref','thrustVelocity.s_ref')
        #self.connect('cruiseAlpha.v_cruise','ThrustVelocity.v_cruise')
        # Iteration loop
        self.solver.add_parameter('cruiseAlpha.v_cruise')
        self.solver.add_constraint('cruiseAlpha.v_cruise = ThrustVelocity.v_cruise')
        self.solver.max_iteration = 100
        self.solver.tolerance = .00001

        #Driver settings
        
        
class CruiseAlpha(Component):
    """
    Simply computes W=L. Used in conjunction with T-V solver.
    """
    s_ref = Float(0.6, iotype='in', desc='Reference surface area (planiform)')
    v_cruise = Float(12.0, iotype='in', desc='Cruise velocity in m/s')
    b_ref = Float(1.4, iotype='in', desc='Wing span')
    cla = Float(iotype='in', desc='CL_alpha')
    cl0 = Float(iotype='in', desc='CL at alpha = 0')
    m_total = Float(iotype='in', desc='Total mass')
    
    a_cruise = Float(iotype='out', desc='Cruise angle of attack')
    
    def execute(self):
        W = 2.0*9.81*self.m_total
        (cl, a_cruise) = alpha_cruise(self.v_cruise, W, self.s_ref, self.cla,
                                      self.cl0)
        self.a_cruise = a_cruise
        
class ThrustVelocity(Component):
    """
    Computes the max velocity using the thrust-velocity curve.
    """
    s_ref = Float(0.6, iotype='in', desc='Reference surface area (planiform)')
    b_ref = Float(1.4, iotype='in', desc='Wing span')
    cla = Float(iotype='in', desc='CL_alpha')
    cl0 = Float(iotype='in', desc='CL at alpha = 0')
    CD0 = Float(0.04, iotype='in', desc='CD at alpha = 0')    
    a_cruise = Float(iotype='out', desc='Cruise angle of attack')
    
    v_cruise = Float(iotype='out', desc='Cruise velocity in m/s')
        
    def execute(self):
        (v_max, T_res) = maxSpeedWithThrust(self.CD0,self.b_ref,self.s_ref,
                                            self.cla,self.cl0,self.a_cruise)
        self.v_cruise = v_max
        self.T_res = T_res
class AeroStab(Component):
    """ 
    Aerodynamic and stability analysis using AVL.
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
    b_ref = Float(iotype='out', desc='Full wing span')
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
        (s, c, b, M) = write_avl_files(self.body_chord, self.body_span, 
                                    self.body_sweep, self.wing_chord, 
                                    self.wing_span, self.wing_x_offset, 
                                    self.wing_sweep, self.wing_taper, 
                                    self.wing_twist, self.transition)     
        self.s_ref = s
        self.c_ref = c
        self.b_ref = b
        self.m_total = M
        
        (cl0, cm0, cla0, cma0) = avl_analysis()
                                    
        self.cl0 = cl0
        self.cla = cla0
        self.cm0 = cm0
        self.cma = cma0
                       
if __name__ == "__main__":

    import time

    analysis = BWBIterator()

    tt = time.time()
    analysis.run()

#    print "Elapsed time: ", time.time()-tt, "seconds"
#
#    x = analysis.driver.case_inputs.test.x
#    y = analysis.driver.case_inputs.test.y
#    f_xy = analysis.driver.case_outputs.test.brightness
#
#    for i in range(0, len(x)):
#        print "x: {} y: {} f(x, y): {}".format(x[i], y[i], f_xy[i])