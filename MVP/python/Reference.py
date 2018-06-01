import json
# Author: Howard Webb
# Data: 7/25/2017

import MySQLdb as mdb
import MySQLdb.cursors
import sys
from config import config
import json

python_dir=config['python_dir']
ref_file=python_dir + 'reference.py'

def getRef():
    ref={}
    ref['Environment_Subject']=getEnvironSubject()
    ref['Phenotype_Subject']=getPhenoSubject()    
    ref['Field_Location']=getFieldLocation()
    ref['Environment_Attribute']=getEnvironmentAttribute()
    ref['Participant']=getDevice()
    ref['Phenotype_Attribute']=getPhenoAttribute()
    ref['Status']=getStatus()
    ref['Status_Qualifier']=getStatusQualifier()
    saveDict('ref', ref_file, ref)    
    return ref

def getEnvironSubject():
    sql="SELECT name, environment_subject_id from MarsFarm.Environment_Subject;"
    dic={}
    rows=getSQLResults(sql)
    for row in rows:
        dic[row['name']]={'id':int(row['environment_subject_id'])}
    return dic

def getPhenoSubject():
    sql="SELECT name, phenotype_subject_id from MarsFarm.Phenotype_Subject;"
    dic={'Plant':{'id': 1}, 'Leaf':{'id':2}}
    return dic
    rows=getSQLResults(sql)
    for row in rows:
        dic[row['name']]={'id':int(row['environment_subject_id'])}
    return dic


def getFieldLocation():
    sql="SELECT name, location_id from MarsFarm.Field_Location;"
    dic={}
    rows=getSQLResults(sql)
    for row in rows:
        dic[row['name']]={'id':int(row['location_id'])}
    return dic

def getEnvironmentAttribute():
    sql="SELECT name, environment_attribute_id from MarsFarm.Environment_Attribute;"
    dic={}
    rows=getSQLResults(sql)
    for row in rows:
        dic[row['name']]={'id':int(row['environment_attribute_id'])}
    return dic

def getDevice():
    sql="SELECT name, device_id from MarsFarm.Device;"
    dic={}
    rows=getSQLResults(sql)
    for row in rows:
        dic[row['name']]={'id':int(row['device_id'])}
    return dic       

def getParticipantRole():
    '''This is really 'Device_Participant', the name is not the device name, as name needs to be unique'''
    sql="SELECT participant as name, participant_id, device, device_description, location from MarsFarm.Device_Participant_Role_View;"
    dic={}
    rows=getSQLResults(sql)
    for row in rows:
        dic[row['name']]={'uuid':int(row['participant_id']), 'participant':{'type':'Device', 'Device':{'name':row['device'], 'description':row['device_description'], 'location':{'name':row['location']}}}}
    return dic       

def getStatus():
    status= {'In Process': {'id':1}, 'Complete':{'id':2}, 'Canceled':{'id':3}, 'Unknown':{'id':4}}
    return status
             
def getStatusQualifier():
    sql="SELECT name, status_qualifier_id from MarsFarm.Status_Qualifier;"
    dic={}
    rows=getSQLResults(sql)
    for row in rows:
        dic[row['name']]={'id':int(row['status_qualifier_id'])}
    return dic  

def getPhenoAttribute():
    sql="SELECT name, phenotype_attribute_id from MarsFarm.Phenotype_Attribute;"
    dic={}
    rows=getSQLResults(sql)
    for row in rows:
        dic[row['name']]={'id':int(row['phenotype_attribute_id'])}
    return dic

def getSQLResults(sql):
    try:
        db=mdb.connect('localhost', 'admin', 'raspberrY', 'MarsFarm', cursorclass=MySQLdb.cursors.DictCursor)
        #cursor=db.cursor(cursors.DictCursor)
        cursor=db.cursor()            
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

    except:
        print(sql)
        print(sys.exc_info()[2])
        raise
 
    finally:
        cursor.close()
        db.close()

def saveDict(name, file_name, dict):
    #print(values)
    f = open(file_name, 'w+')
    tmp=name+'='+str(dict)
    f.write(tmp)
    f.close()

def prettyPrint(txt):
    '''Dump json in nice format'''
    #print type(txt)
    print json.dumps(txt, indent=4, sort_keys=True)    
     
def dumpRef():
    from reference import ref
    prettyPrint(ref)

def test():
    print "Test Ref build"
    part=getParticipantRole()
    prettyPrint(part)

def test2():
    print "Reload Participant"
    part=getParticipantRole()
    from reference import ref
    ref['Participant']=part
#    del ref['Device']
    saveDict('ref', ref_file, ref)
    prettyPrint(ref)

if __name__=="__main__":
    dumpRef() 

