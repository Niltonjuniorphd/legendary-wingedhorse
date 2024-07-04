import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from feature_engine import imputation


class InputNaN(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        nan_list = []
        for i in X.columns:
            if X[i].isnull().sum() > 0:
                nan_list.append(i)

        for i in nan_list:
            if X[i].dtype == 'object':
                cat_imput = imputation.CategoricalImputer(
                    imputation_method='frequent', variables=i)
                X[i] = cat_imput.fit_transform(X[i])
            else:
                X[i] = X[i].fillna(X[i].mean())

        return X
