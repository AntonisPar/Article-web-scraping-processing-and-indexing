from sklearn.datasets import fetch_20newsgroups
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
from nltk.corpus import names
from nltk.stem import PorterStemmer
import numpy as np
import nltk
import pandas as pd
import os
nltk.download('names')
from sklearn.feature_extraction.text import TfidfVectorizer
ps = PorterStemmer()
all_names = names.words()
WNL = WordNetLemmatizer()

path_train= "/home/antonis/Downloads/20news-bydate/20news-bydate-train"
path_test = "/home/antonis/Downloads/20news-bydate/20news-bydate-test"


def gather(path):
    df = pd.DataFrame()
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
            df = pd.concat([df, temp])



    df.content =df.content.replace(to_replace='From:(.*\n)', value='', regex=True) ##remove from to email
    df.content =df.content.replace(to_replace='lines:(.*\n)', value='', regex=True)
    df.content =df.content.replace(to_replace='Subject:(.*\n)', value='', regex=True)
    df.content =df.content.replace(to_replace='[!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~]', value=' ', regex=True) #remove punctuation except
    df.content =df.content.replace(to_replace='-', value=' ', regex=True)
    df.content =df.content.replace(to_replace='\s+', value=' ', regex=True)    #remove new line
    df.content =df.content.replace(to_replace='  ', value='', regex=True)                #remove double white space
    df.content =df.content.apply(lambda x:x.strip())  # Ltrim and Rtrim of whitespace

    df['content']=[entry.lower() for entry in df['content']]
    return df

df_news_train = gather(path_train)
df_news_test = gather(path_test)


def clean(data):
    cleaned = defaultdict(list)
    count = 0
    for group in data:
        for words in group.split():
            if words.isalpha() and words not in all_names:
                words = ps.stem(words)
                cleaned[count].append(WNL.lemmatize(words.lower()))
        cleaned[count] = ' '.join(cleaned[count])
        count +=1
    return(list(cleaned.values()))

x_train = clean(df_news_train['content'])
x_test = clean(df_news_test['content'])


tf = TfidfVectorizer(stop_words='english', max_features=8000)
X_train = tf.fit_transform(x_train)

print(tf.vocabulary_)

