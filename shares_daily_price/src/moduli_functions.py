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
    """
    Initializes and returns a headless Chrome WebDriver instance.
    If the driver is not found, automatically install the appropriate version of the ChromeDriver.

    Returns:
        WebDriver: An instance of the Chrome WebDriver configured to run headless.
    """
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    options.add_argument("--incognito")  # Run in incognito mode
    options.add_argument("--no-sandbox")  # Disable sandboxing
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36")  # Set a user-agent string
    
    # Initialize the driver with the specified options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("Driver ready... ")

    return driver


def send_focus_key(driver, focus_key):
    """
    Sends a search query to Google using the provided WebDriver instance.

    This function navigates to the Google homepage, waits for the search box
    to become visible, and then sends the specified `focus_key` as a search query.
    After submitting the query, it waits briefly to allow the page to load.

    Args:
        driver (WebDriver): The WebDriver instance used to interact with the browser.
        focus_key (str): The search query to be sent to Google's search box.

    Raises:
        Exception: If any error occurs during navigation or interaction with the search
        box.

    """
    try:
        driver.get("https://google.com/ncr")
        WebDriverWait(driver, 5).until(
            EC.url_contains("google.com")
        )
        
        search_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        print("Focus key sent... ")
        search_box.clear()  # Clear any pre-existing text
        search_box.send_keys(focus_key)
        search_box.send_keys(Keys.RETURN)
        
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "search"))
        )

    except Exception as e:
        print(f"Failed to send focus key: {e}")


def get_links(driver, xpath="//a[@jsname='UWckNb']", pg_num=20):
    """
    Extracts links and their associated texts from multiple pages using a specified XPath.

    This function navigates through a series of pages in a web driver, extracting
    the `href` attribute and text content of elements matching the given XPath. The
    function continues to click the "Next" button to paginate through the specified
    number of pages (`pg_num`) or until no more pages are available.

    Args:
        driver (WebDriver): The WebDriver instance used to interact with the browser.
        xpath (str): The XPath expression used to locate elements containing links.
                     Defaults to "//a[@jsname='UWckNb']".
        pg_num (int): The number of pages to traverse and extract data from. Defaults to 20.

    Returns:
        tuple: A tuple containing two lists:
            - texts (list of str): The text content associated with each link.
            - links (list of str): The URLs extracted from the specified elements.
    
    Raises:
        Exception: If an error occurs while locating elements or navigating pages.
    """
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
            print(f"No elemments with xpath {xpath} found")
        time.sleep(1)

        for element in elements:

            link = []
            link = element.get_attribute("href")
            #link = link.split('?')[0]
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
    """
    Sends HTTP GET requests to a list of URLs and records the responses and status codes.

    This function iterates over a list of URLs, sending an HTTP GET request to each.
    It stores the response objects and their corresponding status codes. If a request
    fails, it logs the exception and records a NaN (Not a Number) in the responses list.

    Args:
        links (list of str): A list of URLs to which the GET requests will be sent.

    Returns:
        tuple: A tuple containing two lists:
            - responses (list): A list of response objects or NaN for failed requests.
            - response_status (list of str): A list of strings indicating the request index,
                                             the status code, or an error message if the request failed.
    
    Raises:
        requests.exceptions.RequestException: Captures and logs exceptions that occur during the requests.

    """
    responses = []
    response_status = []
    print('Initiating getting link responses... ')
    print(f"Total of requests to do: {len(links)}")
    for i in range(len(links)):
        try:
            res = requests.get(links[i], timeout=3)
            time.sleep(1.5)
            responses.append(res)
            response_status.append(
                f'req {i} - status: {responses[i].status_code} ')

            print(f'request link {i+1}/{len(links)} -> status code: {responses[i].status_code} link: {links[i]}')

        except requests.exceptions.RequestException as e:
            print(f"No response from link {i}: {e}")
            responses.append(np.nan)
            response_status.append(f"No response from link {i}: {e}")

    print('Requests done... ')
    return responses, response_status


def get_words_re(responses, words_pattern):
    """
    Extracts words matching a regex pattern from a list of HTTP responses.

    This function processes each HTTP response, parsing the content using BeautifulSoup 
    to extract the text. It then uses a regular expression pattern to find matching words
    within the text. The function counts the frequency of these words and handles specific
    cases such as blocked pages or timeouts.

    Args:
        responses (list): A list of HTTP response objects (or NaN for failed requests).
        words_pattern (str): A regular expression pattern used to search for words in the response text.

    Returns:
        tuple: A tuple containing two lists:
            - words (list of lists): A list of lists, where each sublist contains the words found in a response.
                                     If no words are found, it contains ["No word found"], or other messages for specific cases.
            - freq_word (list of int or float): A list of integers representing the frequency of the found words,
                                                or NaN if no words were found or the page was blocked/timed out.
    """
    words = []
    word = []
    freq_word = []

    for response in responses:
        if type(response) != float:
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text()
            page_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', page_text)
            page_text = page_text.lower()
            page_text = page_text.strip()
            word = re.findall(words_pattern.lower(), page_text)
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
    """
    Creates a DataFrame summarizing the frequency of specific words across multiple web pages.

    This function iterates over a list of word patterns, using the `get_words_re` function
    to extract and count the occurrences of these words in the provided HTTP responses. It
    then compiles the frequency data into a DataFrame and appends the current date.

    Args:
        word_list (list of str): A list of regex patterns representing the words to search for in the responses.
        responses (list): A list of HTTP response objects (or NaN for failed requests).

    Returns:
        pd.DataFrame: A DataFrame containing the sum of word frequencies across all responses
                      and a column with the current date.
    """
    words_freq = pd.DataFrame()
    words_data = pd.DataFrame()

    for words_pattern in word_list:
        word, freq = get_words_re(responses, words_pattern)
        words_data = pd.concat([words_data, pd.Series(word, name=words_pattern)],axis=1)
        words_freq = pd.concat([words_freq, pd.Series(freq, name=words_pattern)],axis=1)

    sample_date = pd.Series(words_freq.sum())
    sample_date['Date'] = pd.Timestamp.today().date() + pd.Timedelta(days=0)
    
    return sample_date

