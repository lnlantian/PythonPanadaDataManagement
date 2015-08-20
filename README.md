# PythonPanadaDataManagement

Cater Visualization User Manual
1 Introduction
1.1 Purpose
1.2 The purpose of this software
2 Summary of Technology Used
2.1 Overview of the ES Engine
2.2 Using ES
2.3 Using cURL
2.4 Overview of Kibana
2.5 Using Kibana
3 Intro to PPDM
3.1 The Purpose
3.2 Using PPDM
4 How it is Built
4.1 PandaFunctions.py
4.1.1 Establishing a connection with the ES server
4.1.2 Querying the data to a list in XML
4.1.3 Using xml2json.py
4.1.4 Reading the newly converted JSON information into Pandas 
4.1.5 Manipulating the data in Pandas by adding additional columns 
4.1.6 Deleting the existing ES index  
4.2 PandaVisualization.py
4.2.1 Establishing a connection with your ES server
4.2.2 Generating a cURL Command to set a Kibana Visualizations into ES
4.2.2.1 visualizationGeneration
4.2.2.2 retrieveTypes
4.2.2.3 Creating new types of Visualizations
4.2.3 dashBoardGeneration
4.3 Future development
4.3.1 Windows Schedule runs, or Run on Call
4.3.2 Graphical development


Introduction
Purpose 
Hello. Firstly I’d like thank you for taking the time to check out this user manual, the purpose of this user manual is to do an in depth step by step explanation through the whole process of this Cater visualization stack.
One important thing I would like to stress is this is not a finished product as my work term has concluded and I have been the sole developer of this project thus far. So in this report I hope to transfer all my knowledge about ElasticSearch (ES) and Kibana,  as well as how my scripts operates to you. I will also try my best to make sure my code is clear and provide good documentation in my code as well.
Before you proceed to read this manual, I highly suggest reading "Cater Support for Dummies", the other documentation I have written which was specifically meant for Cater. Reading that shall help your overall understanding of how Cater works, and be familiar with terms such as rt_id and rq_id and tables such as request_types and request_info.
And lastly if you have any questions, you can contact me with my personal email at yfjd01@gmail.com.
The purpose of this software
The purpose of PythonPandasDataManagement (PPDM) is to replace  the previously existing graphing functionality that once existed in Cater, which is no longer supported due to lack of demand.

There currently does not exist many Cater Users who rely on this functionality, however it would be very nice to have again.
The ultimate goal of PPDM is to have an instance of ES and Kibana running on a virtual machine that will have a scheduled script (PPDM) to update the data in ES and to build visualizations regarding information about their Cater systems. Customers will be able to access these visualizations through Cater links.

The finished Stack should look like this:



PandaFunctions.py and PandaVisualizations.py are two different python scripts that handle different functionalities, but together they form PPDM.
PandaFunctions.py handles the GETting, converting/manipulating and PUTting of data
PandaVisualizations.py which handles GETting the data, creating visualization and dashboard queries, and PUTting it into ES.
 
I shall give you a better explanation of ES and Kibana below.
Summary of Technology Used
Overview of the ES Engine 
ES is an open source search engine that allows you to efficiently index and search for your data. ES can also be used as an NoSQL database but shouldn’t be used as a primary data storage, rather it should be used as a playground for small groups of data. The latter is the main focal component  of ES that we are interested in and what we will primarily using ES for.
There are many advantages to ES. One advantage is that it is easy to use you can access ES with the REST API. It also stores data in a JSON format, and allow you to create multiple indexes for your data. ES is also schema-less, meaning it automatically creates data mapping during index in time.
The main advantage to the ES based solution is that ES is a database of its own, and will save the Kibana visualization you created into ES. The graphing functionality that existed beforehand was essentially a script that queries all the information it previously needed every time someone wanted to see a graph.

Using ES
In order to use ES, you must interact (read and write data) with the REST API. This is an advantage as it makes it simple to use in any backend development language. For the purposes of our project I have decided to use REST API with cURL.
Using cURL
Is a command line tool for transferring data using various protocols (getting or sending files) using URL syntax. cURL is the software I have chosen
Example:
curl -XGET 'http://localhost:9200/twitter/_search?q=user:kimchy'
curl -XPUT http://localhost:9200/.kibana/dashboard/dash_rt_id_376 -d' {"title":"dio" ,"catchphrase""muda muda muda"}'

