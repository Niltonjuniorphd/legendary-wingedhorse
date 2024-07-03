from sklearn.base import BaseEstimator, TransformerMixin

class ChangeType(BaseEstimator, TransformerMixin):
    def __init__(self, column=None):
        self.column = column
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        X[self.column] = X[self.column].astype('object')
        return X
