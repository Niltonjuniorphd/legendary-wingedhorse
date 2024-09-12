#%%
import re
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from moduli_functions_advanced import (get_news,
                              create_result_table,
                              save_table
                              )

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

import numpy as np



#%%

hard_key='ações petrobras'

noticias_t = get_news(hard_key)
df = create_result_table(noticias_t)
save_table(df, hard_key)

#%%
stop_words = stopwords.words("portuguese")
lemmatizer = WordNetLemmatizer()

def tokenize(text):
    # normalize case and remove punctuation
    text = re.sub(r"[^a-zA-ZçÇáàâãéêíóôõúüÁÀÂÃÉÊÍÓÔÕÚÜ\s]", " ", text.lower())
    
    # tokenize text
    tokens = word_tokenize(text)
    
    # lemmatize (replace inflections forms) and remove stop words (nouns, propositions...)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]

    return tokens

print(tokenize(df['content_text'][0]))


# %%

##---CountVectorizer---
# initialize count vectorizer object
vect = CountVectorizer(tokenizer=tokenize)

# get counts of each token (word) in text data
X1 = vect.fit_transform(df['content_text'])

# convert sparse matrix to numpy array to view the counts of each token (word)
# each row is one line in the text (corpus) and the number is the count of a token
X1.toarray()

print(X1.shape)

# %%
vect.vocabulary_

# %%

#%%---TfidfTransformer---
# initialize tf-idf transformer object
transformer = TfidfTransformer(smooth_idf=False)

# Todo: use counts from count vectorizer results to compute tf-idf values using the fit_transform method
tfidf = transformer.fit_transform(X1)

# convert sparse matrix to numpy array to view
# you can see that the counts are normalized
tfidf.toarray()
# %%

#%%---TfidfVectorizer = CountVectorizer + TfidfTransformer---
# TF-IDF
# initialize tf-idf vectorizer object
vectorizer = TfidfVectorizer(tokenizer=tokenize)

# compute bag of word counts and tf-idf values
X2 = vectorizer.fit_transform(df['content_text'])

# convert sparse matrix to numpy array to view
X2.toarray()

# %%
vectorizer.vocabulary_

# %%
dff1 = pd.DataFrame(X1.toarray(), columns=vect.get_feature_names_out())
dff2 = pd.DataFrame(X2.toarray(), columns=vectorizer.get_feature_names_out())

# %%
dff1.sum().sort_values(ascending=False).head(50)

#%%
dff2.sum().sort_values(ascending=False).head(50)



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
