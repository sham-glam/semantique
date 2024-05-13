# utils

import numpy as np
import json
import glob
from pprint import pprint
from collections import defaultdict
import os, math, subprocess

import gensim
import gensim.corpora as corpora
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
#vis
import pyLDAvis
import pyLDAvis.gensim

import BnLemma as lm
from bnlp import BengaliPOS
bn_pos = BengaliPOS()




import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def lemmatize_bangla(text):
    if text is not None:
        lemma = lm.Lemmatizer()
        try:
            lemmatized = lemma.lemma(text)
            # print(lemmatized)
            return lemmatized.split()
        except Exception as e:
            # print(f"Error in lemmatizing text: {e}")
            return None



def filter_doc(texts):  
    filtered = []
    for line in texts:
            # print(line)
            
            # print(line)
            filtered_line = [token for token in line if bn_pos.tag(token)[0][1] in ['NC','NP', 'JQ', 'JJ']] # 'NST',, 'AMN', , 'NCgen'
            filtered_line = [token for token in filtered_line if token not in stopwords and len(token)>2]
            line = lemmatize_bangla(' '.join(filtered_line))
            if line is not None:
                filtered.append(line)
                   
    return filtered


###

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    

def calculate_frequency(texts):
    frequency = defaultdict(int)    
    for text in texts:
        for token in text:
            if bn_pos.tag(token)[0][1] in ['NC','NP', 'JQ', 'JJ'] :
                frequency[token] +=1
                
    return dict(frequency)



def specif(f, F, t, T):
    try:
        r_command = f'R --vanilla -s -e \'library("textometry", lib="."); \
                    res <- specificities.distribution.plot({f},{F},{t},{T}); print(res["mode"]); \
                    print(res["pfsum"][[1]][[{f}+1]]);\''
        result = subprocess.check_output(r_command, shell=True, text=True).split('\n') # appel R
        mode, proba = str(result[1]).split()[1], str(result[3]).split()[1]
        if is_float(mode) and is_float(proba):
            mode, proba  = float(mode), float(proba)
            try:
                if mode <= f:
                    specificite = math.fabs(math.log10(math.fabs(proba))) 
                else :
                    specificite = -math.fabs(math.log10(math.fabs(proba))) 
                return specificite
            except ValueError:
                return None
    except subprocess.CalledProcessError as e:
            print(f" {e}.\nErreur en calculant la spécificité  pour : <{f}>, <{F}>, <{t}>, <{T}>")
            return None
    

## calcule f F t T -> appelle specif ##
def process_specif(focus_freq, window_freq, path):
    # if path exists else create it
    if not os.path.exists(path):
        os.makedirs(path)
    F = sum(focus_freq.values())
    T = sum(window_freq.values())
    spec_dict={}
    for key in focus_freq.keys():
        f = focus_freq[key]
        if key in window_freq.keys():
            t = window_freq[key]
        # on exlut les t=0
            specificite = specif(f, F, t, T) # specificite pour mot=key
            if specificite is not None:
                spec_dict[key] = specificite
                filename = path + f"/specif-{f}-{F}-{t}-{T}.txt" 
                with open(filename, 'w') as file:
                    file.write(f'{key}\t{specificite}\n')
        
    return spec_dict      

