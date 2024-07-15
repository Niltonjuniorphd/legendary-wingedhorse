# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt

df0 = pd.read_csv('C:/Git projects/legendary-wingedhorse/WebScraping/data.csv')
df0 = df0.drop(['Unnamed: 0', 'index'], axis = 1)
df = df0.copy()
# %%
df.info()

# %%
df['não_letal_G'] = df[['não letal', 'não-letal','não letais', 'não-letais']].sum(axis=1)
# %%
df['year'] = pd.to_datetime(df['date_b']).dt.year
sns.barplot(data=df, y='condor', x='year', hue='condor')

# %%
df.select_dtypes('number').sum()

# %%
df.groupby('year')[['condor', 'não_letal_G', 'morte', 'mortos', 'morreu', 'feriu']].sum()

# %%
