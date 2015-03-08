""" Blended wing body (BWB) geometry parameterization.
"""
import numpy as np
from math import sin, cos, tan

avl_file_template = 'avl/avl_template.avl'
mass_file_template = 'avl/mass_template.mass'
default_wing_airfoil = 'avl/airfoils/MILEY_M06-13-128.dat'
#default_wing_airfoil = 'avl/airfoils/e330.dat'
default_body_airfoil = 'avl/airfoils/e330.dat'
avl_file_out = 'avl/out/default.avl'
mass_file_out = 'avl/out/default.mass'
default_density = 0.3 # kg/m^2
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
    body_area = 0.5*(body_chord+tran_chord)*body_span
    tran_area = 0.5*(tran_chord+wing_chord)*tran_span
    wing_area = 0.5*(wing_chord+wing_tip_chord)*wing_span
    return (body_area, tran_area, wing_area) 
    
    

# ALL POSITIONS AS CALCULATED FROM THE LOWER RIGHT CORNER OF EACH TRAPEZOID AS 
# YOU SEE FROM THE DIAGRAM GIVEN TO ME
def wingcg(bwing,lambdawing,sweepwing,cwing):
	"""
     Returns cg location as measured from the lower right corner of the 
     trapezoid.
     """
	h = bwing
	a = lambdawing
	b = cwing
	temp1 = cwing-lambdawing-bwing*sin(sweepwing)
	c = (bwing**2 + temp1**2)**0.5
	d = bwing/2*cos(sweepwing)
	xbar = b/2 + (2*a+b)*(c**2-d**2)/6/(b**2-a**2)
	ybar = (b+2*a)*h/(3*(a+b))
	cg = (xbar,ybar)
	return cg


def bodycg(cbody,bbody,bodysweep,ytran):
	a = cbody - (bbody-ytran)*sin(bodysweep)
	b = cbody
	c = (bbody-ytran)
	d = (bbody-ytran)/2*cos(bodysweep)
	h = bbody-ytran
	xbar = b/2 + (2*a+b)*(c**2-d**2)/6/(b**2-a**2)
	ybar = (b+2*a)*h/(3*(a+b))
	cg = (xbar,ybar)
	return cg

def trancg(ytran,cwing,cbody,bbody,sweepbody,xwing):
	b = cbody - (bbody-ytran)*sin(sweepbody)
	h = ytran
	a = cwing
	temp1 = xwing - (bbody-ytran)*sin(sweepbody)
	c = (ytran**2 + temp1**2)**0.5
	temp2 = cbody - cwing - xwing
	d = (ytran**2 + temp2**2)**0.5
	xbar = b/2 + (2*a+b)*(c**2-d**2)/6/(b**2-a**2)
	ybar = (b+2*a)*h/(3*(a+b))
	cg = (xbar,ybar)
	return cg

def wingIxx(bwing,lambdawing,cwing):
	h = bwing
	a = lambdawing
	b = cwing
	Ixx = h**3*(a**2+4*a*b+b**2)/(36*(a+b))
	return Ixx

def wingIyy(bwing,lambdawing,cwing,sweepwing):
	a = lambdawing
	b = cwing
	h = bwing
	c = cwing - lambdawing - bwing*sin(sweepwing)
	Iyy = h*(4*a*b*c**2 + 3*a**2*b*c - 3*a*b**2*c + a**4 + b**4 + 2*a**3*b + \
              a**2*c**2 + a**3*c + 2*a*b**3 - c*b**3 + b**2*c**2)/36/(a+b)
	return Iyy

def wingIzz(bwing,lambdawing,cwing, sweepwing):
	a = lambdawing
	b = cwing
	h = bwing
	c = cwing - lambdawing - bwing*sin(sweepwing)
	Izz = h*(4*h**2*a*b + h**2*b**2 + h**2*a**2 + 4*a*b*c**2 + 3*a**2*b*c - \
              3*a*b**2*c + a**4 + b**4 + 2*a**3*b + a**2*c**2 + a**3*c + 2*a*b**3 - \
              b**3*c + b**2*c**2)/36/(a+b)
	return Izz

def tranIxx(ytran,cwing,cbody,bbody,sweepbody):
	b = cbody - (bbody-ytran)*sin(sweepbody)
	h = ytran
	a = cwing
	Ixx = h**3*(a**2+4*a*b+b**2)/(36*(a+b))
	return Ixx

def tranIyy(ytran,cwing,cbody,bbody,sweepbody,xwing):
	a = cwing
	b = cbody - (bbody-ytran)*sin(sweepbody)
	h = ytran
	c = cbody - cwing - xwing
	Iyy = h*(4*a*b*c**2 + 3*a**2*b*c - 3*a*b**2*c + a**4 + b**4 + 2*a**3*b + \
              a**2*c**2 + a**3*c + 2*a*b**3 - c*b**3 + b**2*c**2)/36/(a+b)
	return Iyy


