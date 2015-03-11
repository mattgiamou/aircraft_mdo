"""
Console BWB Designer
"""
from avl_bridge import avl_analysis, avl_trimmed_analysis
import bwb_geometry
from bwb_geometry import write_avl_files
from cruise_analysis import get_thrust_available, CruiseSolver
import numpy as np
from matplotlib import pyplot as plt
from aer406_cost_function import flight_score
from scipy import optimize

# Airfoils
miley = 'avl/airfoils/MILEY_M06-13-128.dat'
e330 = 'avl/airfoils/e330.dat'

# Parameters
cd0 = 0.04
e = 0.8


#2.411174E-01   3.863906E-01   1.750302E-01   3.008679E+01   4.219785E-01
#      -5.018741E+00

# Geometry
body_chord = 0.7
body_span = 0.25
body_sweep = 10.0
wing_chord = 2.411174E-01  #0.24
wing_span = 3.863906E-01 #0.4
wing_x_offset = 1.750302E-01 #0.2
wing_sweep = 3.008679E+01 #30.0
wing_taper = 4.219785E-01 #0.5
wing_twist = -5.018741E+00 #-5.
transition = 0.1

def cons_chord1(x):
    return x[0] - 0.15
def cons_span1(x):
    return x[1] - 0.25
def cons_x1(x):
    return x[2] - 0.1
def cons_sweep1(x):
    return x[3]
def cons_taper1(x):
    return x[4] - 0.3
def cons_twist1(x):
    return x[4] + 7.0
    
def bwb_objective(x):
    """
    Objective function. 
    x = [wing_chord, wing_span, wing_x_offset, wing_sweep, wing_taper, wing_twist]
    """
    (S, c, b, M) = write_avl_files(body_chord, body_span, body_sweep, 
                                   x[0], x[1], x[2], 
                                   x[3], x[4], x[5], 
                                   transition,
                                   wing_airfoil=miley,
                                   body_airfoil=e330)
    # Worried about this only at zero approach, but post processing works
    try:
        (cl0, cm0, cla, cma) = avl_analysis()
        kn = -cma/cla
        if kn < 0.15:
            return 10000
        if cm0 < 0.01:
            return 10000
        cruise = CruiseSolver(M, S, b, cl0, cla, cd0, e)
        alpha_cruise, v_cruise = cruise.solve_cruise_alpha()
        cm_cruise = cm0 + cma*alpha_cruise
    except:
        return 10000
    return abs(cm_cruise)
    
def analyze_design(body_chord, body_span, body_sweep, wing_chord, wing_span, 
                   wing_x_offset, wing_sweep, wing_taper, wing_twist,
                   transition, wing_airfoil=miley, body_airfoil=e330,
                   cd0=0.04, e=0.8):
    """
    High level design script.
    """
    (S, c, b, M) = write_avl_files(body_chord, body_span, body_sweep, 
                                   wing_chord, wing_span, wing_x_offset, 
                                   wing_sweep, wing_taper, wing_twist, 
                                   transition,
                                   wing_airfoil=wing_airfoil,
                                   body_airfoil=body_airfoil)
    # Worried about this only at zero approach, but post processing works
    (cl0, cm0, cla, cma) = avl_analysis()
    kn = -cma/cla
    cruise = CruiseSolver(M, S, b, cl0, cla, cd0, e)
    
    N = 100
    v = np.linspace(10.0, 17.0, N)
    #alpha_vec = np.zeros(v_vec.shape)
    alpha = cruise.get_cruise_alpha(v)
    D = cruise.compute_drag(alpha, v)
    T = get_thrust_available(v)
    #index = np.argmin(abs(T-D))
    #v_cruise = v[index]
    #D_cruise = D[index]
    #alpha_cruise = alpha[index]
    alpha_cruise, v_cruise = cruise.solve_cruise_alpha()
    cl_cruise = cl0 + cla*alpha_cruise
    cm_cruise = cm0 + cma*alpha_cruise
    #T_cruise = T[index]
    # Plot 
    plt.figure()
    plt.plot(v, T, 'r')
    plt.grid()
    plt.plot(v, D, 'b')
    plt.xlabel('Velocity (m/s)')
    plt.ylabel('Force (N), Degrees')
    plt.legend(('Thrust Available', 'Drag', 'alpha'))
    (alpha_trim, elevator, CD, e_trim, hm) = avl_trimmed_analysis(v_cruise)
    
    # For flight score
    s_density = 0.0533*c*bwb_geometry.default_density
    struct_mass = s_density*S
    # Need to output: 
    #   T available and drag vs. velocity for cruise alpha (must solve)
    #   Cm0, Cm at cruise alpha
    #   mass
    #   surface area
    #   flight score
    #   binary fly/no fly
    #   plots
    
    # Compute flight score
    t_balls = 0
    g_balls = 13
    p_balls = 13
    turn_t = 5.0
    empty_mass = struct_mass + 0.326 # Electronics, etc.
    fs = flight_score(t_balls, g_balls, p_balls, v_cruise, turn_t, empty_mass, M)
    
    # Display results to console
    print "Alpha Cruise: ", alpha_cruise
    print "V Cruise: ", v_cruise
    print "CL Cruise: ", cl_cruise
    print "CL Takeoff: ", (cl0 + 9.0*cla)
    print "Cm Cruise: ", cm_cruise
    print "Cm0: ", cm0
    print "Static Margin: ", kn
    print "S: ", S
    AR = b**2/S
    print "K: ", 1/(np.pi*AR*e)
    #print "Structure Mass: ", struct_mass
    print "Total Mass: ", M
    print "Alpha trimmed: ", alpha_trim
    #print "Elevator trimmed: ", elevator
    print "Trimmed Oswald Efficiency: ", e_trim
    #print "Hinge moment: ", hm
    print "CD Trimmed: ", CD
    print "Flight Score: ", fs
    print '-------------------------------------\n'
    
if __name__=='__main__':
    
    analyze_design(body_chord, body_span, body_sweep, wing_chord, wing_span, 
                   wing_x_offset, wing_sweep, wing_taper, wing_twist,
                   transition, miley, e330, cd0, e)
    
    # Attempt to optimize
#    x0 = [wing_chord, wing_span, wing_x_offset, wing_sweep, wing_taper, 
#          wing_twist]
#          
#    x = optimize.fmin_cobyla(bwb_objective, x0, [cons_chord1, cons_span1,
#                                                 cons_sweep1, cons_taper1,
#                                                 cons_twist1, cons_x1],
#                                                 maxfun=100, disp=1)
    