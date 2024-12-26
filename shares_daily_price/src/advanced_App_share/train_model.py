# %%

X = df['content_text']
y = dff2['alta'].apply(lambda x: 1 if x > 0 else 0)

def display_results(y_test, y_pred):
    labels = [0,1] #np.unique(y_pred)
    confusion_mat = confusion_matrix(y_test, y_pred, labels=labels)
    accuracy = (y_pred == y_test).mean()

    print("Labels:", labels)
    print("Confusion Matrix:\n", confusion_mat)
    print("Accuracy:", accuracy)


def main(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.15)
    print('X_train.shape: {}'.format(X_train.shape))
    print('X_test.shape: {}'.format(X_test.shape))
    print('y_train.shape: {}'.format(y_train.shape))
    print('y_test.shape: {}'.format(y_test.shape))

    # build pipeline
    pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', RandomForestClassifier())
    ])
       
    # train classifier
    pipeline.fit(X_train, y_train)
    # predict on test data
    y_pred = pipeline.predict(X_test)

    # display results
    display_results(y_test, y_pred)

    return pipeline, X_test, y_test

#%%
main(X, y)
# %%
from sklearn.metrics import ConfusionMatrixDisplay
pipeline, X_test, y_test = main(X,y)    
ConfusionMatrixDisplay.from_estimator(pipeline, X_test, y_test)
# %%
