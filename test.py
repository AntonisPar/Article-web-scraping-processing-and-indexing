import os
import json
import requests
import time
start_time = time.time()
word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
WORDS = response.content.splitlines()

with open('tf_idf.json') as json_file:
    tf_idf = json.load(json_file)
with open('article_map.json') as json_file:
    map = json.load(json_file)


queries = ['apple','bike','banana','covid','omicron','hospital','death','uk','usa','germany','marriage','greece','study','university','bag','car','airport','rest','summer','winter',
           'create vaccine','drop music','new business','goverment failed','summer vacation','winter vacation','ski resort','car business','new treatment','trips cancelled',
           'help people','first aid','wasted time','plant trees','save earth','soial justice','save earth','elected president','covid cases','novel books',
           'machine learning carreer','save the planet','plant more trees','new season revealed','netflix increases prices','world chip shortage','goverment bans smoking',
           'new years resolution','inflation rises gobally','geopolitical issues aegean','summer vacation greece','save your time','invest economics crypto','omicron cases rise',
           'spend money now','sales season started','christmas vacation london','study in london','create new business','plant more trees','gigantic cap fallacious','faint assorted handle',
           'so sunny outside','wear a costume','buy a milk','eat a cake','kiss some girls','got vacations tomorrow','school need renovation','iphones best phones',
           'psychotic sneaky dog','apple bike banana covid','omicron hospital death uk','usa germany marriage Greece','study university bag car','airport rest summer winter',
           'create vaccine drop music','new business goverment failed','summer vacation winter vacation','ski resort car business','new treatment trips cancelled',
           'help people first aid','wasted time plant trees','save earth social justice','save earth elected president','covid cases novel books',
           'machine learning carreer save' 'the planet plant more','new season revealed netflix','increases prices world chip','invest economics crypto omicron',
           'Strangest Thing In  Refrigerator','Favorite Toy Growing Up','horror movie night before','eally strain your ears','moved forward only because','hand sanitizer helps actually','preparation for the race','teeth brush her nails','mysterious diary records simple','difference between Pepsi Coke']
number_of_queries = len(queries)
for query in queries:
    distinct = []
    count = 1
    feedback = {}
    if query == 'exit!':
        select = 0
        break
    temp = {}
    if len(query.split()) >= 1:
        for term in query.split():
            for lemma in tf_idf:
                if lemma == term:            #checks if query term exists
                    result = tf_idf[lemma]   #returns the articles containing this term and the corresponding tfidf values
                    for article in result:
                        if article not in distinct: #using distinct to prevent duplicate articles.Some term may return the same article
                            distinct.append(article)
                            url = map[article] #storing the article's url
                            weight = result[article] #saving the term's tfidf value in the article
                            feedback[url] = weight #gia kathe article dinw san varos to tfidf pou epistrafhke
                        else:
                            url = map[article]
                            weight = result[article]
                            feedback[url] = feedback[url] + weight #athroisma varwn twn orwn pou entopisthkan se ena article

        feedback = sorted(feedback.items(), key=lambda x: x[1], reverse=True)
        for i in feedback:
            print(query)
            print(i)

time_elapsed = time.time() - start_time
print("--- %s seconds ---" % time_elapsed)
time_per_query = time_elapsed/number_of_queries
print("--- %s time per query  ---" %time_per_query)











