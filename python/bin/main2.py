import speech_recognition as sr
import json
import os
from json import dumps
import pyaudio
from kafka import KafkaProducer

import threading,time
WAIT_TIME_SECONDS = 1

from datetime import datetime
import pytz

r= sr.Recognizer()
name=input("Benvenuto, digita il tuo nome per entraPremi un tasto per cominciare a parlarere")



def main():
    tz_Rome = pytz.timezone('Europe/Rome')

    datetime_Rome=datetime.now(tz_Rome)

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)


        #print("Current dir"+os.getcwd())
        #input("Premi un tasto per cominciare a parlare")
        print("Comincia a parlare")

        audio = r.listen(source)
        print("elaboro il messaggio")

       # file = open("testo.txt","w+")

        try:
            text = r.recognize_google(audio,language="it-IT")
            print("you have said :" + text)
            
            final_txt= (''.join(text)).encode('utf-8').lower()
            print("Passed encode")

            wordArray=final_txt.decode().split(' ')
            print(wordArray)
            print("Passed split")

            json_str='{ "'+name+'" : [ '
            for word in wordArray[:-1]:
                date=datetime_Rome.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
                print(date)
                tmp='{"'+word+'":"'+date+'"},'
                json_str+=tmp

            date=datetime_Rome.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
            json_str+='{"'+wordArray[-1]+'":"'+date+'"}'
            json_str+=']}'
            # print(json_str)

            producer = KafkaProducer(bootstrap_servers=['192.168.1.28:9092']
            ,
            value_serializer=lambda x: 
            dumps(x).encode('utf-8')
            )
            
            data = {'Oggetto' : json_str}

            producer.send('myTap',value=data)
           


            producer.flush()


        except Exception as e:
            print("Error : "+str(e))

#raw_input("Premi un pulsante per cominciare a parlare")
ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
    main()
#changeDir(json_str)
