from app.db import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    balance = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"<Account {self.number} - {self.name}>"
