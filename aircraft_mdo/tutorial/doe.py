from openmdao.main.api import Assembly
from openmdao.main.api import Component
from openmdao.lib.drivers.api import DOEdriver
from openmdao.lib.doegenerators.api import CSVFile, Uniform
from openmdao.lib.datatypes.api import Float

from openmdao.examples.simple.paraboloid import Paraboloid

from openmdao.lib.casehandlers.api import JSONCaseRecorder

# This tutorial didn't work without defining my own paraboloid compenent.
class ParabolaTest(Component):
    """ Evaluates the equation f(x,y) = (x-3)^2 + xy + (y+4)^2 - 3 """

    # set up interface to the framework
    x = Float(0.0, iotype='in', desc='The variable x')
    y = Float(0.0, iotype='in', desc='The variable y')

    f_xy = Float(0.0, iotype='out', desc='F(x,y)')


    def execute(self):
        """f(x,y) = (x-3)^2 + xy + (y+4)^2 - 3
            Minimum: x = 6.6667; y = -7.3333
        """

        x = self.x
        y = self.y

        self.f_xy = (x-3.0)**2 + x*y + (y+4.0)**2 - 3.0    

class Analysis(Assembly):

    def configure(self):
        self.add('paraboloid', Paraboloid())

        self.add('driver', DOEdriver())
        self.driver.DOEgenerator = Uniform(1000)

        self.driver.add_parameter('paraboloid.x', low=-50, high=50)
        self.driver.add_parameter('paraboloid.y', low=-50, high=50)

        self.driver.add_response('paraboloid.f_xy')

        self.recorders = [JSONCaseRecorder(out='doe.json')]

if __name__ == "__main__":
    #-----------------------------
    # Run analysis
    #-----------------------------
    import os
    from openmdao.lib.casehandlers.api import CaseDataset
    if os.path.exists('doe.json'):
        os.remove('doe.json')

    analysis = Analysis()
    analysis.run()
    import time
    
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib import pyplot as p
    from openmdao.lib.casehandlers.api import caseset_query_to_csv
    from openmdao.lib.casehandlers.api import caseset_query_dump

    case_dataset = CaseDataset('doe.json', 'json')
    #----------------------------------------------------
    # Print out history of our objective for inspection
    #----------------------------------------------------
    case_dataset = CaseDataset('doe.json', 'json')
    data = case_dataset.data.by_case().fetch()

    for case in data:
        print "x: %f, y:%f, f_xy:%s"%(case['paraboloid.x'], case['paraboloid.y'], case['paraboloid.f_xy'])    
        
    #----------------------------------------------------
    # Plot from json object
    #----------------------------------------------------
    data = case_dataset.data.by_variable().fetch()
    x    = data['paraboloid.x']
    y    = data['paraboloid.y']
    f_xy    = data['paraboloid.f_xy']
    p.ion()
    fig = p.figure()
    ax = Axes3D(fig)
    
    every_10 = range(3,len(x))[::10]
    
    
    for i in every_10:
        ax.clear()
        ax.set_xlim(-60,60)
        ax.set_ylim(-60,60)
        ax.set_zlim(-1000,6000)
        ax.grid(False)
    
        #3d surface plot
        ax.plot_trisurf(x[:i],y[:i],f_xy[:i], cmap=cm.jet, linewidth=0.2)
    
        p.draw()
        time.sleep(.005) #slow things down so you can see the changes
    
    p.ioff()
    
    # Convenience functions for writing to csv files, and dumping to screen
    case_dataset = CaseDataset('doe.json', 'json')
    data = case_dataset.data.by_case().fetch()
    
    caseset_query_to_csv(data, filename='doe.csv')
    caseset_query_dump(data)
