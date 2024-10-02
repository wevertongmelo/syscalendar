# controllers/equipment_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.equipment import Equipment
from create_app import db

equipment_controller = Blueprint('equipment_controller', __name__)

@equipment_controller.route('/list', methods=['GET'])
def list_equipments():
    """Lista todos os equipamentos cadastrados."""
    equipments = Equipment.query.all()
    return render_template('equipments.html', equipments=equipments)

@equipment_controller.route('/add', methods=['GET', 'POST'])
def add_equipment():
    """Adiciona um novo equipamento."""
    # Verificar se o usuário está logado
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'error')
        return redirect(url_for('user_controller.login'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        if name and description:
            new_equipment = Equipment(name=name, description=description)
            db.session.add(new_equipment)
            db.session.commit()
            flash('Equipamento adicionado com sucesso!', 'success')
            return redirect(url_for('equipment_controller.list_equipments'))
        else:
            flash('Por favor, preencha todos os campos.', 'error')
    
    return render_template('add_equipment.html')
