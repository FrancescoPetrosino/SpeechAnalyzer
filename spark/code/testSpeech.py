from __future__ import print_function
import sys
import json
from json import loads
from pyspark import SparkContext

from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import Row

from pyspark.sql.session import SparkSession
import pyspark.sql.types as tp
from pyspark.sql.types import *
import pyspark.sql.functions as F
from pyspark.sql import SQLContext
import re
from pyspark.sql.functions import lit
import pytz
from datetime import datetime



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

schema = StructType([StructField("name", StringType(), True),StructField("message", StringType(), True),StructField("topic", StringType(),True)])
#cols = ['name', 'message']



#storage=spark.createDataFrame(sc.emptyRDD[Row], schema)
storage = sqlContext.createDataFrame(sc.emptyRDD(), schema)
#tmpDf = sqlContext.createDataFrame(sc.emptyRDD(), schema)



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
    #print("My time \n")
    #print(datetime.datetime.now())
    #print(datetime_Rome.now())
    #print(words.collect())
    #print(count)


    #name=rdd.map(lambda (value): json.loads(value)).map(lambda json_object: json_object["name"])
    #message=rdd.map(lambda (value): json.loads(value)).map(lambda json_object: json_object["message"])

    df3 = sqlContext.createDataFrame(full, schema)

    appendend  = storage.union(df3)
    appendend=appendend.withColumn("word_count", F.size(F.split(appendend['message'],' ')))
    appendend=appendend.withColumn("profanity_count",F.lit(count))
    appendend=appendend.withColumn("time",F.lit(datetime_Rome.now())).show(truncate=False)



kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1},)
#kvs.pprint()



#print(type(kvs))

#dati arrivati in ordine

lines = kvs.map(lambda x: x[1])
lines2=lines.map(lambda x: loads(x.encode('utf-8')))


lines2.pprint()
lines2.foreachRDD(getInfo)


#Estrapolo il nome
#lines3 = lines2.map(lambda (value): json.loads(value)).map(lambda json_object:(json_object["name"]))
#lines3.pprint()

#Estrapolo l'intero messaggio che arriva
#lines4 = lines2.map(lambda (value): json.loads(value)).map(lambda json_object:(json_object["message"]))
#lines4.pprint()





ssc.start()
ssc.awaitTermination()

# { \"name\":\"ciccio\",\"Message\" : [ {\"key\":\"ciao\"},{\"key\":\"come\"},{\"key\":\"stai\"}]}