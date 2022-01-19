import requests
from bs4 import BeautifulSoup
import numpy as np
from urllib3.connectionpool import xrange
import pandas as pd
import json

url = 'https://www.huffingtonpost.co.uk/'

r1 = requests.get(url)
coverpage = r1.content

soup1 = BeautifulSoup(coverpage,'html.parser')

coverpage_news = soup1.find_all('div',class_='card__headlines')



links = []
titles = []
dictkeys = {}
for article in coverpage_news:

    link = article.find('a')['href']
    links.append(link)
    title = article.find('h3').text
    titles.append(title)
    dictkeys[title] = link

dict = {}
for story in dictkeys:
    article = requests.get(dictkeys[story])
    content = article.content
    soup_article = BeautifulSoup(content,'html.parser')
    body = soup_article.find_all('div', class_='entry__content-and-right-rail-container')
    if body:
        x = body[0].find_all('p')
    else:
        continue
    list_paragraphs = []
    for p in xrange(1, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)
    dict[dictkeys[story]] = final_article



#
#
with open('Huffpost.json'.format(1), 'w', encoding='utf-8') as file:
    json.dump(dict, file, ensure_ascii=False)

