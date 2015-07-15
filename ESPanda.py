import cx_Oracle
import arrow
import datetime
import os
import re
import pandas as pd


from xml.dom.minidom import parse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk, bulk

es = Elasticsearch('http://localhost:9200')

USER = 'TRS_ADMIN'
PASS = 'H8Q5ZP9'

dsn = '''
    (DESCRIPTION =
        (ADDRESS = (PROTOCOL = TCP)(HOST = dbi00cnc-ptrs.rim.net)(PORT = 1521))
            (CONNECT_DATA =
                (SERVER = DEDICATED)
                    (SERVICE_NAME = PTRS)
                 )
    )'''.replace(' ','').replace('\n','').replace('\t','')
 
db = cx_Oracle.connect(user = USER, password = PASS, dsn = dsn)



XMLDATAQuery = '''
    select  XMLType.GetStringVal(rq_info) from TRS.CATER_XMLDATA_V3 where rt_id = 376 and Last_UPDATED >= sysdate - 7
'''


#select XMLType.GetStringVal(rq_info) from trs.cater_xmlDATA_V3 where data_id = 2143058



curs = db.cursor()
curs.execute(XMLDATAQuery)
columns = [c[0].lower() for c in curs.description]
columnNames = []
bulk_records = []

while True:
    rows = curs.fetchmany();
    if rows == []:
         break

    for row in rows:
        doc = {
            columns[c]: row[c] if type(row[c]) is not cx_Oracle.LOB else row[c].read() for c in range(len(columns))
        }

        xmlStr =  doc.get('xmltype.getstringval(rq_info)')
        f = open('xml.txt' , 'w')
        f.write(str(xmlStr))
        f.close()


        #jsoned = os.system("python xml2json.py xml.txt")
        jsoned = os.popen("python xml2json.py xml.txt").read()
        #print jsoned

        #See here is where we need to use python, we need to read jsoned(which is a string) into you know, a panada json object.
        pandwas = pd.read_json(jsoned)
        
        #print type(pandwas) #<class <'pandas.core.frame.DataFrame'>

        #requestor = pandwas.iat[6,0]    
        #print requestor

        pandwas = pandwas.drop(pandwas.index[[6,8]])    
        print pandwas

        print '/////////////////////////////////////////////////////////////////////////'
        

        #jsoned['_index'] = 'Panda'
        #jsoned['_type'] = 'timing' 
        #jsoned['_id'] = doc['rq_id'] 
        #f.write("%s %s\n" % (arrow.now().strftime("%Y-%m-%d %H:%M:%S"), str(doc['_id'])))        

        #bulk_records.append(jsoned)

    #res = bulk(client = es, actions = bulk_records, chunk_size=10000)
    #bulk_records = []


#xmlFirst = columnNames[0].get('xmltype.getstringval(rq_info)')

db.close()


#f = open('xml.txt' , 'w')
#f.write(str(xmlStr))


#print os.system("python xml2json.py xml.txt")

'''
bulk_records = []curs.execute(pivotQuery)

with open('lastrun.txt', 'w') as f:
    while True:
        rows = curs.fetchmany();
        if rows == []:
            break

        for row in rows:
            doc = {
              columns[c]: row[c] if type(row[c]) is not cx_Oracle.LOB else row[c].read() for c in range(len(columns))
            }
            # doc['submitted_date'] = arrow.get(doc['submitted_date'], 'YYYY-MM-DD').datetime
            # doc['closed_date'] = arrow.get(doc['closed_date'], 'YYYY-MM-DD').datetime
            doc['_index'] = index
            doc['_type'] = 'timing' #Each types of data must have their own type
            #doc['_id'] = doc['stamp_id'] #This is questionable....  If we can have a row for each rq_id we can use rq_id but we cant
            doc['_id'] = doc['rq_id']
            #print doc

            #print columns

            f.write("%s %s\n" % (arrow.now().strftime("%Y-%m-%d %H:%M:%S"), str(doc['_id'])))
            #print ("%s %s\n" % (arrow.now().strftime("%Y-%m-%d %H:%M:%S"), str(doc['_id'])))


            bulk_records.append(doc)

        res = bulk(client = es, actions = bulk_records, chunk_size=10000)
        #print res
        bulk_records = []


timers = open('timelog.txt', 'w')

f.write(datetime.time)
'''