import requests
import pandas as pd
import os



def nyt_summary(key_word):
    NYT_KEY = os.environ["NYT_KEY"]
    full_text_nyt = ''
    df0 = pd.DataFrame()

    for page in range(0, 5):
        response = []
        data = []
        artcles = []

        url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={key_word}&page={page}&api-key={NYT_KEY}'

        response = requests.get(url)

        data = response.json()

        articles = data['response']['docs']

        articles_df = pd.DataFrame(articles)

        df0 = pd.concat([df0, articles_df], axis=0)

    df0 = df0.reset_index(drop=True)

    print(df0.columns.to_list())

    full_text_nyt = ' '.join(df0['abstract'].unique())\
        .replace('...', '')\
        .replace('\r\n', ' ')\
        .replace('\n', ' ')\
        .replace('.', ' ')\
        .replace('  ', ' ')\
        .replace('   ', ' ')\
        .replace('(', '')\
        .replace(')', '')\
        .replace(',', '')\
        .replace('"', '')\
        .strip()

    return full_text_nyt
