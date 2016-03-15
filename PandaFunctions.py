import cx_Oracle
import arrow
import datetime
import os
import re
import pandas as pd

from xml.dom.minidom import parse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk, bulk


def curlManipulation(nameOfESIndex):

	#You can tottal XDELETE something that doesnt exist
	curDelete = '''
		 curl -XDELETE localhost:9200/{0}
	'''
	curDelete = curDelete.replace('{0}', nameOfESIndex).replace('\n','').replace('\t','')
	os.system(curDelete) #make sure curl is installed

	curlCommand = '''

	 curl -XPUT localhost:9200/{0} -d '
	 {
		"mappings": {
			"_default_": {
				"dynamic_templates": [
					{
					 "TEMP": {
						"match": "*",
						"match_mapping_type": "string",
						"mapping": {
									
									"index" : "not_analyzed"
									}
						}        
					}
				]
			}
		}   
	}
	'''

	curlCommand = curlCommand.replace('{0}', nameOfESIndex).replace('\n','').replace('\t','')
	os.system(curlCommand) #make sure curl is installed


def oracleConnection():
	es = Elasticsearch('http://localhost:9200')

	USER = '##############'
	PASS = '##############'

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





def xmlCursor(db, es, nameOfESIndex, rtid):

	XMLDATAQuery = '''
    	select  XMLType.GetclobVal(rq_info) from TRS.CATER_XMLDATA_V3 where rt_id = {0} and Last_UPDATED >= sysdate - 360
	'''
	XMLDATAQuery = XMLDATAQuery.replace('{0}' , rtid)

	curs = db.cursor()
	curs.execute(XMLDATAQuery)
	columns = [c[0].lower() for c in curs.description]
	bulk_records = []
	listOfDf = []


	while True:
	    rows = curs.fetchmany()

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

	        f = open('xml.txt' , 'w')
	        f.write(str(xmlStr))
	        f.close()
	        jsoned = os.popen("python xml2json.py xml.txt").read()
	        pandwas = pd.read_json(jsoned)

	        pandwas = pandwas.drop(pandwas.index[[6,8]])    
	        pandwas.loc['_index'] =  [nameOfESIndex] #This was changed
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

	db.close()


def main():
	#########################################
	#ReAssign these 
	#IE: from userinput or another source of input
	#########################################
	nameOfESIndex = 'rt_id_11'
	rtid = '11'
	#########################################

	curlManipulation(nameOfESIndex)
	
	db, es = oracleConnection()

	xmlCursor(db, es, nameOfESIndex, rtid)
	print "Curl Added"
if __name__ == "__main__":
	main()
