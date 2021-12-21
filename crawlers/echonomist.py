import requests
from bs4 import BeautifulSoup
import numpy as np
from urllib3.connectionpool import xrange
import pandas as pd
import json

url = 'https://www.economist.com/'

r1 = requests.get(url)
coverpage = r1.content

soup1 = BeautifulSoup(coverpage,'html.parser')

coverpage_news = soup1.find_all('a',class_='ds-navigation-link ds-navigation-link--inverse')


links = []
titles = []
dictkeys = {}

for i in coverpage_news:
    link = i.attrs['href']
    if 'http' in link or '/api' in link:
        continue
    else:
        link = 'https://www.economist.com'+link
        links.append(link)

for link in links:

    r1 = requests.get(link)
    coverpage = r1.content

    soup1 = BeautifulSoup(coverpage, 'html.parser')

    coverpage_news = soup1.find_all('a', class_='headline-link')


    for article in coverpage_news:
        link = article.attrs['href']
        if 'https' in link:
            continue
        else:
            link = 'https://www.economist.com'+link
        title = article.text
        titles.append(title)
        dictkeys[title] = link



dict = {}
for story in dictkeys:
    article = requests.get(dictkeys[story])
    content = article.content
    soup_article = BeautifulSoup(content,'html.parser')
    print(soup_article)
    body = soup_article.find_all('div', class_='ds-layout-grid ds-layout-grid--edged layout-article-body')
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
#
# #
# #
with open('echonomist.json'.format(1), 'w', encoding='utf-8') as file:
    json.dump(dict, file, ensure_ascii=False)
#
