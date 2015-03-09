"""
Top level design loop. 
"""

from avl_bridge import avl_analysis
from bwb_geometry import write_avl_files
from cruise_analysis import cruise_residual, maxSpeedWithThrust
import numpy as np
from scipy.optimize import broyden1
from time import time
# Fix body parameters, loop over wing parameters. 


if __name__=='__main__':                        
    N = 4
    CD0 = 0.04
    body_chord_vec = np.linspace(0.5, 0.9, N)
    body_span = 0.25
    body_sweep = 20.0
    transition = 0.1
    wing_twist = -0.0
    wing_chord_vec = np.linspace(0.3, 0.6, N)
    wing_span_vec = np.linspace(0.30, 0.5, N)
    wing_x_offset_vec = np.linspace(0.1, 0.45, N)
    wing_sweep_vec = np.linspace(5.0, 35.0, N)
    wing_taper_vec = np.linspace(0.3, 1.0, N)
    
    residual_best = 1000.0
    cm_best = 1000.0
    cm0_best = -1000.0
    kn_best = -1000.0
    alpha_best = -1000.0
    v_best = -1000.0
    total_mass_best = 1000.0
    s_ref_best = 1000.0
    c_ref_best = 1000.0
    cl0_best = 1000.0
    cla0_best = 1000.0
    wing_chord_best = -1.0
    wing_span_best = -1.0
    wing_x_offset_best = -1.0
    wing_sweep_best = -1.0
    wing_taper_best = -1.0
    body_chord_best = -1000.0
    for idx in xrange(0,N):
        print "Idx: ", idx, "\n"
        t1 = time()
        wing_chord = wing_chord_vec[idx]
        for jdx in xrange(0,N):
            wing_span = wing_span_vec[jdx]
            for kdx in xrange(0,N):
                wing_x_offset = wing_x_offset_vec[kdx]
                for ldx in xrange(0,N):
                    wing_sweep = wing_sweep_vec[ldx]
                    for mdx in xrange(0,N):
                        wing_taper = wing_taper_vec[mdx]
                        for ndx in xrange(0,N):
                            body_chord = body_chord_vec[ndx]
                            (s_ref, c_ref, b_ref, total_mass) = \
                                write_avl_files(body_chord, body_span, body_sweep, 
                                                wing_chord, wing_span, wing_x_offset, 
                                                wing_sweep, wing_taper, wing_twist, 
                                                transition)
                            try:
                                (cl0, cm0, cla0, cma0) = avl_analysis()
                            except:
                                break
                            kn = -cma0/cla0                        
                            alpha = 0.5
                            while alpha < 4.0:
                                v_max, T_res = maxSpeedWithThrust(CD0,b_ref,s_ref,
                                                                  cla0,cl0,alpha)
                                r2 = cruise_residual(total_mass, v_max, s_ref, cl0, 
                                                     cla0, alpha)
                                #print "V_max: ", v_max, "\n"
                                #print "Residual: ", r2, "\n"
                                if r2 <= 0.0:
                                    cm = cm0 + cma0*alpha
                                    if abs(cm) < abs(cm_best):
                                        if kn > 0.15:
                                            alpha_best = alpha
                                            v_best = v_max
                                            cm_best = cm
                                            residual_best = r2
                                            wing_chord_best = wing_chord
                                            wing_span_best = wing_span
                                            wing_x_offset_best = wing_x_offset
                                            wing_sweep_best = wing_sweep
                                            wing_taper_best = wing_taper
                                            body_chord_best = body_chord
                                            cm0_best = cm0
                                            kn_best = kn
                                            total_mass_best = total_mass
                                            s_ref_best = s_ref
                                            c_ref_best = c_ref
                                            cl0_best = cl0
                                            cla0_best = cla0
                                            print "Alpha: ", alpha, '\n'
                                            print "V: ", v_max, '\n'
                                            print wing_chord_best
                                            print wing_span_best
                                            print wing_x_offset_best
                                            print wing_sweep_best
                                            print wing_taper_best
                                            print body_chord_best
                                            
                                    break
                                else:
                                    alpha = alpha + 0.1
        print "One iter: ", time()-t1, "\n"
    print "Done.\n"