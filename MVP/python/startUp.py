# Check status on boot
# Check lights correctly set
# Make sure Solenoid is closed

from Light import *
from env import env
from datetime import datetime

def check(test=False):
    checkLight(test)

def checkLight(test=False):
    # Get times from env and split into components
    s=env['Lights']['On']
    s=s.split(':')
    e=env['Lights']['Off']
    e=e.split(':')
    # Munge date into times
    t=datetime.now()
    st=t.replace(hour=int(s[0]), minute=int(s[1]), second=int(s[2]))
    et=t.replace(hour=int(e[0]), minute=int(e[1]), second=int(e[2]))
    if test:
        print "Start Time: ", st
        print "End Time: ", et
    l=Light()
    msg="Lights should be On"
    if (st < datetime.now()) and (et > datetime.now()):
        l.setLightOn()
    else:
        msg="Lights should be Off"
        l.setLightOff(test)
    if test:
        print msg

def test():
    print 'Test'
    print 'Time: ', datetime.now()
    s=env['Lights']['On']
    s=s.split(':')
    e=env['Lights']['Off']
    e=e.split(':')

    t=datetime.now()
    st=t.replace(hour=int(s[0]), minute=int(s[1]), second=int(s[2]))
    et=t.replace(hour=int(e[0]), minute=int(e[1]), second=int(e[2]))
    print "Start: ", st
    print "End: ", et    
    if (st < datetime.now()) and (et > datetime.now()):
        print "Lights should be on"
    else:
        print "Lights should be off"

if __name__=="__main__":
    check(True)
     
