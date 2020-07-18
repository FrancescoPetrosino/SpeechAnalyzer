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

class MLAPI:

    def tokenize(text):
        return [stemmer.stem(word) for word in tokenizer.tokenize(text.lower())]

    def __init__(self):
        k_model = joblib.load("python/bin/MachineL/k_model.sav")
        punc = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',"%"]
        stop_words = text.ENGLISH_STOP_WORDS.union(punc)
        vectorizer3 = TfidfVectorizer(stop_words = stop_words, tokenizer = tokenize, max_features = 1000)
        

    def getPrediction(self,message):
        Y = vectorizer3.transform([message])
        prediction = k_model.predict(Y)
        print(prediction)
        return prediction
