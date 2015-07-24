import cx_Oracle
import arrow
import datetime
import os
import re
import pandas as pd
import json
import unicodedata

from xml.dom.minidom import parse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk, bulk
from pandas.io.json import json_normalize

def oracleConnection():
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

	return db, es




def xmlCursor(db, es):
	XMLDATAQuery = '''
    	select  XMLType.GetclobVal(rq_info) from TRS.CATER_XMLDATA_V3 where rt_id = 376 and Last_UPDATED >= sysdate - 360
	'''

	#select XMLType.GetStringVal(rq_info) from trs.cater_xmlDATA_V3 where data_id = 2143058

	curs = db.cursor()
	curs.execute(XMLDATAQuery)
	columns = [c[0].lower() for c in curs.description]
	bulk_records = []
	listOfDf = []


	while True:
	    rows = curs.fetchmany()
	    
	    print 'Fight da powa'
	    x = 0
	    xmlStr = ''
	    if rows == []:
	   	      break


	    for row in rows:
	        doc = {
	            columns[c]: row[c] if type(row[c]) is not cx_Oracle.CLOB else row[c].read() for c in range(len(columns))
	        }
	        xmlStr =  doc.get('xmltype.getclobval(rq_info)')
	        x = x + 1
	        print x

	        f = open('xml.txt' , 'w')
	        f.write(str(xmlStr))
	        f.close()
	        jsoned = os.popen("python xml2json.py xml.txt").read()
	        pandwas = pd.read_json(jsoned)

	        pandwas = pandwas.drop(pandwas.index[[6,8]])    
	        pandwas.loc['_index'] =  ['yifan_is_awesome1']
	        pandwas.loc['_type'] =  ['timing']
	        df_transposed =  pandwas.transpose()    #pivot 

	        listOfDf.append(df_transposed)

	    appendedDF = listOfDf[0].to_dict(orient='records')

	    iterDF = iter(listOfDf) 
	    next(iterDF)
	    for x in iterDF:
	        appendedDF += x.to_dict(orient='records')

	    bulk_records = appendedDF

	    res = bulk(client = es, actions = bulk_records, chunk_size=10000)
	    appendedDF =[]
	    rows = []


	    print 'Written.'
	db.close()


def retrieveTypes():
	curlRetrieve = 'curl -XGET http://localhost:9200/yifan_is_awesome1/_mappings/timing'
	curlRetrieve = curlRetrieve.replace('\n','').replace('\t','')

	#print curlRetrieve
	strOutput = os.popen(curlRetrieve).read() #make sure curl is installed

	jsonOutput = json.loads(strOutput)

	#print jsonOutput['yifan_is_awesome1']
	levelOne = jsonOutput['yifan_is_awesome1']
	levelTwo = 	levelOne['mappings']
	levelThree = levelTwo['timing']
	levelFour = levelThree['properties']
	
	listofKeys = []

	for key in levelFour:
		print type(key)

		listofKeys.append(str(key))
	

	print listofKeys
	#mappings = pandwas.loc['mappings']
	#print mappings
	
	
	#print output


def main():
	db, es = oracleConnection()
	print 'You are connected baby!'
	retrieveTypes()


if __name__ == "__main__":
	main()
