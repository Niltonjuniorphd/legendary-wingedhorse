# %%
import pandas as pd
from modules import EDA_module
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ks_2samp


def is_equal(df, feature):
    '''
    Tests if the distributions of the specified feature for the survived and not-survived groups are equal 
    using the Kolmogorov-Smirnov test.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing the data.
    feature (str): The column name of the feature to be tested.

    Returns:
    None

    Prints:
    A message indicating the null hypothesis, the p-value, and the result of the hypothesis test 
    (whether the distributions are different or not at a significance level of 1%).

    '''
    sns.kdeplot(df[df['Survived'] == 0][feature], label='not survived')
    sns.kdeplot(df[df['Survived'] == 1][feature], label='survived')
    plt.legend()
    plt.show()

    age_not_survived = df[df['Survived'] == 0][feature].dropna()
    age_survived = df[df['Survived'] == 1][feature].dropna()

    # Kolmogorov-Smirnov Test
    ks_statistic, p_value = ks_2samp(age_not_survived, age_survived)

    print('H0: The distributions of the two samples are identical.')

    if p_value < 0.01:
        print(f'p-value = {p_value}')
        print('is p-value < 0.01? YES, then:')
        print("The distributions are different (reject the null hypothesis).")
    else:
        print(f'p-value = {p_value}')
        print('is p-value < 0.01? NO, then:')
        print("The distributions are not different (fail to reject the null hypothesis).")


# %%
df0 = pd.read_csv(
    'C:/Git projects/legendary-wingedhorse/Titanic/data/train.csv')

df = df0.copy()

# %%
# Describe the status of data. Is there any missing data, if so in which columns?
df.info()
print('\n')
print(df.isnull().sum())

# %%
# What is the overall survival rate ?
df['Survived'].mean()

# %%
df['Sib_Par'] = df.apply(lambda row: f"{row['SibSp']},{row['Parch']}", axis=1)

df['surnames'] = pd.Series([df['Name'].apply(lambda x: x.split(' '))[i][1] for i in df.index])

personal_names = pd.Series([df['Name'].apply(lambda x: x.split(','))[i][1] for i in df.index], index=df.index)
df['personal_names'] = pd.Series([personal_names.apply(lambda x: x.split())[i][0] for i in personal_names.index])

df['sum_Sib_Par'] = df.apply(lambda row: row['SibSp'] + row['Parch'], axis=1)

# %%
# How is survival rate different for Females and Males?
df.groupby('Sex')['Survived'].mean()

# %%
# Which passenger class had the highest survival rate ?
# first class
df.groupby('Pclass')['Survived'].mean()

# %%
# How is survival rate different for Females and Males of various pssenger classes?
df.groupby(['Pclass', 'Sex'])['Survived'].mean()

# %%
# What is the age distribution of people onboard?
sns.kdeplot(df['Age'])
plt.show()

# %%
# Are the ages of people who survived substantially different from the one who did not?
is_equal(df, 'Age')

# %%
# Is there difference in the fares of people who suvived and who did not?
is_equal(df, 'Fare')

# %%
# hb_plot is a module
EDA_module.hb_plot(df, 'Age')

# %%
df2 = df.drop('PassengerId', axis=1)
EDA_module.deep_hb_plot(df2)

# %%
sns.barplot(df, x="SibSp", y="Survived", hue="Sex")

# %%
sns.barplot(df, x="Sib_Par", y="Survived")

# %%
df.groupby(['SibSp'])['Survived'].agg(['count', 'sum', 'mean'])

# %%
df.groupby(['Parch'])['Survived'].agg(['count', 'sum', 'mean'])

# %%
df.groupby(['Sib_Par'])['Survived'].agg(['count', 'sum', 'mean'])

# %%
df.groupby(df[df['Survived'] == 1]['Parch'])[
    'Survived'].agg(['count', 'sum', 'mean'])

# %%
sns.countplot(data=df, x="SibSp", hue='Sex')  # , y="Sex", hue="Sex")

# %%
sns.countplot(data=df, x="Parch", hue='Sex')  # , y="Sex", hue="Sex")

# %%
sns.countplot(data=df, x="Sib_Par", hue='Sex')  # , y="Sex", hue="Sex")

# %%
df.groupby(by=['Sib_Par'], dropna=False).agg({'Survived': ['count','mean'], 'Age': ['count','mean', 'min', 'max']})

# %%
df.groupby(by=['personal_names', 'Sib_Par', 'sum_Sib_Par'], dropna=False).agg({'Survived': ['count','mean'], 'Age': ['count','mean', 'min', 'max']}).head(50)


# %%
df.groupby(by=['Embarked'], dropna=False).agg({'Survived': ['count','mean'], 'Fare': ['count','mean', 'min', 'max']})

# %%
