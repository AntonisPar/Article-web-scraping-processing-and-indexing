import requests
from bs4 import BeautifulSoup
import numpy as np
from urllib3.connectionpool import xrange
import pandas as pd
import json

url = 'https://www.dailymail.co.uk/home/index.html'

r1 = requests.get(url)
coverpage = r1.content

soup1 = BeautifulSoup(coverpage,'html.parser')

coverpage_news = soup1.find_all('ul',class_='nav-primary cleared bdrgr3 cnr5')


links = []
titles = []
results = []
resultsx = []
dictkeys = {}

for i in coverpage_news:
    results=i.find_all('a')
for i in results:
    if 'https://' not in i['href'] and '/registration' not in i['href']:
        links.append('https://www.dailymail.co.uk'+i['href'])

article_links = []
for link in links:

    r1 = requests.get(link)
    coverpage = r1.content

    soup1 = BeautifulSoup(coverpage, 'html.parser')

    coverpage_news = soup1.find_all('h2', class_='linkro-darkred')


    for i in coverpage_news:
        resultsx.append(i.find('a',href=True))

    for article in resultsx:
        link = 'https://www.dailymail.co.uk'+article['href']

        title = article.text
        titles.append(title)
        dictkeys[title] = link


dict = {}
for story in dictkeys:
    article = requests.get(dictkeys[story])
    content = article.content
    soup_article = BeautifulSoup(content,'html.parser')
    body = soup_article.find_all('div', itemprop='articleBody')
    if body:
        x = body[0].find_all('p')
    else:
        continue
    list_paragraphs = []
    for p in xrange(1, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)
        print(final_article)
    dict[dictkeys[story]] = final_article
print(dict)
print(len(dict))
with open('dailymail.json'.format(1), 'w', encoding='utf-8') as file:
    json.dump(dict, file, ensure_ascii=False)

