# Importing MySQL connector
import mysql.connector

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
}


conn = None

try:
    # Estabelece conexão sem especificar o banco de dados
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Tenta criar o banco de dados
    cursor.execute("CREATE DATABASE IF NOT EXISTS prova")
    print("Banco de dados 'prova' criado ou já existente.")

    # Fecha a conexão e abre uma nova com o banco de dados 'prova'
    cursor.close()
    conn.close()

    db_config['database'] = 'prova'
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    print("Conexão estabelecida com sucesso ao banco de dados 'prova'.")

except mysql.connector.Error as erro:
    print(f"Erro ao conectar ou criar banco de dados: {erro}")
finally:
    if conn is not None:
        conn.close()

if conn is not None:
    # Abre conexão novamente para executar o script SQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Localização do SQL
    SCHEMA = "database/banco.sql"

    # Declara o SQL para o banco
    with open(SCHEMA, 'r') as f:
        sql_script = f.read()

    # Executa cada statement do script SQL
    for statement in sql_script.split(';'):
        if statement.strip():
            try:
                cursor.execute(statement)
            except mysql.connector.Error as e:
                print(f"Erro ao executar statement: {e}")

    # Encerra operações
    conn.commit()
    cursor.close()
    conn.close()
    print("Script executado com sucesso.")