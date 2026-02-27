from tkinter.messagebox import IGNORE
from models.database import db
from datetime import datetime

class Destination(db.Model):
    __tablename__ = "destination"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=False) 
    contact = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