Overview of Kibana
Kibana is an analytics tool created by the same makers of ES and is meant to be used alongside ES. Kibana is used to create visualizations and dashboards for data stored in ES. Kibana is quick and easy to use.
Using Kibana
There are two ways that we can create Kibana visualizations and dashboards. The first being through cURL in the command line where we can -XPUT information into http://localhost:9200/.kibana/. This is how our python scripts would insert its generated visualizations and dashboards.
 
Example:

curl -XPUT http://localhost:9200/.kibana/ visualization/Yifan_is_the_best -d' 
{  
"_index":".kibana",  
"_type":"visualization",  
"_id":"Yifan_is_the_best",   
"_version":1,  
"found":true,"_source":  
{  
"title":"Yifan_is_the_best",
"visState":"
{
\"type\":\"area\",
\"params\":
{
\"shareYAxis\":true,
\"addTooltip\":true,
\"addLegend\":true,
\"mode\":\"stacked\",
\"defaultYExtents\":false
},
\"aggs\":[
{
\"id\":\"1\",
\"type\":\"count\",
\"schema\":\"metric\",
\"params\":{}
},
{
\"id\":\"2\",
\"type\":\"terms\",
\"schema\":\"segment\",
\"params\":
{
\"field\":\"The_best_field\",
\"size\":100,
\"order\":\"desc\",
\"orderBy\":\"1\"
}
}
],
\"listeners\":{}
}",
"description":"",
"version":1,
"kibanaSavedObjectMeta":
{
"searchSourceJSON":"
{
\"index\":\"The_Best_index\",
\"query\":
{
\"query_string\":
{
\"query\":\"*\",\"analyze_wildcard\":true
}
},\"filter\":[]
}"
}
}
}'  


 
The second way is to create, manage and edit Kibana visualizations and dashboard through Kibana's browser interface located at http://localhost:5601/. 
To learn more about Kibana, please refer to:
https://www.timroes.de/2015/02/07/kibana-4-tutorial-part-1-introduction/


Intro to PPDM
PPDM was the actual part of the stack that I developed in python 2.7 and requires a Unix environment to function.
The Purpose
The purpose of this software is to provide a method of generating graphs and visualizations for Cater customers. The software we were using to generate graphs beforehand is no longer being supported. The goal is to develop a software that is lightweight, easily to maintain, and flexible to work with which is why we have selected to use the ES Kibana stack.
The two purposes that PPDM serves are to, first get the relevant data from our Oracle database where Cater is currently located and works to manipulate the data so that it is accepted by ES. where the data is then PUT into our ES server. The second part of the process is to create Kibana visualizations and dashboards by GETting the data, creating visualization and dashboard queries, and PUTting it into ES.

The features described above are split into two files.
PandaFunctions.py which handles the GETting, converting/manipulating and PUTting data
PandaVisualizations.py which handles GETting the data, creating visualization and dashboard queries, and PUTting it into ES.
 
Using PPDM
Currently how you would use PPDM is to first run PandaFunctions.py, providing it with the interested rt_id (Request_type id) for the Cater system in question. It should then query, convert and write all the related data of the system within the past year, (Or however long you set the date to go back, note this part is hardcoded)
The next step would be to open the Kibana browser interface and configure the index you have created in ES as a valid index pattern(I have yet to find a workaround to this step, but I’m sure it does exist.)
The final step would be to run PandaVisualizations .py which would generate all of the visualizations and dashboards. 
Note: PythonPanadaDataManagement (PPDM) was the actual part of the stack that I developed in python 2.7 and requires a Unix environment to function
How it is Built
PandaFunctions.py
Establishing a connection with cx_Oracle
First we need to establish a connection with our Oracle database with the cx_Oracle extension for python. We use the “connect” function passing in our login information for our database into its three parameters (username, password, and data source name).
  
