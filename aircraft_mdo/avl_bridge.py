"""
AVL bridge using pexpect.
"""
import pexpect

avl_expect = '[crs]>'

class AVL():
    avl_expect = '[crs]>'
    
    def __init__(self, avl_filename):
        """
        Construct a new bridge each time the geometry is modified. Use the 
        'with' statement to avoid leaving the process running.
        """
        self.p = pexpect.spawn('avl ' + avl_filename)
        
    def set_parameter(self, param, value):
        """
        Sets a parameter in AVL.
        """
        pass
    
    def set_constraint(self, param, constrainer, constraint):
        """
        Sets a constraint in AVL.
        E.g.: param = 'a', constrainer = 'c', constraint = 0.2 would constrain
        alpha such that CL = 0.2
        """
        pass
    
    def run(self):
        """
        Returns aerodynamics and stability values.
        """
        pass        
        

    # These encourage this class to be used with a "with" statement        
    def __enter__(self):
        return self
        
    def __exit__(self):
        self.p.close(force=True)
        
def pexpect_attempt():
    """ 
    For testing pexpect with AVL.
    """
    avl = pexpect.spawn('avl avl/eppler330_config_no_tail')
    fout = open('log/avl_test_log1.txt','w+')
    avl.logfile_read = fout # or sys.stdout for screen
    print "Spawned process."
    avl.expect(avl_expect)
    avl.sendline('oper')
    print "Sent oper. \n"
    avl.expect(avl_expect)
    avl.sendline('m')
    avl.expect(avl_expect)
    avl.sendline('v')
    avl.expect(avl_expect)
    avl.sendline('15')
    avl.expect(avl_expect)
    avl.sendline('')
    avl.expect(avl_expect)
    avl.sendline('x')
    avl.expect(avl_expect)
    avl.sendline('st')
    avl.expect(avl_expect)
    avl.sendline(' ')
    avl.expect(avl_expect)
    print avl.before   
    avl.close(True)    
    fout.close()
    print "\nClosed process."
    
if __name__ == '__main__':
    pexpect_attempt()
    