"""
Console BWB Designer
"""
from avl_bridge import avl_analysis
import bwb_geometry
from bwb_geometry import write_avl_files
from cruise_analysis import get_thrust_available, CruiseSolver
import numpy as np
from matplotlib import pyplot as plt

# Parameters
cd0 = 0.04
e = 0.8

# Geometry
body_chord = 0.8
body_span = 0.25
body_sweep = 15.0
wing_chord = 0.3
wing_span = 0.45
wing_x_offset = 0.3
wing_sweep = 25.0
wing_taper = 0.7
wing_twist = 0.0
transition = 0.1

if __name__=='__main__':
    
    (S, c, b, M) = write_avl_files(body_chord, body_span, body_sweep, 
                                   wing_chord, wing_span, wing_x_offset, 
                                   wing_sweep, wing_taper, wing_twist, 
                                   transition)
    # Worried about this only at zero approach, but post processing works
    (cl0, cm0, cla, cma) = avl_analysis()
    kn = -cma/cla
    cruise = CruiseSolver(M, S, b, cl0, cla, cd0, e)
    
    N = 100
    v = np.linspace(5.0, 16.0, N)
    #alpha_vec = np.zeros(v_vec.shape)
    alpha = cruise.get_cruise_alpha(v)
    D = cruise.compute_drag(alpha, v)
    T = get_thrust_available(v)
    plt.figure()
    plt.plot(v, T, 'r')
    plt.grid()
    plt.plot(v, D, 'b')
    #plt.plot(v, alpha, 'g')
    plt.xlabel('Velocity (m/s)')
    plt.ylabel('Force (N), Degrees')
    plt.legend(('Thrust Available', 'Drag', 'alpha'))
    # Need to output: 
    #   T available and drag vs. velocity for cruise alpha (must solve)
    #   Cm0, Cm at cruise alpha
    #   mass
    #   surface area
    #   flight score
    #   binary fly/no fly
    #   plots
    
    # For flight score
    struct_mass = bwb_geometry.default_density*S
    
    # Display results to console
    print "Static Margin: ", kn, '\n'
    print "Structure Mass: ", struct_mass, '\n'