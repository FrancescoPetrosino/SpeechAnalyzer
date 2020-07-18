# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 13:51:24 2020

@author: Aldo
"""


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
#import seaborn as sns
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from pathlib import Path

import joblib
tokenizer = RegexpTokenizer(r'[a-zA-Z\']+')
stemmer = SnowballStemmer('english')

def tokenize(text):
        return [stemmer.stem(word) for word in tokenizer.tokenize(text.lower())]

class MLAPI:

    vectorizer3 = None
    k_model = None

    def __init__(self):
        
        self.k_model = joblib.load("python/bin/MachineL/k_model.sav")
        self.vectorizer3 = joblib.load('python/bin/MachineL/vectroizer.pkl')


    def getPrediction(self,message):
        Y = self.vectorizer3.transform([message])
        prediction = self.k_model.predict(Y)
        print(prediction)
        #return prediction




obj = MLAPI()

obj.getPrediction("today my team has scored 4 goals")