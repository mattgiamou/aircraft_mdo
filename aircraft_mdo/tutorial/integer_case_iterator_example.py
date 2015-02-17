import numpy as np

from openmdao.main.api import Assembly, Component
from openmdao.lib.drivers.api import CaseIteratorDriver
from openmdao.lib.datatypes.api import Float, Int

from openmdao.lib.casehandlers.api import JSONCaseRecorder

class IntTest(Component): 
    x = Int(0, iotype='in', desc='x coord')
    y = Int(0, iotype='in', desc='y coord')

    brightness = Int(iotype='out', desc='brightness at location')

    def execute(self): 
        self.brightness = self.x + self.y

class Analysis(Assembly):

    def configure(self):
        self.add('test', IntTest())

        self.add('driver', CaseIteratorDriver())

        self.driver.add_parameter('test.x', low=-50, high=50)
        self.driver.add_parameter('test.y', low=-50, high=50)

        self.driver.add_response('test.brightness')

        self.driver.case_inputs.test.x = list(np.random.randint(0,10,20))
        self.driver.case_inputs.test.y = list(np.random.randint(0,10,20))

if __name__ == "__main__":

    import time

    analysis = Analysis()

    tt = time.time()
    analysis.run()

    print "Elapsed time: ", time.time()-tt, "seconds"

    x = analysis.driver.case_inputs.test.x
    y = analysis.driver.case_inputs.test.y
    f_xy = analysis.driver.case_outputs.test.brightness

    for i in range(0, len(x)):
        print "x: {} y: {} f(x, y): {}".format(x[i], y[i], f_xy[i])