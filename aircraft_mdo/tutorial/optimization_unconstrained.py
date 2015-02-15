from openmdao.main.api import Assembly
from openmdao.lib.drivers.api import SLSQPdriver
from openmdao.examples.simple.paraboloid import Paraboloid

class OptimizationUnconstrained(Assembly):
    """Unconstrained optimization of the Paraboloid Component."""

    def configure(self):

        # Create Optimizer instance
        self.add('driver', SLSQPdriver())

        # Create Paraboloid component instances
        self.add('paraboloid', Paraboloid())

        # Iteration Hierarchy
        self.driver.workflow.add('paraboloid')

        # SLSQP Flags
        self.driver.iprint = 0

        # Objective
        self.driver.add_objective('paraboloid.f_xy')

        # Design Variables
        self.driver.add_parameter('paraboloid.x', low=-50., high=50.)
        self.driver.add_parameter('paraboloid.y', low=-50., high=50.)
        
if __name__ == "__main__":

    opt_problem = OptimizationUnconstrained()

    import time
    tt = time.time()

    opt_problem.run()

    print "\n"
    print "Minimum found at (%f, %f)" % (opt_problem.paraboloid.x, \
                                     opt_problem.paraboloid.y)
    print "Elapsed time: ", time.time()-tt, "seconds"