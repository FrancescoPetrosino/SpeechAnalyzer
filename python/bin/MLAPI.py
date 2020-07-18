# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 13:51:24 2020

@author: Aldo
"""

import asyncio
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from pathlib import Path


class MLAPI:

    def __init__(self):
        k_model = joblib.load("k_model.sav")

    def getPrediction(self,message):
    Y = vectorizer3.transform([message])
    prediction = kmeans.predict(Y)
    print(prediction)
    return prediction
