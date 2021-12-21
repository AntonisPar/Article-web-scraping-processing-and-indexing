import os
import json

with open('tf_idf.json') as json_file:
    tf_idf = json.load(json_file)
with open('article_map.json') as json_file:
    map = json.load(json_file)



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
                        if lemma == term:            #an to term tou query yparxei sto eurethrio
                            result = tf_idf[lemma]   #epistrefei ta articles pou periexoun auton ton oro kai ta tfidf varh
                            for article in result:
                                if article not in distinct: #xrhsimopoiw to distinct giati mporei parapanw apo ena  term tou query na epistrefoun to idio article.We dont want duplicates.
                                    distinct.append(article)
                                    url = map[article] #epistrefw to utl tou article mesw tou article_map
                                    weight = result[article] #tfidf tou term sto article
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












