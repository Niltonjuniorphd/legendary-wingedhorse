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
from modules import personal
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
    train_size=0.8,
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

features_to_drop = ['PassengerId', 'Name', 'Ticket', 'Cabin'] #, 'Age'
num_missing = ['Age']
cat_missing = ['Embarked']
cat_features = X_train.select_dtypes('object').columns.to_list()

to_drop = selection.DropFeatures(features_to_drop=features_to_drop)
num_imput = imputation.MeanMedianImputer(
    imputation_method='median', variables=num_missing)
cat_imput = imputation.CategoricalImputer(
    imputation_method='frequent', variables=cat_missing)
new_feature = new_feature.NewFeatureAdder()
perso_name = personal.PersonalTitle()
onehot = encoding.OneHotEncoder()  # variables=cat_features)
change1 = changeType.ChangeType(column='SibSp')
change2 = changeType.ChangeType(column='Parch')


# %%
#model = ensemble.RandomForestClassifier(random_state=42)
model = ensemble.GradientBoostingClassifier(random_state=42)

paramRF = {
    "max_depth": [4, 6, 8, 10],
    "min_samples_leaf": [2, 5, 10],
    "n_estimators": [50, 200, 500]

}

paramGB = {
    'learning_rate': [0.01, 0.1, 0.2, 0.3],
    'n_estimators': [50, 100, 200, 300],
    'subsample': [0.6, 0.8, 1.0],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# param base_line
#param = {
#    "max_depth": [4, 8, 10, 15, 50],
#    "min_samples_leaf": [5, 10, 20, 100],
#    "n_estimators": [100, 200, 500]
#
#}

grid = model_selection.GridSearchCV(model,
                                    param_grid=paramGB,
                                    scoring='roc_auc',
                                    cv=3,
                                    n_jobs=-1)

model_pipe = pipeline.Pipeline([
    #('perso_name', perso_name),
    ('new_feature', new_feature),
    #('changeTYpe1', change1),
    ('changeTYpe2', change2),
    ('to_drop', to_drop),
    ('num_imput', num_imput),
    #('cat_imput', cat_imput),
    ('onehot', onehot),
    ('model', grid)
])

# %%
model_pipe_df = pipeline.Pipeline([
    #('perso_name', perso_name),
    ('new_feature', new_feature),
    #('changeTYpe1', change1),
    ('changeTYpe2', change2),
    ('to_drop', to_drop),
    ('num_imput', num_imput),
    #('cat_imput', cat_imput),
    ('onehot', onehot)])

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

# best
#AUC Score train: 0.8655932720379973
#AUC Score test: 0.8423852957435047
#AUC Score validation: 0.96875

#AUC Score train: 0.9038730547298479
#AUC Score test: 0.839690436705362
#AUC Score validation: 0.8766233766233766

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


