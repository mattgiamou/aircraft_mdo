"""
Top level design loop. 
"""

from avl_bridge import avl_analysis
from bwb_geometry import write_avl_files
from cruise_analysis import cruise_residual, maxSpeedWithThrust
import numpy as np
from scipy.optimize import broyden1
# Fix body parameters, loop over wing parameters. 


if __name__=='__main__':                        
    N = 2
    CD0 = 0.04
    body_chord = 0.8
    body_span = 0.25
    body_sweep = 15.0
    transition = 0.1
    wing_twist = -2.0
    wing_chord_vec = np.linspace(0.2, 0.4, N)
    wing_span_vec = np.linspace(0.35, 0.5, N)
    wing_x_offset_vec = np.linspace(0.1, 0.4, N)
    wing_sweep_vec = np.linspace(15.0, 30.0, N)
    wing_taper_vec = np.linspace(0.3, 0.8, N)
    
    cm_best = 1000.0
    cm0_best = -1000.0
    kn_best = -1000.0
    alpha_best = -1000.0
    v_best = -1000.0
    wing_chord_best = -1.0
    wing_span_best = -1.0
    wing_x_offset_best = -1.0
    wing_sweep_best = -1.0
    wing_taper_best = -1.0
    for idx in xrange(0,N):
        print "Idx: ", idx, "\n"
        wing_chord = wing_chord_vec[idx]
        for jdx in xrange(0,N):
            wing_span = wing_span_vec[jdx]
            for kdx in xrange(0,N):
                wing_x_offset = wing_x_offset_vec[kdx]
                for ldx in xrange(0,N):
                    wing_sweep = wing_sweep_vec[ldx]
                    for mdx in xrange(0,N):
                        wing_taper = wing_taper_vec[mdx]
                        (s_ref, c_ref, b_ref, total_mass) = \
                            write_avl_files(body_chord, body_span, body_sweep, 
                                            wing_chord, wing_span, wing_x_offset, 
                                            wing_sweep, wing_taper, wing_twist, 
                                            transition)
                        (cl0, cm0, cla0, cma0) = avl_analysis()
                        kn = -cma0/cla0
                        # Solve for alpha
#                        def cruise_system(x):
#                            alpha = x#[0]
#                            #v = x[1]
#                            v_max, T_res = maxSpeedWithThrust(CD0,b_ref,s_ref,
#                                                              cla0,cl0,alpha)
#                            
#                            r1 = abs(T_res)
#                            r2 = cruise_residual(total_mass, v_max, s_ref, cl0, cla0, 
#                                               alpha)
#                            return r1 + r2
#                        try:
#                            #(alpha, v) = broyden1(cruise_system, [0.0, 12.0])
#                            alpha = broyden1(cruise_system, 0.0)
#                            v, T = maxSpeedWithThrust(CD0,b_ref,s_ref,
#                                                              cla0,cl0,alpha)
#                            print "Alpha: ", alpha, '\n'
#                            print "V: ", v, '\n'
#                        except:
#                            print "Failed.\n"
#                            alpha = 10000.0
#                            v = -1.0
                        
                        alpha = 0.5
                        while alpha < 4.0:
                            v_max, T_res = maxSpeedWithThrust(CD0,b_ref,s_ref,
                                                              cla0,cl0,alpha)
                            r2 = cruise_residual(total_mass, v_max, s_ref, cl0, 
                                                 cla0, alpha)
                            print "V_max: ", v_max, "\n"
                            print "Residual: ", r2, "\n"
                            if r2 <= 0.0:
                                cm = cm0 + cma0*alpha
                                if abs(cm) < abs(cm_best):
                                    alpha_best = alpha
                                    v_best = v_max
                                    cm_best = cm
                                    wing_chord_best = wing_chord
                                    wing_span_best = wing_span
                                    wing_x_offset_best = wing_x_offset
                                    wing_sweep_best = wing_sweep
                                    wing_taper_best = wing_taper
                                    cm0_best = cm0
                                    kn_best = kn
                                    print "Alpha: ", alpha, '\n'
                                    print "V: ", v_max, '\n'
                                break
                            else:
                                alpha = alpha + 0.1
    print "Done.\n"