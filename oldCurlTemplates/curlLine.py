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
	curl -XPUT http://localhost:9200/.kibana/visualization/yifan_is_awesome2.1?=pretty -d'
	{
	    "title":"yifan_is_awesome2.1",
	    "visState":"{\\"type\\":\\"line\\",\\"params\\":{\\"shareYAxis\\":true,\\"addTooltip\\":true,\\"addLegend\\":true,\\"defaultYExtents\\":false},\\"aggs\\":[{\\"id\\":\\"1\\",\\"type\\":\\"count\\",\\"schema\\":\\"metric\\",\\"params\\":{}},{\\"id\\":\\"2\\",\\"type\\":\\"date_histogram\\",\\"schema\\":\\"segment\\",\\"params\\":{\\"field\\":\\"SUBMITDATE\\",\\"interval\\":\\"week\\",\\"min_doc_count\\":1,\\"extended_bounds\\":{}}}],\\"listeners\\":{}}",
	    "description":"",
	    "version":1,
	    "kibanaSavedObjectMeta":
	    {
	        "searchSourceJSON":"{\\"index\\":\\"yifan_is_awesome1\\",\\"query\\":{\\"query_string\\":{\\"query\\":\\"*\\",\\"analyze_wildcard\\":true}},\\"filter\\":[]}"
	    }
	}'
	'''