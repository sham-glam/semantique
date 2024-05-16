# utils

from pprint import pprint
from collections import defaultdict, Counter
import os, math, subprocess, random
from itertools import chain

import gensim
import gensim.corpora as corpora
from gensim.corpora import Dictionary
from gensim.models import TfidfModel

from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
#vis
import pyLDAvis
import pyLDAvis.gensim

import BnLemma as lm
from bnlp import BengaliPOS
import regex


# global variables
bn_pos = BengaliPOS()
from bnlp import BengaliCorpus as corpus
stopwords = corpus.stopwords[:20] + ['রি' + 'টি']

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)



def filter_doc(texts):  
    filtered = []
    for line in texts:
            filtered_line = [token for token in line if bn_pos.tag(token)[0][1] in ['NC','NP']] # 'NST',, 'AMN', , 'NCgen'
            filtered_line = [token for token in filtered_line if token not in stopwords and len(token)>2]
            line = ' '.join(filtered_line)
            line = regex.sub(r'(শুক্রবার|শনিবার|রবিবার|সোমবার|মঙ্গলবার|বুধবার|বৃহস্পতিবার)', '', line)
            line = regex.sub(r'(১২৩৪৫৬৭৮৯০)', '', line)
            line = regex.sub(r'(জানুয়ারী|ফেব্রুয়ারী|মার্চ|এপ্রিল|মে|জুন|জুলাই|আগস্ট|সেপ্টেম্বর|অক্টোবর|নভেম্বর|ডিসেম্বর)', '', line)
            line = lemmatize_bangla(line)

            if line is not None:
                filtered.append(line)
                   
    return filtered



# lecture des fichiers txt , aka corpus
# def read_corpus(corpus, num_lines=1000):
#     data = open(corpus, 'r')
#     lines = data.readlines(num_lines) # lecture par ligne
#     lines = [line for line in lines if not line.startswith('Image') and len(line)>0]
#     docs = [line.split() for line in lines]
#     filtered_docs = filter_doc(docs)

#     return filtered_docs

def read_corpus(corpus, num_lines=1000):
    random.seed(42)
    data = open(corpus, 'r')
    lines = data.readlines()  # lecture de toutes les lignes
    lines = [line for line in lines if not line.startswith('Image') and len(line)>0]
    random.shuffle(lines)  # mélange des lignes
    lines = lines[:num_lines]  # sélectionne les num_lines premières lignes
    docs = [line.split() for line in lines]
    filtered_docs = filter_doc(docs)

    return filtered_docs



def lemmatize_bangla(text):
    if text is not None:
        lemma = lm.Lemmatizer()
        try:
            lemmatized = lemma.lemma(text)
            return lemmatized.split()
        except Exception as e:
            return None




def get_corpus(corpus, id2word):

    tfidf = TfidfModel(corpus, id2word=id2word)
    low_value = 0.03
    words = []
    words_missing_in_tfidf = []

    # enlève les termes trops fréquents
    for i in range(0, len(corpus)):
        bow = corpus[i]
        low_value_words = [] 
        tfidf_ids = [id for id, value in tfidf[bow]]
        bow_ids = [id for id, value in bow]
        low_value_words = [id for id, value in tfidf[bow] if value < low_value]
        drops = low_value_words+words_missing_in_tfidf
        for item in drops:
            words.append(id2word[item])
        words_missing_in_tfidf = [id for id in bow_ids if id not in tfidf_ids] # The words with tf-idf socre 0 will be missing

        new_bow = [b for b in bow if b[0] not in low_value_words and b[0] not in words_missing_in_tfidf]
        corpus[i] = new_bow

    return corpus



### Partie II - calcul de spécificité ###

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
            if bn_pos.tag(token)[0][1] in ['NC','NP'] :
                # if token not in frequency.keys():
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


# get_higest_lowest_specificity
def get_higest_lowest_specificity(filtered_docs, num=20):
    focus_ratio = 1/3
    split_index = int(len(filtered_docs) * focus_ratio)
    focus_dict = calculate_frequency(filtered_docs[:split_index])
    window_dict= calculate_frequency(filtered_docs[split_index:])
    specificite = process_specif(focus_dict, window_dict, path="cache/") # dict specificite
    max_values = dict(sorted(specificite.items(), key=lambda item: -item[1])[:num])
    min_values = dict(sorted(specificite.items(), key=lambda item: item[1])[:num])

    return max_values, min_values

