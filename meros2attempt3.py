from sklearn.datasets import fetch_20newsgroups
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
from nltk.corpus import names
import numpy as np
import nltk
import pandas as pd
import os
nltk.download('names')
from sklearn.feature_extraction.text import TfidfVectorizer

path = "/home/antonis/Downloads/20news-bydate/20news-bydate-train"

# groups = fetch_20newsgroups()
#
# data_train = fetch_20newsgroups(subset='train', random_state=21)
# train_label = data_train.target
# data_test = fetch_20newsgroups(subset='test', random_state=21)
# test_label = data_test.target
# len(data_train.data), len(data_test.data), len(test_label)
#
# np.unique(test_label)
df_news = pd.DataFrame()
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

all_names = names.words()
WNL = WordNetLemmatizer()



def clean(data):
    cleaned = defaultdict(list)
    count = 0
    for group in data:
        for words in group.split():
            if words.isalpha() and words not in all_names:
                cleaned[count].append(WNL.lemmatize(words.lower()))
        cleaned[count] = ' '.join(cleaned[count])
        count +=1
    return(list(cleaned.values()))

x_train = clean(df_news['content'])

print(x_train)


tf = TfidfVectorizer(stop_words='english', max_features=1000)
X_train = tf.fit_transform(x_train)

print(X_train)