cx_Oracle.connect(user = USER, password = PASS, dsn = dsn)  

Actual implementation can be seen at the oracleConnection function in the PandaFunctions.py file.

Establishing a connection with the ES server
To establish a connection to our ES server, we use the “ElasticSearch” extension in python. We then provide the “ElasticSearch” object with the localhost  url, the default being: http://localhost:9200 

es = Elasticsearch('http://localhost:9200')  

Actual implementation can be seen at the oracleConnection function in the PandaFunctions.py file.
 
Querying the data to a list in XML
The purpose of this step is to retrieve the changes, within the specified timeframe, to the trs.requests_info table for the Cater system in question.
The current hardcoded query is:

select  XMLType.GetclobVal(rq_info) from TRS.CATER_XMLDATA_V3 where rt_id = {0} and Last_UPDATED >= sysdate - 360  

Where {0} is the variable we use change the rt_id. 
At this moment, since this project is not being scheduled to run every day, I have set it to query a years worth of information for the specified system. 
The data that our Oracle Database (where Cater is located) has a pre-built table that produces an XML formatted output displaying all changes made to the trs.requests_info table for the Cater system in question.
We then write this data into a list where each entry in the list represents a row of information from the query.
This is a part of an iteration. This process will run once for each row of the XML data.
 
Using xml2json.py
In this step we will take the XML data and convert it into a JSON format, The reason this step is necessary is because ES only accepts data in a JSON format.
xml2json.py was a script I found on GitHub, its author is Hay Kranen and its repository can be found at  https://github.com/hay/xml2json. 
In this part of the script we require the “OS” extension in python which allows us to execute a string as if it was a command in the console.
We first write the XML data into a temporary file, run xml2json.py on the temporary file and read back the output into a python object.
The important thing to note is that we are doing it through iteration, where we handle one entry from the list of XML data at a time.  
Actual implementation can be seen in the xmlCursor function in the PandaFunctions.py file.
 
Reading the newly converted JSON information into Pandas﻿
In this part of the script we require the “Pandas” extension in python. Pandas is an easy to use data-analysis and data structure tool for python. We will not be getting deep into its core functionalities, we are instead just using its dataframe feature. In this step of the process we will use Pandas as a convenient place to manipulate our data, we will insert the newly created python object from xml2json into a Pandas datafame.
Note this step is also a part of the iteration mentioned above, this process will run for each row of the XML data.
 
Manipulating the data in Pandas by adding additional columns﻿
In this step of the process we will remove some un-useful columns and add back the ES index as well as the type. The purpose of us adding these two additional columns is so that ES will know how to index this information. Afterwards, we pivot our data frame, as it was one row with various columns of data, into various rows and one column of data. The purpose of this is to manipulate it into a ES friendly shape. At this point, we append the Panda's dataframe into a list.
Note this step is also a part of the iteration mentioned above, this process will run for each row of the XML data. Afterwards we should be left with a list of dataframes with the corrected data.
 
Deleting the existing ES index ﻿
This step is unfortunately ill thought out, and its primary purpose was for testing during development to ensure the correct data was being written.
In the desired product, we should not need to delete any ES indexes as we should be updating the existing data with new entries through a scheduled run. However in the current state of this product, we are deleting and rewriting the existing index and data every time we reload a system.
 
Enter the new index along with the new data
﻿By default you can always PUT data into ES without setting a index however by default it will mark every string mapping as “analyzed”  which means that it will analyze every string word for word separated by a space instead of the whole string itself.
Which this a problem for our purposes as several of the visualization rely on people's names meaning it would create a entry for first name and another for last name
Example 
analyzed: “Yifan”,” Dai”
not_analyzed: “Yifan Dai” 
To solve this I have forced my script to always enter a manual index to handle this case

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






PandaVisualization.py

Establishing a connection with your ES server

This process is exactly the same as establishing a ES connection in Panda Functions.

Generating a cURL Command to set a Kibana Visualizations into ES

This is perhaps the most complex process of the whole program, and perhaps I did not implement this process in the most optimized manner as it does go through a quite a few functions.
 
