# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#import hb_plot

# %%
def hb_plot(df, feature):
    fig, ax = plt.subplots(2,1)

    sns.histplot(df[feature].value_counts(dropna=False), ax = ax[0])
    sns.boxplot(df[feature], ax = ax[1],orient='h',)
    plt.tight_layout()


# %%
df = pd.read_csv('C:/Git projects/legendary-wingedhorse/Titanic/data/train.csv')

# %%
df.info()
df.isnull().sum()




hb_plot(df, 'Age')

# %%
