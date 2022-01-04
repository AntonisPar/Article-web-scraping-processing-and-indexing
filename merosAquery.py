import os
import json

with open('tf_idf.json') as json_file:
    tf_idf = json.load(json_file)
with open('article_map.json') as json_file:
    map = json.load(json_file)
print(map)


print("hello there")
print("Enter 1 to search via query")
select = int(input())
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
while select != 0:
    if select == 1:
        while True:
            distinct = []
            count = 1
            feedback = {}
            print("Enter search query terms (type \'exit!\' to exit search)")
            query = str(input())
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
                print("URL's")
                for i in feedback:
                    print(i)
    else:
        print('invalid input')
        print('Enter 1 to search via query or 0 to exit the program')
        select = int(input())












