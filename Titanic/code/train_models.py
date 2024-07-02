# %%
import pandas as pd
from sklearn import model_selection
from sklearn import ensemble
from sklearn import pipeline
from sklearn import metrics

from feature_engine import selection
from feature_engine import encoding
from feature_engine import imputation


# %%
# Data
df = pd.read_csv('C:/Git projects/legendary-wingedhorse/Titanic/data/train.csv')

# %%
#Sample
target = 'Survived'
features = df.drop('Survived').columns.tolist()

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

features_to_drop = ['PassengerId', 'Survived', 'Name']
num_missing = ['Age']
cat_missing = ['Cabin', 'Embarked']
cat_features = X_train.select_dtypes('object').columns.to_list()

to_drop = selection.DropFeatures(features_to_drop=features_to_drop)
num_imput = imputation.MeanMedianImputer(imputation_method='mean', variables=num_missing)
cat_imput = imputation.CategoricalImputer(imputation_method='frequent', variables=cat_missing)
onehot = encoding.OneHotEncoder() #variables=cat_features)

# %%
model = ensemble.RandomForestClassifier(random_state=42)

param = {
    "max_depth": [4, 8, 10, 15],
    "min_samples_leaf": [10, 20, 100],
    "n_estimators": [100, 200, 500]

}

grid = model_selection.GridSearchCV(model, 
                                    param_grid=param,
                                    scoring='roc_auc',
                                    cv=3,
                                    n_jobs=-1)

model_pipe = pipeline.Pipeline([
    ('to_drop', to_drop),
    ('num_imput', num_imput),
    ('cat_imput', cat_imput),
    ('onehot', onehot),
    ('model', grid)
])



# %%
model_pipe.fit(X_train, y_train)


# %%
train_pred = model_pipe.predict_proba(X_train)
test_pred = model_pipe.predict_proba(X_test)
val_pred = model_pipe.predict_proba(df_valid)

auc_train = metrics.roc_auc_score(y_train, train_pred[:,1])
auc_test = metrics.roc_auc_score(y_test, test_pred[:,1])
auc_val = metrics.roc_auc_score(df_valid[target], val_pred[:,1])

print("AUC Score train:", auc_train)
print("AUC Score test:", auc_test)
print("AUC Score val:", auc_val)

# %%
df_test = pd.read_csv('C:/Git projects/legendary-wingedhorse/Titanic/data/test.csv')

# %%
df_test.info()


# %%

K_test_pred = model_pipe.predict_proba(df_test)
# %%
