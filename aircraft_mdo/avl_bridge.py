"""
AVL bridge.
"""
import pexpect
import sys
import subprocess
from time import sleep

avl_expect = '[crs]>'
avl_commands = ['']

def avl_file_IO():
    """ Uses subprocess to write AVL forces and stability derivatives to file.
    """
    
    

def subprocess_attempt():
    fout = open('log/avl_test_log1.txt','w+')
    avl = subprocess.Popen(['avl', 'avl/eppler330_config_no_tail'],
                           stdin=subprocess.PIPE, stdout=sys.stdout,
                           stderr=subprocess.PIPE)
    print "Spawned avl."
    #stdout1, stderr1 = avl.communicate('oper')
    # The second time I try to communicate with it, it breaks.
    avl.stdin.write('oper')
    avl.stdin.write('x')
    #avl.stdout.flush()
    
    fout.close()
    avl.terminate()
    
def pexpect_attempt():
    """ 
    Eventually, wrap as its own class.
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
    