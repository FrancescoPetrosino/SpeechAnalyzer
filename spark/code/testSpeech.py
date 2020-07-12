from __future__ import print_function
import sys
import json
from json import loads
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
#from urllib.parse import unquote
from pyspark.sql import Row
<<<<<<< HEAD
#import org.apache.spark.sql.Row
=======
>>>>>>> 4634f062eed34b1b47702d42fcf27dec3e6a5b10
#from pyspark.sql import Col
from pyspark.sql.session import SparkSession
import pyspark.sql.types as tp
from pyspark.sql.types import *
from pyspark.sql.functions import *
<<<<<<< HEAD
from pyspark.sql import SQLContext


sc = SparkContext(appName="SpeechConsumerTest")
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 2)

spark=SparkSession(sc)
sqlContext = SQLContext(sc)
=======

sc = SparkContext(appName="SpeechConsumerTest")
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 1)

spark=SparkSession(sc)

>>>>>>> 4634f062eed34b1b47702d42fcf27dec3e6a5b10

zkQuorum="127.0.0.1:2181"
topic = "myTap"

<<<<<<< HEAD
schema = StructType([StructField("name", StringType(), True),StructField("message", StringType(), True)])
#cols = ['name', 'message']



#storage=spark.createDataFrame(sc.emptyRDD[Row], schema)
storage = sqlContext.createDataFrame(sc.emptyRDD(), schema)
tmpDf = sqlContext.createDataFrame(sc.emptyRDD(), schema)
def getInfo(rdd):
=======
schema = StructType([StructField('name',StringType()), StructField('message',StringType())])
#cols = ['name', 'message']

def getName(rdd):
>>>>>>> 4634f062eed34b1b47702d42fcf27dec3e6a5b10

    #Prende entrambi


    full = rdd.map(lambda (value): json.loads(value)).map(lambda json_object: (json_object["name"], json_object["message"]))
<<<<<<< HEAD

    '''
    name1=full.map(lambda x: (x[0]))
    nameCollect=name1.collect()
    print(nameCollect)

    message1=full.map(lambda x: (x[0]))
    messageCollect=message1.collect()
    print(messageCollect)
    '''


    #name=rdd.map(lambda (value): json.loads(value)).map(lambda json_object: json_object["name"])
    #message=rdd.map(lambda (value): json.loads(value)).map(lambda json_object: json_object["message"])

    df3 = sqlContext.createDataFrame(full, schema)

    appendend  = storage.union(df3)

    #storage=tmpDf.union(df3)
    appendend.show()






    #nameCollect=name.collect()
    #messageCollect=message.collect()
    #fullCollect=full.collect()
=======
    

   

    
    name=rdd.map(lambda (value): json.loads(value)).map(lambda json_object: json_object["name"])
    message=rdd.map(lambda (value): json.loads(value)).map(lambda json_object: json_object["message"])

    

    #nameCollect=name.collect()
    #messageCollect=message.collect()
    fullCollect=full.collect()
>>>>>>> 4634f062eed34b1b47702d42fcf27dec3e6a5b10

    '''
    if not nameCollect:
        print("No name")
        return
    if not messageCollect:
        print("No Message")
        return
<<<<<<< HEAD
       
    if not fullCollect:
        print("No Message")
        return
    '''
=======
    '''   
    if not fullCollect:
        print("No Message")
        return
    
>>>>>>> 4634f062eed34b1b47702d42fcf27dec3e6a5b10
    

    print("********************")
    
    #print((nameCollect))
    #print((messageCollect))
<<<<<<< HEAD
    #print(fullCollect)
    
    #print(full.collect()[0])
    #print(full.take(1)[1-1])
=======
    print(fullCollect)

>>>>>>> 4634f062eed34b1b47702d42fcf27dec3e6a5b10
    #foreach element in nameCollect
    #df = spark.createDataFrame([element], schema)

    #Crea rdd
<<<<<<< HEAD
    
=======
    #rowRdd = name.map(lambda w: Row(id=1,name=w))
>>>>>>> 4634f062eed34b1b47702d42fcf27dec3e6a5b10
    

    #fullRdd=full.map(lambda w: Row(name=w)) 


<<<<<<< HEAD
    #owRdd = name.map(lambda w: Row(name=w)) 
    #rowRdd2 = message.map(lambda w1: Row(message=w1))

    #newRdd = rowRdd.concat()


    #merge = rowRdd.union(rowRdd2)
    #print(merge.collect())
    #da rdd a dataframe

    
    #messageDataFrame = spark.createDataFrame(rowRdd2)

    #resultDataframe = spark.createDataFrame(merge,schema)
    #resultDataframe.show()

    #print("Dataframe : \n")
=======
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
>>>>>>> 4634f062eed34b1b47702d42fcf27dec3e6a5b10
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
<<<<<<< HEAD
lines2.foreachRDD(getInfo)
=======
lines2.foreachRDD(getName)
>>>>>>> 4634f062eed34b1b47702d42fcf27dec3e6a5b10


#Estrapolo il nome
#lines3 = lines2.map(lambda (value): json.loads(value)).map(lambda json_object:(json_object["name"]))
#lines3.pprint()

#Estrapolo l'intero messaggio che arriva
#lines4 = lines2.map(lambda (value): json.loads(value)).map(lambda json_object:(json_object["message"]))
#lines4.pprint()





ssc.start()
ssc.awaitTermination()

# { \"name\":\"ciccio\",\"Message\" : [ {\"key\":\"ciao\"},{\"key\":\"come\"},{\"key\":\"stai\"}]}