#%%
import requests
import pandas as pd

#%%
key_word = 'petrobras'

#%%
df0 = pd.DataFrame()
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

# %%
full_text = ' '.join(df0['abstract'].unique())\
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

# %%
