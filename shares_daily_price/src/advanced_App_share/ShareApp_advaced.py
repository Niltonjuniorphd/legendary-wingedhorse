#%%
#import re
#from bs4 import BeautifulSoup
#import requests
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

from moduli_functions_advanced import (get_news,
                              create_result_table,
                              save_table,
                              tokenize,
                              countVector_tfidf
                              )

import nltk
#from nltk.corpus import stopwords
#from nltk.stem.wordnet import WordNetLemmatizer
#from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
#from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

#import numpy as np




#%%

hard_key='ações petrobras'

noticias_t = get_news(hard_key) #request the url (folha-uol) passing the hard_key returning the site 'li' class:'c-headline' elements
df = create_result_table(noticias_t) #create a dataframe with the news elements: columns=[date, name, title_text, content_text, link]
save_table(df, hard_key) #save the dataframe in a csv data file (file name format: data_yyyy-mm-dd_hard_key.csv)

#%%
print(tokenize(df['content_text'][0])) #show the first line of the 'content_text' column tokenized/lemmatized

# %%

##---CountVectorizer + tfidf---
tfidf_1, columns_1 = countVector_tfidf(df['title_text'])
tfidf_2, columns_2 = countVector_tfidf(df['content_text'])
dff1 = pd.DataFrame(tfidf_1.toarray(), columns=columns_1)
dff2 = pd.DataFrame(tfidf_2.toarray(), columns=columns_2)

# %%
dff1.sum().sort_values(ascending=False).head(50)

#%%
dff2.sum().sort_values(ascending=False).head(50)



