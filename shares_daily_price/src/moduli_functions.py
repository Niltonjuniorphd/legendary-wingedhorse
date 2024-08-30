from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
import requests
import numpy as np
import pandas as pd
import os
import sqlite3


def call_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    options = Options()
    options.add_argument("--headless")

    print("Driver ready... ")

    return driver


def send_focus_key(driver, focus_key):
    try:
        driver.get("https://google.com/ncr")
        time.sleep(2.5)
        search_box = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='APjFqb']")))
        time.sleep(2)
        print("Focus key sent... ")
        search_box.send_keys(focus_key)
        time.sleep(2)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

    except:
        print("Fail to send focus key")


def get_links(driver, xpath="//a[@jsname='UWckNb']", pg_num=20):
    links = []
    elements = []
    texts = []
    k = 0
    count_elements = 0
    for i in range(pg_num):
        try:
            elements = WebDriverWait(driver, 4).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath)))
            time.sleep(2)
        except:
            print("No elemments found")
        time.sleep(1)

        for element in elements:

            link = element.get_attribute("href")
            link = link.split('?')[0]
            if link != '':
                links.append(link)
            else:
                links.append("No link")

            text = []
            text = element.text
            if text != '':
                texts.append(text)
            else:
                texts.append("No text")

        k = i + 1
        count_elements = count_elements + len(elements)
        print(f"page {k} done with {len(elements)
                                    } elements found. Total elements: {count_elements}")

        try:
            driver.find_element(By.XPATH, '//*[@id="pnnext"]').click()
            time.sleep(1)
        except:
            print("end of pages")
            break
    print('\033[92mlinks and texts acquired... \033[0m\n')
    return texts, links


def get_response(links):
    responses = []
    response_status = []
    print('Initiating getting link responses... ')
    for i in range(len(links)):
        try:
            res = requests.get(links[i], timeout=3)
            time.sleep(1.5)
            responses.append(res)
            print(f'request link {
                  i} -> status code: {responses[i].status_code} link: {links[i]}')
            response_status.append(
                f'req {i} - status: {responses[i].status_code} ')

        except requests.exceptions.RequestException as e:
            print(f"No response from link {i}: {e}")
            response_status.append(f"No response from link {i}: {e}")
            responses.append(np.nan)

    print(f"Total requests: {len(links)}")
    print('Requests done... ')
    return responses, response_status


def get_emails_re(response, email_pattern):
    emails = []

    for i in range(len(response)):
        if response[i] != np.nan:
            soup = BeautifulSoup(response[i].content, 'html.parser')
            page_text = soup.get_text()
            email = re.findall(email_pattern, page_text)
            if email:
                emails.append(email)

            elif response[i].status_code == 403:
                emails.append(["page blocked"])

            else:
                emails.append(["No email found"])
        else:
            emails.append(["Time out"])
    print('Emails saved...')
    return emails


def get_mailto(responses):

    emails = []
    for response in responses:
        if response != np.nan:
            mailto = []
            soup = BeautifulSoup(response.content, 'html.parser')
            mailto = soup.find_all(
                'a', href=lambda href: href and 'mailto' in href)

            if mailto:
                e = []
                for email_tag in mailto:
                    e.append(email_tag.text)
                emails.append(e)

            elif response.status_code == 403:
                emails.append(["page blocked"])

            else:
                emails.append(["No email found"])

        else:
            emails.append(["Time out"])
    print('Mailto saved...')
    return emails


def get_words_re(responses, words_pattern):
    words = []
    word = []
    freq_word = []

    for response in responses:
        if type(response) != float:
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text()
            word = re.findall(words_pattern, page_text)
            if word:
                words.append(word)
                freq_word.append(len(word))

            elif response.status_code == 403:
                words.append(["page blocked"])
                freq_word.append(np.nan)

            else:
                words.append(["No word found"])
                freq_word.append(np.nan)
        else:
            words.append(["Time out"])
            freq_word.append(np.nan)
    print(f'counting word "{words_pattern}"  done...')
    return words, freq_word


def make_sample_df(word_list, responses):
    words_freq = pd.DataFrame()
    words_data = pd.DataFrame()

    for words_pattern in word_list:
        word, freq = get_words_re(responses, words_pattern)
        words_data = pd.concat([words_data, pd.Series(word, name=words_pattern)],axis=1)
        words_freq = pd.concat([words_freq, pd.Series(freq, name=words_pattern)],axis=1)

    sample_date = pd.DataFrame(words_freq.sum()).T
    sample_date['Date'] = pd.Timestamp.today().date() + pd.Timedelta(days=0)
    
    return sample_date

def create_database():
    daily_csv = 'database/daily_data.csv'
    historical_csv = 'database/historical_data.csv'

    if os.path.exists(historical_csv):
        df_daily = pd.read_csv(daily_csv, encoding='utf-8')
        today = pd.Timestamp.today().date() + pd.Timedelta(days=0)
        if df_daily['Date'].loc[0] == today.strftime('%Y-%m-%d'):
            print(f'\nDate context used value {today}')
            print('\033[91mData already exists in the historical CSV\033[0m\n')
            print('\033[91mNo Data has been added to the database\033[0m\n')
        else:
            df_daily.to_csv(historical_csv, mode='a', header=False, index=False, encoding='utf-8')
            print('Data added to the historical CSV.')
            print('Initiating save sqlite3 data... ')
            create_database_sqlite3()
            print('Save sqlite3 data successfully done...\n ')

        
    else:
        df_historical = pd.read_csv(daily_csv, encoding='utf-8')
        df_historical.to_csv(historical_csv, index=False)
        print('Creating a historical CSV and add the first daily data.')
        print('Creating the sqlite3 database... ')
        create_database_sqlite3()
        print('All successfully done...\n ')



def create_database_sqlite3():
    daily_data_csv = 'database/daily_data.csv'

    # Conecta ao banco de dados SQLite (ou cria se não existir)
    conn = sqlite3.connect('historical_data.db')
    cursor = conn.cursor()

    # Carrega os dados do CSV mestre
    df = pd.read_csv(daily_data_csv)

    # Cria a tabela no banco de dados (se não existir)
    df.to_sql('historical_data', conn, if_exists='append', index=False)

    # Fecha a conexão
    conn.close()


def query_database():
    # Conecta ao banco de dados SQLite
    conn = sqlite3.connect('historical_data.db')
    cursor = conn.cursor()

    # Executa uma consulta SQL
    cursor.execute("SELECT * FROM historical_data")
    rows = cursor.fetchall()

    # Imprime os resultados
    for row in rows:
        print(row)

    # Fecha a conexão
    conn.close()