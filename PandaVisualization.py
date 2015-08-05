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
	curl -XPUT http://localhost:9200/.kibana/visualization/{0}_% -d'
	{
	    "title":"{0}_%",
	    "visState":"{\\"type\\":\\"pie\\",\\"params\\":{\\"shareYAxis\\":true,\\"addTooltip\\":true,\\"addLegend\\":true,\\"isDonut\\":false},\\"aggs\\":[{\\"id\\":\\"1\\",\\"type\\":\\"count\\",\\"schema\\":\\"metric\\",\\"params\\":{}},{\\"id\\":\\"2\\",\\"type\\":\\"terms\\",\\"schema\\":\\"segment\\",\\"params\\":{\\"field\\":\\"%\\",\\"size\\":100,\\"order\\":\\"desc\\",\\"orderBy\\":\\"1\\"}}],\\"listeners\\":{}}",
	    "description":"",
	    "version":1,
	    "kibanaSavedObjectMeta":
	    {
	        "searchSourceJSON":"{\\"index\\":\\"{1}\\",\\"query\\":{\\"query_string\\":{\\"query\\":\\"*\\",\\"analyze_wildcard\\":true}},\\"filter\\":[]}"
	    }
	}'   
	'''.replace('{0}', nameOfVisualization).replace('{1}',nameOfESIndex)

	listofPieKeys =[]

	for key in listOfKeys:
		pieKey =nameOfVisualization+'_'+key	
		listofPieKeys.append(pieKey)

		curlDocPie = curlPie.replace('%',key).replace('@', pieKey)		
		curlDocPie = curlDocPie.replace('\n','').replace('\t','')
		os.system(curlDocPie)

	return listofPieKeys


def lineGraphGeneration(listOfKeys,nameOfVisualization,nameOfESIndex):
	curlLine = '''
	curl -XPUT http://localhost:9200/.kibana/visualization/{0}_% -d'
	{
	    "title":"{0}_%",
	    "visState":"{\\"type\\":\\"line\\",\\"params\\":{\\"shareYAxis\\":true,\\"addTooltip\\":true,\\"addLegend\\":true,\\"defaultYExtents\\":false},\\"aggs\\":[{\\"id\\":\\"1\\",\\"type\\":\\"count\\",\\"schema\\":\\"metric\\",\\"params\\":{}},{\\"id\\":\\"2\\",\\"type\\":\\"date_histogram\\",\\"schema\\":\\"segment\\",\\"params\\":{\\"field\\":\\"SUBMITDATE\\",\\"interval\\":\\"week\\",\\"min_doc_count\\":1,\\"extended_bounds\\":{}}}],\\"listeners\\":{}}",
	    "description":"",
	    "version":1,
	    "kibanaSavedObjectMeta":
	    {
	        "searchSourceJSON":"{\\"index\\":\\"{1}\\",\\"query\\":{\\"query_string\\":{\\"query\\":\\"*\\",\\"analyze_wildcard\\":true}},\\"filter\\":[]}"
	    }
	}'
	'''.replace('{0}', nameOfVisualization).replace('{1}',nameOfESIndex)


	listofLineKeys =[]
	
	for key in listOfKeys:
		lineKey =nameOfVisualization+'_'+key
		
		listofLineKeys.append(lineKey)

		curlDocLine = curlLine.replace('%',key).replace('@', lineKey)		
		curlDocLine = curlDocLine.replace('\n','').replace('\t','')
		os.system(curlDocLine)
		print curlDocLine
	
	return listofLineKeys

def areaGraphGeneration(listOfKeys,nameOfVisualization,nameOfESIndex):
	curlArea= '''
	curl -XPUT http://localhost:9200/.kibana/visualization/{0}_% -d'
	{
		"title":"{0}_%",
		"visState":"{\\"type\\":\\"area\\",\\"params\\":{\\"shareYAxis\\":true,\\"addTooltip\\":true,\\"addLegend\\":true,\\"mode\\":\\"stacked\\",\\"defaultYExtents\\":false},\\"aggs\\":[{\\"id\\":\\"1\\",\\"type\\":\\"count\\",\\"schema\\":\\"metric\\",\\"params\\":{}},{\\"id\\":\\"2\\",\\"type\\":\\"date_histogram\\",\\"schema\\":\\"segment\\",\\"params\\":{\\"field\\":\\"SUBMITDATE\\",\\"interval\\":\\"month\\",\\"min_doc_count\\":1,\\"extended_bounds\\":{}}}],\\"listeners\\":{}}",
		"description":"",
		"version":1,
		"kibanaSavedObjectMeta":
		{
			"searchSourceJSON":"{\\"index\\":\\"{1}\\",\\"query\\":{\\"query_string\\":{\\"query\\":\\"*\\",\\"analyze_wildcard\\":true}},\\"filter\\":[]}"
		}
	}'
	'''.replace('{0}', nameOfVisualization).replace('{1}',nameOfESIndex)
	
	listofAreaKeys =[]

	for key in listOfKeys:
		areaKey =nameOfVisualization+'_'+key

		listofAreaKeys.append(areaKey)

		curlDocArea = curlArea.replace('%',key).replace('@', areaKey)	
		curlDocArea = curlDocArea.replace('\n','').replace('\t','')
		os.system(curlDocArea) 

	return listofAreaKeys


#Controlls the visulatution to create
def visualizationGeneration():
	listOfKeys = retrieveTypes()

	#listofAreaKeys = areaGraphGeneration(listOfKeys, 'yifan_test_area_3','yifan_is_awesome1')
	listofLineKeys = lineGraphGeneration(listOfKeys, 'yifan_test_line_3','yifan_is_awesome1')
	#listofPieKeys = pieGraphGeneration(listOfKeys, 'yifan_test_pie_3','yifan_is_awesome1')
	
	############################
	#TD: some thing that appends the list of keys
	############################
	listOfGraphs = []
	#listOfGraphs.append(listofAreaKeys)
	listOfGraphs.append(listofLineKeys)
	#listOfGraphs.append(listofPieKeys)

	print 'visualizationGeneration: '

	print 'listOfGraphs: '
	print listOfGraphs
	print 'len: ', len(listOfGraphs)

	return listOfGraphs

	

def dashBoardGeneration(listOfGraphs):
	#sommething happens here
	dashboardGen = '''
	curl -XPUT http://localhost:9200/.kibana/dashboard/{a} -d'
	{b}'
  	'''

  	sourceGen = '''
  	{"title":"{0}","hits":0,"description":"","panelsJSON":"[
  	{1}
  	]","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\\"filter\\":[{\\"query\\":{\\"query_string\\":{\\"query\\":\\"*\\",\\"analyze_wildcard\\":true}}}]}"}}
  	'''

  	#{\"id\":\"yifan_test_area_3_CONTAINS_UPLOADS\",\"type\":\"visualization\",\"size_x\":3,\"size_y\":2,\"col\":1,\"row\":1}

  	colGen ='''
  	{\\"id\\":\\"{9}\\",\\"type\\":\\"visualization\\",\\"size_x\\":{10},\\"size_y\\":{11},\\"col\\":{12},\\"row\\":{13}},
  	''' 	

  	urlGen ='''
  	(col:{12},id:{9},row:{13},size_x:{10},size_y:{11},type:visualization),
  	'''

  	appendedColGen = ''
  	appendedUrlGen = ''

  	size_x = 3
  	size_y = 2
  	col = 1 
  	row = 1

  	for x in listOfGraphs:  
  
  		for y in x:
  			tempGraph = colGen.replace('{9}',str(y)).replace('{10}',str(size_x)).replace('{11}',str(size_y)).replace('{12}',str(col)).replace('{13}',str(row))	
  			appendedColGen = appendedColGen + tempGraph 
  			urlsAws = urlGen.replace('{9}',str(y)).replace('{10}',str(size_x)).replace('{11}',str(size_y)).replace('{12}',str(col)).replace('{13}',str(row))	
  			appendedUrlGen = appendedUrlGen + urlsAws

  			if col == 10:
  				row += 2		
  				col = 1
  			else:
  				col += 3

  	appendedColGen = appendedColGen.replace('\n','').replace('\t','').replace(' ','')
  	
  	appendedColGen = appendedColGen[:-1] #This will remove the last comma
  	

  	sourceFinal = sourceGen.replace('{0}', 'yifans_dashboard' ).replace('{1}', appendedColGen).replace(' ', '')
  	dashboardFinal = dashboardGen.replace('{a}', 'yifans_dashboard' ).replace('{b}', sourceFinal)
  	print 'Dashboard Gen:'


  	############################
	#Lets try running it
	############################
	
	dashboardFinal = dashboardFinal.replace('\n','').replace('\t','')
	print dashboardFinal
	
	print 'urlAws: ' 
	print appendedUrlGen

	os.system(dashboardFinal) 

#This is obviously temporery until we figure better  ways to load information tinto code


def main():
	db, es = oracleConnection()
	print 'You are connected baby!'
	listOfGraphs = visualizationGeneration()
	#dashBoardGeneration(listOfGraphs)


if __name__ == "__main__":
	main()
