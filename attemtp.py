import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
import os
from nltk.stem import SnowballStemmer
from nltk import FreqDist
nltk.download('averaged_perceptron_tagger')
import json
stopword = stopwords.words('english')
wordnet_lemmatizer = WordNetLemmatizer()
snowball_stemmer = SnowballStemmer('english')
nltk.download('wordnet')
nltk.download('punkt')


def preprocess(newsite,id):
    idl = id
    articles = []
    for i in newsite:
        newsite[i] = newsite[i].lower()
        articles.append(nltk.word_tokenize(newsite[i]))

    articles_processed = []
    vocabulary = []
    for article in articles:
        article = [word for word in article if word not in stopword]
        article = [word for word in article if word.isalnum()]
        article = [wordnet_lemmatizer.lemmatize(word) for word in article]
        vocabulary.extend(article)
        articles_processed.append(article)

    # Creating an index for each word in our vocab.
    index_dict = {}  # Dictionary to store index for each word
    i = 0
    for word in vocabulary:
        index_dict[word] = i
        i += 1

    # keep the count of the documents containing a word
    def count_dict(articles_processes):
        word_count = {}
        for word in vocabulary:
            word_count[word] = 0
            for sent in articles_processed:
                if word in sent:
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
        return np.log(len(articles) / word_occurance)

    def tf_idf(article):
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
    for sent in articles_processed:
        pairs = tf_idf(sent)
        dict.update(pairs)

    print(dict)



for file in os.listdir('news'):
        id = 0
        if file.endswith('.json'):
                path = os.path.join('news',file)
                f = open(path)
                newsite = json.load(f)
                id = id+1
                preprocess(newsite,id)
        else:
                print('ok')
                continue

