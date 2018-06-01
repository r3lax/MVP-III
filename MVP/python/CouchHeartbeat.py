# CouchDB heartbeat
# Check database and if not running, restart
# Restarting CouchDB does not always go clear, reboot is better

import requests
import json
import os
from datetime import tzinfo, datetime

def checkCouchDB(port, test = False):
    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.utcnow())
    print timestamp, " checkCouchDB"
    try:
        r = requests.get('http://localhost:'+port)
        if r.json()["couchdb"] == 'Welcome':
            if test:
                print "Port:", port, "Couch Up"
    except requests.ConnectionError as e:
        if test:
            print "Port:", port, " Couch Down"
            print e
        restart()            
#        startCouchDB(test)            

def startCouchDB(test=False):
    cmd='bash /home/pi/MVP/scripts/startCouchDB.sh'
    os.system(cmd)
    if test:
        print 'Running '+cmd

def restart(test=False):
    cmd='sudo reboot'
    if test:
        Print 'Running', cmd
    os.system(cmd)
    

def test():
    checkCouchDB('5984', True)  

if __name__=="__main__":
    test()
        
