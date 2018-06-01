#Daily and Weekly summary records
import json
# Author: Howard Webb
# Data: 7/25/2017

import sys
import MySQLdb as mdb
import MySQLdb.cursors
import json

MIN=1
MAX=2
AVG=3


#Use a view in CouchDB to get the data
#use the first key for attribute type
#order descending so when limit the results will get the latest at the top

def getDaily(cond):
    # specify columns so any changes to the view will not break the mapping
    sql="SELECT start_time, field_uuid, subject, subject_location_name, attribute, daily_min_value, daily_max_value, daily_average_value, participant, participant_type, device, device_location from MarsFarm.Daily_Environment_Summary_View" + cond + ";"
    return getSQLResults(sql)

def getPheno(cond):
    sql="SELECT start_time, mac, trial_id, subject_name, subject_location_name, row, `column`, attribute, attribute_value, status_qualifier, participant, participant_type, comment from MarsFarm.Phenotype_Observation_Exp" + cond + ";"
    return getSQLResults(sql)

    
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
     
def buildPhenoJSON(work):
    out={}
    
    timestamp={'timestamp': str(work['start_time'])}
    out['start_date']=timestamp
    env={'field_uuid':work['field_uuid']}
    out['environment']=env
    out['trial_id']=work['trial_id']
    loc={'subject_location_name': work['subject_location_name'], 'row':str(work['row']), 'column': str(work['column'])}
    subject={'name':work['subject_name'], 'location': loc}
    out['subject']=subject
    attrib={'name':work['attribute'], 'value':work['attribute_value']}
    subject['attribute']=attrib
    partic={'uuid':'xxxx', 'type':work['participant_type'], 'name': work['participant']}
    out['participant']=partic
    status={'status':'Complete', 'status_qualifier':work['status_qualifier'], 'status_qualifier_reason':'', 'comment':work['comment']}
    out['status']=status
    return out

def buildDailyJSON(work, type):
    out={}
    out['activity_type']='Environment_Summary'    
    timestamp={'timestamp': str(work['start_time']), 'span':'Daily'}
    out['start_date']=timestamp
    env={'field_uuid':work['field_uuid']}
    out['environment']=env
    subject={'name':work['subject']}
    loc={'name': work['subject_location_name']}    
    subject['location']=loc
    val=0
    if type==MIN:
        val=work['daily_min_value']
        qual='Minimum'
    elif  type==MAX:
        val=work['daily_max_value']
        qual='Maximum'        
    elif  type==AVG:
        val=work['daily_average_value']
        qual='Average'        
    attrib={'name':work['attribute'], 'value':val, 'qualifier': qual}
    subject['attribute']=attrib
    out['subject']=subject    
    partic={'uuid':'xxxx', 'type':work['participant_type'], 'name': work['participant']}
    out['participant']=partic
    return out
    

def processEnvResults(results):
    for rec in results:
        d=dict(rec)
        jsn=buildEnvJSON(d)
        return jsn

def processPhenoResults(results):
    for rec in results:
        #print rec
        d=dict(rec)
        jsn=buildPhenoJSON(d)
        return jsn

def processDailyResults(results):
    for rec in results:
        #print rec
        d=dict(rec)
        jsn=buildDailyJSON(d, MIN)
        prettyPrint(jsn)
        jsn=buildDailyJSON(d, MAX)
        prettyPrint(jsn)        
        jsn=buildDailyJSON(d, AVG)
        prettyPrint(jsn)
        return jsn

def exportEnvCSV(res):
    import csv
    keys=['start_time', 'field_uuid', 'subject', 'subject_location_name', 'attribute', 'daily_min_value', 'daily_max_value', 'daily_average_value', 'participant', 'participant_type', 'device', 'device_location']
    with open('/home/pi/EnvTest.csv', 'wb') as csvfile:
        f=csv.DictWriter(csvfile, keys)
        f.writeheader()
        for rec in res:
            f.writerow(rec)
        

def prettyPrint(txt):
    '''Dump json in nice format'''
    #print type(txt)
    print json.dumps(txt, indent=4, sort_keys=True)

def trialEnvDump():
    from env import env
    start_date=env['trials'][1]['start_date']
    end_date=env['trials'][1]['end_date']    
    cond=" WHERE start_time BETWEEN DATE('"+start_date + "') AND DATE('" + end_date +"') ORDER BY start_time, subject, subject_location, attribute"
    res=getDaily(cond)
#    processDailyResults(res)
    exportCSV(res)
    

def testEnv():
    limit=' LIMIT 10'
    res=getEnv(limit)
    if len(res)>0:
        processEnvResults(res)

def testPheno():
    limit=' LIMIT 10'
    res=getPheno(limit)
    if len(res)>0:
        processPhenoResults(res)

def test():
    cond=' LIMIT 10'    
    res=getDaily(cond)
    processDailyResults(res)
    

if __name__=="__main__":
    trialEnvDump() 

