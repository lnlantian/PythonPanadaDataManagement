import cx_Oracle
import arrow
import datetime
import os
import re
import pandas as pd

from xml.dom.minidom import parse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk, bulk


def curlManipulation():

	#You can tottal XDELETE something that doesnt exist
	curDelete = '''
		 curl -XDELETE localhost:9200/yifan_is_awesome_rtid_3
	'''
	curDelete = curDelete.replace('\n','').replace('\t','')
	os.system(curDelete) #make sure curl is installed

	curlCommand = '''

	 curl -XPUT localhost:9200/yifan_is_awesome_rtid_3 -d '
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

	curlCommand = curlCommand.replace('\n','').replace('\t','')
	os.system(curlCommand) #make sure curl is installed


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





def xmlCursor(db, es, nameOfESIndex, rt_id):

	XMLDATAQuery = '''
    	select  XMLType.GetclobVal(rq_info) from TRS.CATER_XMLDATA_V3 where rt_id = {0} and Last_UPDATED >= sysdate - 360
	'''.replace('{0}', rt_id)

	#'''
    #	select  XMLType.GetclobVal(rq_info) from TRS.CATER_XMLDATA_V3 where rt_id = 376 and Last_UPDATED >= sysdate - 360
	#'''

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

	        f = open('xml.txt' , 'w')
	        f.write(str(xmlStr))
	        f.close()
	        jsoned = os.popen("python xml2json.py xml.txt").read()
	        pandwas = pd.read_json(jsoned)

	        pandwas = pandwas.drop(pandwas.index[[6,8]])    
	        pandwas.loc['_index'] =  ['rt_id_376']
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


def main():
	#########################################
	#ReAssign these 
	#########################################
	nameOfESIndex = 'rt_id_376'
	rt_id = 376

	#########################################

	curlManipulation()
	print "Curl Added"
	db, es = oracleConnection()
	print "Oracle Connection M"


	xmlCursor(db, es,nameOfESIndex, rt_id)

if __name__ == "__main__":
	main()
