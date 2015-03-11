"""
Cruise Analysis
Call CruiseAnalysis(V_Cruise,W,S,rh0,CLa,CL0) to obtain Cruise CL,and the 
required alpha given motocalc and AVL/XFLR5 lift slope info.
"""

import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.optimize import fsolve

rho = 1.225
#alpha given in deg.
V = [0.00,2.00,4.00,6.00,8.00,10.0,12.0,14.0,15.0,16.0]
T = [6.50,6.25,6.00,5.75,5.50,5.20,4.80,4.40,4.20,3.8]
#Interpolate the thrust curve:
V_interp = np.arange(0,16.0,0.1)    #Arbitrarily set.
T_interp = np.interp(V_interp,V,T)
T_spline = UnivariateSpline(V,T)

# 10x5
V_10x5 = [0,   2,   4,   6,   8,   10,  12,  14, 15.0,15.5]
T_10x5 = [8.2, 7.8, 7.4, 6.95,6.3, 5.55,4.6, 3.6,2.95,2.65]
T_interp = np.interp(V_interp,V_10x5,T_10x5)
T_spline = UnivariateSpline(V_10x5,T_10x5)


def get_thrust_available(v):
    return T_spline(v)
    
    
class CruiseSolver():
    """ 
    Used to solve for cruise alpha, velocity.
    """
    def __init__(self, M, S, b, cl0, cla, cd0=0.04, e=0.8):
        self.W = M*9.81
        self.b = b
        self.S = S
        self.cl0 = cl0
        self.cla = cla
        self.cd0 = cd0
        self.e = e
        self.AR = b**2/S
        self.K = 1/(self.AR*self.e*np.pi)
        
    def get_cruise_alpha(self, v):
        return (2*self.W/(rho*v**2*self.S) - self.cl0)/self.cla        
        
    def get_cruise_v(self, alpha):
        return np.sqrt((2*self.W)/(rho*self.S*(self.cl0 + alpha*self.cla)))        
        
    def compute_drag(self, alpha, v):
        
        return (self.cd0 + self.K*(self.cl0 + alpha*self.cla)**2)*\
                0.5*rho*v**2*self.S
    
    def thrust_differential(self, alpha):
        v = self.get_cruise_v(alpha)
        D = self.compute_drag(alpha, v)
        T = get_thrust_available(v)
        return T - D
    def solve_cruise_alpha(self):
        alpha = fsolve(self.thrust_differential, 0.2)
        v = self.get_cruise_v(alpha)
        return alpha, v[0]

def cruise_residual(m, v_cruise, s_ref, cl0, cla, alpha):
    return 9.81*m - 0.5*1.225*v_cruise**2*s_ref*(cl0 + cla*alpha)
    
def alpha_cruise(V_Cruise,W,S,CLa,CL0):
	#V_Cruise = 15.5; #m/s (from motoCalc)
	#W = 2*9.8;      #kg
	#S = 0.62;   #m**2
	#rh0 = 1.225;

	#Using input arguments we calcuate
	#the required CL for steady level flight.
	CL=CL_Cruise(W,S,V_Cruise)
	alphaCruise = CruiseAlpha(CL0,CLa,CL) #in degrees
	return (CL,alphaCruise)

def CL_Cruise(W,S,V_Cruise):
	CL = 2*W/(S*rho*V_Cruise**2)
	return CL
	
def CruiseAlpha(CL0,CLa,CL):
	alpha = (CL-CL0)/CLa
	return alpha

def maxSpeedWithThrust(CD0,b,S,CLa,CL0,alpha,e=0.8):
    #Calculate aspect ratio
    AR = b**2/S
    K = 1/(np.pi*e*AR)
    #Generate D curve
    V = V_interp
    # Had *np.pi/180 below... probably wrong
    D = (CD0 + K*(CL0 + CLa*alpha)**2)*S*0.5*rho*V**2
#    plt.figure()
#    plt.plot(V_interp, D, 'b*')
#    plt.grid()
#    plt.plot(V_interp, T_interp, 'r--')
#    plt.legend(('Drag', 'Thrust Available'))
#    plt.xlabel('V (m/s)')
#    plt.ylabel('Force (N)')
    #Find the index of where delta is minimized:
    delta = abs(T_interp - D)
    V_index = np.argmin(delta)
    T_res = D[V_index] - T_interp[V_index]
    #Determine V at the index of minimum delta:
    Vmax = V_interp[V_index]
    return Vmax, T_res   

if __name__ == '__main__':
    CD0 = 0.04
    b = 1.2333
    S = 0.519
    #CLa = 0.0524*180/np.pi
    CLa = 0.04965
    CL0 = 0.0483
    alpha = 3.6
    print maxSpeedWithThrust(CD0,b,S,CLa,CL0,alpha)
    V_Cruise = 14.9 #m/s (from motoCalc)
    W = 1.622*9.8      #kg
    S = 0.5193   #m**2
    rh0 = 1.225
    rho = 1.225
    CLa = 3.2659
    CL0 = -0.02
    CL_Cruise,alphaCruise = alpha_cruise(V_Cruise,W,S,CLa,CL0)
    print CL_Cruise, alphaCruise