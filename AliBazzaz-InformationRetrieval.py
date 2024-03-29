# -*- coding: utf-8 -*-


#!pip install hazm

from google.colab import drive
drive.mount('/content/gdrive')

from __future__ import unicode_literals
from hazm import *
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import csv

news = pd.read_csv("/content/gdrive/My Drive/Colab Notebooks/IR-Proj/IR.csv", error_bad_lines = False, sep = "\t" )
print(news.shape)
print(list(news.columns))
news.describe()
print(news)

#news = "/content/gdrive/My Drive/Colab Notebooks/IR-Proj/IR.csv"
#file = open(news,encoding = "utf-8")
#txt = file.read()

#news[0:20]
#news.describe()
#news.shape()
#print(news.loc[[2,9,15]])
#news.count()

AKHBAR = []
with open("/content/gdrive/My Drive/Colab Notebooks/IR-Proj/IR.csv") as csvfobj:
  readCSV = csv.reader(csvfobj, delimiter=',')

  for row in readCSV:
    khabar = row[0]

    AKHBAR.append(khabar)

#print(AKHBAR[1:1000])

normalizer = Normalizer()
normal = normalizer.normalize(str(AKHBAR[0:1000]))
normal

#normal2 = normalizer.normalize(str(AKHBAR[100000:100200]))
#normal2

re_news1 = re.sub(r'\d+', '', str(normal))
re_news1

#re_news2 = re.sub(r'\d+', '', str(normal2))
#re_news2

stop_set = set(stopwords_list())

def filter_stop1(re_news1):
    return [token for token in input_tokens if token not in stopwords_set]

stop_set

#stop_set = set(stopwords_list())

#def filter_stop2(re_news2):
#    return [token for token in input_tokens if token not in stopwords_set]

#stop_set

wt10 = word_tokenize(re_news1)

stopchars = wt10
s_chars = ' '.join(e for e in stopchars if e.isalnum())

wt1 = word_tokenize(s_chars)
wt1

#wt20 = word_tokenize(re_news2)

#stopchars = wt20
#s_chars = ' '.join(e for e in stopchars if e.isalnum())

#wt2 = word_tokenize(s_chars)
#wt2

st1 = sent_tokenize(re_news1)
st1

#st2 = sent_tokenize(re_news2)
#st2

stemmer = Stemmer()
word = wt1
for w in word:
    #w_stem =  w,'->',stemmer.stem(w)
    stem1 = stemmer.stem(w)

    print(stem1)

#stemmer = Stemmer()
#word = wt2
#for w in word:
#    w_stem =  w,'->',stemmer.stem(w)
#    stem2 = stemmer.stem(w)

#    print(stem2)

lemmatizer = Lemmatizer()
word = wt1
for w in word:
    #lemma1 = w,'->',lemmatizer.lemmatize(w)
    lemma1 = lemmatizer.lemmatize(w)
    print(lemma1)

#lemmatizer = Lemmatizer()
#word = wt2
#for w in word:
#    lemma2 = w,'->',lemmatizer.lemmatize(w)
#    lemma2 = lemmatizer.lemmatize(w)
#    print(lemma2)

from google.colab import drive
drive.mount('/content/gdrive')

tagger = POSTagger (model = '/content/gdrive/My Drive/Colab Notebooks/IR-Proj/resources/postagger.model')
tagger.tag(word_tokenize(str(wt1[0:20])))
#print(tagger.tag(word_tokenize(str(w2_t2))))

chunker = Chunker(model = '/content/gdrive/My Drive/Colab Notebooks/IR-Proj/resources/chunker.model')
tagged = tagger.tag(word_tokenize(str(wt1[0:20])))
tree2brackets(chunker.parse(tagged))
#print(tree2brackets(chunker.parse(tagged)))

parser = DependencyParser (tagger = tagger, lemmatizer = lemmatizer)
parser.parse(word_tokenize(str(wt1[0:20])))

a1 = word_tokenize(str(wt1))
texts = a1
texts
#print(str(texts))

#a2 = word_tokenize(str(wt2))
#test = a2
#test
#print(test)

tfidf_vector = TfidfVectorizer (min_df =1, max_df =0.5, ngram_range = (1,2),max_features=500,sublinear_tf = False, stop_words = stop_set )
features = tfidf_vector.fit_transform(texts)

a = pd.DataFrame(features.todense(),columns = tfidf_vector.get_feature_names())
print(a)
print(tfidf_vector.get_feature_names())

# ابعاد دیتاست
print(features.shape)
# داده های دیتاست
#df = pd.DataFrame(features)
#print(features.head())
# وضعیت آماری
#print(features.describe())
#for i, feature in enumerate(tfidf_vector.get_feature_names()):
#    print(i,feature)

X_data = a.to_numpy()
X_data

# Commented out IPython magic to ensure Python compatibility.
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
# %matplotlib inline

kmn=KMeans(n_clusters=3)
kmn.fit(X_data)
labels=kmn.predict(X_data)
labels

#X_data.shape

center=kmn.cluster_centers_
center

plt.scatter(X_data[:,0],X_data[:,1],c=labels, s=250) 
plt.scatter(center[:,0],center[:,1],marker='+',c='black', s=100) 
plt.show()

kmn.inertia_

y=[]
for k in np.arange(1,6):
    kmn=KMeans(n_clusters=k)
    kmn.fit(X_data)
    y.append(kmn.inertia_)
y

plt.plot(np.arange(1,6),y,'o-')
plt.xlabel('nuber of cluster')
plt.ylabel('inertia')
plt.show()

plt.scatter(X_data[:,0],X_data[:,1],c=labels)
plt.xlabel("X0")
plt.ylabel("X1")

from scipy.cluster.hierarchy import linkage,dendrogram,fcluster

hirarachical = linkage(X_data,method='complete')
dendrogram(hirarachical)
plt.show()

from sklearn.cluster import MeanShift

ms=MeanShift()
ms.fit(X_data)
labels = ms.labels_
center=ms.cluster_centers_

plt.scatter(X_data[:,0],X_data[:,1],c=labels)
plt.scatter(center[:,0],center[:,1],marker='+',linewidths=5,s=5)
plt.show()

from sklearn.cluster import DBSCAN

dbscan=DBSCAN()
dbscan.fit(X_data)
labels=dbscan.labels_

labels

plt.scatter(X_data[:,0],X_data[:,10],c=labels)
plt.show()
