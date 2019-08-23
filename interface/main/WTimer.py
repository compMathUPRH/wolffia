'''
Created on Jan 24, 2013

@author: jse
'''

import inspect, time

class WTimer(object):
    '''
    classdocs
    '''


    def __init__(self, id=""):
        '''
        Constructor
        '''
        self.caller = inspect.stack()[1][3]
        self.callersCaller = inspect.stack()[2][3]
        self.start = time.clock()
        self.id = id


    def report(self):
        print("Timer(", self.id,"): ", time.clock()-self.start, " from ", self.caller, " called from ", self.callersCaller)
    
#--------------------------------------------------------------------------------

def aMethod():
    t = WTimer()
    t.report()

if __name__ == '__main__' or __name__ == 'interface.main.Wolffia':
    aMethod()