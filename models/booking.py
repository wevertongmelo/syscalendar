from create_app import db
from datetime import datetime

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    equipment = db.relationship('Equipment', back_populates='bookings')
    def __repr__(self):
        return f'<Booking {self.id} - Equipment {self.equipment_id}>'
