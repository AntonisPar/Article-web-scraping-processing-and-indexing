
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
import os
import threading
from nltk.stem import SnowballStemmer
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
import time
start_time = time.time()
import multiprocessing as mp

nltk.download('averaged_perceptron_tagger')
import json

basic_stopwords = stopwords.words('english')
wordnet_lemmatizer = WordNetLemmatizer()
snowball_stemmer = SnowballStemmer('english')
nltk.download('wordnet')
nltk.download('punkt')
ps = PorterStemmer()
articles_processed = []
vocabulary = []
article_ids = []

closed_categories = ['CC', 'CD', 'DT', 'EX', 'IN', 'LS', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'RP', 'TO', 'UH', 'WDT',
                     'WP', 'WP$', 'WRB']


def gather():
    articles_processed = {}
    vocabulary = []
    article_ids = {}
    id = 0
    iid = 0
    for file in os.listdir('news'):#loading the news articles from the news folder

        if file.endswith('.json'):
            path = os.path.join('news', file)
            f = open(path)
            newsite = json.load(f)

        else:
            continue
        articles = []
        for i in newsite:
            id = id + 1
            article_ids[id] = i #creating an id -> link article map
            newsite[i] = newsite[i].lower()  #converting all the letters of the articles to lowercase
            articles.append(nltk.word_tokenize(newsite[i])) #divide articles into tokens with nltk
        for article in articles:
            iid = iid + 1
            article = [word for word in article if word not in basic_stopwords and word.isalnum()]  # remove basic stopwords
            tagged_article = nltk.pos_tag(article) #classifying words into their parts of speech and labeling them accordingly
            stopwords = gather_stopwords(tagged_article)  # creating a list with the stopwords found
            article = [custom_lemmatizer(word[0],word[1]) for word in tagged_article] #lemmatizing words with the help of pos tags...word[0] is the word and word[1] is the tag
            article = [word for word in article if word not in stopwords]#remove stopwords found from pos tags
            articles_processed[iid] = article #id -> article map


    return articles_processed, article_ids

def gather_stopwords(tagged_article): #giving as argument the tokenized article with pos tags
    stopwords = []
    for word in tagged_article:
        lemmatized_word = custom_lemmatizer(word[0], word[1])
        if lemmatized_word == 1: #if custom_lemmatizer returns 1, the word is stopword
            stopwords.append(word[0]) #creating a list with stopwords found in the article
    return stopwords

def custom_lemmatizer(word, pos_tag): #takes as argument the word and the pos tag

    flag = 0
    for tag in closed_categories:
        if pos_tag == tag: #if pos tag is a close category tag, the functions returns flag with value 1
            flag = 1
            return flag
    if flag == 0: #if not , the word gets lemmatized according to its part of speech
        if pos_tag.startswith("N"):
            word = wordnet_lemmatizer.lemmatize(word, wordnet.NOUN)
            vocabulary.append(word)
            return (word)
        elif pos_tag.startswith('V'):
            word = wordnet_lemmatizer.lemmatize(word, wordnet.VERB)
            vocabulary.append(word)
            return (word)
        elif pos_tag.startswith('J'):
            word = wordnet_lemmatizer.lemmatize(word, wordnet.ADJ)
            vocabulary.append(word)
            return (word)
        elif pos_tag.startswith('R'):
            word = wordnet_lemmatizer.lemmatize(word, wordnet.ADV)
            vocabulary.append(word)
            return (word)
        else:
            return None

# keep the count of the documents containing a word
def count_dict(articles_processed):
    word_count = {}
    for word in vocabulary:
        word_count[word] = 0
        for article in articles_processed:
            if word in articles_processed[article]:
                word_count[word] += 1
    return word_count


def termfreq(document, word): #calculating the term frequency
    N = len(document)
    occurance = len([token for token in document if token == word])
    return occurance / N


def inverse_doc_freq(word): #calculating the idf value
    try:
        word_occurance = word_count[word] + 1
    except:
        word_occurance = 1
    return np.log(len(articles_processed) / word_occurance)


def create_index(articles_processed): #creating the inverted index
    iter = 0
    inverted_index = {}
    for word in vocabulary:
        wordd = {} #using this dictionary to create the final nested dictionary
        for i in articles_processed:
            if word in articles_processed[i]:#if word exists in an article, calculate the tfidf value on that article and append it on the wordd dictionary
                tf = termfreq(articles_processed[i], word)
                idf = inverse_doc_freq(word)
                value = tf * idf
                wordd[i] = value
        inverted_index[word] = wordd #append the wordd dictionary to the inverted_index dictionary using as key the word
        iter = iter + 1
    return inverted_index


dictionary = {}


articles_processed, article_ids = gather()
vocabulary = set(vocabulary)
print(len(vocabulary))
word_count = count_dict(articles_processed)
inverted_index = create_index(articles_processed)
print(len(articles_processed))

def save(file, name):
    a_file = open(name + ".json", "w")
    json.dump(file, a_file)
    a_file.close()
save(inverted_index, "tf_idf")
save(article_ids, "article_map")

print("--- %s articles processed ---" % len(articles_processed))
print("--- %s vocabulary length ---" % len(vocabulary))

print("--- %s processing time ---" % (time.time() - start_time))










