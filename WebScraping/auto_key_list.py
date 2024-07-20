# %%
import pandas as pd

# %%
df = pd.read_csv('data_2024-07-19_bala_de_borracha.csv')

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
    .strip()

# %%
print(full_text)


# %%
with open('unique_string_vector.txt', 'w', encoding='utf-8') as file:
    file.write(full_text)

# %%
keys = pd.Series(full_text.strip().split(' '))

# %%
keys.value_counts().head(50)
