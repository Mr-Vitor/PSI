from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

# Gerenciador de login do Flask
login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERDIFICIL2'

# Inicializa o gerenciador de login
login_manager.init_app(app)


# Carrega o usuário pelo ID (matrícula)
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# Rota para login de usuários
@app.route('/', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        matricula = request.form["matricula"]
        senha = request.form["senha"]

        user = User.select_data_user_matricula(matricula)
        if user:
            # Verifica a senha do usuário
            hash = user.senha
            if check_password_hash(hash, senha):
                login_user(user)
                return redirect(url_for('inicial'))
            else:
                return redirect(url_for('login'))
    return render_template('index.html')


# Rota para o cadastro de novos usuários
@app.route('/cadastro', methods = ["POST", "GET"])
def cadastro():
    if request.method == "POST":
        matricula = request.form['matricula']
        email = request.form["email"]
        senha = request.form["senha"]
        # Gera hash para senha e email
        hash = generate_password_hash(senha)
        hashmail = generate_password_hash(email)

        # Insere o novo usuário e faz login automático
        User.insert_data_user(matricula, hashmail, hash)
        user = User.select_data_user_matricula(matricula)
        login_user(user)

        return redirect(url_for("inicial"))
    
    return render_template('cadastro.html')


# Página inicial, disponível apenas para usuários logados
@app.route("/inicial")
@login_required
def inicial():
    user = current_user.email  # Obtém o email do usuário logado
    return render_template("inicial.html", user=user)


# Rota para gerenciar exercícios do usuário logado
@app.route("/exercicios", methods = ["POST", "GET"])
@login_required
def exercicios():
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        id = current_user.matricula
        # Insere um novo exercício
        User.insert_data_exercicio(nome, descricao, id)

    # Busca e exibe os exercícios do usuário
    id = current_user.id
    exercicios = User.select_data_exercicios(id)
    return render_template("exercicios.html", exercicios=exercicios)


# Rota para logout do usuário
@app.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    if request.method == "POST":
        logout_user()
        return redirect(url_for("login"))
    return render_template("logout.html")