def create_database(sample_date):

    """
    Manages the creation and updating of a historical data CSV and a SQLite database.

    This function checks for the existence of a historical data CSV file. If the file exists,
    it verifies whether the latest daily data is already included. If not, it appends the daily
    data to the historical CSV and updates a corresponding SQLite database. If the historical CSV
    does not exist, the function creates it using the daily data and initializes the SQLite database.

    The function uses the following files:
    - 'database/daily_data.csv': The daily data CSV file.
    - 'database/historical_data.csv': The historical data CSV file.

    It also calls `create_database_sqlite3()` to handle the SQLite database updates.

    """
    daily_csv = 'database/daily_data.csv'
    historical_csv = 'database/historical_data.csv'

    if os.path.exists(historical_csv):
        df_daily = pd.read_csv(daily_csv, encoding='utf-8')
        df_historical = pd.read_csv(historical_csv, encoding='utf-8')
        today = pd.Timestamp.today().date() + pd.Timedelta(days=0)

        if df_historical['Date'].iloc[-1] == today.strftime('%Y-%m-%d'):
            print(f'\nDate context used value {today}')
            print('\033[91mData already exists in the historical CSV\033[0m\n')
            print('\033[91mNo Data has been added to the database\033[0m\n')
        else:
            df_daily.to_csv(historical_csv, mode='a', header=False, index=False, encoding='utf-8')
            print('Data added to the historical CSV.')
            print('Initiating save sqlite3 data... ')
            #create_database_sqlite3()
            handle_database(sample_date)
            print('Save sqlite3 data successfully done...\n ')

        
    else:
        df_historical = pd.read_csv(daily_csv, encoding='utf-8')
        df_historical.to_csv(historical_csv, index=False)
        print('Creating a historical CSV and add the first daily data.')
        print('Creating the sqlite3 database... ')
        #create_database_sqlite3()
        handle_database(sample_date)
        print('All successfully done...\n ')




def handle_database(data):

    database_path = 'database/historical_data.db'

    if os.path.exists(database_path):
        insert_data(data)
        print('Daily data added to the database.')
    else:
        create_database_sqlite3()
        insert_data(data)
        print('Creating database and added the first daily data.')

def create_database_sqlite3():
    """
    Appends daily data from a CSV file to a SQLite database.

    This function reads daily data from the 'database/daily_data.csv' file and 
    appends it to a table named 'historical_data' in a SQLite database named 'historical_data.db'.
    If the table does not exist, it is created automatically. The function closes the 
    database connection after the operation.

    """

    #daily_data_csv = 'database/daily_data.csv'
    #conn = sqlite3.connect('historical_data.db')
    #cursor = conn.cursor()
    #df = pd.read_csv(daily_data_csv)
    #df.to_sql('historical_data', conn, if_exists='append', index=False)
    #conn.close()

    sql_create_order = """
        CREATE TABLE IF NOT EXISTS historical_data (
        subiu DECIMAL(10,2),
        caiu DECIMAL(10,2),
        salta DECIMAL(10,2),
        queda DECIMAL(10,2),
        aumenta DECIMAL(10,2),
        dispara DECIMAL(10,2),
        desaba DECIMAL(10,2),
        desabam DECIMAL(10,2),
        podem_cair DECIMAL(10,2),
        podem_subir DECIMAL(10,2),
        barata DECIMAL(10,2),
        Date DATETIME,
        value DECIMAL(10,2),
        value_close DECIMAL(10,2)
    );
    """
    try:
        conn = sqlite3.connect('database/historical_data.db')
        cur = conn.cursor()
        cur.execute(sql_create_order)
        conn.commit()
        print("Database created successfully")
    except conn.DatabaseError as erro:
        print("Erro no banco de dados", erro)
    finally:
        if conn:
            conn.close()
            print("Connection closed")



def insert_data(data):
    """
    Inserts data into a SQLite database.
    """
    sql_insert_order = """
        INSERT INTO historical_data (
        subiu,
        caiu,
        salta,
        queda,
        aumenta,
        dispara,
        desaba,
        desabam,
        podem_cair,
        podem_subir,
        barata,
        Date,
        value,
        value_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

    conn = sqlite3.connect('database/historical_data.db')
    cur = conn.cursor()
    cur.execute(sql_insert_order, data)
    conn.commit()
    conn.close()
    print('Data inserted successfully.')



def query_database(db__path):
    """
    Queries and prints all records from the 'historical_data' table in a SQLite database.

    This function connects to the 'historical_data.db' SQLite database, retrieves all rows
    from the 'historical_data' table, and prints each row. After the query is executed, the
    database connection is closed.

    Raises:
        sqlite3.DatabaseError: If there is an error connecting to or querying the SQLite database.
    """
    conn = sqlite3.connect(db__path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM historical_data")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()