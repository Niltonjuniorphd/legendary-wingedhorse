
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from moduli_functions import (call_driver,
                              send_focus_key,
                              get_links,
                              get_response,
                              make_sample_df,
                              create_database,
                              query_database
                              )
import time
import pandas as pd


driver = call_driver()

time.sleep(2)
focus_key = 'ações petrobras'
send_focus_key(driver, focus_key=focus_key)


time.sleep(5)
values = WebDriverWait(driver, 4).until(
    EC.presence_of_all_elements_located((By.XPATH, "//span[@jsname='vWLAgc']")))
value = values[0].text

time.sleep(5)
values_close = WebDriverWait(driver, 4).until(
    EC.presence_of_all_elements_located((By.XPATH, "//span[@jsname='qRSVye']")))
value_close = values_close[0].text

time.sleep(5)
values_other = WebDriverWait(driver, 4).until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='maIvLb']")))

texts, links = get_links(driver, xpath="//a[@jsname='UWckNb']", pg_num=20)

responses, response_status = get_response(links)


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

sample_date = make_sample_df(word_list, responses)
sample_date['value'] = value
sample_date['value_close'] = value_close

print('all counting words done... ')


date = pd.Timestamp.today().date() + pd.Timedelta(days=0)
sample_date.to_csv(f'data_raw/sample_date_{focus_key}_{date}.csv')
sample_date.to_csv(f'database/daily_data.csv')

create_database()
print('\033[92m\n-----All process successfully done...-----\033[0m\n')
print('\033[92m\n         -----End of program-----\033[0m\n')

time.sleep(2)
query_database()
