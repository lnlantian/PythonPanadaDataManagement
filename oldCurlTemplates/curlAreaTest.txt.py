curl -XPUT http://localhost:9200/.kibana/visualization/yifan_is_awesome2.3?=pretty -d'
{
	"title":"yifan_is_awsome1.3",
	"visState":"{\"type\":\"area\",\"params\":{\"shareYAxis\":true,\"addTooltip\":true,\"addLegend\":true,\"mode\":\"stacked\",\"defaultYExtents\":false},\"aggs\":[{\"id\":\"1\",\"type\":\"count\",\"schema\":\"metric\",\"params\":{}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"SUBMITDATE\",\"interval\":\"month\",\"min_doc_count\":1,\"extended_bounds\":{}}}],\"listeners\":{}}",
	"description":"",
	"version":1,
	"kibanaSavedObjectMeta":
	{
		"searchSourceJSON":"{\"index\":\"yifan_is_awesome1\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"
	}
}'