The way it is implemented at the moment only allows us to be able to create one dimensional visualizations with one set (axis) of relevant data. However this does not prevent the end user from using the Kibana’s browser interface to create multi-variable or more complex visualizations.

The primary goal of this process is to generate cURL queries that represent visualizations which we can load into ES and have them display in Kibana.
 
Retrieving index should appear as:


curl -XGET http://localhost:9200/{0}/_mappings/timing


where {0} is the ES index
 
 
A sample visualization cURL query should appear as:


curl -XPUT http://localhost:9200/.kibana/visualization/{0}_{1}_{#} -d'
{
	"title":"{0}_{1}_{#}",
	"visState":"
{
"type":"pie",
"params":
{
"shareYAxis":true,
"addTooltip":true,
"addLegend":true,
"isDonut":false
},
"aggs":[
{
"id":"1",
"type":"count",
"schema":"metric",
"params":{}
},
{
"id":"2",
"type":"terms",
"schema":"segment",
"params":
{
"field":"{%}",
"size":100,
"order":"desc",
"orderBy":"1"
}
}],
"listeners":{}}",
	"description":"",
	"version":1,
	"kibanaSavedObjectMeta":
	{
		"searchSourceJSON":"
{
"index":"{1}",
"query":
{
"query_string":
{
"query":"*",
"analyze_wildcard":true
}
},
"filter":[]
               }"
       }
}'


  
  
Every single visualization of the same type (Ie. pie chart, histogram, line graph) would have a similar cURL query, all we have to do is replace the variables.

visualizationGeneration

It starts off in the visualizationGeneration(...) function.
The first step is to retrieve all the different types of variables with the retrieveTypes(...) function.

retrieveTypes

This is the function which uses cURL to retrieve back the JSON data of an index in ES. It then manually (as in hardcoded) goes through the nested levels of the JSON data to find the names of the keys.

Generally all fields are stored in:

NameOfindex 
{
mappings 
{
timing 
{
properties 
{ 
HERE 
}
}
}
}



After it iteratively steps through the whole JSON and collects the names of all the keys, it will return a list of the keys it has gathered.

Creating new types of Visualizations

What actually happens when Kibana loads a saved visualization, it is technically just reading the visualization data from ES. So my approach was to directly insert a valid Kibana visualization cURL queries into ES.

After the retrieveTypes(...) function call in visualizationGeneration(...), we can pass on a list of the keys, which we can then use to generate our cURL queries.

I have manually created a few cURL query templates. What happens is we are filling in the missing fields of these templates  with the appropriate “index for visualization”, “name of visualization”, “key” and “index for data” and then running the cURL query into ES.

For each type of graph, there exists a specific python function and template  for its visualization generation

For example: lineGraphGeneration(listOfKeys,nameOfVisualization,nameOfESIndex):

The actual templates of the cURL queries are located in curlTemplates.py
lineGraphGeneration(...) will produce and run a cURL query for a line graph visualization for each field in the listofKeys(...).

lineGraphGeneration(...) will return a list of visualization indexes it has created.

visualizationGeneration(...) will then return a list of all of the visualization indexes appended together. This will be needed for generating the dashboards.

dashBoardGeneration

Similar to generating visualizations, we have a hard coded cURL template for generating dashboards. 

When generating a dashboard cURL query, we pass the dashBoardGeneration(...) function a list of all visualization indexes, as well as a dashboard index (where we want to store the dashboard). It will then build a cURL query, that holds every single visualization from the list of all visualization indexes, and run the query. 

One important thing we need to manage when creating the dashboard are the sizes of the visualizations and how they will fit on the dashboard.

For simplicity, I have set every visualization to be sized 3 units wide and 2 units tall, where 5 visualizations would fit per row (a row being of height 2 unit);

Note: A user can still manipulate the dashboard as well as the size and position of the visualizations through the Kibana browser interface
 
Future development

Windows Schedule runs, or Run on Call 

Graphical development 
Set up a windows schedules environment where data would be updated daily with the newest entries, 
In the future, the next step for this project would be to not use Kibana, but instead create our own JavaScript visualization tool with the information we have in ES


