import pandas as pd
import numpy as np
import os
import re
import operator
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
import operator
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
# groups = fetch_20newsgroups()
# print(groups.target)

path = "/home/antonis/Downloads/20news-bydate/20news-bydate-train"

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
df_news.content =df_news.content.replace(to_replace='[!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~]',value=' ',regex=True) #remove punctuation except
df_news.content =df_news.content.replace(to_replace='-',value=' ',regex=True)
df_news.content =df_news.content.replace(to_replace='\s+',value=' ',regex=True)    #remove new line
df_news.content =df_news.content.replace(to_replace='  ',value='',regex=True)                #remove double white space
df_news.content =df_news.content.apply(lambda x:x.strip())  # Ltrim and Rtrim of whitespace

df_news['content']=[entry.lower() for entry in df_news['content']]

df_news['Word_tokenize']= [word_tokenize(entry) for entry in df_news.content]
print(df_news)

df_news.to_csv('dfNews.csv')


# WordNetLemmatizer requires Pos tags to understand if the word is noun or verb or adjective etc. By default it is set to Noun
def wordLemmatizer(data):
    tag_map = defaultdict(lambda: wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    file_clean_k = pd.DataFrame()
    for index, entry in enumerate(data):
        print(index)
        # Declaring Empty List to store the words that follow the rules for this step
        Final_words = []
        # Initializing WordNetLemmatizer()
        word_Lemmatized = nltk.WordNetLemmatizer()
        # pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
        for word, tag in nltk.pos_tag(entry):
            # Below condition is to check for Stop words and consider only alphabets
            if len(word) > 1 and word not in stopwords.words('english') and word.isalpha():
                word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
                Final_words.append(word_Final)
                # The final processed set of words for each iteration will be stored in 'text_final'
                file_clean_k.loc[index, 'Keyword_final'] = str(Final_words)
                file_clean_k.loc[index, 'Keyword_final'] = str(Final_words)
                file_clean_k = file_clean_k.replace(to_replace="\[.", value='', regex=True)
                file_clean_k = file_clean_k.replace(to_replace="'", value='', regex=True)
                file_clean_k = file_clean_k.replace(to_replace=" ", value='', regex=True)
                file_clean_k = file_clean_k.replace(to_replace='\]', value='', regex=True)
    return file_clean_k

# file_clean = wordLemmatizer(df_news['Word tokenize'])
#
# file_clean.to_csv('file_clean.csv')
# vocabulary = set()
# for doc in df_news.word:
#     vocabulary.update(doc.split(','))
# vocabulary = list(vocabulary)
#
# print(vocabulary)