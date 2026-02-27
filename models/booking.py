
from models.database import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = "booking"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    name = db.Column(db.String(150), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(255), nullable=True)
    package = db.Column(db.String(100), nullable=True)

    adults = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer, nullable=False)

    date = db.Column(db.String(20), nullable=False)

    total_price = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def create(data):
        booking = Booking(**data)
        db.session.add(booking)
        db.session.commit()