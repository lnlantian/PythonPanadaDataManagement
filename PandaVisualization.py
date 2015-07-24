import cx_Oracle
import arrow
import datetime
import os
import re
import pandas as pd
import json

from xml.dom.minidom import parse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk, bulk

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

	curlTemplate = 	'''    
	curl -XPUT http://localhost:9200/.kibana/visualization/yifan_test_pie_% -d'
    {
        "title":"yifan_test_pie_%",
        "visState":"{\\"type\\":\\"pie\\",\\"params\\":{\\"shareYAxis\\":true,\\"addTooltip\\":true,\\"addLegend\\":true,\\"isDonut\\":false},\\"aggs\\":[{\\"id\\":\\"1\\",\\"type\\":\\"count\\",\\"schema\\":\\"metric\\",\\"params\\":{}},{\\"id\\":\\"2\\",\\"type\\":\\"terms\\",\\"schema\\":\\"segment\\",\\"params\\":{\\"field\\":\\"%\\",\\"size\\":100,\\"order\\":\\"desc\\",\\"orderBy\\":\\"1\\"}}],\\"listeners\\":{}}",
        "description":"",
        "version":1,
        "kibanaSavedObjectMeta":
        {
            "searchSourceJSON":"{\\"index\\":\\"yifan_is_awesome1\\",\\"query\\":{\\"query_string\\":{\\"query\\":\\"*\\",\\"analyze_wildcard\\":true}},\\"filter\\":[]}"
        }
    }'   
    '''
	strOutput = os.popen(curlRetrieve).read() #make sure curl is installed
	jsonOutput = json.loads(strOutput)
	#curlTemplate = curlTemplate.replace('\n','').replace('\t','')

	levelOne = jsonOutput['yifan_is_awesome1'] #non-static
	levelTwo = 	levelOne['mappings']
	levelThree = levelTwo['timing']
	levelFour = levelThree['properties']
	
	listofKeys = []

	for key in levelFour:
		##################### 
		#TO-DO
		#####################

		#make sure we go deeper, check to see if the next child 


		listofKeys.append(str(key))
	
	print listofKeys


	#curlDoc = curlTemplate.replace('%',listofKeys[0]).replace('@', 'yifan_test_pie_'+listofKeys[0])

	#f = open('workfile.txt', 'w')
	#f.write(curlDoc)
	#f.close()
	

	for key in listofKeys:
		print 'yifan_test_pie_'+key
		curlDoc = curlTemplate.replace('%',key).replace('@', 'yifan_test_pie_'+key)
		curlDoc = curlDoc.replace('\n','').replace('\t','')
		os.system(curlDoc)

def dashBoardGeneration():
	#sommething happens here
	a = 1





def main():
	db, es = oracleConnection()
	print 'You are connected baby!'
	retrieveTypes()


if __name__ == "__main__":
	main()
