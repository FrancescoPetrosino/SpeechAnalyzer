import speech_recognition as sr
import json
import os
from json import dumps
import pyaudio
from kafka import KafkaProducer

import threading,time
WAIT_TIME_SECONDS = 1
#import time
#from datetime import datetime


import sys
reload(sys)
sys.setdefaultencoding("utf-8")

r = sr.Recognizer()
name = raw_input("Benvenuto, digita il tuo nome per entrare: ")
#name = "turi"

pa = pyaudio.PyAudio()
deviceIndex = 0
'''
for i in range(pa.get_device_count()) :
    print(pa.get_device_info_by_index(i))
    print( "----")
    if pa.get_device_info_by_index(i).get("name") == "hdmi" :
        deviceIndex = i
'''


def check_offline(text):
    list_pro = open('./python/bin/badwords.txt','r+')
    content = list_pro.read()
    list_content = content.split('\n')
    for word in list_content :
        if word in text :
            remplacement = "*" * len(word)
            text = text.replace(word ,remplacement)
            #print word
            #print remplacement
    return text




def main():
    

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
            #print("you have said :" + text)
            
            final_txt= (''.join(text)).encode('utf-8').lower()
            print("Final text : "+final_txt)

            filter_text=check_offline(final_txt)
            print("Testo filtrato - : "+filter_text)

            wordArray=filter_text.decode().split(' ')
            #print(wordArray)
            #print("Passed split")

            #prefabs
            
            key="key"
            fieldname="name"

            '''
            #approccio 1
            json_str='{"'+fieldname+'":"'+name+'" , "message" : [ '
            for word in wordArray[:-1]:

                print(date)
                tmp='{"'+key+'":"'+word+'"},'
                json_str+=tmp

            #date=datetime_Rome.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
            json_str+='{"'+key+'":"'+wordArray[-1]+'"}'
            json_str+=']}'
            

            #approccio 2
            json_str = ''
            for word in wordArray[:-1] :
                json_str += '{"' + name + '" : "' + word + '"}, '

            json_str += '{"' + name + '" : "' + wordArray[-1] + '"}'
            '''

            #approccio 3
            json_str='{"'+fieldname+'":"'+name+'" , "message" : "'
            for word in wordArray[:-1] :
                json_str += word + ' '
            json_str += wordArray[-1] +'"}'

            print(json_str)

            producer = KafkaProducer(bootstrap_servers=['192.168.1.28:9092'],
            value_serializer=lambda x: 
            dumps(x).encode('utf-8')
            )
            
            data = json_str

            producer.send('myTap',value=data)
           


            producer.flush()


        except Exception as e:
            print("Error : "+str(e))

#raw_input("Premi un pulsante per cominciare a parlare")



ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
    #print(os.getcwd())
    main()
