# %%
import requests
from bs4 import BeautifulSoup

# %%
response = requests.get('https://g1.globo.com/')

# %%
#print(response.status_code)

# %%
#print(response.headers)

# %%
#print(response.content)

# %%
content = response.content
site = BeautifulSoup(content, 'html.parser')

# %%
noticias = site.find_all('div', attrs={'class': 'feed-post-body'})
#print(noticias.prettify())


# %%
for noticia in noticias:
    #print(noticia.prettify())
    titulo = noticia.find('a', attrs={'class': 'feed-post-link'})
    print('titulo:', titulo.text)


    subtitulo = noticia.find('div', attrs={'class': 'feed-post-body-resumo'})
    if subtitulo:
        print('subtitulo:', subtitulo.text)
    
    print('---')

# %%
