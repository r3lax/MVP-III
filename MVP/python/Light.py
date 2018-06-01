#Light Control
# Author: Howard Webb
# Date: 7/25/2017
#Controls the turning on and turning off of lights
#Lights are wired into Relay #4 (Pin 29)

from Relay import *
from JsonUtil import makeEnvJson
import CouchDB

class Light(object):

    def __init__(self):
        self.r=Relay()        

    def setLightOn(self, test=False):
        "Check the time and determine if the lights need to be changed"
        self.r.setOn(lightPin, test)
        self.logState("On", test)        
        
    def setLightOff(self, test=False):
        '''Turn light relay off'''
        self.r.setOff(lightPin, test)
        self.logState("Off", test)

    def getState(self, test=False):
        return self.r.getState(lightPin, test)
        

    def logState(self, value, test=False):
        status_qualifier='Success'
        if test:
            status_qualifier='Test'
        jsn=makeEnvJson('State_Change', 'Lights', 'Top', 'State', value, 'Lights', status_qualifier)
        CouchDB.logEnvObsvJSON(jsn)

    def test(self):
        print "Test Light"
        print "Light State: ", self.getState(True)
        print "Turn Light On"
        self.setLightOn(True)
        print "Light State: ", self.getState(True)
        print "Turn Light Off"        
        self.setLightOff(True)
        print "Light State: ", self.getState(True)
        print "Turn Light On"        
        self.setLightOn(True)
        print "Light State: ", self.getState(True)
        print "Done"

if __name__=="__main__":
    l=Light()
    l.test()    
                
    

