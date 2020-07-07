import speech_recognition as sr
import json
import os

import subprocess
import threading,time
WAIT_TIME_SECONDS = 10
isListen=False

from datetime import datetime
import pytz

r= sr.Recognizer()

def main():
    #tz_Rome = pytz.timezone('Europe/Rome')

    #datetime_Rome=datetime.now(tz_Rome)

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)


        print("Current dir"+os.getcwd())
        
        print("Comincia a parlare")

        isListen = True
        audio = r.listen(source)
        print("elaboro il messaggio")
        isListen = False

        file = open("testo.txt","a+")

        try:
            text = r.recognize_google(audio,language="it-IT")
            print("you have said :" + text)
            
            final_txt= (''.join(text)).encode('utf-8').lower()

            wordArray=final_txt.split(' ')
            print(wordArray)

            json_str='{ "Discorso" : [ '
            for word in wordArray[:-1]:
                date=datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
                print(date)
                tmp='{"'+word+'":"'+date+'"},'
                json_str+=tmp

            date=datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
            json_str+='{"'+wordArray[-1]+'":"'+date+'"}'
            json_str+=']}'
            print(json_str)


        # jsonObj = json.loads(json_str)

            file.write(json_str)
            file.close()
           # changeDir(json_str)

        except Exception as e:
            print("Error : "+str(e))

def changeDir(x):
    os.chdir("./Desktop/TapUni/python/bin/")
    file1 = open ("./testo.txt","a+" )
    file1.write(x)
    file1.close()
    path="../../kafka/"
    os.chdir(path)
    print("Cur DIR"+ os.getcwd())
    subprocess.call(["./kafkaProd.sh"],shell=True)
    os.chdir("../../../")

    
#raw_input("Premi un pulsante per cominciare a parlare")
ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
 if(isListen==False):
    main()
    #changeDir(json_str)
