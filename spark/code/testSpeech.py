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
import os

from elasticsearch import Elasticsearch



tz_Rome = pytz.timezone('Europe/Rome')
datetime_Rome = datetime.now(tz_Rome)

with open('../tap/user.txt', 'r') as file:
     data = file.read().split(' ')

topicKafka = data[1].lower()     

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sc = SparkContext(appName="SpeechConsumerTest")
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 2)

spark=SparkSession(sc)
sqlContext = SQLContext(sc)

zkQuorum="127.0.0.1:2181"
topic = topicKafka

elastic_host="localhost"
elastic_index="users"
elastic_document="_doc"


es_write_conf = {
"es.nodes" : elastic_host,
"es.port" : '9200',
"es.resource" : '%s/%s' % (elastic_index,elastic_document),
"es.input.json" : "yes"
}

# Elastic Search
conf = SparkConf(loadDefaults=False)
conf.set("es.index.auto.create", "true")



schema = StructType([StructField("id",StringType(),True),StructField("name", StringType(), True),StructField("message", StringType(), True),StructField("topic", StringType(),True),StructField("language",StringType(),True)])
#cols = ['name', 'message']



storage = sqlContext.createDataFrame(sc.emptyRDD(), schema)




def getInfo(rdd):


    full = rdd.map(lambda (value): json.loads(value)).map(lambda json_object: (json_object["id"],json_object["name"], json_object["message"],json_object["topic"],json_object["language"]))

    line = full.map(lambda x: x[2])
    
    words = line.flatMap(lambda line: line.split(" "))
    count = words.filter(lambda w : w.find("*")>=0).count()


    print("---")
    #print(topicKafka) ## implementazione futura
    #print(count)
    df3 = sqlContext.createDataFrame(full, schema)

    
    milli = int(datetime.now().strftime("%s")) * 1000 
    #print(milli)


    appendend  = storage.union(df3)
    appendend=appendend.withColumn("word_count", F.size(F.split(appendend['message'],' ')))
    appendend=appendend.withColumn("profanity_count",F.lit(count))
    appendend=appendend.withColumn("timestamp",F.lit(milli))
    appendend.show()


    new = appendend.rdd.map(lambda item: {'timestamp': milli ,'id': item['id'],'name': item['name'],'message': item['message'],'profanity_count': item['profanity_count'],'words_count': item['word_count'],'language': item['language'],'topic': item['topic']})
    final_rdd = new.map(json.dumps).map(lambda x: ('key', x))
    print(final_rdd.collect())
      


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
