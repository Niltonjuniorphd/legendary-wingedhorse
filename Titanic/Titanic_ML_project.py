# %%
import pandas as pd

# %%

df = pd.read_csv('C:/Git projects/legendary-wingedhorse/Titanic/data/train.csv')

# %%
df.info()

# %%
df.isnull().sum()

# %%
