
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Message(db.Model):
    """table model"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    message = db.Column(db.String(2000), nullable=False)
    date = db.Column(db.String(2000))