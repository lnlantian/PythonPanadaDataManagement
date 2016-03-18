import cx_Oracle
import arrow
import datetime
import os
import re
import pandas as pd
import json

import curlTemplates as ct

from xml.dom.minidom import parse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk, bulk


def recusiveTree(tree, appendStr = '', appendList = []):

	if('#text' not in tree and '@USERID' not in tree):
		orgStr = appendStr

		for x in tree:
			if(x != 'properties'):
				appendStr += str(x)+'.'
			recusiveTree(tree[x],appendStr)
			appendStr = orgStr
	else:
		if(appendStr is not ''):
			for key in tree:
				appendList.append(str(appendStr)+key)
			
	return appendList



def oracleConnection():
	es = Elasticsearch('http://localhost:9200')

	USER = '##############'
	PASS = '##############'

	dsn = '''
	    (DESCRIPTION =
	        (ADDRESS = (PROTOCOL = TCP)(HOST = ############################)(PORT = ####))
	            (CONNECT_DATA =
	                (SERVER = DEDICATED)
	                    (SERVICE_NAME = PTRS)
	                 )
	    )'''.replace(' ','').replace('\n','').replace('\t','')
	 
	db = cx_Oracle.connect(user = USER, password = PASS, dsn = dsn)

	return db, es

#we need some paramaters in this
def retrieveTypes(nameOfESIndex):
	curlRetrieve = 'curl -XGET http://localhost:9200/{0}/_mappings/timing'.replace('{0}', nameOfESIndex)
	curlRetrieve = curlRetrieve.replace('\n','').replace('\t','')

	strOutput = os.popen(curlRetrieve).read() #make sure curl is installed
	jsonOutput = json.loads(strOutput.encode('utf-8'))

	########################
	#TODO:
	#Do a try catch, if this doesn't exist it will create an error, which is the users fault
	########################
	levelOne = jsonOutput[nameOfESIndex] #non-static
	levelTwo = 	levelOne['mappings']
	levelThree = levelTwo['timing']
	levelFour = levelThree['properties']
	
	listofKeys = []

	########################
	#This will handle nested conditions
	########################

	for key in levelFour:
		if('properties' in levelFour[key]):
			recursiveKeys = recusiveTree(levelFour[key], str(key)+'.')
			for x in recursiveKeys:
				listofKeys = listofKeys + [x.encode('ascii','ignore')]		
		else:
			listofKeys.append(str(key))
	
	return listofKeys


def pieGraphGeneration(listOfKeys,nameOfVisualization,nameOfESIndex):
	curlPie = ct.curlPie.replace('{0}', nameOfVisualization).replace('{1}',nameOfESIndex)

	listofPieKeys =[]

	for key in listOfKeys:
		hashLessKey = key.replace('#', '')
		pieKey =nameOfVisualization+'_'+nameOfESIndex+'_'+hashLessKey	

		if(pieKey not in listofPieKeys):
			listofPieKeys.append(pieKey)

			curlDocPie = curlPie.replace('{#}',hashLessKey).replace('{%}',key)		
			curlDocPie = curlDocPie.replace('\n','').replace('\t','')
			os.system(curlDocPie)

	return listofPieKeys


def lineGraphGeneration(listOfKeys,nameOfVisualization,nameOfESIndex):
	curlLine = ct.curlLine.replace('{0}', nameOfVisualization).replace('{1}',nameOfESIndex)

	listofLineKeys =[]
	
	for key in listOfKeys:
		hashLessKey = key.replace('#', '')
		lineKey =nameOfVisualization+'_'+nameOfESIndex+'_'+hashLessKey

		if(lineKey not in listofLineKeys):
			listofLineKeys.append(lineKey)
			curlDocLine = curlLine.replace('{#}',hashLessKey).replace('{%}',key)
			curlDocLine = curlDocLine.replace('\n','').replace('\t','')
			os.system(curlDocLine)


	return listofLineKeys


def areaGraphGeneration(listOfKeys,nameOfVisualization,nameOfESIndex):
	curlArea= ct.curlArea.replace('{0}', nameOfVisualization).replace('{1}',nameOfESIndex)
	
	listofAreaKeys =[]

	for key in listOfKeys:
		hashLessKey = key.replace('#', '')
		areaKey =nameOfVisualization+'_'+nameOfESIndex+'_'+hashLessKey

		if(areaKey not in listofAreaKeys):
			listofAreaKeys.append(areaKey)
			curlDocArea = curlArea.replace('{#}',hashLessKey).replace('{%}',key)	
			curlDocArea = curlDocArea.replace('\n','').replace('\t','')
			os.system(curlDocArea) 

	return listofAreaKeys

