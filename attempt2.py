import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
import os
from nltk.stem import SnowballStemmer
import random
from nltk import FreqDist
nltk.download('averaged_perceptron_tagger')
import json
stopword = stopwords.words('english')
wordnet_lemmatizer = WordNetLemmatizer()
snowball_stemmer = SnowballStemmer('english')
nltk.download('wordnet')
nltk.download('punkt')

articles_processed = []
vocabulary = []

article_ids = []

def gather():
    articles_processed = {}
    vocabulary = []
    article_ids = {}
    id = 0
    for file in os.listdir('news'):

        if file.endswith('.json'):
            path = os.path.join('news', file)
            f = open(path)
            newsite = json.load(f)

        else:
            print('ok')
            continue
        articles = []
        for i in newsite:
            newsite[i] = newsite[i].lower()
            articles.append(nltk.word_tokenize(newsite[i]))
            # [res.append(x) for x in test_list if x not in res]
        for article in articles:
            id = id + 1
            article_ids[i] = id
            article = [word for word in article if word not in stopword]
            article = [word for word in article if word.isalnum()]
            article = [wordnet_lemmatizer.lemmatize(word) for word in article]
            vocabulary.extend(x for x in article if x not in vocabulary)
            articles_processed[id] = article


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
            for sent in articles_processed:
                if word in articles_processed[sent]:
                    word_count[word] += 1
        return word_count

    word_count = count_dict(articles_processed)

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

    def tf_idf(article,id):
        pairs = {}
        tf_idf_vec = np.zeros((len(vocabulary),))
        for word in article:
            tf = termfreq(article, word)
            idf = inverse_doc_freq(word)
            value = tf * idf
            tf_idf_vec[index_dict[word]] = value
            pairs[word] = value
        # return tf_idf_vec
        return pairs

    dict = {}
    for id in articles_processed:
        pairs = tf_idf(articles_processed[id],id)
        dict.update(pairs)
    return dict


dictionary = {}
vocabulary,articles_processed,article_ids = gather()
dictionary = create(vocabulary,articles_processed)









