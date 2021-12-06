import os
import json

with open('tf_idf.json') as json_file:
    tf_idf = json.load(json_file)
with open('article_map.json') as json_file:
    map = json.load(json_file)



print("GLOSSIKI TEXNOLOGIA")
print("Enter 1 to search via query")
select = int(input())
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
while select != 0:
    if select == 1:
        while True:
            distinct = []
            count = 1
            feedback = {}
            print("Enter search query terms (type \'exit!\' to finish query or exit search)")
            query = str(input())
            temp = {}
            if len(query.split()) > 1:
                for term in query.split():
                    for lemma in tf_idf:
                        if lemma == term:
                            result = tf_idf[lemma]
                            for article in result:
                                if article not in distinct:
                                    distinct.append(article)
                                    url = map[article]
                                    weight = result[article]
                                    feedback[url] = weight
                                else:
                                    url = map[article]
                                    weight = result[article]
                                    feedback[url] = feedback[url] + weight

                feedback = sorted(feedback.items(), key=lambda x: x[1], reverse=True)
                print("URL's")
                for i in feedback:
                    print(i)










