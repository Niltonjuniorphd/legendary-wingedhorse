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
        zp = pd.Series(zip(df_new['SibSp'], df_new['Parch']), index=df_new.index, name='Sib_Par')
        df_new = pd.concat([df_new, zp], axis=1)

        return df_new
