from openmdao.main.api import ArchitectureAssembly
from openmdao.lib.optproblems.sellar import Discipline1, Discipline2

class SellarProblem(ArchitectureAssembly):
    """ Sellar test problem definition.
    Creates a new Assembly with this problem

    Optimal Design at (1.9776, 0, 0)
    Optimal Objective = 3.18339"""

    def configure(self):
        #add the discipline components to the assembly
        self.add('dis1', Discipline1())
        self.add('dis2', Discipline2())

        #START OF MDAO Problem Definition
        #Global Des Vars
        self.add_parameter(("dis1.z1","dis2.z1"), name="z1", low=-10, high=10, start=5.0)
        self.add_parameter(("dis1.z2","dis2.z2"), name="z2", low=0, high=10, start=2.0)

        #Local Des Vars
        self.add_parameter("dis1.x1", low=0, high=10, start=1.0)

        #Coupling Vars
        self.add_coupling_var(("dis2.y1","dis1.y1"), name="y1", start=1.0)
        self.add_coupling_var(("dis1.y2","dis2.y2"), name="y2", start=1.0)

        self.add_objective('(dis1.x1)**2 + dis1.z2 + dis1.y1 + math.exp(-dis2.y2)', name="obj1")
        self.add_constraint('3.16 < dis1.y1')
        self.add_constraint('dis2.y2 < 24.0')


        #END OF Sellar Problem Definition


if __name__=="__main__":

    from openmdao.lib.architectures.api import IDF, MDF, CO, BLISS, BLISS2000

    def display_results():
        print "Minimum found at (%f, %f, %f)" % (problem.dis1.z1,
                                        problem.dis1.z2,
                                        problem.dis1.x1)
        print "Couping vars: %f, %f" % (problem.dis1.y1, problem.dis2.y2)
        print "Function calls dis1: %d, dis2: %d"%(problem.dis1.exec_count,problem.dis2.exec_count)
        print "\n"

    print "Running SellarProblem with MDF"
    problem = SellarProblem()
    problem.architecture = MDF()
    problem.run()

    display_results()

    print "Running SellarProblem with CO"
    problem = SellarProblem()
    problem.architecture = CO()
    problem.run()

    display_results()

    print "Running SellarProblem with BLISS"
    problem = SellarProblem()
    problem.architecture = BLISS()
    problem.run()

    display_results()

    print "Running SellarProblem with BLISS2000"
    #Note that BLISS2000 is stochastic and unstable and does not reliably converge
    # you might get an OverflowError
    problem = SellarProblem()
    problem.architecture = BLISS2000()
    problem.run()

    display_results()

    print "Running SellarProblem with IDF"
    problem = SellarProblem()
    problem.architecture = IDF()
    problem.run()

    display_results()