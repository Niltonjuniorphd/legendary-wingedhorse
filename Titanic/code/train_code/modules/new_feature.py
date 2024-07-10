import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class NewFeatureAdder(BaseEstimator, TransformerMixin):
    """
    A custom transformer for adding new features to a DataFrame.

    This transformer adds a new column 'Sib_Par' to the input DataFrame,
    which combines the 'SibSp' and 'Parch' columns into a tuple.

    Methods
    -------
    __init__()
        Initializes the transformer. No parameters are needed.

    fit(X, y=None)
        Fits the transformer to the data. This method doesn't do anything
        since this transformer doesn't need to learn from the data.

    transform(X)
        Transforms the input DataFrame by adding the 'Sib_Par' column.

    Parameters
    ----------
    X : pd.DataFrame
        Input data to transform.
    y : None
        Ignored, exists for compatibility with sklearn pipeline.

    Returns
    -------
    pd.DataFrame
        Transformed DataFrame with the new 'Sib_Par' column.
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df_new = X.copy()
        Sib_Par = pd.Series(df_new.apply(lambda row: f"{row['SibSp']},{row['Parch']}", axis=1), index=df_new.index, name='Sib_Par')
        personal_names = pd.Series([df_new['Name'].apply(lambda x: x.split(','))[i][1] for i in df_new.index], index=df_new.index, name='personal_names')
        surnames = pd.Series([personal_names.apply(lambda x: x.split())[i][0] for i in df_new.index], index=df_new.index, name='surnames')
        sum_Sib_Par = pd.Series(df_new.apply(lambda row: row['SibSp'] + row['Parch'], axis=1), index=df_new.index, name='sum_Sib_Par')

        df_new = pd.concat([df_new, Sib_Par, surnames, sum_Sib_Par], axis=1)

        return df_new
