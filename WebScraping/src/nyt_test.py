
#%%
import requests
import pandas as pd


full_text_nyt = ''

df0 = pd.DataFrame()
key_word = 'japão'

try:
    for page in range(0, 5):
        response = []
        data = []
        artcles = []
        url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={key_word}&page={page}&api-key=XsoNAoGpQgAjeWQmXobmXYOYXJwRbh3Y'
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
    
except KeyError as e:
    print(f"KeyError: {e} - The key was not found in the searching.")
except TypeError as e:
    print(f"TypeError: {e} - The data structure is not in the expected format.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
# %%
