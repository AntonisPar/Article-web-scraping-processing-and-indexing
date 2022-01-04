import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
import os
from nltk.stem import SnowballStemmer
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet

import random
from nltk import FreqDist
nltk.download('averaged_perceptron_tagger')
import json
stopword = stopwords.words('english')
wordnet_lemmatizer = WordNetLemmatizer()
snowball_stemmer = SnowballStemmer('english')
nltk.download('wordnet')
nltk.download('punkt')
ps = PorterStemmer()
articles_processed = []
vocabulary = []
article_ids = []

closed_categories = ['CC','CD','DT','EX','IN','LS','MD','PDT','POS','PRP','PRP$','RP','TO','UH','WDT','WP','WP$','WRB']

def gather():
    articles_processed = {}
    vocabulary = []
    article_ids = {}
    id = 0
    iid = 0
    for file in os.listdir('news'):

        if file.endswith('.json'):
            path = os.path.join('news', file)
            f = open(path)
            newsite = json.load(f)

        else:
            continue
        articles = []
        for i in newsite:
            id = id + 1
            article_ids[id] = i
            newsite[i] = newsite[i].lower()
            articles.append(nltk.word_tokenize(newsite[i]))
            # [res.append(x) for x in test_list if x not in res]
        for article in articles:
            iid = iid + 1
            article = nltk.pos_tag(article)
            for i in article:
                print(i)
                pos_tag = i[1]
                word = i[0]
                flag = 0
                for tag in closed_categories:
                    if i[1] == tag:
                        flag = 1
                if flag == 0:
                    if pos_tag.startswith("N"):
                        vocabulary.append(wordnet_lemmatizer.lemmatize(word, wordnet.NOUN))
                    elif pos_tag.startswith('V'):
                        vocabulary.append(wordnet_lemmatizer.lemmatize(word, wordnet.VERB))
                    elif pos_tag.startswith('J'):
                        vocabulary.append(wordnet_lemmatizer.lemmatize(word, wordnet.ADJ))
                    elif pos_tag.startswith('R'):
                        vocabulary.append(wordnet_lemmatizer.lemmatize(word, wordnet.ADV))
            articles_processed[iid] = article

    return vocabulary,articles_processed,article_ids





def create(vocabulary,articles_processed):
    # Creating an index for each word in our vocab.
    index_dict = {}  # Dictionary to store index for each word
    i = 0
    for word in vocabulary:
        index_dict[word] = i
        i += 1

# keep the count of the documents containing a word
def count_dict(articles_processed):
    word_count = {}
    for word in vocabulary:
        word_count[word] = 0
        for article in articles_processed:
            if word in articles_processed[article]:
                word_count[word] += 1
    return word_count



def termfreq(document, word):
    N = len(document)
    occurance = len([token for token in document if token == word])
    return occurance / N

def inverse_doc_freq(word):
    try:
        word_occurance = word_count[word] + 1
    except:
        word_occurance = 1
    return np.log(len(articles_processed) / word_occurance)


def create_index(articles_processed):
    inverted_index = {}
    for word in vocabulary:
        wordd = {}
        for i in articles_processed:
            if word in articles_processed[i]:
                tf = termfreq(articles_processed[i],word)
                idf = inverse_doc_freq(word)
                value = tf * idf
                wordd[i] = value
        inverted_index[word] = wordd
    return inverted_index


dictionary = {}
vocabulary,articles_processed,article_ids = gather()
word_count = count_dict(articles_processed)
# dictionary = create(vocabulary,articles_processed)
inverted_index = create_index(articles_processed)

print(len(vocabulary))
print(len(articles_processed))
def save(file,name):
    a_file = open(name+".json", "w")
    json.dump(file, a_file)
    a_file.close()


save(inverted_index, "tf_idf")
save(article_ids,"article_map")