def tranIzz(ytran,cwing,cbody,bbody,sweepbody,xwing):
	a = cwing
	b = cbody - (bbody-ytran)*sin(sweepbody)
	h = ytran
	c = cbody - cwing - xwing
	Izz = h*(4*h**2*a*b + h**2*b**2 + h**2*a**2 + 4*a*b*c**2 + 3*a**2*b*c - \
              3*a*b**2*c + a**4 + b**4 + 2*a**3*b + a**2*c**2 + a**3*c + 2*a*b**3 - \
              b**3*c + b**2*c**2)/36/(a+b)
	return Izz

def bodyIxx(bbody,ytran,cbody,sweepbody):
	a = cbody - (bbody-ytran)*sin(sweepbody)
	h = bbody-ytran
	b = cbody
	Ixx = h**3*(a**2+4*a*b+b**2)/(36*(a+b))
	return Ixx

def bodyIyy(bbody,xtran,cbody,sweepbody):
	a = cbody - (bbody-xtran)*sin(sweepbody)
	h = bbody-xtran
	b = cbody
	c = 0 #THIS IS A DIFFERENT C FROM THE CG CALCULATIONS
	Iyy = h*(4*a*b*c**2 + 3*a**2*b*c - 3*a*b**2*c + a**4 + b**4 + 2*a**3*b + \
              a**2*c**2 + a**3*c + 2*a*b**3 - c*b**3 + b**2*c**2)/36/(a+b)
	return Iyy

def bodyIzz(bbody,ytran,cbody,sweepbody):
	a = cbody - (bbody-ytran)*sin(sweepbody)
	h = bbody-ytran
	b = cbody
	c = 0 #THIS IS A DIFFERENT C FROM THE CG CALCULATIONS
	Izz = h*(4*h**2*a*b + h**2*b**2 + h**2*a**2 + 4*a*b*c**2 + 3*a**2*b*c -\
              3*a*b**2*c + a**4 + b**4 + 2*a**3*b + a**2*c**2 + a**3*c + 2*a*b**3 -\
              b**3*c + b**2*c**2)/36/(a+b)
	return Izz


def cgfromnose(bwing,lambdawing,sweepwing,cwing,cbody,bbody,bodysweep,ytran,
               xwing):
     """
     Returns cgs of sections relative to nose (aircraft frame in AVL)
     """
     bodycgx, bodycgy = bodycg(cbody,bbody,bodysweep,ytran)
     nosebodycgx = bodycgy
     nosebodycgy = bodycgx - cbody
     trancgx, trancgy = trancg(ytran,cwing,cbody,bbody,bodysweep,xwing)
     nosetrancgx = trancgy + bbody - ytran
     nosetrancgy = trancgy - cbody
     wingcgx, wingcgy = wingcg(bwing,lambdawing,sweepwing,cwing)
     nosewingcgx = bbody + wingcgy
     c = cbody - cwing - xwing
     nosewingcgy = -cbody + c + wingcgx
     return (nosebodycgx, nosebodycgy, nosetrancgx, nosetrancgy, \
             nosewingcgx, nosewingcgy)
    
