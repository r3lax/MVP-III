#Light Control
# Author: Howard Webb
# Date: 7/25/2017
# Consideration was given to making "Light" an object, but the overhead of code (loading multiple functions) compared to the time this runs does not justify the overhead.
#Controls the turning on and turning off of lights
#Lights are wired into Relay #4 (Pin 29)

import RPi.GPIO as GPIO
import time

ON=1
OFF=0

Relay1 = 29 # Fan
Relay2 = 31
Relay3 = 33 # LED
Relay4 = 35 # Solenoid

class Relay(object):

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(Relay1, GPIO.OUT)
        GPIO.setup(Relay2, GPIO.OUT)
        GPIO.setup(Relay3, GPIO.OUT)
        GPIO.setup(Relay4, GPIO.OUT)        
    
    def setState(self, pin, state):
        '''Change state if different'''
#        print "Current ", state, GPIO.input(pin)
        if state==ON and not GPIO.input(pin):
            self.setOn(pin)
        elif state==OFF and GPIO.input(pin):
            self.setOff(pin)
        else:        
 #           print("No Change")
            pass

    def getState(self, pin):
        '''Get the current state of the pin'''
        state=GPIO.input(pin)
        return state

    def setOff(self, pin, test=False):
        GPIO.output(pin, GPIO.LOW)
        if test:
            print("Pin ", pin, " Off")
            
    def setOn(self, pin, test=False):
        GPIO.output(pin, GPIO.HIGH)
        if test:
            print("Pin ", pin, " On")

    def test(self, test=False):
        
        print "Test"
        print "Read #3 Unknown: ", self.getState(Relay3)
        print "Test Fan and Lights"
        print "Turn Fan On"
        self.setOn(fanPin, True)
        time.sleep(5)
        print "Turn Light On"
        self.setState(lightPin, True)
        time.sleep(5)
        print "Turn Fan Off"
        self.setOff(fanPin, True)
        time.sleep(5)        
        print "Turn Light Off"
        self.setOff(lightPin, True)
        time.sleep(5)

        print "Conditional Turn Fan On"
        self.setState(fanPin, ON, True)
        time.sleep(5)        
        print "Conditional Turn Fan On"
        self.setState(fanPin, ON, True)
        time.sleep(5)
        print "Conditional Turn Fan Off"
        self.setState(fanPin, OFF, True)
        time.sleep(5)        
        print "Conditional Turn Fan Off"
        self.setState(fanPin, OFF, True)

    def test1(self):
        self.setState(Relay1, ON)
        self.setState(Relay1, OFF)
        self.setState(Relay2, ON)
        self.setState(Relay2, OFF)
        self.setState(Relay3, ON)
        self.setState(Relay3, OFF)
        self.setState(Relay4, ON)
        self.setState(Relay4, OFF)

    def test2(self):
        print "Test 2"
        print "Read #3 Unknown: ", self.getState(Relay3)
        print "Turn On"
        self.setState(Relay3, ON)
        print "Turn On"
        self.setState(Relay3, ON)

#        print "Read #3 On: ", self.getState(Relay3)    
        print "Turn Off"
        self.setState(Relay3, OFF)
        print "Turn Off"
        self.setState(Relay3, OFF)
        time.sleep(5)
#        print "Read #3 Off: ", self.getState(Relay3)    
        print "Turn On"
        self.setState(Relay3, ON)
#        print "Read #3 On: ", self.getState(Relay3)
        print "Turn Off"
        self.setOff(Relay3)

        print "Turn On"
        self.setOn(Relay3)

if __name__=="__main__":
    r=Relay()
    r.test()    
    
            
    

