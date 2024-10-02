from create_app import create_app, db
from models.user import User

def create_admin_user():
    app = create_app()

    with app.app_context():
        db.create_all()
        
        # Verifica se o usuário admin já existe
        if not User.query.filter_by(username='admin').first():
            # Cria o usuário admin com uma senha hash segura
            admin_user = User(username='admin')
            admin_user.set_password('password123')  # Defina a senha com hash
            db.session.add(admin_user)
            db.session.commit()
            print("Usuário admin criado com sucesso!")
        else:
            print("Usuário admin já existe.")

if __name__ == "__main__":
    create_admin_user()
