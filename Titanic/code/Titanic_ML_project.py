# %%
import pandas as pd
from modules import EDA_module

# %%
df = pd.read_csv('C:/Git projects/legendary-wingedhorse/Titanic/data/train.csv')

# %%
df.info()
df.isnull().sum()
df = df.drop('PassengerId', axis=1)

# %%
#hb_plot is a module
EDA_module.hb_plot(df, 'Age')

# %%
EDA_module.deep_hb_plot(df)
# %%
sns.barplot(df, x="island", y="body_mass_g", hue="sex")