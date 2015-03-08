import numpy as np
from matplotlib import pyplot as plt
rho = 1.225
#alpha given in deg.
V = [0.00,2.00,4.00,6.00,8.00,10.0,12.0,14.0,15.0]
T = [6.50,6.25,6.00,5.75,5.50,5.20,4.80,4.40,4.20]

#Interpolate the thrust curve:
V_interp = np.arange(0,15.0,0.1)    #Arbitrarily set.
T_interp = np.interp(V_interp,V,T)

def maxSpeedWithThrust(CD0,b,S,CLa,CL0,alpha,e=0.8):
    #Calculate aspect ratio
    AR = b**2/S
    K = 1/(np.pi*e*AR)
    #Generate D curve
    V = V_interp
    D = (CD0 + K*(CL0 + CLa*alpha*np.pi/180.0)**2)*S*0.5*rho*V**2
    plt.figure()
    plt.plot(V_interp, D, 'b*')
    plt.grid()
    plt.plot(V_interp, T_interp, 'r--')
    plt.legend(('Drag', 'Thrust Available'))
    plt.xlabel('V (m/s)')
    plt.ylabel('Force (N)')
    #Find the index of where delta is minimized:
    delta = abs(T_interp-D)
    V_index = np.argmin(delta)
    T_res = D[V_index] - T_interp[V_index]
    #Determine V at the index of minimum delta:
    Vmax = V_interp[V_index]
    return Vmax, T_res   
    
if __name__ == '__main__':
    CD0 = 0.04
    e = 1.0
    b = 1.3
    S = 0.7
    CLa = 0.0524*180/np.pi
    CL0 = 0.01
    alpha = 3.0
    print maxSpeedWithThrust(CD0,b,S,CLa,CL0,alpha)