from create_app import db

class Equipment(db.Model):
    """Modelo de equipamento."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    bookings = db.relationship('Booking', back_populates='equipment')

    def __repr__(self):
        return f'<Equipment {self.name}>'
