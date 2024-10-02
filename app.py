from flask import Flask, render_template, redirect, url_for, session, flash, request
from create_app import create_app, db
from models.user import User
from controllers.user_controller import user_controller
from controllers.equipment_controller import equipment_controller
from controllers.booking_controller import booking_controller
from utils.report_generator import ReportGenerator
from werkzeug.security import generate_password_hash

app = create_app()

# Registrar Blueprints com prefixos de URL
app.register_blueprint(user_controller, url_prefix='/user')
app.register_blueprint(equipment_controller, url_prefix='/equipment')
app.register_blueprint(booking_controller, url_prefix='/booking')


@app.route('/')
def index():
    """Redireciona para o dashboard se o usuário estiver autenticado."""
    if 'username' in session:
        return redirect(url_for('user_controller.dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Mostra o dashboard do usuário se estiver autenticado, caso contrário redireciona para o login."""
    if 'username' not in session:
        return redirect(url_for('user_controller.login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/report')
def report():
    """Gera e exporta um relatório se o usuário estiver autenticado, caso contrário redireciona para o login."""
    if 'username' not in session:
        return redirect(url_for('user_controller.login'))
    
    report_generator = ReportGenerator()
    try:
        report_generator.generate_booking_report('report.csv')
        flash('Relatório exportado como report.csv')
    except Exception as e:
        flash(f'Erro ao gerar relatório: {e}')
    return render_template('report.html')

@app.route('/logout')
def logout():
    """Desloga o usuário e redireciona para a página inicial."""
    session.pop('username', None)
    return redirect(url_for('index'))


@app.before_request
def create_tables():
    db.create_all()
    
    # Criar o usuário admin se não existir
    if not User.query.filter_by(username='admin').first():
        hashed_password = generate_password_hash('password123', method='pbkdf2:sha256') # type: ignore
        user = User(username='admin', password=hashed_password)
        db.session.add(user)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
