import speech_recognition as sr
import json
import os
from json import dumps
import pyaudio
from kafka import KafkaProducer
from rfc5654Language import *
from kafka.admin import KafkaAdminClient, NewTopic


import threading,time
WAIT_TIME_SECONDS = 1


import pickle
import uuid
from MachineL.API import MLAPI

#POSSIBILE IMPLEMENTAZIONE FUTURA, le frasi dette le reinserisco nel dataset per poterlo ampliarlo

with open('./spark/user.txt', 'r') as file:
     data = file.read().split(' ')

print("****** Starting main******")




#Informazioni
 #Nome
 #Compagnia (Topic)
 #Language (English, Italian, ecc...)

#print("MyLG")
#print(RfcLanguage[data[2]].value)


#from MachineL.API import MLAPI
#model = MLAPI()

model = None


from googletrans import Translator
translator = Translator()




r = sr.Recognizer()
#name = input("Benvenuto, digita il tuo nome per entrare: ")
#name = "turi"

name = data[0]

topicKafka = data[1].lower()

myLanguage=RfcLanguage[data[2]].value
u_id = uuid.uuid4().hex[:8]

print(myLanguage)
language = data[2]

try:
    admin_client = KafkaAdminClient(
        bootstrap_servers="192.168.1.28:9092", 
        client_id='test'
    )
    topic_list = [NewTopic(name=topicKafka, num_partitions=1, replication_factor=1)]
    admin_client.create_topics(new_topics=topic_list, validate_only=False)

except Exception as e:
    print("Topic exists : "+str(e)) 



def check_offline(text):
    list_pro = open('./python/bin/badwords.txt','r+')
    content = list_pro.read()
    list_content = content.split('\n')
    for word in list_content :
        if word in text :
            remplacement = "*" * len(word)
            text = text.replace(word ,remplacement)
    return text


def sendInfo():
    

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print(StartToSpeachTranslate[language].value)

        audio = r.listen(source)
        #print(audio)
        print(MessageProcessTranslate[language].value)

       # file = open("testo.txt","w+")

        try:
            text = r.recognize_google(audio,language=myLanguage)
            final_txt= (''.join(text)).lower()
            filter_text=check_offline(final_txt)

            scrString = myLanguage.split('-')[0]
            print(scrString)

            translated = translator.translate(filter_text, src=scrString,dest='en')
            print(TranslateTextTranslate[language].value + " : " + translated.text)
                 
            
            number = model.getPrediction(translated.text)
            topicStr=""
            switcher = { 
                0: "Entertainment", 
                1: "Sport", 
                2: "Business",
                3: "Tech",
                4: "Politics", 
            }

            topicStr=switcher.get(number,"None") 


            #print(PredictionTranslate[language].value + " : -- " + str(number))

            wordArray=translated.text.split(' ')
            #print(wordArray)
            #print("Passed split")

            #prefabs
            
            key="key"
            fieldname="name"
            topic = "topic"
            

            #approccio 3
            json_str='{"'+fieldname+'":"'+name+'" , "message" : "'
            for word in wordArray[:-1] :
                json_str += word + ' '
            json_str += wordArray[-1] +'","'+topic+'" : "'+topicStr+'","language" : "'+scrString+'","id":"'+u_id+'"}'

            print(json_str)

            producer = KafkaProducer(bootstrap_servers=['192.168.1.28:9092'],
            value_serializer=lambda x: 
            dumps(x).encode('utf-8')
            )
            
            data = json_str

            producer.send(topicKafka,value=data)
           


            producer.flush()


        except Exception as e:
            print("Error : "+str(e))

ticker = threading.Event()
if __name__=='__main__':
    with open('./python/bin/MachineL/kmodel.pkl', 'rb') as f:
        model = pickle.load(f)
    while not ticker.wait(WAIT_TIME_SECONDS):
        sendInfo()