def histGraphGeneration(listOfKeys,nameOfVisualization,nameOfESIndex):
	curlHist= ct.curlHist.replace('{0}', nameOfVisualization).replace('{1}',nameOfESIndex)

	listofHistKeys =[]

	for key in listOfKeys:
		hashLessKey = key.replace('#', '')
		histKey = nameOfVisualization+'_'+nameOfESIndex+'_'+hashLessKey

		if(histKey not in listofHistKeys):
			listofHistKeys.append(histKey)
			curlDocHist = curlHist.replace('{#}',hashLessKey).replace('{%}',key)	
			curlDocHist = curlDocHist.replace('\n','').replace('\t','')
			os.system(curlDocHist) 

	return listofHistKeys


#Controlls the visulatution to create
def visualizationGeneration(nameOfESIndex):
	listOfKeys = retrieveTypes(nameOfESIndex)

	############################
	#We will generate a different SET of graphs for each type of visualization
	#A SET of visualization is one for every key
	############################
	typesOfGraph = ['line','area','pie','hist']
	listOfGraphs

	listofLineKeys = lineGraphGeneration(listOfKeys, 'line',nameOfESIndex)
	listofAreaKeys = areaGraphGeneration(listOfKeys, 'area',nameOfESIndex)
	listofPieKeys = pieGraphGeneration(listOfKeys, 'pie',nameOfESIndex)
	listofHistKeys =  histGraphGeneration(listOfKeys, 'hist',nameOfESIndex)

	############################
	#This will manually append all of the visualization indexes together to return
	############################

	listOfGraphs = []
	listOfGraphs.append(listofAreaKeys)
	listOfGraphs.append(listofLineKeys)
	listOfGraphs.append(listofPieKeys)
	listOfGraphs.append(listofHistKeys)

	e = open('listOfGraphs.txt', 'w')
	e.write(str(listOfGraphs))

	return listOfGraphs

	

def dashBoardGeneration(listOfGraphs, dashboardIndex):
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

  	colGen ='''
  	{\\"id\\":\\"{9}\\",\\"type\\":\\"visualization\\",\\"size_x\\":{10},\\"size_y\\":{11},\\"col\\":{12},\\"row\\":{13}},
  	''' 	

  	urlGen ='''
  	(col:{12},id:{9},row:{13},size_x:{10},size_y:{11},type:visualization),
  	'''

  	appendedColGen = ''
  	appendedUrlGen = ''

  	#This sets the size which won't change
  	#All Tables should be 3 units wide and 2 units hight
  	size_x = 3 
  	size_y = 2
  	#This sets the location which will change, we start from the top left corner (1,1)
  	col = 1 
  	row = 1

  	#The purspoe of this nested iternation is to actuaily build the dashboard

  	for x in listOfGraphs:  
  
  		for y in x:
  			tempGraph = colGen.replace('{9}',str(y)).replace('{10}',str(size_x)).replace('{11}',str(size_y)).replace('{12}',str(col)).replace('{13}',str(row))	
  			appendedColGen = appendedColGen + tempGraph 
  			urlsAws = urlGen.replace('{9}',str(y)).replace('{10}',str(size_x)).replace('{11}',str(size_y)).replace('{12}',str(col)).replace('{13}',str(row))	
  			appendedUrlGen = appendedUrlGen + urlsAws
  		
  			#When we get to the (x,10) we would want to move down 2 rows, this is what condition does
 
  			if col == 10:
  				row += 2		
  				col = 1
  			else:
  				col += 3

  	appendedColGen = appendedColGen.replace('\n','').replace('\t','').replace(' ','')	
  	appendedColGen = appendedColGen[:-1] #This will remove the last comma
  	

  	sourceFinal = sourceGen.replace('{0}', dashboardIndex ).replace('{1}', appendedColGen).replace(' ', '')
  	dashboardFinal = dashboardGen.replace('{a}', dashboardIndex).replace('{b}', sourceFinal)
  	#print 'Dashboard Gen:'


  	############################
	#Lets try running it
	############################
	
	dashboardFinal = dashboardFinal.replace('\n','').replace('\t','')

	f = open('curlDashboard', 'w')
	f.write(dashboardFinal)
	
	#Running the cURL query 
	os.system(dashboardFinal) 

#This is obviously temporery until we figure better  ways to load information tinto code

def main():
	#########################################
	#ReAssign these 
	#IE: from userinput or another source of input
	#########################################
	nameOfESIndex = 'rt_id_3'
	nameOfDashboard = 'dash_rt_id_3'
	#########################################
	print 'You are connected baby!'

	db, es = oracleConnection()
	
	listOfGraphs = visualizationGeneration(nameOfESIndex)
	dashBoardGeneration(listOfGraphs, nameOfDashboard)


if __name__ == "__main__":
	main()
