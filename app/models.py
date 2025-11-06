from app.db import db

class Account(db.Model):
    __tablename__ = 'accounts'   # Table name in DB

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(50), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"<Account {self.id} - {self.name}>"
