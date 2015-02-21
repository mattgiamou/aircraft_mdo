from openmdao.main.api import ArchitectureAssembly
from aer406_cost_function import FlightScore, cargo_units

class LoadOptimization(ArchitectureAssembly):
    """ Test architecture for simple cost function optimization.
    """
    
    def configure(self):
        #add the discipline components to the assembly
        self.add('flight_score', FlightScore())

        #START OF MDAO Problem Definition
        #Global Des Vars
        self.add_parameter("flight_score.t_balls", name="t_balls", low=0, 
                           high=10, start=5)
        self.add_parameter("flight_score.g_balls", name="g_balls", low=0, 
                           high=24, start=5)
        self.add_parameter("flight_score.p_balls", name="p_balls", low=0, 
                           high=120, start=10)                           
                           
        #Local Des Vars
        self.add_parameter("flight_score.v", low=0, high=30, start=12.0)
        self.add_parameter("flight_score.empty_mass", low=0.1, high=2.0, 
                           start = 0.8)
        #Coupling Vars
        #self.add_coupling_var(("dis2.y1","dis1.y1"), name="y1", start=1.0)
        #self.add_coupling_var(("dis1.y2","dis2.y2"), name="y2", start=1.0)

        self.add_objective('-flight_score.flight_score', name="flight_score")
        self.add_constraint('120*flight_score.t_balls +' 
                            '50*flight_score.g_balls + 10*flight_score.p_balls <= 1200.0')
        self.add_constraint('flight_score.v < 20*flight_score.empty_mass')
    
if __name__ == '__main__':
    from openmdao.lib.architectures.api import IDF, MDF, CO, BLISS, BLISS2000

    def display_results():
        print "Maximum: ", problem.flight_score.flight_score
        print "Max found at (%f, %f, %f)" % (problem.flight_score.t_balls,
                                        problem.flight_score.g_balls,
                                        problem.flight_score.p_balls)
        print "Local vars: %f, %f" % (problem.flight_score.v, problem.flight_score.empty_mass)
        print "Function calls: %d"%(problem.flight_score.exec_count)
        print "\n"

    print "Running LoadOptimization with MDF"
    problem = LoadOptimization()
    problem.architecture = MDF()
    problem.run()

    display_results()
