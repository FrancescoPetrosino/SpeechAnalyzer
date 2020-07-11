from __future__ import print_function
import sys
import json
from json import loads
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
#from urllib.parse import unquote
from pyspark.sql import Row
#from pyspark.sql import Col
from pyspark.sql.session import SparkSession
import pyspark.sql.types as tp
from pyspark.sql.types import *
from pyspark.sql.functions import *

sc = SparkContext(appName="SpeechConsumerTest")
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 1)

spark=SparkSession(sc)


zkQuorum="127.0.0.1:2181"
topic = "myTap"

schema = StructType([StructField('name',StringType()), StructField('message',StringType())])
#cols = ['name', 'message']

def getName(rdd):

    #Prende entrambi


    full = rdd.map(lambda (value): json.loads(value)).map(lambda json_object: (json_object["name"], json_object["message"]))
    

   

    
    name=rdd.map(lambda (value): json.loads(value)).map(lambda json_object: json_object["name"])
    message=rdd.map(lambda (value): json.loads(value)).map(lambda json_object: json_object["message"])

    

    #nameCollect=name.collect()
    #messageCollect=message.collect()
    fullCollect=full.collect()

    '''
    if not nameCollect:
        print("No name")
        return
    if not messageCollect:
        print("No Message")
        return
    '''   
    if not fullCollect:
        print("No Message")
        return
    
    

    print("********************")
    
    #print((nameCollect))
    #print((messageCollect))
    print(fullCollect)

    #foreach element in nameCollect
    #df = spark.createDataFrame([element], schema)

    #Crea rdd
    #rowRdd = name.map(lambda w: Row(id=1,name=w))
    

    #fullRdd=full.map(lambda w: Row(name=w)) 


    rowRdd = name.map(lambda w: Row(name=w)) 
    rowRdd2 = message.map(lambda w1: Row(message=w1))

    newRdd = rowRdd.concat()


    merge = rowRdd.union(rowRdd2)
    print(merge.collect())
    #da rdd a dataframe

    #nameDataFrame = spark.createDataFrame(rowRdd)
    #messageDataFrame = spark.createDataFrame(rowRdd2)

    resultDataframe = spark.createDataFrame(merge,schema)
    resultDataframe.show()

    print("Dataframe : \n")
    #nameDataFrame.show()
    #messageDataFrame.show()
    #resultDataframe.show()
   # df.show()

kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1},)
kvs.pprint()



#print(type(kvs))

#dati arrivati in ordine

lines = kvs.map(lambda x: x[1])
lines2=lines.map(lambda x: loads(x.decode('utf-8')))


lines2.pprint()
lines2.foreachRDD(getName)


#Estrapolo il nome
#lines3 = lines2.map(lambda (value): json.loads(value)).map(lambda json_object:(json_object["name"]))
#lines3.pprint()

#Estrapolo l'intero messaggio che arriva
#lines4 = lines2.map(lambda (value): json.loads(value)).map(lambda json_object:(json_object["message"]))
#lines4.pprint()





ssc.start()
ssc.awaitTermination()

# { \"name\":\"ciccio\",\"Message\" : [ {\"key\":\"ciao\"},{\"key\":\"come\"},{\"key\":\"stai\"}]}