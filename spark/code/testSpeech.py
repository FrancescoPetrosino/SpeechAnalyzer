from __future__ import print_function
import sys
import json
from json import loads
from pyspark import SparkContext

from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import Row
from pyspark.conf import SparkConf
from pyspark.sql.session import SparkSession
import pyspark.sql.types as tp
from pyspark.sql.types import *
import pyspark.sql.functions as F
from pyspark.sql import SQLContext
import re
from pyspark.sql.functions import lit
import pytz
import pandas as pd
from datetime import date, datetime


from elasticsearch import Elasticsearch



tz_Rome = pytz.timezone('Europe/Rome')
datetime_Rome = datetime.now(tz_Rome)


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sc = SparkContext(appName="SpeechConsumerTest")
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 2)

spark=SparkSession(sc)
sqlContext = SQLContext(sc)

zkQuorum="127.0.0.1:2181"
topic = "myTap"

elastic_host="localhost"
elastic_index="users"
elastic_document="_doc"

'''
#conf1



------------------------------------------------------------------------
#conf2
conf={ "es.resource" : "<INDEX> / <INDEX>", "es.mapping.id":"id", 
         "es.input.json": "true", "es.net.http.auth.user":"elastic",
         "es.write.operation":"index", "es.nodes.wan.only":"false",
         "es.net.http.auth.pass":"changeme", "es.nodes":"<NODE1>, <NODE2>, <NODE3>...",
         "es.port":"9200" })
'''
es_write_conf = {
# specify the node that we are sending data to (this should be the master)
"es.nodes" : elastic_host,
# specify the port in case it is not the default port
"es.port" : '9200',
# specify a resource in the form 'index/doc-type'
"es.resource" : '%s/%s' % (elastic_index,elastic_document),
# is the input JSON?
"es.input.json" : "yes"
}
# Elastic Search
conf = SparkConf(loadDefaults=False)
conf.set("es.index.auto.create", "true")



schema = StructType([StructField("name", StringType(), True),StructField("message", StringType(), True),StructField("topic", StringType(),True)])
#cols = ['name', 'message']


#storage=spark.createDataFrame(sc.emptyRDD[Row], schema)
storage = sqlContext.createDataFrame(sc.emptyRDD(), schema)
#tmpDf = sqlContext.createDataFrame(sc.emptyRDD(), schema)

def transform(doc):
    import hashlib

    _json = json.dumps(doc)
    keys = doc.keys()
    for key in keys:
        if doc[key] == 'null' or doc[key] == 'None':
            del doc[key]
    if not doc.has_key('id'):
        id = hashlib.sha224(_json).hexdigest()
        doc['id'] = id
    else:
        id = doc['id']
    _json = json.dumps(doc)

    #print(_json)
    return (_json)


def print_rows(row):
    data = json.loads(row)
    for key in data:
        print ("{key}:{value}".format(key=key, value=data[key]))

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def getInfo(rdd):


    full = rdd.map(lambda (value): json.loads(value)).map(lambda json_object: (json_object["name"], json_object["message"],json_object["topic"]))
    #full2 = rdd.map(lambda (value): json.loads(value)).map(lambda json_object: (json_object["name"], json_object["topic"]))

    line = full.map(lambda x: x[1])
    #number = full2.map(lambda x: x[1])
    #numberPredict = full.map(lambda x: x[2])

    #counts = words.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)
    words = line.flatMap(lambda line: line.split(" "))
    count = words.filter(lambda w : w.find("*")>=0).count()


    print("---")
    df3 = sqlContext.createDataFrame(full, schema)
    date_time = datetime_Rome.now().strftime("%m/%d/%Y")

    appendend  = storage.union(df3)
    appendend=appendend.withColumn("word_count", F.size(F.split(appendend['message'],' ')))
    appendend=appendend.withColumn("profanity_count",F.lit(count))
    appendend=appendend.withColumn("time",F.lit(date_time))
    appendend.show()

    

    new = appendend.rdd.map(lambda item: {'name': item['name'],'message': item['message'],'profanity_count': item['profanity_count'],'topic': item['topic'],'time': item['time']})
    final_rdd = new.map(json.dumps).map(lambda x: ('key', x))
    print(final_rdd.collect())
      
    '''
    #Metodo1
    appendend.write.format(
    'org.elasticsearch.spark.sql'
    ).option(
    'es.nodes', 'localhost'
    ).option(
    'es.port', 9200
    ).option(
    'es.resource', '%s/%s' % (elastic_index,elastic_document)
    ).save()
    '''
    '''
    #Metodo2
    rdd_mapped = appendend.rdd.map(lambda y: y.asDict())
    result_rdd = rdd_mapped.map(json.dumps(appendend,indent=4, sort_keys=True, default=str))
    final_rdd = result_rdd.map(lambda x: ('key', x))
    '''

    #print("***")
    #print(final_rdd.collect())

    
    final_rdd.saveAsNewAPIHadoopFile(
    path='-',
    outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
    keyClass="org.apache.hadoop.io.NullWritable",
    valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
    conf=es_write_conf)
    

kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1},)

lines = kvs.map(lambda x: x[1])
lines2=lines.map(lambda x: loads(x.encode('utf-8')))
#lines2.pprint()
lines2.foreachRDD(getInfo)

'''
mapping = {
  "mappings": {
    "properties": {
      "name":    { "type": "text" },  
      "message":  { "type": "text"  }, 
      "prof_count":   { "type": "integer"  },
      "words_count":   { "type": "integer"  },
      "time":     { "type": "date", "format": "MM-dd-dd"}
    }
  }
}
'''
mapping = {
    "mappings": {
        "properties": {
            "timestamp": {
                "type": "date"
            }
        }
    }
}


elastic = Elasticsearch(hosts=[elastic_host])

response = elastic.indices.create(
    index=elastic_index,
    body=mapping,
    ignore=400 # ignore 400 already exists code
)

if 'acknowledged' in response:
    if response['acknowledged'] == True:
        print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])

# catch API error response
elif 'error' in response:
    print ("ERROR:", response['error']['root_cause'])
    print ("TYPE:", response['error']['type'])



ssc.start()
ssc.awaitTermination()
