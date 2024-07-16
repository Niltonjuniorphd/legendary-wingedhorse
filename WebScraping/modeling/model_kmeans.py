# %%

import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler


# %%
df = pd.read_csv('C:\Git projects\legendary-wingedhorse\WebScraping\modeling\df_folha_minção_não_letal.csv')
df = df.drop(['Unnamed: 0'], axis=1)
df = df.drop_duplicates()

# %%
df.info()

# %%
df.duplicated().sum()

# %%
df.head()

# %%
kme = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kme.fit_predict(df.select_dtypes('number'))

# %%
df
# %%
plt.scatter(df['condor'], df['munição'], c=df['cluster'], cmap='viridis')
plt.xlabel('condor')
plt.ylabel('munição')
plt.title('Visualização dos Clusters')
plt.show()


# %%
#sns.pairplot(df.select_dtypes('number'), hue='cluster')


# %%
df_p1 = df[['condor', 'guarda', 'disparo', 'matou', 'morto', 'mortos', 'morte',
       'morreu', 'feriu', 'bala', 'fatal', 'não letal', 'não-letal', 'year',
        'cluster']]

df_p2 = df[['não letais', 'não-letais', 'bala de borracha', 'munição', 'borracha',
       'granada', 'lacrimogêneo', 'condor_t', 'não_letal_G', 'morte_G',
       'bala_de_borracha_G', 'year', 'cluster']]

df_p3 = df[['condor_t', 'não_letal_G', 'morte_G',
       'bala_de_borracha_G', 'year', 'cluster']]

scaler = StandardScaler()
df_p1 = pd.DataFrame(scaler.fit_transform(df_p1), columns=df_p1.columns)
df_p2 = pd.DataFrame(scaler.fit_transform(df_p2,), columns=df_p2.columns)
df_p3 = pd.DataFrame(scaler.fit_transform(df_p3), columns=df_p3.columns)

# %%
sns.pairplot(df_p2, hue='cluster',palette='viridis')

# %%
