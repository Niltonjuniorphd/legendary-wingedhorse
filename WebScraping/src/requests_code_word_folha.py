# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

name = []
date = []
title_text = []
content_text = []
link_text = []

hard_key = '"bala de borracha"'

for page in range(1,201,25):
    noticias = []

    when = f'https://search.folha.uol.com.br/?q={hard_key}&site=todos&sr={page}'

    response = requests.get(when, headers=headers)

    content = response.content
    site = BeautifulSoup(content, 'html.parser')

    noticias = site.find_all('li', attrs={'class': 'c-headline c-headline--newslist'})
    
    for noticia in noticias:
        journal = noticia.find('h3', attrs={'class': 'c-headline__kicker c-kicker c-search__result_h3'})
        if journal:
            name.append(journal.text.replace('/n ', '').strip())
        else:
            name.append('sem name')

        noticia_date = noticia.find('time')
        if noticia_date:
            date.append(noticia_date.text.replace('/n ', '').strip())
        else:
            date.append('sem date')
        
        title = noticia.find('h2', attrs={'class': 'c-headline__title'})
        if title:
            title_text.append(title.text.replace('/n ', '').strip())
        else:
            title_text.append('sem title')
    
        content = noticia.find('p', attrs={'class': 'c-headline__standfirst'})
        if content:
            content_text.append(content.text.replace('/n ', '').strip())
        else:
            content_text.append('sem content')

        link = noticia.find('a')
        if link:
            link_text.append(link['href'])
        else:
            link_text.append('sem link')

df0 = pd.DataFrame({'date': date, 'name': name, 'title_text': title_text, 'content_text': content_text, 'link': link_text})
df = df0.copy()
df = df.drop_duplicates()
df.info()

h = pd.Timestamp.today()
df.to_csv(f'data_{h.date()}_{hard_key.replace('"','').replace(' ', '_')}.csv')
print('\n Quantidade de notícias encontradas: ',len(df0))
print('\n Quantidade de notícias duplicadas: ',df0.duplicated().sum())
print('\n Quantidade de notícias consideradas: ',len(df))