def write_avl_files(body_chord, body_span, body_sweep, wing_chord, wing_span, 
                    wing_x_offset, wing_sweep, wing_taper, wing_twist, 
                    transition=0.1, wing_airfoil=default_wing_airfoil,
                    body_airfoil=default_body_airfoil, avl_file=avl_file_out,
                    mass_file=mass_file_out, density=default_density):
    """
    Creates .avl and .mass files for AVL. All units are meters and degrees.
    All spanwise (y-directional) variables are half spans. 
    -------
    
    Inputs    
    body_chord - root chord of the body section
    body_span - span of the body section
    body_sweep - sweep of the body in degrees
    wing_chord - 'root' chord of the wing section (also defines body's taper)
    wing_span - span of the wing section
    wing_x_offset - chord-wise offset of the start of the wing
    wing_sweep - wing sweep in degrees
    wing_taper - wing taper
    wing_twist - twist of the wing tip at its end, linearly interpolated
    transition - spanwise length of transition between wing and body
    -------
    """
    # Compute geometry
    tran_y = body_span-transition
    tran_x = tan(body_sweep*np.pi/180.0)*(tran_y)
    tran_c = body_chord - tran_x
    
    wing_tip_c = wing_taper*wing_chord
    wing_tip_x = wing_x_offset + np.tan(wing_sweep*np.pi/180.0)*wing_span
    
    body_span_n = int(round(3.0*(body_span-transition)/0.1))
    tran_span_n = int(round(3.0*(transition)/0.1))
    wing_span_n = int(round(3.0*wing_span/0.1))
         
    (s_body, s_tran, s_wing) = compute_ref_area(body_chord, body_span, tran_c, 
                                                transition, wing_chord, 
                                                wing_span, wing_tip_c)
    s_ref = 2.0*(s_body+s_tran+s_wing)
    b_ref = 2.0*(body_span+wing_span)
    c_ref = s_ref/b_ref
    
    # Create the .avl file by filling in the template
    with open(avl_file_template, 'r') as f_avl:
        s_avl = f_avl.read()
        s_avl_out = s_avl.replace('S_REF', str(s_ref)).\
                          replace('C_REF', str(c_ref)).\
                          replace('B_REF', str(b_ref)).\
                          replace('BODY_ROOT_CHORD', str(body_chord)).\
                          replace('BODY_SPAN_N', str(body_span_n)).\
                          replace('TRANSITION_X_OFFSET', str(tran_x)).\
                          replace('TRANSITION_Y_OFFSET', str(tran_y)).\
                          replace('TRANSITION_CHORD', str(tran_c)).\
                          replace('TRANSITION_SPAN_N', str(tran_span_n)).\
                          replace('WING_X_OFFSET', str(wing_x_offset)).\
                          replace('WING_Y_OFFSET', str(body_span)).\
                          replace('WING_CHORD_ROOT', str(wing_chord)).\
                          replace('WING_SPAN_N', str(wing_span_n)).\
                          replace('TIP_X_OFFSET', str(wing_tip_x)).\
                          replace('FULL_SPAN', str(b_ref/2.0)).\
                          replace('WING_CHORD_TIP', str(wing_tip_c)).\
                          replace('WING_AIRFOIL', wing_airfoil).\
                          replace('BODY_AIRFOIL', body_airfoil).\
                          replace('TWIST', str(wing_twist))
        with open(avl_file, 'w') as f_avl_out:
            f_avl_out.write(s_avl_out)
    # Compute first and second moments of mass 
    (bodycgx, bodycgy, trancgx, \
     trancgy,wingcgx, wingcgy) = cgfromnose(wing_span, wing_taper,
                                            wing_sweep*np.pi/180.0, wing_chord, 
                                            body_chord, body_span, 
                                            body_sweep*np.pi/180.0, tran_y,
                                            wing_x_offset)
    
    Ixx_body = bodyIxx(body_span, tran_y, body_chord, body_sweep*np.pi/180.0)
    Iyy_body = bodyIyy(body_span, tran_x, body_chord, body_sweep*np.pi/180.0)
    Izz_body = bodyIzz(body_span, tran_y, body_chord, body_sweep*np.pi/180.0)
    Ixx_tran = tranIxx(tran_y, wing_chord, body_chord, body_span, 
                       body_sweep*np.pi/180.0)
    Iyy_tran = tranIyy(tran_y, wing_chord, body_chord, body_span, 
                       body_sweep*np.pi/180.0, wing_x_offset)
    Izz_tran = tranIzz(tran_y, wing_chord, body_chord, body_span, 
                       body_sweep*np.pi/180.0, wing_x_offset)                               
    Ixx_wing = wingIxx(wing_span, wing_taper, wing_chord)
    Iyy_wing = wingIyy(wing_span, wing_taper, wing_chord, 
                       wing_sweep*np.pi/180.0)
    Izz_wing = wingIzz(wing_span, wing_taper, wing_chord, 
                       wing_sweep*np.pi/180.0)
    
    # Create the .avl file by filling in the template
    with open(mass_file_template, 'r') as f_mass:
        s_mass = f_mass.read()
        s_mass_out = s_mass.replace('BODY_MASS', str(s_body*density)).\
                            replace('BODY_X', str(bodycgx)).\
                            replace('BODY_Y', str(bodycgy)).\
                            replace('BODY_IXX', str(Ixx_body*density)).\
                            replace('BODY_IYY', str(Iyy_body*density)).\
                            replace('BODY_IZZ', str(Izz_body*density)).\
                            replace('TRAN_MASS', str(s_tran*density)).\
                            replace('TRAN_X', str(trancgx)).\
                            replace('TRAN_Y', str(trancgy)).\
                            replace('TRAN_IXX', str(Ixx_tran*density)).\
                            replace('TRAN_IYY', str(Iyy_tran*density)).\
                            replace('TRAN_IZZ', str(Izz_tran*density)).\
                            replace('WING_MASS', str(s_wing*density)).\
                            replace('WING_X', str(wingcgx)).\
                            replace('WING_Y', str(wingcgy)).\
                            replace('WING_IXX', str(Ixx_wing*density)).\
                            replace('WING_IYY', str(Iyy_wing*density)).\
                            replace('WING_IZZ', str(Izz_wing*density))

        with open(mass_file, 'w') as f_mass_out:
            f_mass_out.write(s_mass_out)
    return 
    
if __name__ == '__main__':
    body_chord = 0.8
    body_span = 0.25
    body_sweep = 15.0
    wing_chord = 0.4
    wing_span = 0.45
    wing_x_offset = 0.3
    wing_sweep = 45.0
    wing_taper = 0.5
    wing_twist = -4.0
    write_avl_files(body_chord, body_span, body_sweep, wing_chord, wing_span,
                    wing_x_offset, wing_sweep, wing_taper, wing_twist)
    