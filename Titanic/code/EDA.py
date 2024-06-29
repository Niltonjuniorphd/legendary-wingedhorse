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

    print('The distributions of the two samples are identical.')

    if p_value < 0.01:
        print(f'p-value = {p_value}')
        print('is p-value < 0.01? YES, then:')
        print("The distributions are different (reject the null hypothesis).")
    else:
        print(f'p-value = {p_value}')
        print('is p-value < 0.01? NO, then:')
        print("The distributions are not different (fail to reject the null hypothesis).")



# %%
df = pd.read_csv('C:/Git projects/legendary-wingedhorse/Titanic/data/train.csv')

# %%
# Describe the status of data. Is there any missing data, if so in which columns?
df.info()
print('\n')
print(df.isnull().sum())

# %%
#What is the overall survival rate ?
df['Survived'].mean()

# %%
#How is survival rate different for Females and Males?
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


# %%
#hb_plot is a module
EDA_module.hb_plot(df, 'Age')

# %%
df2 = df.drop('PassengerId', axis=1)
EDA_module.deep_hb_plot(df2)

# %%
sns.barplot(df, x="SibSp", y="Survived", hue="Sex")

# %%
df.groupby(['SibSp'])['Survived'].agg(['count', 'sum', 'mean'])

# %%
df.groupby(['Parch'])['Survived'].agg(['count', 'sum', 'mean'])

# %%
df.groupby(df[df['Survived']==1]['Parch'])['Survived'].agg(['count', 'sum', 'mean'])

# %%
sns.countplot(data=df, x="SibSp", hue='Sex') #, y="Sex", hue="Sex")

# %%

sns.countplot(data=df, x="Parch", hue='Sex') #, y="Sex", hue="Sex")

# %%
df['Name']

# %%
surnames = pd.Series([df['Name'].apply(lambda x: x.split(','))[i][0] for i in range(len(df['Name']))])
surnames 

# %%
surnames.value_counts()

# %%
surnames.value_counts().value_counts().sort_index()

# %%
surnames.nunique()

# %%
pd.Series(list(zip(df['SibSp'], df['Parch']))).value_counts()
# %%
