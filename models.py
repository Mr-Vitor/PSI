from flask_login import UserMixin
import mysql.connector as sql

# Função para obter a conexão com o banco de dados
def obter_conexao():
    db_config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'prova'
    }
    return sql.connect(**db_config)


class User(UserMixin):
    id: str
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha

    # Busca um usuário pelo id (matrícula) no banco de dados
    @classmethod
    def get(cls, id):
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE matricula=%s', (id,))
        dados = cursor.fetchone()
        cursor.close()
        conexao.close()

        if dados:
            user = User(dados[1], dados[2])
            user.id = dados[0]
        else:
            user = None
        return user

    # Insere um novo usuário no banco de dados
    @classmethod
    def insert_data_user(cls, matricula, email, senha):
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO usuarios (matricula, email, senha) VALUES (%s, %s, %s)', (matricula, email, senha))
        conexao.commit()
        cursor.close()
        conexao.close()

    # Busca um usuário pelo número de matrícula
    @classmethod
    def select_data_user_matricula(cls, matricula):
        conexao = obter_conexao()
        cursor = conexao.cursor(buffered=True)
        cursor.execute('SELECT * FROM usuarios WHERE matricula=%s', (matricula,))
        dados = cursor.fetchone()
        cursor.close()
        conexao.close()
        if dados:
            user = User(dados[1], dados[2])
            user.id = dados[0]
            return user

    # Insere um novo exercício associado a um usuário
    @classmethod
    def insert_data_exercicio(cls, nome, descricao, id):
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO exercicios (nome, descricao, exe_usuario_id) VALUES (%s, %s, %s)', (nome, descricao, id))
        conexao.commit()
        cursor.close()
        conexao.close()

    # Busca todos os exercícios associados a um usuário
    @classmethod
    def select_data_exercicios(cls, id):
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute('SELECT * FROM exercicios WHERE ex_usuario_id=%s', (id,))
        dados = cursor.fetchall()
        cursor.close()
        conexao.close()
        return dados if dados else None
