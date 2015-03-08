"""
Athena Vortex Lattice (AVL) wrapper using pexpect library. 
AVL must be installed and on the path.

TODO: Make XFOIL version as well!!
TODO: Create standard configuration geometry code (like bwb_geometry.py).
"""

import pexpect
import re
import numpy as np
from matplotlib import pyplot as plt
from time import time

# Reg. expression for AVL console
avl_expect = '[crs]>'
default_file = 'avl/out/default'

class AVL():
    
    def __init__(self, avl_filename=default_file):
        """
        Construct a new bridge each time the geometry is modified. Use the 
        'with' statement to avoid leaving the process running.
        """
        self.p = pexpect.spawn('avl ' + avl_filename)
        # Ready the AVL process for execution
        self.expect() # The first instance of c>
        self.p.sendline('mset 0') # Set the c.g. from the mass file
        self.expect()
        self.p.sendline('oper')
        self.expect()
        
    def expect(self, token=avl_expect):
        """
        Convenience method. Advances the reader along the output stream until
        'token' or EOF is found. The string between the 2nd last expect() 
        call's token and the last expect() call's token is available as 
        "p.before".
        """
        self.p.expect(token)
        
    def set_parameter(self, param, value):
        """
        Sets a parameter in AVL.
        """
        self.p.sendline('m')
        self.expect()
        self.p.sendline(param)
        self.expect()
        self.p.sendline(str(value))
        self.expect()
        self.p.sendline()
        self.expect()
        return self.p.before
    
    def set_constraint(self, param, constrainer, constraint):
        """
        Sets a constraint in AVL.
        E.g.: param = 'a', constrainer = 'c', constraint = 0.2 would constrain
        alpha such that CL = 0.2.
        """
        self.p.sendline(param+' '+constrainer+' '+str(constraint))
        self.expect()
        return self.p.before
        
    def run(self):
        """
        Returns aerodynamics and stability values.
        """
        # Execute AVL's solver for current parameters and constraints
        self.p.sendline('x')        
        self.expect()
        
        # Extract aerodynamic coefficients
        output = self.p.before
        CL = self.get_output_val(output, 'CLtot')
        CD = self.get_output_val(output, 'CDtot')
        CM = self.get_output_val(output, 'Cmtot')
        e = self.get_output_val(output, 'e')
        # Extract stability derivatives
        self.p.sendline('st')
        self.expect()
        self.p.sendline()
        self.expect()
        stab_output = self.p.before
        # These have output unit of inverse radians, convert to degrees
        CL_alpha = self.get_output_val(stab_output, 'CLa')*np.pi/180.0
        CM_alpha = self.get_output_val(stab_output, 'Cma')*np.pi/180.0
        
        return (CL, CD, CM, CL_alpha, CM_alpha, e)
        
        
    def get_output_val(self, output, var):
        """
        Extract variable 'var' from string output.
        """
        # Needs +,-,., and E (for exponential notation)
        match1 = re.search(str(var)+' =[ ]+[\.\-\+0-9E]+', output)
        subquery = output[match1.start():match1.end()]
        # Extract the number from the sub-query
        submatch = re.search('[\.\-\+0-9E]+', subquery)
        val = subquery[submatch.start():submatch.end()]
        return float(val) 

    # These encourage this class to be used with a "with" statement        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        """ 
        Closes the AVL process.
        """
        self.p.close(force=True)
        
def avl_analysis(filename=default_file):
    """
    Compute moment and lift vs. alpha as well as static margin, surface area, 
    mean chord, etc. 
    """
    with AVL(filename) as avl:
        avl.set_constraint('a', 'a', 0.0)
        cl0,cd0,cm0,cla0,cma0 = avl.run()
        
    return (cl0, cm0, cla0, cma0)
        
if __name__ == '__main__':
    # Test basic functionality (with ensures that the AVL process is closed on 
    # exit)
    with AVL() as avl:
        param_output = avl.set_parameter('CD', 0.04)
        #print param_output
        constraint_output = avl.set_constraint('a', 'a', 0.5)
        #print constraint_output
        constraint_output = avl.set_constraint('a', 'a', 3)
        #print constraint_output
        run_output = avl.run()
        #print run_output
        
    with AVL(default_file) as avl:
        N = 11
        alpha = np.linspace(0, 10, N)
        CL = np.zeros(alpha.shape)
        CD = np.zeros(CL.shape)
        CM = np.zeros(CL.shape)
        E = np.zeros(CL.shape)
        avl.set_parameter('v', 11)
        #avl.set_parameter('x', 0.2)
        for idx in xrange(0, N):
            t = time()
            avl.set_constraint('a','a',alpha[idx])
            cl,cd,cm,cla,cma, e = avl.run()
            CL[idx] = cl
            CD[idx] = cd
            CM[idx] = cm
            E[idx] = e
            print "Static margin: ", str(-cma/cla), '\n'
            #print 'Time: ', (time()-t), ' s\n'
            
#        avl.set_constraint('a', 'a', 0.0)
#        cl0,cd0,cm0,cla0,cma0 = avl.run()
#        avl.set_constraint('a', 'a', 5.0)
#        cl1,cd1,cm1,cla1,cma1 = avl.run()
#        print "CL0: ", cl0, '\n'
#        print "Cma_0: ", cma0, '\n'
#        print "CLa_0: ", cla0, '\n'
#        print "Cma avg: ", (cm1-cm0)/5.0, '\n'
#        print "CLa avg: ", (cl1-cl0)/5.0, '\n'
#        print "Cma_1: ", cma1, '\n'
#        print "CLa_1: ", cla1, '\n'
        
        plt.figure()
        plt.plot(alpha, CL)
        plt.grid()
        plt.plot(alpha,CD)
        plt.plot(alpha, CM)
        plt.plot(alpha, E)
        plt.xlabel('alpha (deg)')
        plt.legend(('CL','CD','CM', 'e'))
        