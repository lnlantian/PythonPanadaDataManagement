#####################################################################
# Curl Templates 
# Notes: Add them as you need it
# Yifan Dai is a very handsome man!
######################################################################


#Legend
#{0} : The type of graph it is (ie line, hist, pie, area)
#{1} : The name of the index (ie: rt_id_376)
#{%} : The name of the field you are trying to graph (ie: PEOPLE.ASSIGNED.@USERID)


curlLine ='''
curl -XPUT http://localhost:9200/.kibana/visualization/{0}_{1}_{%} -d'
{
	"title":"{0}_{1}_{%}",
	"visState":"{\\"aggs\\":[{\\"id\\":\\"1\\",\\"params\\":{},\\"schema\\":\\"metric\\",\\"type\\":\\"count\\"},{\\"id\\":\\"2\\",\\"params\\":{\\"field\\":\\"{%}\\",\\"order\\":\\"desc\\",\\"orderBy\\":\\"1\\",\\"size\\":100},\\"schema\\":\\"segment\\",\\"type\\":\\"terms\\"}],\\"listeners\\":{},\\"params\\":{\\"addLegend\\":true,\\"addTooltip\\":true,\\"defaultYExtents\\":false,\\"shareYAxis\\":true},\\"type\\":\\"line\\"}",
	"description":"","version":1,
	"kibanaSavedObjectMeta":
	{
		"searchSourceJSON":"{\\"index\\":\\"{1}\\",\\"query\\":{\\"query_string\\":{\\"analyze_wildcard\\":true,\\"query\\":\\"*\\"}},\\"filter\\":[]}"
	}
}'
'''

curlLineDate = '''
curl -XPUT http://localhost:9200/.kibana/visualization/{0}_{1}_{%} -d'
{
    "title":"{0}_{1}_{%}",
    "visState":"{\\"type\\":\\"line\\",\\"params\\":{\\"shareYAxis\\":true,\\"addTooltip\\":true,\\"addLegend\\":true,\\"defaultYExtents\\":false},\\"aggs\\":[{\\"id\\":\\"1\\",\\"type\\":\\"count\\",\\"schema\\":\\"metric\\",\\"params\\":{}},{\\"id\\":\\"2\\",\\"type\\":\\"date_histogram\\",\\"schema\\":\\"segment\\",\\"params\\":{\\"field\\":\\"{%}\\",\\"interval\\":\\"week\\",\\"min_doc_count\\":1,\\"extended_bounds\\":{}}}],\\"listeners\\":{}}",
    "description":"",
    "version":1,
    "kibanaSavedObjectMeta":
    {
        "searchSourceJSON":"{\\"index\\":\\"{1}\\",\\"query\\":{\\"query_string\\":{\\"query\\":\\"*\\",\\"analyze_wildcard\\":true}},\\"filter\\":[]}"
    }
}'
'''


curlHist= '''
curl -XPUT http://localhost:9200/.kibana/visualization/{0}_{1}_% -d'
'{
	"title":"title":"{0}_{1}_%",
	"visState":"{\\"type\\":\\"histogram\\",\\"params\\":{\\"shareYAxis\\":true,\\"addTooltip\\":true,\\"addLegend\\":true,\\"mode\\":\\"stacked\\",\\"defaultYExtents\\":false},\\"aggs\\":[{\\"id\\":\\"1\\",\\"type\\":\\"count\\",\\"schema\\":\\"metric\\",\\"params\\":{}},{\\"id\\":\\"2\\",\\"type\\":\\"terms\\",\\"schema\\":\\"segment\\",\\"params\\":{\\"field\\":\\"%\\",\\"size\\":100,\\"order\\":\\"desc\\",\\"orderBy\\":\\"1\\"}}],\\"listeners\\":{}}",
	"description":"",
	"version":1,"
	kibanaSavedObjectMeta":
	{
		"searchSourceJSON":"{\\"index\\":\\{1}\\",\\"query\\":{\\"query_string\\":{\\"query\\":\\"*\\",\\"analyze_wildcard\\":true}},\\"filter\\":[]}"
	}
}'
'''

curlArea= '''
curl -XPUT http://localhost:9200/.kibana/visualization/{0}_{1}_% -d'
{
	"title":"{0}_{1}_%",
	"visState":"{\\"type\\":\\"area\\",\\"params\\":{\\"shareYAxis\\":true,\\"addTooltip\\":true,\\"addLegend\\":true,\\"mode\\":\\"stacked\\",\\"defaultYExtents\\":false},\\"aggs\\":[{\\"id\\":\\"1\\",\\"type\\":\\"count\\",\\"schema\\":\\"metric\\",\\"params\\":{}},{\\"id\\":\\"2\\",\\"type\\":\\"date_histogram\\",\\"schema\\":\\"segment\\",\\"params\\":{\\"field\\":\\"%\\",\\"interval\\":\\"month\\",\\"min_doc_count\\":1,\\"extended_bounds\\":{}}}],\\"listeners\\":{}}",
	"description":"",
	"version":1,
	"kibanaSavedObjectMeta":
	{
		"searchSourceJSON":"{\\"index\\":\\"{1}\\",\\"query\\":{\\"query_string\\":{\\"query\\":\\"*\\",\\"analyze_wildcard\\":true}},\\"filter\\":[]}"
	}
}'
'''

curlPie = '''    
curl -XPUT http://localhost:9200/.kibana/visualization/{0}_{1}_% -d'
{
    "title":"{0}_{1}_%",
    "visState":"{\\"type\\":\\"pie\\",\\"params\\":{\\"shareYAxis\\":true,\\"addTooltip\\":true,\\"addLegend\\":true,\\"isDonut\\":false},\\"aggs\\":[{\\"id\\":\\"1\\",\\"type\\":\\"count\\",\\"schema\\":\\"metric\\",\\"params\\":{}},{\\"id\\":\\"2\\",\\"type\\":\\"terms\\",\\"schema\\":\\"segment\\",\\"params\\":{\\"field\\":\\"%\\",\\"size\\":100,\\"order\\":\\"desc\\",\\"orderBy\\":\\"1\\"}}],\\"listeners\\":{}}",
    "description":"",
    "version":1,
    "kibanaSavedObjectMeta":
    {
        "searchSourceJSON":"{\\"index\\":\\"{1}\\",\\"query\\":{\\"query_string\\":{\\"query\\":\\"*\\",\\"analyze_wildcard\\":true}},\\"filter\\":[]}"
    }
}'   
'''