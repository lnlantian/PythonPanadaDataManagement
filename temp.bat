curl -XPUT 'http://localhost:9200/pizza16' -d '
{
   "mappings": {
"timing" : {
       "properties" : {
                     "delivery_address": {"type" : "string" , "index": "not_analyzed"},
                     "total_cost" : {"type" : "double"},
                     "pizza_type" : {"type" : "string" , "index": "not_analyzed"},
                     "cost" : {"type" : "string" , "index": "not_analyzed"},
"special_notes" : {"type" : "string" , "index": "not_analyzed"},
 "processing_notes" : {"type" : "string" , "index": "not_analyzed"},
"number_of_pizzas":  {"type" : "string" , "index": "not_analyzed"},
"date_delivered" : {"type" : "date", "format" : "MMM/dd/yyyy HH:mm:ss"},
"crust" : {"type" : "string" , "index": "not_analyzed"},
"rq_id" : {"type" : "long"}
                     }
  }
  }
}
'