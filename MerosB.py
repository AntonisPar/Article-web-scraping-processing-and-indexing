from sklearn.datasets import fetch_20newsgroups
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
from nltk.corpus import names
from nltk.stem import PorterStemmer
import numpy as np
import nltk
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import sigmoid_kernel
import json
import sys
from sklearn.feature_extraction.text import TfidfTransformer
from numpy import asarray
from numpy import savetxt

nltk.download('names')
ps = PorterStemmer()
all_names = names.words()
WNL = WordNetLemmatizer()

path_train= "/home/antonis/Downloads/20news-bydate/20news-bydate-train"
path_test= "/home/antonis/Downloads/20news-bydate/20news-bydate-test"


#gathering all the articles from 20news-bydate-train in a single dataframe
def gather(path):
    df = pd.DataFrame() #this will be the final dataframe
    for file in os.listdir(path):
        tag = file
        for doc in os.listdir(path+'/'+file):
            docpath = path+'/'+file+'/'+doc
            f = open(docpath, "r",encoding='cp1252')
            content = f.read()
            temp = pd.DataFrame( #creating a temporary dataframe to store the current content and tag
                {
                    'content':content,
                    'tag':tag
                },index=[0]
            )
            df = pd.concat([df, temp]) #merge the temp dataframe with the final one



    df.content =df.content.replace(to_replace='From:(.*\n)', value='', regex=True) ##remove from to email
    df.content =df.content.replace(to_replace='lines:(.*\n)', value='', regex=True)
    df.content =df.content.replace(to_replace='Subject:(.*\n)', value='', regex=True)#remove subject
    df.content =df.content.replace(to_replace='[!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~]', value=' ', regex=True) #remove punctuation
    df.content =df.content.replace(to_replace='-', value=' ', regex=True)
    df.content =df.content.replace(to_replace='\s+', value=' ', regex=True)    #remove new line
    df.content =df.content.replace(to_replace='  ', value='', regex=True)                #remove double white space
    df.content =df.content.apply(lambda x:x.strip())  # ltrim and ltrim of whitespace

    df['content']=[entry.lower() for entry in df['content']] #to lowercase
    return df

df_news_train = gather(path_train)



def clean(data):
    cleaned = defaultdict(list)
    count = 0
    for group in data:
        for words in group.split():
            if words.isalpha():
                words = ps.stem(words) #creating stems
                cleaned[count].append(words.lower())#to lowercase
        cleaned[count] = ' '.join(cleaned[count])
        count +=1
    return(list(cleaned.values()))

x_train = clean(df_news_train['content'])


tf = TfidfVectorizer(stop_words='english', max_features=8000,use_idf=True) #Initializing the vectorizer.Setting 8000 features
tfidf = tf.fit_transform(x_train)#fit_transform learns vocabulary and idf, returns document-term matrix.

vocab = tf.vocabulary_

#EVALUATION PART

#perform the same process for the test data
def clean_test(data):
    cleaned = defaultdict(list)
    count = 0
    for words in data.split():
        if words.isalpha() and words not in all_names:
            words = ps.stem(words)
            cleaned[count].append(WNL.lemmatize(words.lower()))
    cleaned[count] = ' '.join(cleaned[count])
    count +=1
    return(list(cleaned.values()))

df_news_test = gather(path_test)

df_news_test['content'] = df_news_test['content'].apply(clean_test)

# x_test = clean(df_news_test['content'])

def similarity(document,tfidf,metric):
    testvector = tf.transform(document)#create vector for each document that needs to be classified
    if metric=='cosine':
        score = cosine_similarity(testvector, tfidf)
    elif metric=='euclidean':
        score = euclidean_distances(testvector, tfidf)
    elif metric == 'sigmoid':
        score = sigmoid_kernel(testvector, tfidf)
    else:
        sys.exit()
    prediction = np.argmax(score, 1)#returns the index of the biggest value
    predicted = df_news_train['tag'].iloc[prediction]#locating the tag of the article that had the biggest score
    return predicted

#df=df_news_test
def classify(df,metric):
    classified = pd.DataFrame()#this is were the classified docs will be stored
    doc_count = len(df.index)
    correct = 0
    for row in df.itertuples():
        predicted = similarity(row[1],tfidf,metric)#returns the predicted class
        temp = pd.DataFrame( #creating a temporary dataframe to store the current classified doc
        {
            'document':row[1],
            'class':predicted
        },index=[0])
        classified = pd.concat([classified, temp])#merge temp dataframe with the final one
        actual = row[2]
        if actual == predicted[0]:#actual is the correct class from the df_news_test
            correct=correct + 1
    accuracy = correct/doc_count
    print(correct)
    percentage = "{:.0%}".format(accuracy)
    print(percentage)
    return classified

classified = classify(df_news_test,'manhattan')

def save(file, name):
    a_file = open(name + ".json", "w")
    json.dump(file, a_file)
    a_file.close()

#
save(classified, "classified")