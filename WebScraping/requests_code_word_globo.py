# %%
import requests
from bs4 import BeautifulSoup

import pandas as pd
import webbrowser


# %%
name = []
date = []
title_text = []
content_text = []
link_text = []

hard_key = 'armas+não+letais'

for page in range(1,11,1):
    noticias = []

    when = f'https://www.globo.com/busca/?q="{hard_key}"&from=now-5y&page={page}'
    response = requests.get(when)

    content = response.content
    site = BeautifulSoup(content, 'html.parser')

    noticias = site.find_all('li', attrs={'class': 'widget widget--card widget--info'})
    #print(noticias.prettify())
    
    for noticia in noticias:
        #print(noticia.prettify())
        journal = noticia.find('div', attrs={'class': 'widget--info__meta--card'})
        if journal:
            #print('journal:', journal.text)
            name.append(journal.text.split('\n')[1])
            date.append(journal.text.split('\n')[3])
        else:
            name.append('sem name')
            date.append('sem date')
        
        title = noticia.find('div', attrs={'class': 'widget--info__title product-color'})
        if title:
            title_text.append(title.text.replace('\n ', '').strip())
        else:
            title_text.append('sem title')
    
        content = noticia.find('p', attrs={'class': 'widget--info__description'})
        if content:
            content_text.append(content.text.replace('\n ', '').strip())
        else:
            content_text.append('sem content')

        link = noticia.find('a', attrs={'class': 'widget--info__media'})
        if link:
            link_text.append(link['href'])
        else:
            link_text.append('sem link')



        #text_content = noticia.find('p', attrs={'class': 'widget--info__description'})
        #if text_content:
        #    print('text_content:', text_content.text)
        
        #print('---')

# %%
df0 = pd.DataFrame({'date': date, 'name': name, 'title_text': title_text, 'content_text': content_text, 'link': link_text})
df0.info()

# %%
df = df0.copy()

for i, j in enumerate(df['date']):
    try:
        pd.to_datetime(j, dayfirst=True)
        df.loc[i, 'date_b'] = pd.to_datetime(j, dayfirst=True)

    except ValueError:
        if j.split(' ')[2] == 'dia' or j.split(' ')[2] == 'dias':
            d = int(j.split(' ')[1])
            df.loc[i, 'date_b'] = pd.Timestamp.today() - pd.Timedelta(days=d)
        else:
            df.loc[i, 'date_b'] = pd.Timestamp.today() 

#df['date'] = pd.to_datetime(df['date'])

# %%
df = df.sort_values(by=['date_b'], ascending=False)
df = df.reset_index()

# %%
webbrowser.open(when)

# %%

word_key_list = [
                 'condor',
                 'guarda',
                 'disparo',
                 'matou',
                 'morto',
                 'mortos',
                 'morte',
                 'morreu',
                 'feriu',
                 'bala',
                 'fatal',
                 'não letal',
                 'não-letal',
                 'não letais',
                 'não-letais',
                 ]

for i, j in enumerate(df['content_text']):
    for p in word_key_list:
        if p in j.lower():
            df.loc[i, p] = 1
        else:
            df.loc[i, p] = 0

df.info()
df.select_dtypes('number').sum()

# %%
h = pd.Timestamp.today()
df.to_csv(f'C:/Git projects/legendary-wingedhorse/WebScraping/data_{h}.csv')

# %%
df[(df['guarda'] == 1) & (df['morto'] == 1) ]

# %%