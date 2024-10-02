# controllers/booking_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from datetime import datetime
from create_app import db
import logging
from models.equipment import Equipment
from models.booking import Booking
from services.report_service import generate_booking_report

# Inicializar o logger
logger = logging.getLogger(__name__)

booking_controller = Blueprint('booking_controller', __name__)

@booking_controller.route('/report')
def report():
    """Gera e envia um relatório de reservas por e-mail ou para download."""
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.')
        return redirect(url_for('user_controller.login'))

    try:
        # Gerar o relatório
        report_path = generate_booking_report()
        flash('Relatório gerado com sucesso!')
        logger.info("Relatório gerado e enviado para download.")
        return send_file(report_path, as_attachment=True)
    except Exception as e:
        flash('Ocorreu um erro ao gerar o relatório.')
        logger.error(f"Erro ao gerar o relatório: {e}")
        return redirect(url_for('booking_controller.create_booking'))

@booking_controller.route('/create', methods=['GET', 'POST'])
def create_booking():
    """Cria uma nova reserva de equipamento."""
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.')
        return redirect(url_for('user_controller.login'))

    if request.method == 'POST':
        equipment_id = request.form.get('equipment_id')
        end_time_str = request.form.get('end_time')
        if not equipment_id or not end_time_str:
            flash('Todos os campos são obrigatórios.')
            return redirect(url_for('booking_controller.create_booking'))

        try:
            # Ajustar o formato para coincidir com o datetime-local
            end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')
            start_time = datetime.now()

            # Verificar se o equipamento existe
            equipment = Equipment.query.get(equipment_id)
            if not equipment:
                flash('Equipamento não encontrado.')
                return redirect(url_for('booking_controller.create_booking'))

            # Verificar conflitos de reserva
            conflicting_booking = Booking.query.filter(
                Booking.equipment_id == equipment_id,
                Booking.end_time > start_time,
                Booking.start_time < end_time
            ).first()

            if conflicting_booking:
                flash('O equipamento já está reservado nesse período.')
                return redirect(url_for('booking_controller.create_booking'))

            # Criar e adicionar a reserva
            booking = Booking(
                equipment_id=equipment_id,
                username=session['username'],
                start_time=start_time,
                end_time=end_time
            )
            db.session.add(booking)
            db.session.commit()
            flash('Reserva criada com sucesso!')
            return redirect(url_for('booking_controller.create_booking'))
        except ValueError:
            flash('Formato de data inválido. Use o formato correto (YYYY-MM-DDTHH:MM).')
        except Exception as e:
            db.session.rollback()  # Reverte a transação em caso de erro
            flash(f'Erro ao criar reserva: {e}')
            logger.error(f"Erro ao criar reserva: {e}")

    # Listar equipamentos para a interface de criação de reserva
    equipments = Equipment.query.all()
    return render_template('create_booking.html', equipments=equipments)

@booking_controller.route('/list', methods=['GET'])
def list_bookings():
    """Lista todas as reservas do usuário logado, incluindo informações dos equipamentos."""
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.')
        return redirect(url_for('user_controller.login'))

    try:
        # Consultar todas as reservas do usuário logado, incluindo os equipamentos relacionados
        bookings = Booking.query.filter_by(username=session['username']).all()

        # Opcional: Ordenar por data de início
        bookings.sort(key=lambda b: b.start_time)

        logger.info(f"Usuário {session['username']} visualizou suas reservas.")
        return render_template('list_bookings.html', bookings=bookings)
    except Exception as e:
        flash('Ocorreu um erro ao listar as reservas.')
        logger.error(f"Erro ao listar reservas: {e}")
        return redirect(url_for('booking_controller.create_booking'))
