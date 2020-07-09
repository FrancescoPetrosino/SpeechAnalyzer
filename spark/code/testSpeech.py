from __future__ import print_function
import sys
import json
from json import loads
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


sc = SparkContext(appName="SpeechConsumerTest")
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 1)

zkQuorum="127.0.0.1:2181"
topic = "myTap"



def getName():
    name=rdd.map(lambda (value): json.loads(value)).map(lambda json_object: json_object["name"])
    namesCollect=name.collect()
    if not namesCollect:
        print("No name")
        return




kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1},)
kvs.pprint()

kvs.foreachRDD(getName)

#print(type(kvs))

#dati arrivati in ordine

lines = kvs.map(lambda x: x[1])
lines2=lines.map(lambda x: loads(x.decode('utf-8')))

#Estrapolo il nome
#lines3 = lines2.map(lambda (value): json.loads(value)).map(lambda json_object:(json_object["name"]))
#lines3.pprint()

#Estrapolo l'intero messaggio che arriva
#lines4 = lines2.map(lambda (value): json.loads(value)).map(lambda json_object:(json_object["message"]))
#lines4.pprint()





ssc.start()
ssc.awaitTermination()

# { \"name\":\"ciccio\",\"Message\" : [ {\"key\":\"ciao\"},{\"key\":\"come\"},{\"key\":\"stai\"}]}