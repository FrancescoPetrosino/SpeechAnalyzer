from time import sleep
from json import dumps
from kafka import KafkaProducer

file = open("testo.txt","r+")

discorso = file.read()
print("QUi")
print(discorso)

producer = KafkaProducer(bootstrap_servers=['10.0.100.23:9092']
            ,
            value_serializer=lambda x: 
            dumps(x).encode('utf-8')
            )
            
data = {'Oggetto' : discorso}

producer.send('myTap',value=data)
producer.flush()