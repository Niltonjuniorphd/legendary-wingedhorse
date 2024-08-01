# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import webbrowser

df0 = pd.read_csv('data_2024-07-22_bala_de_borracha.csv')
df0 = df0.drop(['Unnamed: 0'], axis = 1)
df = df0.copy()

# %%
for i, j in enumerate(df['date']):
    df.loc[i, 'date_b'] = pd.to_datetime(j.replace('às', '')
                                         .replace('à', '')
                                         .replace('mai', 'may')
                                         .replace('out', 'oct')
                                         .replace('set', 'sep')
                                         .replace('dez', 'dec')
                                         .replace('º','')
                                         .replace('ago', 'aug')
                                         .replace('abr', 'apr')
                                         .replace('fev', 'feb'), dayfirst=True).date()

df['date_b'] = pd.to_datetime(df['date_b'])
df['day'] = df['date_b'].dt.day
df['month'] = df['date_b'].dt.month

# %%
df = df.sort_values(by=['date_b'], ascending=False)
df = df.reset_index()

# %%
df.info()

text_key_list = [
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
                 'bala de borracha',
                 'munição',
                 'borracha',
                 'granada',
                 'lacrimogêneo',
                 'spray',
                 ]

for i, j in enumerate(df['content_text']):
    for p in text_key_list:
        if p in j.lower():
            df.loc[i, p] = 1
        else:
            df.loc[i, p] = 0

title_key_list = [
                 'condor_t'
                 ]

for i, j in enumerate(df['title_text']):
    for p in title_key_list:
        if p in j.lower():
            df.loc[i, p] = 1
        else:
            df.loc[i, p] = 0




df.info()
df.select_dtypes('number').sum()


df['não_letal_G'] = df[['não letal', 'não-letal','não letais', 'não-letais']].sum(axis=1)
df['morte_G'] = df[['matou', 'morto', 'mortos', 'morte', 'morreu']].sum(axis=1)
df['bala_de_borracha_G'] = df[['bala', 'borracha', 'bala de borracha']].sum(axis=1)
df['year'] = pd.to_datetime(df['date_b']).dt.year

df_group = df.groupby('year')[['condor_t',
                    'condor',
                    'não_letal_G',
                    'morte_G',
                    'bala_de_borracha_G',
                    'munição',
                    'granada',
                    'disparo',
                    'lacrimogêneo',
                    'spray']].sum().astype('int')
df_group.to_csv('df_group.csv')
df_group

df_group_day = df.groupby('day')[['condor_t',
                    'condor',
                    'não_letal_G',
                    'morte_G',
                    'bala_de_borracha_G',
                    'munição',
                    'granada',
                    'disparo',
                    'lacrimogêneo',
                    'spray']].sum().astype('int')

df_group_day

df_group_month = df.groupby('month')[['condor_t',
                    'condor',
                    'não_letal_G',
                    'morte_G',
                    'bala_de_borracha_G',
                    'munição',
                    'granada',
                    'disparo',
                    'lacrimogêneo',
                    'spray']].sum().astype('int')

df_group_month

# %%
df.select_dtypes('number').sum()


#webbrowser.open(df[(df['year'] == 2024) & (df['morreu'] == 1)].loc[18, 'link'])


# %%
ax = sns.barplot(x=df['year'].value_counts().index, y=df['year'].value_counts().values, color='red')
ax.bar_label(ax.containers[0], fontsize=10)
plt.savefig('fig_year.png')
plt.show()

# %%
ax = sns.barplot(x=df['month'].value_counts().index, y=df['month'].value_counts().values, color='red')
ax.bar_label(ax.containers[0], fontsize=10)
plt.savefig('fig_month.png')
plt.show()

# %%
ax = sns.barplot(data=df_group, x='year', y='condor', color='red')
ax.bar_label(ax.containers[0], fontsize=10)
plt.savefig('fig_condor.png')
plt.show()

# %%
ax = sns.barplot(data=df, x='year', y='condor_t', color='red', errorbar=None)
for container in ax.containers:
    ax.bar_label(container, labels=[f'{v.get_height():.2f}' for v in container], fontsize=10)
plt.show()

# %%
#df_group.to_csv('data_group_bala_de_borracha.csv')

# %%
print(df[df['disparo'] == 1][['date_b', 'title_text']])

# %%
fig, ax = plt.subplots(figsize=(10, 3))

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_frame_on(False)

table = ax.table(cellText=df_group.values, colLabels=df_group.columns, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(6)
plt.show()

plt.savefig('dataframe_table.png', bbox_inches='tight', pad_inches=0.5)

plt.close()

# %%
fig, ax = plt.subplots()

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_frame_on(False)

ax.text(0.05, 0.9, f'a quantidade total de notícias é de {len(df)}', fontsize=12)
ax.text(0.05, 0.7, f'notícias com morte:', fontsize=12)

l =0.6
for i in df[df['morte_G']==1][['date','title_text']].index:
    ax.text(0.05, l, f'{df[df['morte_G']==1]['date_b'].loc[i]} - {df[df['morte_G']==1]['title_text'].loc[i]}', fontsize=12)
    l -= 0.1

ax.text(0.05, l-0.1, f'notícias com lacrimogêneo:', fontsize=12)

l = l - 0.2
for i in df[df['lacrimogêneo']==1][['date','title_text']].index:
    ax.text(0.05, l, f'{df[df['lacrimogêneo']==1]['date_b'].loc[i]} - {df[df['lacrimogêneo']==1]['title_text'].loc[i]}', fontsize=12)
    l -= 0.1

plt.savefig('fig_noticias.png', bbox_inches='tight', pad_inches=0.5)



# %%
[df[df['morte_G']==1][['date', 'title_text']].loc[i] for i in df[df['morte_G']==1][['date', 'title_text']].index]