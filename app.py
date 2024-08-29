from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
#Criando uma constante com o nome do arquivo do BD.
DATABASE = 'database.db'

app = Flask(__name__)

# habilitar mensagens flash 
#(nem sei se ele usou isso, mas essa anotação ja tava aqui :P)
app.config['SECRET_KEY'] = 'muitodificil'

# obtém conexão com o banco de dados
def get_connection():
    #Colocando na variavel "conn" a conexão com o banco
    #connect(Nome do arquivo do banco), que está salvo na variavel "DATABASE" criada na linha 4.
    conn = sqlite3.connect(DATABASE)

    #comando pra transformar as tuplas (valor padrão de retorno) em dicionários.
    conn.row_factory = sqlite3.Row

    return conn

@app.route('/')
def index():
    #Pegando a variavel que faz conexão com o BD pela função get_connection (linha 13)
    conn = get_connection()

    #Usando (SELECT *) na tabela "users" do BD
    #Usando a função "fetchall" para pegar todas as colunas da tabela.
    users = conn.execute("SELECT * FROM users").fetchall()
    
    conn.close()
    return render_template('pages/index.html', users=users)

@app.route('/create', methods=['POST', 'GET'])
def create():
    #Esse IF serve pra verificar se essa função está sendo rodada pela propria página de cadastro, pelo botão de confirmar criação de conta
    #ou se a função está vindo da pagina index, pelo botão de "Add"
    #Se tiver vindo do index ele redireciona para a página (create.html) (linha 67)
    #Se tiver vindo do botão de confirmar cadastro, roda esses códigos todos e volta pro index
    if request.method == 'POST':
        #Coletando os dados para o cadastro (de create.html)
        email = request.form['email'] #Linha 8 de create.html
        senha= request.form['password'] #Linha 12 de create.html

        #Verificando se tem email
        if not email:
            flash('Email é obrigatório')
        #não sei se da pra criar sem senha, mas por via das duvidas...
        #if not senha:
        #   flash('Senha é obrigatória')
        else:
            #Else pra caso esteja tudo certinho e o cara tenha colocado email:
            #o mesmo processo da linha 26, variável pra repressentar o BD
            conn = get_connection()
            #(INSERT INTO users) => (Inserir na tabela users)
            #quais colunas? => (email, senha)
            #quais os valores? => (?,?) por que não da pra colocar uma variavel do python direto no comando sqlite
            #logo depois do comando sqlite, coloca os valores em ordem respectiva para as interrogações
            conn.execute("INSERT INTO users(email, senha) VALUES (?,?)", (email, senha))
            #commit para confirmar e salvar as alterações, igual github
            conn.commit()
            #fechar a conexão, sempre lembrar de fazer
            conn.close()
            return redirect(url_for('index'))
    
    return render_template('pages/create.html')

#essa linha parece meio assustadora por ter coisa nova e parecer meio confusa mas confia que é simples
#la no index.html, tem os botões para editar os usuarios cadastrados, naquele simbolo do lado do email de cada um
#aquela lista de usuarios ta sendo feita com um for (linhas 11 a 19)
#cada usuario é chamado de "user" =>(for user in users)(linha 11)
#quando clica no icone, ele aciona a function edit enviando como parametro: id=user['id']
#isso significa: parametro "id" será a coluna id do objeto usuario especifico.
@app.route('/<int:id>/edit', methods=['POST', 'GET'])
def edit(id):

    #mesma coisa das linhas 26 e 55, colocar o banco na variavel conn
    conn = get_connection()

    #Pegando id, email e senha da tabela user where id = parametro da função edit na qual estamos
    user = conn.execute('SELECT id, email, senha FROM users WHERE id == ?', (str(id))).fetchone()
    #verificando se o usuario existe
    if user == None:
        return redirect(url_for('error', message='Usuário Inexistente'))

    if request.method == 'POST':
        #pegando o valor do formulario de edição (linha 7 do arquivo edit.html)
        email = request.form['email']
        #atualizando com update o email no id especifico, novamente usando o parametro
        conn.execute('UPDATE users SET email=? WHERE id=?', (email, id))
        return redirect(url_for('index'))
    
    return render_template('pages/edit.html', user=user)

#ele fez essa rota aqui só por capricho, acho que é ignoravel, mas ela ta sendo chamada na linha 85 pelo erro de não existir o usuario que está tentando editar
@app.route('/error')
def error():
    error = request.args.get('message')
    return render_template('errors/error.html', message=error)
