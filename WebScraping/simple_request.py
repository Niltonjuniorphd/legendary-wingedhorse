# %%
import requests
from bs4 import BeautifulSoup

# %%
hard_key = 'armas+não+letais'

when = f'https://search.folha.uol.com.br/search?q={hard_key}&periodo=todos&sd=&ed=&site=todos'

response = requests.get(when)
content = response.content

site = BeautifulSoup(content, 'html.parser')
print(site.prettify())


# %%
noticias = site.find_all('li', attrs={'class': 'c-headline c-headline--newslist'})

# %%
noticia = noticias[0]

print(noticia.prettify())

# %%
