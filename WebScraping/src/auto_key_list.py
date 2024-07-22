# %%
import pandas as pd

# %%
df = pd.read_csv('data_2024-07-20_ações_da_petrobras.csv')

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
                                         .replace('fev', 'feb')
                                         .replace('sem date', ''), dayfirst=True).date()

df['date_b'] = pd.to_datetime(df['date_b'])
df['day'] = df['date_b'].dt.day
df['month'] = df['date_b'].dt.month
df['year'] = df['date_b'].dt.year

# %%
df = df.sort_values(by=['date_b'], ascending=False)
df = df.reset_index()

content_text = df['content_text']

# %%
full_text = ' '.join(content_text.unique())\
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

import re

def remover_artigos_preposicoes(texto):
    palavras_para_remover = r'\b(?:que|foi|tem|dia|dispensar|diz|ou|pelo|pelos|anos|agora|ser|quando|mais|gente|ano|deste|como|seu|é|não|se|ter|sido|são|duas|ele|ela|ficou|e|a|o|as|os|um|uns|uma|umas|de|do|da|dos|das|em|no|na|nos|nas|por|pelos|pela|pelas|ao|aos|à|às|com|para|perante|contra|entre|sob|sobre|trás)\b'
    
    # Usando regex para substituir as palavras por uma string vazia
    texto_limpo = re.sub(palavras_para_remover, '', texto, flags=re.IGNORECASE)
    
    # Remover espaços múltiplos resultantes da substituição
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
    
    return texto_limpo

# Exemplo de uso
texto = full_text
full_text_cleaned = remover_artigos_preposicoes(texto)
print(full_text_cleaned)

# %%
with open('unique_string_vector.txt', 'w', encoding='utf-8') as file:
    file.write(full_text)

# %%
keys = pd.Series(full_text_cleaned.lower().strip().split(' '))

# %%

df_c=pd.Series()
for i, j in enumerate(df['content_text']):
    col = pd.DataFrame()
    for p in keys.value_counts().head(100).index:
        if p in j.lower():
            col.loc[i, p] = 1
            
        else:
            col.loc[i, p] = 0
    df_c = pd.concat([df_c, col], axis=0)

dfw = pd.concat([df, df_c.drop(0, axis=1).astype('int')], axis=1)

# %%
dfw.select_dtypes('int').sum()[0:50].sort_values(ascending=False)