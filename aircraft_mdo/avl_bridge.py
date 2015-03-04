"""
Athena Vortex Lattice (AVL) wrapper using pexpect library. 
AVL must be installed and on the path.
"""

import pexpect
import re

# Reg. expression for AVL console
avl_expect = '[crs]>'
default_file = 'avl/eppler330_config_no_tail'

class AVL():
    
    def __init__(self, avl_filename=default_file):
        """
        Construct a new bridge each time the geometry is modified. Use the 
        'with' statement to avoid leaving the process running.
        """
        self.p = pexpect.spawn('avl ' + avl_filename)
        # Ready the AVL process for execution
        self.expect() # The first instance of c>
        self.p.sendline('oper')
        self.expect()
        
    def expect(self, token=avl_expect):
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
        self.p.sendline('x')        
        self.expect()
        return self.p.before
        
    def get_output_val(self, output, var):
        """
        Extract variable 'var' from string output.
        """
        # Needs +,-,., and E for exponential notation
        match1 = re.search(str(var)+' =[ ]+[\.\-\+0-9E]+', run_output)
        subquery = output[match1.start():match1.end()]
        # Extract the number from the sub-query
        submatch = re.search('[\.\-\+0-9E]+', subquery)
        val = subquery[submatch.start():submatch.end()]
        return float(val) 

    # These encourage this class to be used with a "with" statement        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.p.close(force=True)
        
if __name__ == '__main__':
    #Test basic functionality
    with AVL() as avl:
        param_output = avl.set_parameter('CD', 0.02)
        print param_output
        constraint_output = avl.set_constraint('a', 'a', 0.5)
        print constraint_output
        constraint_output = avl.set_constraint('a', 'a', 3)
        print constraint_output
        run_output = avl.run()
        print run_output
        zref = avl.get_output_val(run_output, 'Zref')
        print zref