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




def xmlCursor(db, es):
	XMLDATAQuery = '''
    	select  XMLType.GetclobVal(rq_info) from TRS.CATER_XMLDATA_V3 where rt_id = 3 and Last_UPDATED >= sysdate - 360
	'''

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
	        print x

	        f = open('xml.txt' , 'w')
	        f.write(str(xmlStr))
	        f.close()
	        jsoned = os.popen("python xml2json.py xml.txt").read()
	        pandwas = pd.read_json(jsoned)

	        pandwas = pandwas.drop(pandwas.index[[6,8]])    
	        pandwas.loc['_index'] =  ['yifan_is_awesome_rtid_3']
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

def visualizationGen():
	visualJson =  '''
  	{
  		"_index" : ".kibana",
  		"_type" : "visualization",
 		"_id" : "yifan_is_awesome1",
  		"_version" : 1,
  		"found" : true,
  		"_source": %
  	}
  	'''
	

  	pie = '''
    curl -XPUT http://localhost:9200/.kibana/visualization/yifan_is_awesome2?=pretty -d'
    {
        "title":"yifan_is_awesome2",
        "visState":"{\"type\":\"pie\",\"params\":{\"shareYAxis\":true,\"addTooltip\":true,\"addLegend\":true,\"isDonut\":false},\"aggs\":[{\"id\":\"1\",\"type\":\"count\",\"schema\":\"metric\",\"params\":{}},{\"id\":\"2\",\"type\":\"terms\",\"schema\":\"segment\",\"params\":{\"field\":\"REQUESTOR.#text\",\"size\":100,\"order\":\"desc\",\"orderBy\":\"1\"}}],\"listeners\":{}}",
        "description":"",
        "version":1,
        "kibanaSavedObjectMeta":
        {
            "searchSourceJSON":"{\"index\":\"yifan_is_awesome1\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"
        }
    }'  
	'''

	line = '''
	curl -XPUT http://localhost:9200/.kibana/visualization/yifan_is_awesome2.1?=pretty -d'
	{
	    "title":"yifan_is_awesome2.1",
	    "visState":"{\"type\":\"line\",\"params\":{\"shareYAxis\":true,\"addTooltip\":true,\"addLegend\":true,\"defaultYExtents\":false},\"aggs\":[{\"id\":\"1\",\"type\":\"count\",\"schema\":\"metric\",\"params\":{}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"SUBMITDATE\",\"interval\":\"week\",\"min_doc_count\":1,\"extended_bounds\":{}}}],\"listeners\":{}}",
	    "description":"",
	    "version":1,
	    "kibanaSavedObjectMeta":
	    {
	        "searchSourceJSON":"{\"index\":\"yifan_is_awesome1\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"
	    }
	}'
	'''
	
	markdown = '''
	curl -XPUT http://localhost:9200/.kibana/visualization/Spongebob -d '
	{
		"title":"Spongebob",
		"visState":
		"{\"type\":\"markdown\",\"params\":{\"markdown\":\"Who lives in a pineapple under the sea\"},\"aggs\":[],\"listeners\":{}}",
		"description":"",
		"version":1,
		"kibanaSavedObjectMeta":
		{
			"searchSourceJSON":"{\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"
		}
	}'
	'''


def dashboardGen():
	#Version refers to : everytimeyou save there is a new version

	dashboardGen = '''
	{
		"_index" : ".kibana",
  		"_type" : "dashboard",
  		"_id" : "yifan_is_awesome1",
  		"_version" : 4,
  		"found" : true,
  		"_source":%
  	}
  	'''


def main():
	curlManipulation()
	print "Curl Added"
	db, es = oracleConnection()
	print "Oracle Connection Made"
	xmlCursor(db, es)

if __name__ == "__main__":
	main()
