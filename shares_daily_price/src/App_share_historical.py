
#%%
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

from moduli_functions import (call_driver,
                              send_focus_key,
                              get_links,
                              get_response,
                              make_sample_df,
                              query_database,
                              create_database
                              )


#%%
driver = call_driver()

time.sleep(2)
focus_key = 'ações petrobras'
send_focus_key(driver, focus_key=focus_key)# 

print('initiating get the share values... ')
time.sleep(5)
values = WebDriverWait(driver, 4).until(
    EC.presence_of_all_elements_located((By.XPATH, "//span[@jsname='vWLAgc']")))#valor da ação em focus_key para 'https://google.com/ncr
value = values[0].text

time.sleep(5)
values_close = WebDriverWait(driver, 4).until(
    EC.presence_of_all_elements_located((By.XPATH, "//span[@jsname='qRSVye']")))#valor do aumento/queda da ação em focus_key
value_close = values_close[0].text

time.sleep(5)
values_other = WebDriverWait(driver, 4).until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='maIvLb']")))#valores de outras ações (painel lateral)

print('end get the share dayli values... ')
print('---------------------------------------')
print(f'value: {value}')
print(f'value_close: {value_close}')
print(f'value_other: {values_other[0].text}')
print('---------------------------------------')


texts, links = get_links(driver, xpath="//a[@jsname='UWckNb']", pg_num=1)#monta a lista de links e textos das fontes relacionadas na pg do google, desde a página de 1 até pg_num.

responses, response_status = get_response(links)#monta a lista de requests em cada uma das fontes em links


print('initiating save words... ')

word_list = [
    'subiu',
    'caiu',
    'salta',
    'queda',
    'aumenta',
    'dispara',
    'desaba',
    'desabam',
    'podem cair',
    'podem subir',
    'barata']

sample_date = make_sample_df(word_list, responses)#usa get_words_re() e cria 
sample_date['value'] = value
sample_date['value_close'] = value_close

print('all counting words done... ')

#%%

date = pd.Timestamp.today().date() + pd.Timedelta(days=0)
sample_date.to_csv(f'data_raw/sample_date_{focus_key}_{date}.csv', index=False)
pd.DataFrame(sample_date).T.to_csv(f'database/daily_data.csv', index=False)

#%%
create_database(sample_date=sample_date.tolist())


print('\033[92m\n-----All process successfully done...-----\033[0m\n')
print('\033[92m\n         -----End of program-----\033[0m\n')

db__path = 'database/historical_data.db'
query_database(db__path)

#db__path2 = 'historical_data.db'
#query_database(db__path2)
