import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class PersonalTitle(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df2 = X.copy()
        personal_names = pd.Series([df2['Name'].apply(lambda x: x.split(','))[
                                   i][1] for i in df2.index], index=df2.index)
        personal_titles = pd.Series([personal_names.apply(lambda x: x.split())[
                                    i][0] for i in personal_names.index], index=df2.index, name='Personal_name')
        df2 = pd.concat([df2, personal_titles], axis=1)

        return df2
