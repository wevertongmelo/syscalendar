from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    
    # Carregar configurações do arquivo config.py
    app.config.from_object(config_class)
    
    # Inicializar extensões
    db.init_app(app)
    
    # Registrando Blueprints
    from controllers.user_controller import user_controller
    from controllers.equipment_controller import equipment_controller
    from controllers.booking_controller import booking_controller

    return app
