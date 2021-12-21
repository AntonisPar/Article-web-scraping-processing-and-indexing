import requests
from bs4 import BeautifulSoup
import numpy as np
from urllib3.connectionpool import xrange
import pandas as pd
import json

url = 'https://english.elpais.com/'

r1 = requests.get(url)
coverpage = r1.content

soup1 = BeautifulSoup(coverpage,'html.parser')

coverpage_news = soup1.find_all('h2',class_='c_t')

print(coverpage_news[4].find('a')['href'])

list_titles = []
links_with_text = []
for a in soup1.find_all('a', href=True):
    if a.text:
        links_with_text.append(a['href'])

print(links_with_text)
news_contents = []

for link in links_with_text:
    if "http" not in link:
        link = 'https://english.elpais.com' + link
        if "html" not in link:
            continue
        else:
            article = requests.get(link)
            content = article.content
            soup_article = BeautifulSoup(content, 'html5lib')
            title = soup_article('h1',class_='a_t')
            if title:
                list_titles.append(title[0].get_text())
            else:
                continue
            body = soup_article.find_all('div', class_='a_c clearfix')
            if body:
                x = body[0].find_all('p')
            else:
                continue
            list_paragraphs = []
            for p in xrange(1,len(x)):
                paragraph = x[p].get_text()
                list_paragraphs.append(paragraph)
                final_article = " ".join(list_paragraphs)
            news_contents.append(final_article)

    else:
        continue



res = {}
for key in list_titles:
    for value in news_contents:
        res[key] = value
        news_contents.remove(value)
        break

with open('elpais.json'.format(1), 'w', encoding='utf-8') as file:
    json.dump(res, file, ensure_ascii=False)