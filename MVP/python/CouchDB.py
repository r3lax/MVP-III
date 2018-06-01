import requests
import json

def logEnvObsvJSON(jsn):
    headers = {'content-type': 'application/json'}
#    r = requests.post('http://localhost:5984/env_obsv', data = jsn, headers=headers)
    r = requests.post('http://python_user:TopFarmDog!!@openagcloud.media.mit.edu:5984/webbhm_env_obsv', data = json.dumps(jsn), headers=headers)
    return getStatus(r)

def getStatus(msg):
    print msg
    return True

    
def test():
    pass

if __name__=="__main__":
    test()    
