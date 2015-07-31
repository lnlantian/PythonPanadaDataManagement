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



#we need some paramaters in this
def retrieveTypes():
	curlRetrieve = 'curl -XGET http://localhost:9200/yifan_is_awesome_rtid_3/_mappings/timing'
	curlRetrieve = curlRetrieve.replace('\n','').replace('\t','')

	strOutput = os.popen(curlRetrieve).read() #make sure curl is installed
	jsonOutput = json.loads(strOutput)

	levelOne = jsonOutput['yifan_is_awesome_rtid_3'] #non-static
	levelTwo = 	levelOne['mappings']
	levelThree = levelTwo['timing']
	levelFour = levelThree['properties']
	
	listofKeys = []

	for key in levelFour:
		##################### 
		#TO-DO
		#make sure we go deeper, check to see if the next child 
		#Still thinking of way, but at this point might just leave it as it is
		#####################

		#temp = levelFour[str(key)]
		#print temp
		listofKeys.append(str(key))
	
	return listofKeys


def pieGraphGeneration(listOfKeys,nameOfVisualization,nameOfESIndex):
	curlPie = 	'''    
	curl -XPUT http://localhost:9200/.kibana/visualization/yifan_test_pie_3_% -d'
	{
	    "title":"yifan_test_pie_3_%",
	    "visState":"{\\"type\\":\\"pie\\",\\"params\\":{\\"shareYAxis\\":true,\\"addTooltip\\":true,\\"addLegend\\":true,\\"isDonut\\":false},\\"aggs\\":[{\\"id\\":\\"1\\",\\"type\\":\\"count\\",\\"schema\\":\\"metric\\",\\"params\\":{}},{\\"id\\":\\"2\\",\\"type\\":\\"terms\\",\\"schema\\":\\"segment\\",\\"params\\":{\\"field\\":\\"%\\",\\"size\\":100,\\"order\\":\\"desc\\",\\"orderBy\\":\\"1\\"}}],\\"listeners\\":{}}",
	    "description":"",
	    "version":1,
	    "kibanaSavedObjectMeta":
	    {
	        "searchSourceJSON":"{\\"index\\":\\"yifan_is_awesome_rtid_3\\",\\"query\\":{\\"query_string\\":{\\"query\\":\\"*\\",\\"analyze_wildcard\\":true}},\\"filter\\":[]}"
	    }
	}'   
	'''

	listofPieKeys =[]

	for key in listofKeys:
		pieKey ='yifan_test_pie_'+key	
		listofPieKeys.append(PieKey)

		curlDocPie = curlPie.replace('%',key).replace('@', pieKey)		
		curlDocPie = curlDoc.replace('\n','').replace('\t','')
		os.system(curlDocPie)

	return listofPieKeys


def lineGraphGeneration(listOfKeys,nameOfVisualization,nameOfESIndex):
	curlLine = '''
	curl -XPUT http://localhost:9200/.kibana/visualization/yifan_test_line_3_% -d'
	{
	    "title":yifan_test_line_3_%",
	    "visState":"{\\"type\\":\\"line\\",\\"params\\":{\\"shareYAxis\\":true,\\"addTooltip\\":true,\\"addLegend\\":true,\\"defaultYExtents\\":false},\\"aggs\\":[{\\"id\\":\\"1\\",\\"type\\":\\"count\\",\\"schema\\":\\"metric\\",\\"params\\":{}},{\\"id\\":\\"2\\",\\"type\\":\\"date_histogram\\",\\"schema\\":\\"segment\\",\\"params\\":{\\"field\\":\\"SUBMITDATE\\",\\"interval\\":\\"week\\",\\"min_doc_count\\":1,\\"extended_bounds\\":{}}}],\\"listeners\\":{}}",
	    "description":"",
	    "version":1,
	    "kibanaSavedObjectMeta":
	    {
	        "searchSourceJSON":"{\\"index\\":\\"yifan_is_awesome1\\",\\"query\\":{\\"query_string\\":{\\"query\\":\\"*\\",\\"analyze_wildcard\\":true}},\\"filter\\":[]}"
	    }
	}'
	'''

	listofLineKeys =[]
	
	for key in listofKeys:
	
		lineKey ='yifan_test_line_'+key
		listofLineKeys.append(lineKey)

		curlDocLine = curlLine.replace('%',key).replace('@', lineKey)		
		curlDocLine = curlDocLine.replace('\n','').replace('\t','')
		os.system(curlDocLine)


	return listofLineKeys

def areaGraphGeneration(listOfKeys,nameOfVisualization,nameOfESIndex):
	curlArea= '''
	curl -XPUT http://localhost:9200/.kibana/visualization/yifan_test_area_3_% -d'
	{
		"title":"yifan_test_area_3_%",
		"visState":"{\\"type\\":\\"area\\",\\"params\\":{\\"shareYAxis\\":true,\\"addTooltip\\":true,\\"addLegend\\":true,\\"mode\\":\\"stacked\\",\\"defaultYExtents\\":false},\\"aggs\\":[{\\"id\\":\\"1\\",\\"type\\":\\"count\\",\\"schema\\":\\"metric\\",\\"params\\":{}},{\\"id\\":\\"2\\",\\"type\\":\\"date_histogram\\",\\"schema\\":\\"segment\\",\\"params\\":{\\"field\\":\\"SUBMITDATE\\",\\"interval\\":\\"month\\",\\"min_doc_count\\":1,\\"extended_bounds\\":{}}}],\\"listeners\\":{}}",
		"description":"",
		"version":1,
		"kibanaSavedObjectMeta":
		{
			"searchSourceJSON":"{\\"index\\":\\"yifan_is_awesome1\\",\\"query\\":{\\"query_string\\":{\\"query\\":\\"*\\",\\"analyze_wildcard\\":true}},\\"filter\\":[]}"
		}
	}'
	'''
	
	listofAreaKeys =[]

	for key in listofKeys:
		areaKey ='yifan_test_area_'+key

		listofAreaKeys.append(areaKey)

		curlDocArea = curlArea.replace('%',key).replace('@', areaKey)	
		curlDocArea = curlDocArea.replace('\n','').replace('\t','')
		os.system(curlDocArea)

	return listofAreaKeys


#Controlls the visulatution to create
def visualizationGeneration():
	listOfKeys = retrieveTypes()

	listofAreaKeys = areaGraphGeneration(listOfKeys)
	#listofLineKeys = lineGraphGeneration(listOfKeys)
	#listofPieKeys = pieGraphGeneration(listOfKeys)
	
	############################
	#TD: some thing that appends the list of keys
	############################
	
	return listOfGraphs


def dashBoardGeneration():
	#sommething happens here
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




#This is obviously temporery until we figure better  ways to load information tinto code
def userInput():





def main():
	db, es = oracleConnection()
	print 'You are connected baby!'
	listOfGraphs = visualizationGeneration()
	dashBoardGeneration(listOfGraphs)


if __name__ == "__main__":
	main()
