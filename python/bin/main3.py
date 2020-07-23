import speech_recognition as sr
import json
import os
from json import dumps
import pyaudio
from kafka import KafkaProducer

import threading,time
WAIT_TIME_SECONDS = 1


import joblib

with open('user.txt', 'r') as file:
    data = file.read().split(' ')



print(data[0])
print(data[1])

from MachineL.API import MLAPI
model = MLAPI()



from googletrans import Translator
translator = Translator()




r = sr.Recognizer()
name = input("Benvenuto, digita il tuo nome per entrare: ")
#name = "turi"

pa = pyaudio.PyAudio()
deviceIndex = 0



def check_offline(text):
    list_pro = open('./python/bin/badwords.txt','r+')
    content = list_pro.read()
    list_content = content.split('\n')
    for word in list_content :
        if word in text :
            remplacement = "*" * len(word)
            text = text.replace(word ,remplacement)
    return text


def main():
    

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)


        #print("Current dir"+os.getcwd())
        #input("Premi un tasto per cominciare a parlare")
        print("Comincia a parlare")

        audio = r.listen(source)
        #print(audio)
        print("elaboro il messaggio")

       # file = open("testo.txt","w+")

        try:
            text = r.recognize_google(audio,language="it-IT")
            #kikprint("you have said :" + text)
            
            final_txt= (''.join(text)).lower()
            #print("Final text : "+final_txt)

            filter_text=check_offline(final_txt)
            print("Testo filtrato - IT : "+filter_text)

            translated = translator.translate(filter_text, src="it",dest='en')
            print("Testo filtrato - EN : "+translated.text)
                 
            
            number = model.getPrediction(translated.text)
            print( " predetto : -- "+str(number))

            wordArray=translated.text.split(' ')
            #print(wordArray)
            #print("Passed split")

            #prefabs
            
            key="key"
            fieldname="name"
            topic = "topic"

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
            json_str += wordArray[-1] +'","'+topic+'" : "'+str(number)+'"}'

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

ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
    #print(os.getcwd())
    main()
