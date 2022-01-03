import requests
from bs4 import BeautifulSoup
import numpy as np
from urllib3.connectionpool import xrange
import pandas as pd
import json

url = 'https://www.dailymail.co.uk/home/index.html'

r1 = requests.get(url)
coverpage = r1.content

soup1 = BeautifulSoup(coverpage,'html.parser') #a beatifulsoup object that represents the html document of the page

coverpage_news = soup1.find_all('ul',class_='nav-primary cleared bdrgr3 cnr5') #retrieve some <ul> tags which contain the nav links for different pages in the website


links = []
titles = []
results = []
resultsx = []
dictkeys = {}

for i in coverpage_news:
    results=i.find_all('a') #append all the <a> tags on results
for i in results:
    if 'https://' not in i['href'] and '/registration' not in i['href']: #retrieve specific nav links to navigate through different pages in the website
        links.append('https://www.dailymail.co.uk'+i['href'])

article_links = []
for link in links: #retrieve content for each page in the website

    r1 = requests.get(link)
    coverpage = r1.content

    soup1 = BeautifulSoup(coverpage, 'html.parser')

    coverpage_news = soup1.find_all('h2', class_='linkro-darkred') #this is were the article links and titles are located...so i retrieve them


    for i in coverpage_news:
        resultsx.append(i.find('a',href=True))

    for article in resultsx:
        link = 'https://www.dailymail.co.uk'+article['href'] #retrieving and constructing the full link of each article found

        title = article.text #the text on the <a> tag represents the title of the article
        titles.append(title)
        dictkeys[title] = link #creating a dictionary with titles as keys and links as values

#in this section i am going to retrieve the content of each article
dict = {}
for story in dictkeys:
    article = requests.get(dictkeys[story]) #request to get the webpage of the article
    content = article.content
    soup_article = BeautifulSoup(content,'html.parser')
    body = soup_article.find_all('div', itemprop='articleBody')#i need only the article body from the html document
    if body:
        x = body[0].find_all('p') #i get all the paragraphs from the article body
    else:
        continue
    list_paragraphs = []
    for p in xrange(1, len(x)): #retrieving the text of each paragraph and merge them all together in order to get the full final article
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)
        print(final_article)
    dict[dictkeys[story]] = final_article #creating a dictionary which have links as keys and articles as values
print(dict)
print(len(dict))
with open('dailymail.json'.format(1), 'w', encoding='utf-8') as file: #saving the dictionary as json
    json.dump(dict, file, ensure_ascii=False)

