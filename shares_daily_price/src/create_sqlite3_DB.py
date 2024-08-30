import sqlite3
import pandas as pd


historical_csv = 'database/historical_data.csv'

# Conecta ao banco de dados SQLite (ou cria se não existir)
conn = sqlite3.connect('dados_historicos.db')
cursor = conn.cursor()

# Carrega os dados do CSV mestre

df = pd.read_csv(historical_csv)

# Cria a tabela no banco de dados (se não existir)
df.to_sql('historico_dados', conn, if_exists='append', index=False)

# Fecha a conexão
conn.close()
