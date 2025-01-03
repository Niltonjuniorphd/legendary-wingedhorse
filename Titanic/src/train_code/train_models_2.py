# %%
import pandas as pd
from sklearn import model_selection
from sklearn import ensemble
from sklearn import pipeline
from sklearn import metrics

from feature_engine import selection
from feature_engine import encoding
from feature_engine import imputation

from modules import new_feature
from modules import changeType

# %%
# Data
df0 = pd.read_csv(
    'C:/Git projects/legendary-wingedhorse/Titanic/data/train.csv')
df0['Pclass'] = df0['Pclass'].astype('object')
df = df0.copy()

# %%
df = df.dropna(subset='Embarked', axis=0)

# %%
# Sample
target = 'Survived'
features = df.drop('Survived', axis=1).columns.tolist()

df_valid = df.sample(frac=0.02,  random_state=42)
df_train = df.drop(df_valid.index)

# Explore
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
    train_size=0.80,
    random_state=42,
    stratify=df_train[target])

# explore
print(f'response rate y_train = {y_train.mean()}')
print(f'response rate y_test  = {y_test.mean()}')

# %%
print(f'duplicated rows = {X_train.duplicated().sum()}')
print('\n')
print('explore NaNs')
X_train.isna().sum()


# %%
model = ensemble.RandomForestClassifier(random_state=42)
#model = ensemble.GradientBoostingClassifier(random_state=42)

paramRF = {
    "max_depth": [4, 6, 8, 10],
    "min_samples_leaf": [2, 5, 10],
    "n_estimators": [50, 200, 500]

}

paramGB = {
    'learning_rate': [0.01, 0.1, 0.2, 0.3],
    'n_estimators': [50, 100, 200, 300],
    'subsample': [0.5, 0.8, 1.0],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [2, 5, 10],
}

# param base_line
#param = {
#    "max_depth": [4, 8, 10, 15, 50],
#    "min_samples_leaf": [5, 10, 20, 100],
#    "n_estimators": [100, 200, 500]
#
#}

grid = model_selection.GridSearchCV(model,
                                    param_grid=paramRF,
                                    scoring='roc_auc',
                                    cv=3,
                                    n_jobs=-1)

catinput = imputation.CategoricalImputer(ignore_format=False)
numinput = imputation.MeanMedianImputer(imputation_method='median')
new_feature = new_feature.NewFeatureAdder()
change1 = changeType.ChangeType(column='SibSp')
change2 = changeType.ChangeType(column='Parch')
change3 = changeType.ChangeType(column='sum_Sib_Par')
to_drop = selection.DropFeatures(features_to_drop=
                                 ['PassengerId',
                                  'Name',
                                  'Ticket',
                                  'Cabin',
                                  'SibSp',
                                  'Sib_Par',
                                  ])
onehot = encoding.OneHotEncoder()  

model_pipe = pipeline.Pipeline([
    ('catinput', catinput),
    ('numinput', numinput),
    ('new_feature', new_feature),
    #('changeTYpe1', change1),
    ('changeTYpe2', change2),
    ('changeTYpe3', change3),
    ('to_drop', to_drop),
    ('onehot', onehot),
    ('model', grid)
])

# %%
model_pipe_df = pipeline.Pipeline([
    ('catinput', catinput),
    ('numinput', numinput),
    ('new_feature', new_feature),
    #('changeTYpe1', change1),
    ('changeTYpe2', change2),
    ('changeTYpe3', change3),
    ('to_drop', to_drop),
    ('onehot', onehot),
])

df_pipe = model_pipe_df.fit_transform(X_train)


# %%
model_pipe.fit(X_train, y_train)


# %%
train_pred = model_pipe.predict_proba(X_train)
test_pred = model_pipe.predict_proba(X_test)
val_pred = model_pipe.predict_proba(df_valid[features])

auc_train = metrics.roc_auc_score(y_train, train_pred[:, 1])
auc_test = metrics.roc_auc_score(y_test, test_pred[:, 1])
auc_val = metrics.roc_auc_score(df_valid[target], val_pred[:, 1])

print("AUC Score train:", auc_train)
print("AUC Score test:", auc_test)
print("AUC Score validation:", auc_val)

#GB
#AUC Score train: 0.9575668823220844
#AUC Score test: 0.8287728026533996
#AUC Score validation: 0.935064935064935

#GB mean
#AUC Score train: 0.955984437838783
#AUC Score test: 0.8345771144278606
#AUC Score validation: 0.8701298701298701

#RF mean
#AUC Score train: 0.9298391327155097
#AUC Score test: 0.8432835820895522
#AUC Score validation: 0.9090909090909091

#RF drop ['PassengerId', 'Name','Ticket','Cabin','SibSp','Sib_Par'])
#AUC Score train: 0.9329078510229061
#AUC Score test: 0.8206882255389718
#AUC Score validation: 0.948051948051948

# %%
df_test = pd.read_csv(
    'C:/Git projects/legendary-wingedhorse/Titanic/data/test.csv')

# %%
df_test.info()

# %%
K_test_pred_proba = model_pipe.predict_proba(df_test)
K_test_pred = model_pipe.predict(df_test)
K_test_pred

# %%
df_submission = pd.DataFrame()
df_submission['PassengerId'] = df_test['PassengerId']
df_submission['Survived'] = pd.DataFrame(K_test_pred)
df_submission

# %%
df_submission.to_csv('C:/Git projects/legendary-wingedhorse/Titanic/data/df_submission.csv', index=False)


