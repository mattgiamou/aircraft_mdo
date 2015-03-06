""" Blended wing body (BWB) geometry parameterization.
"""
import numpy as np

avl_file_template = 'avl/avl_template.avl'
mass_file_template = 'avl/mass_template.mass'

def compute_mass():
    """ Used to estimate the empty mass of the plane. Should scale up with 
    surface area of body and wings in some principled manner. 
    """
    electronics = 0.3
    
    mass = electronics
    return mass
    
def compute_ref_area(body_chord, body_span, tran_chord, tran_span, wing_chord,
                     wing_span, wing_tip_chord):
    """
    Simple sum of 3 trapezoids.
    """                     
    return 0.5*( (body_chord+tran_chord)*body_span + \
                 (tran_chord+wing_chord)*tran_span + \
                 (wing_chord+wing_tip_chord)*wing_span) )
    
    
def write_avl_files(body_chord, body_span, body_sweep, wing_chord, wing_span, 
                    wing_x_offset, wing_sweep, wing_taper, wing_twist, 
                    transition=0.1):
    """
    Creates .avl and .mass files for AVL. All units are meters and degrees.
    -------
    Inputs    
    body_chord - root chord of the body section
    body_span - span of the body section
    body_sweep - x-offset of the body's terminal point (linearly interpolated)
    wing_chord - 'root' chord of the wing section (also defines body's taper)
    wing_span - span of the wing section
    wing_x_offset - chord-wise offset of the start of the wing
    wing_sweep - x-offset of the wing's terminal point (linearly interpolated)
    wing_taper - chord at the tip (i.e. not literally taper, but defines it)
    wing_twist - twist of the wing tip at its end, linearly interpolated
    transition - spanwise length of transition between wing and body
    -------
    """
    
    tran_x = np.tan(body_sweep*np.pi/180.0)*(body_span-transition)
    tran_y = body_span-transition
    tran_c = body_chord - tran_x
    
    wing_tip_c = wing_taper*wing_chord
    wing_tip_y = body_span + wing_span
    wing_tip_x = wing_x_offset + np.tan(wing_sweep*np.pi/180.0)

    
    body_span_n = round(3.0*(body_span-transition)/0.1)
    tran_span_n = round(3.0*(transition)/0.1)
    wing_span_n = round(3.0*wing_span/0.1)
         
    s_ref = compute_ref_area(body_chord, body_span, tran_c, transition,
                             wing_chord, wing_span, wing_tip_c)
    b_ref = body_span+wing_span
    c_ref = s_ref/b_ref
    
    with open(avl_file_template, 'r') as f_avl:
        s_avl = f_avl.read()
        s_avl_out = s_avl.replace('S_REF', str(s_ref)).\
                          replace('C_REF', str(c_ref)).\
                          replace('B_REF', str(b_ref)).\
                          replace('BODY_ROOT_CHORD', str(body_chord)).\
                          replace('BODY_SPAN_N', str(body_span_n)).\
                          
    