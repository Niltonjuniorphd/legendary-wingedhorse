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
