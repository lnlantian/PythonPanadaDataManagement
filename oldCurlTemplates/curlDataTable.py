curl -XPUT http://localhost:9200/.kibana/visualization/yifan_is_awesome2.2?=pretty -d'
{
	"title":"yifan_is_awesome2.2",
	"visState":"{\"type\":\"table\",\"params\":{\"perPage\":10,\"showPartialRows\":false,\"showMeticsAtAllLevels\":false},\"aggs\":[{\"id\":\"1\",\"type\":\"count\",\"schema\":\"metric\",\"params\":{}},{\"id\":\"2\",\"type\":\"terms\",\"schema\":\"bucket\",\"params\":{\"field\":\"STATUS\",\"size\":100,\"order\":\"desc\",\"orderBy\":\"1\"}}],\"listeners\":{}}",
	"description":"",
	"version":1,
	"kibanaSavedObjectMeta":
	{
		"searchSourceJSON":"{\"index\":\"yifan_is_awesome1\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"}
}