import pandas as pd
import numpy as np
import os
import re
import operator
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
import operator
from sklearn.feature_extraction.text import TfidfVectorizer
stopwords = stopwords.words('english')
wordnet_lemmatizer = WordNetLemmatizer()
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
# groups = fetch_20newsgroups()
# print(groups.target)

path = "/home/antonis/Downloads/20news-bydate/20news-bydate-train"
clean= pd.read_csv ('file_clean.csv')
# count_vector = CountVectorizer(max_features=500,stop_words='english',lowercase=True)
# data_count = count_vector.fit_transform(groups.data)
# print(count_vector.get_feature_names())


df_news = pd.DataFrame()
print(df_news)



for file in os.listdir(path):
    tag = file
    for doc in os.listdir(path+'/'+file):
        docpath = path+'/'+file+'/'+doc
        f = open(docpath, "r",encoding='cp1252')
        content = f.read()
        temp = pd.DataFrame(
            {
                'content':content,
                'tag':tag
            },index=[0]
        )
        df_news = pd.concat([df_news,temp])



df_news.content =df_news.content.replace(to_replace='From:(.*\n)',value='',regex=True) ##remove from to email
df_news.content =df_news.content.replace(to_replace='lines:(.*\n)',value='',regex=True)
df_news.content =df_news.content.replace(to_replace='Subject:(.*\n)',value='',regex=True)
df_news.content =df_news.content.replace(to_replace='[!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~]',value=' ',regex=True) #remove punctuation except
df_news.content =df_news.content.replace(to_replace='-',value=' ',regex=True)
df_news.content =df_news.content.replace(to_replace='\s+',value=' ',regex=True)    #remove new line
df_news.content =df_news.content.replace(to_replace='  ',value='',regex=True)                #remove double white space
df_news.content =df_news.content.apply(lambda x:x.strip())  # Ltrim and Rtrim of whitespace

df_news['content']=[entry.lower() for entry in df_news['content']]


df_news['Word_tokenize']= [word_tokenize(entry) for entry in df_news.content]
df_news['Word_tokenize']= [word for word in df_news.Word_tokenize if word not in stopwords]


df_news.merge(clean,left_index=True, right_index=True)
df_news.to_csv('letsSee.csv')
# df_news['Word_tokenize']= [wordnet_lemmatizer.lemmatize(entry) for entry in df_news.Word_tokenize]

# article = [wordnet_lemmatizer.lemmatize(word) for word in article]
