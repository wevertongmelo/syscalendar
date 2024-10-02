from flask import Blueprint, request, redirect, url_for, flash, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from create_app import db

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/login', methods=['GET', 'POST'])
def login():
    """Autentica o usuário e inicia a sessão."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = authenticate_user(username, password)
            session['username'] = user.username
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('user_controller.dashboard'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('login.html')

@user_controller.route('/register', methods=['GET', 'POST'])
def register():
    """Registra um novo usuário e inicia a sessão."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = register_user(username, password)
            session['username'] = user.username
            flash('Registro bem-sucedido! Você está agora logado.', 'success')
            return redirect(url_for('user_controller.dashboard'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('register.html')

def register_user(username, password):
    """Registra um novo usuário."""
    if User.query.filter_by(username=username).first():
        raise ValueError("Usuário já existe.")
    
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, password=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Erro ao registrar o usuário: {e}")
    
    return new_user

def authenticate_user(username, password):
    """Autentica um usuário existente."""
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    else:
        raise ValueError("Nome de usuário ou senha inválidos.")

@user_controller.route('/logout')
def logout():
    """Finaliza a sessão do usuário e redireciona para a página de login."""
    if 'username' in session:
        username = session.pop('username', None)  # Remove o usuário da sessão
        flash(f'{username}, você saiu com sucesso!', 'success')
        return render_template('logout.html')
    else:
        flash('Você não está logado.', 'warning')
        return redirect(url_for('user_controller.login'))
    
@user_controller.route('/dashboard')
def dashboard():
    """Página do Dashboard do Usuário"""
    if 'username' not in session:
        return redirect(url_for('user_controller.login'))
    return render_template('dashboard.html', username=session['username'])
