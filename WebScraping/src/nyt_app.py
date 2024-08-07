import requests
import pandas as pd
import os
from tqdm import tqdm



def nyt_summary(key_word):
    NYT_KEY = os.environ["NYT_KEY"]
    full_text_nyt = ''
    df0 = pd.DataFrame()

    for page in tqdm(range(0, 5), bar_format='{desc:<5.5}{percentage:3.0f}%|{bar:20}{r_bar}'):
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
