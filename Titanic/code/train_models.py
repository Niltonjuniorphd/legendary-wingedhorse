# %%
import pandas as pd
from sklearn import model_selection


# %%
# Data
df = pd.read_csv('C:/Git projects/legendary-wingedhorse/Titanic/data/train.csv')

# %%
#Sample
target = 'Survived'
features = df.drop(['Survived', 'PassengerId'], axis=1).columns.to_list()

df_valid = df.sample(frac=0.02,  random_state=42)
df_train = df.drop(df_valid.index)

#Explore
df.info()
df_valid.info()
df_train.info()

print('\n')
print(f'response rate df_valid = {df_valid['Survived'].mean()}')
print(f'response rate df_train  = {df_train['Survived'].mean()}')


# %%
# Sample split
X_train, X_test, y_train, y_test = model_selection.train_test_split(
    df_train[features], df_train[target],
    train_size=0.8,
    random_state=42,
    stratify=df_train[target])

#explore
print(f'response rate y_train = {y_train.mean()}')
print(f'response rate y_test  = {y_test.mean()}')

# %%
print(f'duplicated rows = {X_train.duplicated().sum()}')
print('\n')
print('explore NaNs')
X_train.isna().sum()

# %%
