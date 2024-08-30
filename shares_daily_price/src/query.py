import sqlite3

# Conecta ao banco de dados SQLite
conn = sqlite3.connect('historical_data.db')
cursor = conn.cursor()

# Executa uma consulta SQL para selecionar a última linha
cursor.execute("SELECT * FROM historical_data ORDER BY datetime(Date) DESC LIMIT 1")
last_data = cursor.fetchone()  # Atribui a última linha à variável last_data

# Imprime a última linha
print(last_data)

# Fecha a conexão
conn.close()
