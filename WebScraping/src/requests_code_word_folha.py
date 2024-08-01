#%%
import requests
import pandas as pd

from bs4 import BeautifulSoup
from tqdm import tqdm

#%%
hard_key = '"venezuela"'

def get_news(hard_key):

    print(f'\nHard_key used to scrap: {hard_key}')
    print(f'\nDate: {pd.Timestamp.today().date()}')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    noticias_t = []

    #hard_key = '"venezuela"'

    print(f'\n searching for {hard_key} ...\n')

    for page in tqdm(range(1,201,25), bar_format='{desc:<5.5}{percentage:3.0f}%|{bar:20}{r_bar}'):
        noticias = []

        when = f'https://search.folha.uol.com.br/?q={hard_key}&site=todos&sr={page}'

        response = requests.get(when, headers=headers)

        content = response.content
        site = BeautifulSoup(content, 'html.parser')

        #noticias = site.find_all('li', attrs={'class': 'c-headline c-headline--newslist'})
        noticias_t.append(site.find_all('li', attrs={'class': 'c-headline c-headline--newslist'}))
    
    return noticias_t


def create_result_table(news):

    name = []
    date = []
    title_text = []
    content_text = []
    link_text = []

    for i, j in enumerate(news):
        for noticia in j:
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

    print('\n Number of news items found: ',len(df0))
    print(' Number of duplicated news found: ',df0.duplicated().sum())
    print(' Final news considered: ',len(df))

    return df

def save_table(df):
    h = pd.Timestamp.today()
    df.to_csv(f'data_{h.date()}_{hard_key.replace('"','').replace(' ', '_')}.csv')
    print(f'\nSaving DataFrame as data_{h.date()}_{hard_key.replace('"','').replace(' ', '_')}.csv')
    print('\nDataFrame info: \n')
    print(df.info())



#%%
noticias_t = get_news(hard_key=hard_key)
df = create_result_table(noticias_t)
save_table(df)


