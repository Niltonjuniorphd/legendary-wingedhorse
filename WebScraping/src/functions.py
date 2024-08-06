import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import XPos, YPos
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_news(hard_key):
    print(f'\nHard_key used to scrap: {hard_key}')
    print(f'\nDate: {pd.Timestamp.today().date()}')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    noticias_t = []

    # hard_key = '"venezuela"'

    print(f'\n searching for {hard_key} ...\n')

    for page in tqdm(range(1, 201, 25), bar_format='{desc:<5.5}{percentage:3.0f}%|{bar:20}{r_bar}'):
        noticias_t = []

        when = f'https://search.folha.uol.com.br/?q={hard_key}&site=todos&sr={page}'

        response = requests.get(when, headers=headers)

        content = response.content
        site = BeautifulSoup(content, 'html.parser')

        # noticias = site.find_all('li', attrs={'class': 'c-headline c-headline--newslist'})
        noticias_t.append(site.find_all('li', attrs={'class': 'c-headline c-headline--newslist'}))

    return noticias_t


def create_result_table(news):

    name = []
    date = []
    title_text = []
    content_text = []
    link_text = []

    for i, j in enumerate(news):
        for noticia in j:
            journal = noticia.find(
                'h3', attrs={'class': 'c-headline__kicker c-kicker c-search__result_h3'})
            if journal:
                name.append(journal.text.replace('/n ', '').strip())
            else:
                name.append('sem name')

            noticia_date = noticia.find('time')
            if noticia_date:
                date.append(noticia_date.text.replace('/n ', '').strip())
            else:
                date.append('sem date')

            title = noticia.find('h2', attrs={'class': 'c-headline__title'})
            if title:
                title_text.append(title.text.replace('/n ', '').strip())
            else:
                title_text.append('sem title')

            content = noticia.find(
                'p', attrs={'class': 'c-headline__standfirst'})
            if content:
                content_text.append(content.text.replace('/n ', '').strip())
            else:
                content_text.append('sem content')

            link = noticia.find('a')
            if link:
                link_text.append(link['href'])
            else:
                link_text.append('sem link')

    df0 = pd.DataFrame({'date': date, 'name': name, 'title_text': title_text,
                       'content_text': content_text, 'link': link_text})
    df = df0.copy()
    df = df.drop_duplicates()

    print('\n Number of news items found: ', len(df0))
    print(' Number of duplicated news found: ', df0.duplicated().sum())
    print(' Final news considered: ', len(df))

    return df


def save_table(df, hard_key):
    h = pd.Timestamp.today()
    df.to_csv(f'data_{h.date()}_{hard_key.replace(
        '"', '').replace(' ', '_')}.csv')
    print(f'\nSaving DataFrame as data_{h.date()}_{hard_key.replace('"', '').replace(' ', '_')}.csv')
    print('\nDataFrame info: \n')
    print(df.info())


def format_date_column(df):

    for i, j in enumerate(df['date']):
        df.loc[i, 'date_b'] = pd.to_datetime(j.replace('às', '')
                                             .replace('à', '')
                                             .replace('mai', 'may')
                                             .replace('out', 'oct')
                                             .replace('set', 'sep')
                                             .replace('dez', 'dec')
                                             .replace('º', '')
                                             .replace('ago', 'aug')
                                             .replace('abr', 'apr')
                                             .replace('fev', 'feb')
                                             .replace('sem date', ''), dayfirst=True).date()
    df['date_b'] = pd.to_datetime(df['date_b'])
    df['day'] = df['date_b'].dt.day
    df['month'] = df['date_b'].dt.month
    df['year'] = df['date_b'].dt.year

    df = df.sort_values(by=['date_b'], ascending=False)
    df = df.reset_index()

    return df


def full_text(df):
    full_text = ' '.join(df)\
        .replace('...', '')\
        .replace('\r\n', ' ')\
        .replace('\n', ' ')\
        .replace('.', ' ')\
        .replace('  ', ' ')\
        .replace('   ', ' ')\
        .replace('(', '')\
        .replace(')', '')\
        .replace(',', '')\
        .replace('"', '')\
        .strip()

    return full_text


def remover_artigos_preposicoes(texto):
    palavras_para_remover = r'\b(?:que|...|:|mas|ver|foi|tem|dia|dispensar|diz|ou|pelo|pelos|anos|agora|ser|quando|mais|gente|ano|deste|como|seu|é|não|se|ter|sido|são|duas|ele|ela|ficou|e|a|o|as|os|um|uns|uma|umas|de|do|da|dos|das|em|no|na|nos|nas|por|pelos|pela|pelas|ao|aos|à|às|com|para|perante|contra|entre|sob|era|sua|está|dizer|já|eu|você|sobre|trás)\b'

    # Usando regex para substituir as palavras por uma string vazia
    texto_limpo = re.sub(palavras_para_remover, '', texto, flags=re.IGNORECASE)

    # Remover espaços múltiplos resultantes da substituição
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()

    return texto_limpo


def df_words_key(full_text_cleaned, df):
    keys = pd.Series(full_text_cleaned.lower().strip().split(' '))

    df_c = pd.Series()
    for i, j in enumerate(df['content_text']):
        col = pd.DataFrame()
        for p in keys.value_counts().head(100).index:
            if ((len(p) > 2) and (p in j.lower())):
                col.loc[i, p] = 1

            else:
                col.loc[i, p] = 0
        df_c = pd.concat([df_c, col], axis=0)

    return df_c


def save_plot(data, filename, xlabel, ylabel, title):
    sns.barplot(x=data.index, y=data.values)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(filename)
    plt.close()


def add_figure_to_pdf(pdf, image_file, header_text, x=10, y=20, w=190):
    pdf.add_page()
    pdf.set_font('arial', 'B', 12)
    pdf.cell(0, 10, header_text, align='C')
    pdf.image(image_file, x=x, y=y, w=w)
    pdf.ln(85)  # Adjust the space between images


def add_list_to_pdf(pdf, result_list, header_text):
    pdf.add_page()
    pdf.set_font('arial', 'B', 12)
    pdf.cell(0, 10, header_text, align='C')
    pdf.ln(1)
    pdf.set_font('arial', '', 10)

    for i, item in enumerate(result_list):
        for key, value in item.items():
            pdf.cell(0, 5, f'{i} - {key}: {value}',
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def write_text_to_pdf(pdf, text):
    pdf.add_page()
    pdf.set_font("arial", size=10)
    pdf.multi_cell(0, 10, text)
